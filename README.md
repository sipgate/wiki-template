# Team Wiki Template

Ein von LLM-Agents gepflegtes Wiki: [Quartz](https://quartz.jzhao.xyz) als
Static-Site-Generator, Deployment über GitHub Pages, ein mechanischer Wiki-Lint
im CI, und eine `AGENTS.md`, die dem Agent die Pflege vorschreibt.
Basiert auf dem [LLM-Wiki-Pattern von Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

## Aus "Use this template" wird ein Wiki

1. **Repo aus dem Template anlegen** -- Button „Use this template" oben rechts.
2. **Quartz konfigurieren** in `quartz.config.yaml`:
   - `pageTitle`: Name des Wikis
   - `baseUrl`: die Web-Adresse der späteren GitHub-Pages-Site, **ohne** `https://`.
     Sie steht schon vor der Aktivierung fest und ergibt sich immer aus
     `<org>.github.io/<repo-name>` -- für ein Repo in der sipgate-Org heißt das
     z. B. `sipgate.github.io/mein-wiki`. (Nicht zu verwechseln mit dem Repo-Link
     auf `github.com` -- der gehört nur in den Footer-Link, siehe unten.)
     Quartz baut daraus alle internen Links, Sitemap und RSS: steht hier der
     falsche Wert, sind die Links der veröffentlichten Site kaputt.
   - Footer-Link `GitHub:` auf das eigene Repo zeigen lassen, also
     `https://github.com/sipgate/<repo-name>` -- das ist der Repo-Link, nicht die
     Pages-Adresse.
3. **GitHub Pages aktivieren**: Repo → Settings → Pages → Source: **GitHub Actions**.
   Der Workflow `deploy.yml` baut bei jedem Push auf `main` und veröffentlicht die Site.
4. **`AGENTS.md` anpassen**: Thema des Wikis beschreiben (erste Zeilen) und die
   Themenbereiche festlegen, die das Team nutzen will.
5. **Beispiel-Inhalt entfernen**: `wiki/beispiel/`, `raw/beispiel-quelle.md` und die
   Beispiel-Einträge in `wiki/index.md` löschen oder umbauen.
6. **Agent anbinden**: Die `AGENTS.md` funktioniert mit jedem coding-agent, der
   Repo-Anweisungen liest (opencode, Claude Code, Cursor, ...). Der Agent legt
   Ingest-Änderungen als Pull Requests an; das `automerge`-Label merged sie,
   sobald der Lint-Check grün ist.

## Vor dem ersten Merge empfehlen

- Branch-Protection für `main`: Pflichtcheck „Lint Wiki", kein Direktpush.
- Das Label `automerge` im Repo anlegen.

## Lokal arbeiten

```bash
npm ci
npx quartz build --serve -d wiki   # Site auf http://localhost:8080
python3 scripts/lint-wiki.py       # Wiki-Lint, 0 = sauber
```

## Wie das Wiki funktioniert

- `raw/` nimmt Quelldokumente auf (Transkripte, Notizen, Diagramm-Exporte) --
  unveränderlich, nur lesen.
- Der Agent destilliert Quellen in thematische Seiten unter `wiki/`, verlinkt sie
  untereinander und hält `wiki/index.md` und `wiki/log.md` aktuell.
- Alles Weitere -- Strukturprinzip, Zitierregeln, PR-Betrieb -- steht in der
  [`AGENTS.md`](AGENTS.md).
