# Der Gründer-Skill

Elf Claude-Skills auf Deutsch, die dein Business testen, bevor du startest. Kostenlos, MIT, keine Anmeldung,
kein API-Schlüssel, nichts zu verbinden.

`skills/gruender-vorstand` `skills/gruender-marketing` `skills/gruender-finanzen`
`skills/gruender-kunden` `skills/gruender-start` `skills/gruender-preis`
`skills/gruender-angebot` `skills/gruender-konkurrenz` `skills/gruender-marke`
`skills/gruender-betrieb` `skills/gruender-plan`

Einer ist dein Vorstand und prüft deine Idee nach den Frameworks von Alex Hormozi, Peter Thiel und Steve Jobs.
Einer ist dein Marketingchef. Einer ist dein Finanzchef und rechnet deine echten Gewinnmargen aus. Und einer ist
das Kundenpanel: Er baut dir 100 KI-Käufer aus deiner Zielgruppe und schickt dein Business durch 100 Kaufsituationen.

So weißt du, wie du startest, wie du Kunden gewinnst und wie du wirklich Geld verdienst, bevor du Tausende Euro
ausgibst, um es auf die harte Tour herauszufinden.

## Einrichten

Füge den Link zu diesem Repo in Claude ein und sag `install skill`:

```
https://github.com/neubauerwilli/gruender-skill

install skill
```

Oder als Plugin in Claude Code:

```
/plugin marketplace add neubauerwilli/gruender-skill
/plugin install gruender-skill@gruender-skill
```

Als Plugin bekommen die Skills einen Namensraum, sie heißen dann `/gruender-skill:gruender-vorstand` und so
weiter. Wenn du einfach `/gruender-vorstand` willst, kopiere die Ordner:

```bash
git clone https://github.com/neubauerwilli/gruender-skill.git
cp -r gruender-skill/skills/gruender-* ~/.claude/skills/
```

Nur für ein Projekt statt global: dieselben Ordner nach `.claude/skills/` in deinem Projekt kopieren. Gar kein
Claude Code? Füge eine einzelne `SKILL.md` oben in einen Chat ein, dann läuft sie als Modus. Unteragenten und
Python-Werkzeuge fallen dann weg, die Methode funktioniert trotzdem.

Die Werkzeuge brauchen Python 3.8 oder neuer. Nichts per pip installieren. Unter Windows heißt der Aufruf oft
`py` statt `python3`.

## Die elf

| Befehl | Rolle | Was er macht |
| --- | --- | --- |
| `/gruender-vorstand` | Vorstand | Drei Vorstandsmitglieder, jedes ein Unteragent mit einem veröffentlichten Framework (Angebot, aus *$100M Offers*; Monopol, aus *Zero to One*; Produkt, aus Isaacsons *Steve Jobs*), bewerten die Idee, nennen, woran sie scheitern würde, und stimmen ab. |
| `/gruender-konkurrenz` | Konkurrenz-Scout | Sucht direkte und indirekte Konkurrenten und Ersatzlösungen aus öffentlichen Quellen, mit Preisen, Positionierung und dem, worüber sich ihre Kunden beschweren. Jede Angabe verlinkt. |
| `/gruender-kunden` | Kundenpanel | Baut einen Schwarm aus Käufer-Agenten (standardmäßig 100) aus deiner Zielgruppe, jeder mit eigenem Einkommen, eigenen Gewohnheiten und eigenem Einwand, und zählt, wer kauft, wer nicht und warum. |
| `/gruender-preis` | Preisstratege | Macht aus den Preisantworten des Panels eine akzeptierte Preisspanne, legt sie neben Konkurrenz und Marge und wählt, was getestet wird. |
| `/gruender-angebot` | Angebotsarchitekt | Baut das Angebot (Boni, Garantie, echte Dringlichkeit, ein Name), das die Einwände des Panels beantwortet, und testet es erneut am Panel. |
| `/gruender-finanzen` | Finanzchef | Stückrechnung (Unit Economics): Deckungsbeitrag je Verkauf, echte Gewinnmarge, Break-even pro Tag, Jahr 1 Monat für Monat, Kapitalbedarf, Amortisation, Was-wäre-wenn. |
| `/gruender-marketing` | Marketingchef | Positionierung, die Kanäle deiner Käufer, eine datierte 30-Tage-Startkampagne, zehn Hooks und das Maximum, das du für einen Kunden zahlen kannst. |
| `/gruender-marke` | Markendesigner | Namensvorschläge mit den nötigen Marken-, Domain- und Handle-Prüfungen, eine Tonalität, ein Versprechen und ein Briefing für den Look. |
| `/gruender-betrieb` | Betriebsleiter | Lieferanten, Personal, Abläufe ab Tag eins, Werkzeuge, zu prüfende Genehmigungen und ein Risikoregister. Echte Kosten gehen zurück an den Finanzchef. |
| `/gruender-start` | Startleiter | Zuerst ein günstiger Test mit echten Käufern, dann ein datierter Countdown, der Ablaufplan für den Starttag und die ersten 30 Tage. |
| `/gruender-plan` | Businessplaner | Fasst alles in einem Businessplan zusammen, mit einem Urteil, das aus den Zahlen berechnet wird: Profitabel, Noch nicht oder Unvollständig. |

