---
name: gruender-kunden
description: >-
  Das Kundenpanel. Startet einen Schwarm von Käufer-Unteragenten (Standard 100,
  --quick für 20), trainiert auf den Zielkunden des Nutzers, jeder mit anderem
  Einkommen, Alter, Kaufverhalten und Einwand, zeigt jedem denselben Pitch und lässt
  das Business durch 100 Käuferszenarien laufen, um zu sehen, wer kauft, wer nicht
  und warum. Zählt die Antworten zusammen zu Kaufraten nach Segment, den Gründen,
  warum Leute abwinken, in ihren eigenen Worten, was ein Nein kippen würde, und
  Preisantworten für gruender-preis. Nutze den Skill, wenn der Nutzer sagt "würden
  Leute das kaufen", "teste es an Kunden", "starte das Kundenpanel", "simuliere
  Käufer", "wer ist mein Kunde", "prüfe die Nachfrage". Englische Auslöser: "would
  people buy this", "test it on customers", "run the consumer panel", "simulate
  buyers", "who is my customer", "validate demand".
argument-hint: "[--n 100 | --quick] [--seed S]"
---

# gruender-kunden

Der verrückteste Teil des Pakets. Statt zu raten, ob Leute kaufen werden, fragst du
hundert von ihnen, jeder ein Unteragent, der einen bestimmten Käufer aus deinem
Zielkunden spielt. Du bist der Moderator. Du antwortest nie für einen Käufer.

Was der Nutzer nach `/gruender-kunden` getippt hat: `$ARGUMENTS`

## Das Werkzeug

Die ganze Buchführung läuft über `panel.py` im Ordner dieses Skills:

```bash
python3 "${CLAUDE_SKILL_DIR}/panel.py" <Befehl>
```

Unten steht `PANEL` für genau diesen Aufruf. Wird der Pfad nicht aufgelöst, nimm das
Basisverzeichnis, das Claude Code für diesen Skill ausgegeben hat. Der Stand liegt
in `gruender/panel/`.

## Schritt 1: der Zielkunde

Schreibe `gruender/kunde.json` (Form: `kunde.example.json` in diesem Ordner):

- `business` und `target`: wer der Kunde ist, in einer konkreten Zeile.
- `segments`: 2 bis 4 Gruppen mit `share` und einer `income`-Spanne [niedrig, hoch].
- `behaviours`: 4 bis 8 Kaufverhalten mit `share` und einer `how`-Zeile (täglicher
  Stammkunde, Schnäppchenjäger, liest jede Bewertung, einem Wettbewerber treu …).
- `objections`: die 4 bis 8 Zweifel, die diese Art Käufer wirklich hat.
- `habits` (optional): Alltagszeilen, die einen Käufer greifbar machen.

Verankere es in etwas Echtem. Nutze, was der Nutzer über seine Kunden weiß, und,
falls `/gruender-konkurrenz` gelaufen ist, die Beschwerden in
`gruender/konkurrenz.md`. Hat der Nutzer echte Kundendaten (Interviews,
Bewertungen, Umfrageantworten), nimm lieber sie als deine Vermutungen und sag, welche
Teile Vermutungen sind. Zeige dem Nutzer das Profil in wenigen Zeilen und lass ihn
korrigieren, bevor du austeilst: Ein falscher Kunde macht das ganze Panel falsch.

## Schritt 2: der Pitch

Schreibe `gruender/pitch.md`: was ein Käufer tatsächlich sehen würde. Das Produkt,
der Preis, wo und wie man es bekommt, ein Eröffnungsangebot. Drei bis sechs
schlichte Zeilen, keine Superlative, nichts, was das Business nicht liefern kann.
Jeder Käufer sieht genau das.

## Schritt 3: austeilen und laufen lassen

```bash
PANEL init --customer gruender/kunde.json --pitch gruender/pitch.md --n 100
PANEL prompts
```

`init` teilt die Persona-Karten aus (gleicher Seed, gleiche Karten; der Seed wird
festgehalten). `prompts` schreibt einen Brief pro Käufer und listet sie in Wellen zu
je 10 auf. Schicke für jede Welle EINE Nachricht mit einem Agent-Aufruf pro Käufer
dieser Welle (das Agent-Werkzeug heißt in älteren Claude-Code-Versionen Task):

