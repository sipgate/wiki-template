# Team Wiki

Ein von LLM-Agents gepflegtes Wiki für Wissen und Entscheidungen aus dem
Arbeitskosmos des Teams.
Basiert auf dem [LLM-Wiki-Pattern von Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

## Zweck

Dieses Wiki ist eine strukturierte, verlinkte Wissensbasis rund um die Arbeit
des Teams. Der Agent pflegt das Wiki vollständig. Die Kuratiierung der Quellen,
die Fragen und die inhaltliche Steuerung liegen beim Menschen.

## Ordnerstruktur

```
raw/                       -- Quelldokumente (unveränderlich -- niemals bearbeiten)
wiki/                      -- vom Agent gepflegte Markdown-Seiten
wiki/index.md              -- Inhaltsverzeichnis des gesamten Wikis (Startseite der Site)
wiki/log.md                -- append-only Chronik aller Operationen (Anzeigetitel: Changelog)
wiki/<themenbereich>/      -- Themengebiete (je mit index.md als Ordner-Startseite)
```

### Themenbereiche

Seiten liegen in Themenbereichen, die auch die Navigation der Quartz-Site
gruppieren (Explorer links, Ordner-Startseiten, Breadcrumbs):

```
wiki/<themenbereich>/      -- z. B. architektur/, prozesse/, produkt/, strategie/
wiki/meta/                 -- das Wiki über sich selbst: Betrieb, Register
wiki/assets/               -- Bilder und Screenshots
```

- Die konkreten Themenbereiche legt das Team fest -- die Beispiele oben sind
  nur Vorschläge. Passt kein Bereich, beim User nachfragen, ob ein neuer her soll.
- Jeder Themenbereich hat eine `index.md` mit Frontmatter-Titel (großgeschrieben,
  z. B. `title: "Architektur"`), einem einzeiligen Steckbrief und optional
  Links zu externen Diagrammquellen. Beim Anlegen eines neuen Bereichs beides
  mit anlegen; Unterordner folgen demselben Muster.
- Die Ordner-`index.md`-Dateien enthalten **sonst keinen Inhalt** -- die Site
  listet die Seiten des Ordners automatisch auf.

## Strukturprinzip: thematisch, niemals nach Quelle

Das Wiki ist **ausschließlich nach Themen** gegliedert. Eine Seite steht für einen
Sachverhalt, nicht für ein Dokument.

- Es gibt **keine Seite je Meeting, Transkript, Dokument oder Quelltyp**. Kein
  `refinement-2026-08-20.md`, kein `post-mortems.md`, kein `gemini-notizen.md`.
- Seitennamen benennen die Sache: `buchungslogik.md`, `abrechnung-und-billing.md`.
  Sie enthalten kein Datum und keinen Quellenbezug.
- Auch `index.md` gliedert nach Themengebieten, nicht nach Dokumentarten.
- Sagt eine neue Quelle etwas zu einem bestehenden Thema, wird die **bestehende Seite
  ergänzt**, statt eine zweite Seite danebenzustellen.
- Die Herkunft einer Aussage steckt in der Zitatzeile (siehe Zitierregeln), nicht in
  der Seitenstruktur. Vollständigen Überblick über die Quellen gibt der Abschnitt
  „Quellen" in `index.md`.

Der Zuschnitt folgt der Frage, die jemand später stellen wird -- „wie funktioniert
ein Upgrade?" --, nicht der Frage, wo es besprochen wurde.

## Ingest-Workflow

Wenn der User eine neue Quelle in `raw/` legt und um Ingest bittet:

1. Quelle vollständig lesen
2. Nicht arbeitsrelevante Inhalte verwerfen, Diskussionen auf ihr Ergebnis eindampfen;
   wo kein eindeutiges Ergebnis erkennbar ist, beim User nachfragen
3. Kernpunkte mit dem User besprechen, bevor irgendetwas geschrieben wird
4. Die Aussagen der Quelle **den Themen zuordnen**: Welche bestehenden Seiten werden
   ergänzt, welche Themen brauchen eine neue Seite?
5. Neue Seiten in den passenden Themenbereich (Ordner) ablegen; fehlt ein Bereich,
   beim User nachfragen und mit `index.md` (Titel + Steckbrief) anlegen
6. Bestehende Seiten aktualisieren, neue Konzept- und Entitätsseiten nur für Themen
   anlegen, die es noch nicht gibt
7. Wiki-Links ([[seitenname]]) setzen, um verwandte Seiten zu verknüpfen
8. `wiki/index.md` mit neuen Seiten und einzeiligen Beschreibungen aktualisieren,
   die Quelle im Abschnitt „Quellen" ergänzen
9. Eintrag in `wiki/log.md` anhängen: Datum, Quellenname, was sich geändert hat

Eine einzelne Quelle kann 10-15 Wiki-Seiten berühren. Das ist normal.

Widerspricht eine neue Quelle einer bestehenden Seite, wird der Widerspruch auf der
Themenseite festgehalten -- mit beiden Quellen und ihrem Datum -- statt eine
konkurrierende Seite anzulegen.

## Betrieb: Änderungen über Pull Requests

Wiki-Änderungen laufen immer über Pull Requests, nie als Direkt-Push auf `main`.

- Der Agent legt pro Änderung einen Branch `ingest/<datum>-<slug>` an, committet
  alle Seiten dafür und öffnet einen Pull Request.
- Der PR bekommt das Label `automerge`, sobald er bereit ist. GitHub mergt ihn
  automatisch, sobald der Lint-Check (`Lint Wiki`) grün ist und keine Konflikte
  bestehen.
- **Es ist immer nur ein offener wiki-PR des Agents erlaubt.** Der nächste PR wird
  erst eröffnet, wenn der vorherige gemergt oder geschlossen ist.
- Liegen mehrere Änderungen gleichzeitig an (z. B. mehrere Quellen, deren Ingest
  aussteht), werden sie **in einem Branch und einem PR gesammelt**, statt mehrere
  PRs nebeneinander zu öffnen.
- Vor dem Öffnen eines PRs immer `main` einholen und den Branch auf den aktuellen
  Stand rebasen, damit die Änderungen auf dem neuesten Stand aufbauen.
- Meldet GitHub einen Merge-Konflikt, löst der Agent ihn selbst: `main` mergen,
  die betroffenen Dateien (typischerweise `wiki/log.md` und `wiki/index.md`)
  zusammenführen, den Konflikt im Commit auflösen und das Ergebnis im PR als
  Kommentar festhalten.

## Seitenformat

Jede Wiki-Seite beginnt mit einem Frontmatter-Titel, dann folgt der Inhalt:

```markdown
---
title: "Buchungslogik"
---

**Zusammenfassung**: Ein bis zwei Sätze, was diese Seite abdeckt.

**Quellen**: Liste der Rohdokumente, auf denen diese Seite beruht.

**Zuletzt aktualisiert**: Datum der letzten Änderung.

---

Hauptinhalt. Klare Überschriften, kurze Absätze.

Verwandte Konzepte im Text per [[wiki-links]] verlinken.

## Verwandte Seiten

- [[verwandtes-konzept-1]]
- [[verwandtes-konzept-2]]
```

Der Frontmatter-Titel ist der Anzeigetitel der Seite (Explorer, Suche,
Browser-Tab, Changelog-Box); der Dateiname bleibt der Slug für Links.

## Was ins Wiki gehört -- und was nicht

Das Wiki hält Arbeitsergebnisse fest, nicht den Weg dorthin.

- **Nur das Ergebnis einer Diskussion wird festgehalten**, nicht ihr Verlauf. Wer was
  vorgeschlagen, eingewendet oder hinterfragt hat, gehört nicht ins Wiki.
- **Ist das Ergebnis nicht eindeutig, wird nachgefragt.** Der Agent rekonstruiert kein
  Ergebnis aus einer Diskussion, die keines hatte, und schreibt auch keine Zusammen-
  fassung des Meinungsbilds. Entweder es gibt ein Ergebnis, oder der Punkt steht als
  offene Frage -- mit dem, was zur Entscheidung fehlt.
- **Nicht arbeitsrelevante Inhalte werden verworfen**: Begrüßungen, Smalltalk, Technik-
  probleme im Meeting, Terminfindung, Abschweifungen, persönliche Bemerkungen.
- **Keine Personen als Handelnde**, außer wo eine Zuständigkeit die Arbeit betrifft --
  etwa der Owner einer offenen Frage oder das umsetzende Team.

## Zitierregeln

- Jede sachliche Aussage referenziert ihre Quelle
- Format: (Quelle: dateiname.pdf) nach der Aussage
- Bei Transkripten zusätzlich der Zeitstempel der Stelle, z. B. (00:31:11)
- **Keine wörtlichen Zitate von Personen.** Aussagen werden in eigenen Worten als Sach-
  verhalt formuliert und über die Quellenangabe belegt. In Anführungszeichen stehen nur
  Benennungen: UI-Texte, Produkt- und Feldnamen, Statuswerte
- Widersprechen sich zwei Quellen, wird der Widerspruch explizit festgehalten
- Aussagen ohne Quelle werden als "prüfungsbedürftig" markiert
- Zahlen, die in einer automatisch erzeugten Quelle verstümmelt sind, werden ebenfalls
  als prüfungsbedürftig markiert, statt sie zu rekonstruieren

## Fragen beantworten

Wenn der User eine Frage stellt:

1. Zuerst `wiki/index.md` lesen, um relevante Seiten zu finden
2. Diese Seiten lesen und eine Antwort synthetisieren
3. Konkrete Wiki-Seiten in der Antwort zitieren
4. Ist die Antwort nicht im Wiki, das klar sagen
5. Ist die Antwort wertvoll, anbieten, sie als neue Wiki-Seite zu sichern

Gute Antworten gehören zurück ins Wiki, damit sie sich langfristig anhäufen.

## Lint

Zuerst den mechanischen Lint laufen lassen:

```
python3 scripts/lint-wiki.py
```

Er prüft tote Wiki-Links (inklusive der Alias-Schreibweise `[[seite|Anzeigetext]]`),
Waisenseiten, Seitenformat (Frontmatter-Titel), Namensschema, Quellenbezüge auf
`raw/`, Konfliktmarker, Seiten ohne Index-Eintrag sowie Verdachtsfälle auf wörtliche
Zitate und auf Seiten, die nach Quelle statt nach Thema geschnitten sind. Das Skript
liest `wiki/` rekursiv, Ordner-`index.md`-Dateien sind vom Format-Check ausgenommen.
Rückgabewert 0 heißt sauber.

Was das Skript nicht kann, prüft der Agent selbst:

- Widersprüche zwischen Seiten prüfen
- Konzepte identifizieren, die erwähnt werden, aber keine eigene Seite haben
- Aussagen kennzeichnen, die durch neuere Quellen überholt sein könnten
- Die Verdachtsfälle des Skripts bewerten: Ist ein Zitat wirklich eines, ist ein
  Seitenschnitt wirklich quellenbasiert?
- Personenzuschreibungen aufspüren, die dort nicht hingehören
- Befunde als nummerierte Liste mit vorgeschlagenen Fixes reporten

## Regeln

- Niemals etwas in `raw/` verändern
- Seiten thematisch schneiden, niemals nach Quelle, Meeting oder Dokumenttyp
- Ergebnisse festhalten, keine Diskussionsverläufe; keine wörtlichen Zitate
- Nach jeder Änderung `wiki/index.md` und `wiki/log.md` aktualisieren
- Seitennamen klein mit Bindestrichen (z. B. `team-prozess.md`)
- Klar und verständlich schreiben
- Bei Unsicherheit über die Einordnung: nachfragen