## So nutzt du ihn

Führe sie in dieser Reihenfolge aus. Jeder liest, was die anderen in den Ordner `gruender/` in deinem Projekt
geschrieben haben.

```
vorstand -> konkurrenz -> kunden -> preis -> angebot -> finanzen -> marketing -> marke -> betrieb -> start -> plan
```

Ein Beispiel: ein Matcha-Café in München, Iced Matcha Latte für 6,50 € pro Becher. (Alle Eingaben stehen in den
Beispieldateien dieses Repos, du kannst die Werkzeuge also direkt daran ausprobieren.)

1. **`/gruender-vorstand`** schreibt aus deinen Angaben `gruender/idee.md` und legt sie drei Vorstandsmitgliedern
   vor. Jedes bewertet sie, listet die Risiken und stimmt ab: investieren, investieren wenn, oder ablehnen. Die
   Bedingungen werden zur Checkliste für alle weiteren Skills.
2. **`/gruender-konkurrenz`** sucht die Matcha-Bars und Cafés in Laufweite, was sie für einen Latte verlangen und
   worüber sich ihre Bewertungen beschweren.
3. **`/gruender-kunden`** baut die Zielgruppe (Berufstätige in der Stadt, 24 bis 38, die fast täglich Kaffee
   kaufen), verteilt 100 Käuferkarten über Einkommen, Gewohnheiten und Einwände und startet einen Unteragenten je
   Käufer. Zurück kommt, wer kauft, wer nicht, die Gründe in ihren Worten („mein Café ist näher“, „6,50 € ist viel
   für ein Getränk“) und was ein Nein umdrehen würde.
4. **`/gruender-preis`** macht aus den vier Preisantworten je Käufer eine Preisspanne und prüft 6,50 € dagegen und
   gegen die Konkurrenz.
5. **`/gruender-angebot`** beantwortet die häufigsten Einwände mit dem Angebot (ein Eröffnungspreis, eine
   Stempelkarte) und lässt ein kurzes Panel erneut laufen, um zu sehen, ob sich die Kaufquote bewegt.
6. **`/gruender-finanzen`** rechnet die Stückrechnung. Mit den Beispielzahlen: Jeder Becher lässt nach seinen
   eigenen Kosten 4,76 € übrig, der Break-even liegt bei 186 Bechern am Tag, die Gewinnmarge bei den geplanten
   383 Bechern am Tag beträgt 38 %, Jahr 1 bringt nach einem langsamen Anlauf 93.926 € aus dem Betrieb, die
   25.280 € Startkosten sind in Monat 8 wieder drin, und der Gründer braucht 34.092 € Kapital, bevor sich das
   Café selbst trägt.
7. **`/gruender-marketing`**, **`/gruender-marke`**, **`/gruender-betrieb`** und **`/gruender-start`** machen
   daraus eine 30-Tage-Kampagne, einen Namen und einen Look, Lieferanten und Abläufe und einen datierten Start,
   der mit einem Pop-up beginnt, um echte Käufer zu testen.
8. **`/gruender-plan`** fasst alles in `gruender/businessplan.md` zusammen. Das Urteil wird berechnet, nicht
   geschrieben: Profitabel nur, wenn jede Einheit Geld verdient, Jahr 1 Gewinn macht, der Break-even in die
   Kapazität passt und genug Panel-Käufer kaufen.

Du kannst jeden Skill auch einzeln nutzen. `/gruender-kunden --quick` auf eine Idee, über die du gerade nur
nachdenkst, zeigt dir schnell, ob es sich lohnt, weiterzumachen.

## Die Werkzeuge

Vier Stück, alle nur Python-Standardbibliothek. Keines geht ins Internet.

```bash
python3 skills/gruender-finanzen/unit_economics.py gruender/zahlen.json --out gruender/finanzen.md   # Margen, Break-even, Jahr 1
python3 skills/gruender-kunden/panel.py init --customer gruender/kunde.json --pitch gruender/pitch.md
python3 skills/gruender-preis/van_westendorp.py gruender/panel/antworten --price 6.50               # die akzeptierte Preisspanne
python3 skills/gruender-plan/compile.py --dir gruender                                               # der Plan und sein Urteil
```