- `subagent_type`: `general-purpose`
- `description`: `panel <id>`
- `prompt`: `Lies <Brief-Pfad> und folge ihm genau. Er ist dein ganzer Auftrag.`

Warte auf die ganze Welle, bevor die nächste kommt. Claude Code führt standardmäßig
etwa 10 Werkzeugaufrufe gleichzeitig aus, also sind 100 Käufer 10 Wellen. Nach der
letzten Welle:

```bash
PANEL check      # listet fehlende oder kaputte Antworten
PANEL prompts    # schreibt Briefs nur für diese neu; noch einmal laufen lassen
PANEL tally
```

Hat ein Käufer sein JSON in der Antwort ausgegeben, statt die Datei zu schreiben (das
kommt vor), lege seine eigene Antwort mit `PANEL save <id>` ab und gib die Antwort
über stdin; `save` lehnt alles ab, was keine gültige Antwort ist. Ein Käufer, der
zweimal scheitert, wird weggelassen und in den Ergebnissen mitgezählt. Schreibe nie
selbst eine Antwort für einen Käufer.

Sag dem Nutzer vor einem Lauf mit 100 Käufern, dass das 100 Unteragenten-Aufrufe
sind, und schlage `--quick` (20 Käufer) für einen ersten Blick vor. Unteragenten
schreiben je eine Datei nach `gruender/panel/antworten/`; im Standard-Rechtemodus
ist das eine Freigabe pro Datei, also schlage für den Lauf den Modus
"Änderungen akzeptieren" vor (Umschalt+Tab).

## Schritt 4: dem Nutzer vorlesen

`PANEL tally` schreibt `gruender/panel/ergebnis.md` und `ergebnis.json`. Gib dem
Nutzer:

1. Die Schlagzeile: "40 kaufen · 60 nicht" und die Kaufrate.
2. Wer kauft und wer nicht: die Segment- und Verhaltenszeilen, die sich am
   stärksten unterscheiden.
3. Warum sie abwinken: die drei häufigsten Gründe mit je einem Zitat, wie
   geschrieben.
4. Was ein Nein kippen würde: die am häufigsten wiederholten Antworten.
5. Ein Satz dazu, was zu ändern ist, bevor Geld ausgegeben wird, und welcher Skill
   das übernimmt (Preis, Angebot, Marketing).

## Ehrliche Grenzen, einmal sagen

Das sind simulierte Käufer. Sie sind gut darin, Einwände, Segmente und Formulierungen
aufzudecken, an die du nicht gedacht hattest, und schlecht darin, die echte
Konversion vorherzusagen: Sprachmodelle neigen zur Zustimmung, also behandle die
Kaufrate als Obergrenze. Bestätige die großen Entscheidungen mit echten Menschen
(einer Warteliste, einem Vorverkauf, einer Landingpage mit Preis), bevor du etwas
unterschreibst. Gib Panel-Zitate nicht als Kundenstimmen aus.

## Der Brief, den jeder Käufer bekommt

`panel.py` füllt die Karte in eine feste Vorlage (siehe `BRIEF` im Skript): wer der
Käufer ist (Name, Alter, Segment, Einkommen, Kaufverhalten, eine Gewohnheit, der
Zweifel, der ihm in den Sinn kommt), der Pitch Wort für Wort, die Anweisung, nicht
zustimmungsfreudig zu sein und keine Fakten zu erfinden, und das genaue JSON, das zu
schreiben ist: kauft, Käufe im ersten Monat, ein Grundcode, der Grund in der
eigenen Stimme, der Haupteinwand, was seine Meinung ändern würde, und vier
Preisantworten (zu billig, ein Schnäppchen, wird teuer, zu teuer). Ändere nie den
Brief für einen einzelnen Käufer.

## Ergebnis

`gruender/kunde.json`, `gruender/pitch.md`, `gruender/panel/` (Karten, Briefs,
Antworten, Ergebnisse). Als Nächstes: `/gruender-preis` liest die Preisantworten,
`/gruender-angebot` und `/gruender-marketing` lesen die Einwände.
