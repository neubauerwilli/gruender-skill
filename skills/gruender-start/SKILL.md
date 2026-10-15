---
name: gruender-start
description: >-
  Dein Startleiter. Baut einen datierten Schritt-für-Schritt-Startplan: zuerst ein
  günstiger Test in der Wirklichkeit (eine Warteliste, ein Vorverkauf oder ein Pop-up
  mit echtem Preis, damit echte Käufer bestätigen, was das simulierte Panel gesagt
  hat), dann der Countdown bis zum Eröffnungstag mit Verantwortlichen und Fristen, der
  Ablaufplan für den Starttag und die ersten 30 Tage mit dem, was du misst und was du
  änderst. Nutze ihn, wenn der Nutzer sagt "wie starte ich", "Startplan", "wann kann
  ich eröffnen", "Start-Checkliste", "live gehen" oder "Soft Opening" (englisch: "how
  do I launch", "launch plan", "when can I open", "launch checklist", "go live",
  "soft open").
argument-hint: "[gewünschtes Startdatum]"
---

# gruender-start

Ein Start ist ein Projekt mit Datum. Dieser Skill macht aus allem, was das Paket sonst
erzeugt hat, einen datierten Plan und beginnt mit dem günstigsten Weg
herauszufinden, ob echte Menschen zahlen, bevor das große Geld ausgegeben wird.

## Schritt 1: testen, bevor du ausgibst

Such den günstigsten echten Test, der zum Geschäft passt, und führe ihn aus, bevor du
die großen Kosten in `gruender/zahlen.json` eingehst:

| Geschäft | der Test |
| --- | --- |
| Laden oder Café | ein Pop-up, ein Marktstand oder eine Vorbestellliste mit Preis und Datum |
| Onlineprodukt | eine Landingpage mit dem Preis und einem Button "Vorbestellen" oder "Auf die Warteliste" |
| Dienstleistung oder Agentur | drei zahlende Pilotkunden zum geplanten Preis |
| Abo | ein Angebot für Gründungsmitglieder, im Voraus bezahlt |

Schreib die Erfolgslinie auf, bevor du den Test startest (zum Beispiel: 50
Vorbestellungen in zwei Wochen zu 6,50 €), und vergleiche das Ergebnis mit der Kaufquote
des Panels. Bleiben die echten Käufer deutlich hinter dem Panel zurück, vertraue den
echten Käufern und geh zurück zu `/gruender-angebot` oder `/gruender-preis`.

## Schritt 2: der Countdown

Von heute bis zum Starttag, mit echten Daten (frag nach dem Wunschdatum; Vorgabe ist
das früheste realistische Datum unter Berücksichtigung der Lieferzeiten in
`gruender/betrieb.md`). Wochenblöcke, jede Aufgabe mit Verantwortlichem und Frist:

- Recht und Geld: Anmeldung, Bankkonto, Genehmigungen aus `gruender/betrieb.md`.
- Aufbau: Ausbau oder Website, Lieferanten nach ihren Lieferzeiten bestellt.
- Marke: Schild, Verpackung, Profile aus `gruender/marke.md`.
- Marketing: der Kalender in `gruender/marketing.md` ab 14 Tage vor dem Start.
- Team: Einstellung und Einarbeitung anhand der SOPs.
- Ein Soft Opening oder ein Tag für Freunde und Familie vor dem öffentlichen Start.

Markiere den kritischen Pfad: die Aufgaben, die den Starttermin verschieben, wenn sie
sich verzögern.

## Schritt 3: der Starttag

Ein Ablaufplan Stunde für Stunde: wer ist wo, was geht auf welchem Kanal raus, das
Eröffnungsangebot, was zu tun ist, wenn etwas kaputtgeht (aus dem Risikoregister).

## Schritt 4: die ersten 30 Tage

Die wöchentlichen Zahlen, die du verfolgst (vom Finanzchef: Einheiten pro Tag im
Vergleich zum Break-even; vom Marketing: die Kanalzahlen), die Schwelle, die eine
Änderung auslöst, und ein Rückblick an Tag 7, 14 und 30 mit den Fragen, die du
beantworten musst.

## Ergebnis

`gruender/start.md` mit dem Test, dem Countdown, dem Ablaufplan und dem
30-Tage-Rückblick. Als Nächstes: `/gruender-plan` fasst alles im Businessplan
zusammen.