**`unit_economics.py`** liest eine JSON-Datei (Beispiel: `skills/gruender-finanzen/example.json`) und berichtet
Deckungsbeitrag, Break-even, Marge im Plan, Jahr 1 nach Monaten, Kapitalbedarf, Amortisation und drei
Was-wäre-wenn-Fälle. Jede Zahl geht auf eine Eingabe zurück; ein fehlendes Feld ist ein Fehler, nie eine Schätzung.

**`panel.py`** verteilt Persona-Karten aus deiner Zielgruppe (gleicher Seed, gleiche Karten), schreibt ein Briefing
je Käufer, prüft die Antworten und zählt sie aus. Es antwortet nie an Stelle eines Käufers.

**`van_westendorp.py`** liest vier Preisantworten je Käufer (aus dem Panel oder als CSV aus einer echten Umfrage)
und findet die Punkte, an denen ein Preis zu billig oder zu teuer wirkt, den optimalen und den neutralen Preis.

**`compile.py`** setzt den Plan zusammen und berechnet das Urteil.

```bash
python3 -m unittest discover -s tests -v
```

## Kleingedrucktes

**Der Vorstand wendet veröffentlichte Frameworks an. Er ist nicht diese Personen.** Die drei Linsen sind kurze
Zusammenfassungen, in eigenen Worten, von Ideen aus *$100M Offers* von Alex Hormozi, *Zero to One* von Peter
Thiel mit Blake Masters und Walter Isaacsons Biografie über Steve Jobs. Der Vorstand spricht nie als sie, zitiert
sie nicht und behauptet nicht, dass sie etwas empfehlen. Dieses Projekt hat keine Verbindung zu ihnen.

**Das Kundenpanel sind simulierte Käufer, keine Kunden.** Es ist ein schneller, günstiger Weg, Einwände,
Zielgruppen und Formulierungen zu finden, bevor du Geld ausgibst. Es ist keine Prognose: Sprachmodelle stimmen
gern zu, lies die Kaufquote also als Obergrenze und bestätige die großen Entscheidungen mit echten Menschen.
`/gruender-start` beginnt genau mit diesem Test. Panel-Antworten sind Recherche; nutze sie nie als
Kundenstimmen.

**Die Zahlen sind nur so gut wie die Eingaben.** Der Finanzchef markiert jede Schätzung als Schätzung und fragt
nach echten Angeboten. Prüfe Kosten bei Lieferanten und Rechtsform, Lohn und Steuern mit einem Steuerberater.

**Recherche nutzt öffentliche Quellen, mit Links.** Keine erfundenen Konkurrenten, Preise, Bewertungen oder
Zitate. Kein Scraping gegen die Bedingungen einer Seite.

**Keine Finanz-, Rechts- oder Steuerberatung.** Genehmigungen, Marken und Werbeaussagen hängen davon ab, wo du
bist. Die Skills sagen dir, was du wo prüfen musst; eine Fachperson bestätigt es.

## Dateien

```
skills/gruender-vorstand/    SKILL.md, lenses.md
skills/gruender-konkurrenz/  SKILL.md
skills/gruender-kunden/      SKILL.md, panel.py, kunde.example.json, pitch.example.md
skills/gruender-preis/       SKILL.md, van_westendorp.py
skills/gruender-angebot/     SKILL.md
skills/gruender-finanzen/    SKILL.md, unit_economics.py, example.json
skills/gruender-marketing/   SKILL.md
skills/gruender-marke/       SKILL.md
skills/gruender-betrieb/     SKILL.md
skills/gruender-start/       SKILL.md
skills/gruender-plan/        SKILL.md, compile.py
tests/                       die Tests für jedes Werkzeug
```

Deine eigenen Dateien liegen in `gruender/` in deinem Projekt. Die Skills lesen gegenseitig ihre Ergebnisse.

## Herkunft

Deutsche Fassung von Willi Neubauer, [willineubauer.com](https://willineubauer.com), Instagram
[@willi_neubauer.ai](https://www.instagram.com/willi_neubauer.ai/).

Beruht auf dem englischen [Founder skill](https://github.com/Jakeschincariol/founder-skill) von Jake Schincariol
([opusjake.ai](https://opusjake.ai)), veröffentlicht unter MIT. Übersetzt und für den deutschsprachigen Raum
angepasst (Euro, deutsches Beispiel, Hinweise auf DPMA, Gewerbeamt und IHK).

## Lizenz

MIT, siehe `LICENSE`. Nimm es, ändere es, nutze es.
