#!/usr/bin/env python3
"""Vérifie le portail nsi.xyz avant une pull request.

Contrôles, sans dépendance externe :
  - fichiers HTML lisibles en UTF-8, avec <html lang>, <title> et description ;
  - identifiants HTML uniques ;
  - liens et assets locaux existants ;
  - ancres internes (#...) existantes ;
  - images avec attribut alt ;
  - polices et images référencées dans le CSS inline.

Usage : python3 outils-dev/verifier.py
Code de sortie : 0 si tout est bon, 1 s'il reste au moins une erreur.
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

RACINE = Path(__file__).resolve().parent.parent
EXCLUS = {RACINE / "docs" / "historique"}
SCHEMAS_EXTERNES = ("http://", "https://", "mailto:", "tel:", "data:", "javascript:")

erreurs: list[str] = []
avertissements: list[str] = []


class PageHTML(HTMLParser):
    def __init__(self, chemin: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.chemin = chemin
        self.langue: str | None = None
        self.titre = ""
        self.description: str | None = None
        self.ids: list[str] = []
        self.liens: list[tuple[str, str]] = []  # (balise, valeur)
        self.images_sans_alt: list[str] = []
        self._dans_titre = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        valeurs = {nom: (valeur or "") for nom, valeur in attrs}

        if tag == "html":
            self.langue = valeurs.get("lang") or None
        elif tag == "title":
            self._dans_titre = True
        elif tag == "meta" and valeurs.get("name", "").lower() == "description":
            self.description = valeurs.get("content", "").strip()

        if "id" in valeurs:
            self.ids.append(valeurs["id"])

        if tag == "img" and "alt" not in valeurs:
            self.images_sans_alt.append(valeurs.get("src", "(sans src)"))

        for attribut in ("href", "src"):
            if attribut in valeurs:
                self.liens.append((tag, valeurs[attribut]))

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._dans_titre = False

    def handle_data(self, data: str) -> None:
        if self._dans_titre:
            self.titre += data


def relatif(chemin: Path) -> str:
    return str(chemin.relative_to(RACINE))


def erreur(page: Path, message: str) -> None:
    erreurs.append(f"{relatif(page)} : {message}")


def verifier_cible(page: Path, valeur: str) -> None:
    """Vérifie un href/src local (hors URL externe et hors ancre seule)."""
    valeur = valeur.strip()
    if not valeur or valeur.startswith(SCHEMAS_EXTERNES) or valeur.startswith("//"):
        return

    if valeur.startswith("#"):
        return  # traité avec les ancres de la page

    morceaux = urlsplit(valeur)
    if morceaux.scheme:
        return

    chemin = unquote(morceaux.path)
    if not chemin:
        return

    # Les URL absolues du site (/v2/, /plan/…) pointent vers l’archive ou la
    # production : elles ne sont pas dans ce dépôt.
    if chemin.startswith("/"):
        return

    cible = (page.parent / chemin).resolve()
    try:
        cible.relative_to(RACINE)
    except ValueError:
        erreur(page, f"lien sortant du dépôt : {valeur}")
        return

    if not cible.exists():
        erreur(page, f"cible introuvable : {valeur}")


def verifier_ancres(page: PageHTML) -> None:
    ids = set(page.ids)
    for _, valeur in page.liens:
        if valeur.startswith("#") and len(valeur) > 1:
            ancre = unquote(valeur[1:])
            if ancre not in ids:
                erreur(page.chemin, f"ancre introuvable : {valeur}")


def verifier_css(page: Path, texte: str) -> None:
    for valeur in re.findall(r"url\(\s*['\"]?([^'\")]+)", texte):
        valeur = valeur.strip()
        if not valeur or valeur.startswith(("data:", "#", "%23", "http://", "https://", "//")):
            continue
        cible = (page.parent / unquote(valeur)).resolve()
        try:
            cible.relative_to(RACINE)
        except ValueError:
            erreur(page, f"ressource CSS sortant du dépôt : {valeur}")
            continue
        if not cible.exists():
            erreur(page, f"ressource CSS introuvable : {valeur}")


def main() -> int:
    pages = sorted(
        chemin
        for chemin in RACINE.rglob("*.html")
        if not any(parent in EXCLUS for parent in chemin.parents)
    )

    if not pages:
        print("Aucune page HTML trouvée.")
        return 1

    for chemin in pages:
        try:
            texte = chemin.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            erreur(chemin, "fichier non UTF-8")
            continue

        page = PageHTML(chemin)
        page.feed(texte)
        page.close()

        if not page.langue:
            erreur(chemin, "attribut lang manquant sur <html>")
        if not page.titre.strip():
            erreur(chemin, "titre <title> vide ou manquant")
        if not page.description:
            erreur(chemin, "meta description manquante")

        doublons = {identifiant for identifiant in page.ids if page.ids.count(identifiant) > 1}
        for identifiant in sorted(doublons):
            erreur(chemin, f"identifiant HTML dupliqué : {identifiant}")

        for balise, valeur in page.liens:
            verifier_cible(chemin, valeur)

        for source in page.images_sans_alt:
            erreur(chemin, f"image sans attribut alt : {source}")

        verifier_ancres(page)
        verifier_css(chemin, texte)

    print(f"Pages vérifiées : {len(pages)}")

    if avertissements:
        print("\nAvertissements :")
        for message in avertissements:
            print(f"  - {message}")

    if erreurs:
        print("\nErreurs :")
        for message in erreurs:
            print(f"  - {message}")
        print(f"\n{len(erreurs)} erreur(s) à corriger.")
        return 1

    print("Aucune erreur détectée.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
