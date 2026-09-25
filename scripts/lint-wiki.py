#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mechanischer Lint für das Wiki.

Prüft, was sich automatisch prüfen lässt: Links, Seitenformat, Quellenbezüge,
Namensschema und Hinweise auf Regelverstöße aus AGENTS.md. Inhaltliche Prüfungen
(Widersprüche zwischen Seiten, überholte Aussagen) bleiben Aufgabe des Agents.

Aufruf:  python3 scripts/lint-wiki.py
Rückgabe: 0 wenn sauber, 1 wenn Befunde vorliegen.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI = os.path.join(ROOT, "wiki")
RAW = os.path.join(ROOT, "raw")

# Seiten ohne inhaltliches Seitenformat -- in jedem Ordner
SONDERSEITEN = {"index", "log"}

PFLICHTFELDER = [
    "**Zusammenfassung**",
    "**Quellen**",
    "**Zuletzt aktualisiert**",
    "## Verwandte Seiten",
]

# Dateinamen, die nach Quelle statt nach Thema geschnitten sind
QUELLENSCHNITT = re.compile(
    r"(^\d{4}-\d{2}-\d{2})|(^k3k-\d+)|(refinement|meeting|besprechung|protokoll|notizen)",
    re.I,
)

LINK = re.compile(r"\[\[([^\]]+)\]\]")
ZITAT = re.compile(r"[„\"]([^\"“”„]{3,})[\"“]")
MARKER = re.compile(r"^(<<<<<<<|=======|>>>>>>>)", re.M)
CODEBLOCK = re.compile(r"```.*?```", re.S)
CODESPAN = re.compile(r"`[^`\n]*`")
FRONTMATTER = re.compile(r"\A---\n.*?\n---\n?", re.S)


def ohne_frontmatter(inhalt):
    """Frontmatter-Block am Dateianfang entfernen."""
    return FRONTMATTER.sub("", inhalt, count=1)


def ohne_code(inhalt):
    """Code-Blöcke und Inline-Code entfernen -- dort stehen Beispiele, keine Links."""
    return CODESPAN.sub("", CODEBLOCK.sub("", inhalt))

befunde = []


def melde(kategorie, text):
    befunde.append((kategorie, text))


def seiten():
    for wurzel, _, dateien in os.walk(WIKI):
        for name in sorted(dateien):
            if name.endswith(".md"):
                yield name[:-3], os.path.join(wurzel, name)


def linkziele(inhalt):
    """Wiki-Links auflösen, inklusive [[seite|Alias]] und [[seite#Abschnitt]]."""
    for roh in LINK.findall(inhalt):
        ziel = roh.split("|")[0].split("#")[0].strip()
        if ziel:
            yield ziel


def main():
    # Nach relativem Pfad schlüsseln: seit der Ordnerstruktur gibt es mehrere
    # index.md, die sich bei Schlüsselung nach Dateiname gegenseitig überschreiben.
    texte = {}
    stamm_zu_pfad = {}
    for stem, pfad in seiten():
        rel = os.path.relpath(pfad, WIKI)
        with open(pfad, encoding="utf-8") as f:
            texte[rel] = f.read()
        if stem in SONDERSEITEN:
            continue
        if stem in stamm_zu_pfad:
            melde("Doppelter Seitenname", stem + " -- " + stamm_zu_pfad[stem] + " und " + rel)
        stamm_zu_pfad[stem] = rel

    if not texte:
        print("Keine Wiki-Seiten gefunden -- läuft das Skript im richtigen Repo?")
        return 1

    raw_dateien = set()
    for wurzel, _, dateien in os.walk(RAW):
        for d in dateien:
            raw_dateien.add(os.path.relpath(os.path.join(wurzel, d), RAW))

    # Linkziele sind Seitennamen ohne Ordner; Sonderseiten sind gültige Ziele
    zielbar = set(stamm_zu_pfad) | SONDERSEITEN
    eingehend = {name: 0 for name in stamm_zu_pfad}
    im_index = set()

    for rel, roh in texte.items():
        name = os.path.basename(rel)[:-3]
        inhalt = ohne_frontmatter(roh)
        ziele = list(linkziele(ohne_code(inhalt)))

        # 1. Tote Links
        for ziel in ziele:
            if ziel in zielbar:
                if ziel != name and ziel in eingehend:
                    eingehend[ziel] += 1
            else:
                melde("Toter Link", rel + " -> [[" + ziel + "]]")

        # Jede index.md darf Seiten listen -- geprüft wird über alle zusammen
        if name == "index":
            im_index.update(ziele)

        # 2. Konfliktmarker
        if MARKER.search(inhalt):
            melde("Merge-Marker", rel)

        # 3. Namensschema
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
            melde("Seitenname", rel + " -- klein mit Bindestrichen erwartet")

        # 4. Nach Quelle statt Thema geschnitten
        if QUELLENSCHNITT.search(name):
            melde("Quellenschnitt", rel + " -- Seitenname deutet auf Quelle statt Thema")

        if name in SONDERSEITEN:
            continue

        # 5. Seitenformat: Frontmatter mit Titel, danach der Inhalt
        fm = FRONTMATTER.match(roh)
        if not fm or not re.search(r"^title:\s*\S", fm.group(0), re.M):
            melde("Seitenformat", rel + " -- Frontmatter mit title fehlt")
        for feld in PFLICHTFELDER:
            if feld not in inhalt:
                melde("Seitenformat", rel + " -- " + feld + " fehlt")

        # 6. Quellenangaben zeigen auf vorhandene Rohdateien
        kopf = re.search(r"^\*\*Quellen\*\*:(.*)$", inhalt, re.M)
        if kopf:
            for bezug in re.findall(r"`raw/([^`]+)`", kopf.group(1)):
                pfad = os.path.join(RAW, bezug)
                # Eine Quelle darf eine Datei oder ein ganzes Verzeichnis sein
                if not (bezug in raw_dateien or os.path.isdir(pfad)):
                    melde("Fehlende Quelle", rel + " -> raw/" + bezug)

        # 7. Hinweis auf wörtliche Zitate: lange Passagen in Anführungszeichen
        for gefunden in ZITAT.findall(ohne_code(inhalt)):
            if len(gefunden.split()) > 8:
                kurz = gefunden[:60] + ("..." if len(gefunden) > 60 else "")
                melde("Zitatverdacht", rel + ' -- "' + kurz + '"')

    # 8. Waisenseiten
    for name, anzahl in sorted(eingehend.items()):
        if anzahl == 0:
            melde("Waisenseite", name + " -- keine eingehenden Links")

    # 9. Seiten, die in keiner index.md stehen
    for name in sorted(stamm_zu_pfad):
        if name not in im_index:
            melde("Nicht im Index", name)

    if not befunde:
        print("Lint sauber: " + str(len(stamm_zu_pfad)) + " Seiten geprüft, keine Befunde.")
        return 0

    print("Befunde (" + str(len(befunde)) + "):\n")
    nummer = 0
    letzte = None
    for kategorie, text in sorted(befunde):
        if kategorie != letzte:
            print("\n" + kategorie)
            letzte = kategorie
        nummer += 1
        print("  " + str(nummer) + ". " + text)
    print("\nZitatverdacht und Quellenschnitt sind Hinweise, keine Fehler -- sie brauchen eine inhaltliche Entscheidung.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
