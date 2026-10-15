---
name: gruender-finanzen
description: >-
  Dein Finanzchef (Your CFO). Baut die Stückrechnung (Unit Economics) eines
  Unternehmens, bevor Geld ausgegeben wird: was eine Einheit nach ihren direkten
  Kosten verdient, die echte Gewinnmarge bei der geplanten Menge, den Break-even in
  Einheiten pro Tag, das erste Jahr Monat für Monat, das Geld, das gebraucht wird,
  bevor es sich selbst trägt, wie lange die Startkosten brauchen, bis sie
  zurückverdient sind, und was passiert, wenn der Preis sinkt, der Absatz niedrig
  ausfällt oder die Kosten steigen. Jede Zahl lässt sich auf eine Eingabe
  zurückführen, die der Nutzer prüfen kann. Nutze es, wenn der Nutzer sagt "finde die
  Gewinnmargen", "rechne die Zahlen durch", "ist das profitabel", "Break-even",
  "Stückrechnung", "wie viel brauche ich zum Start" oder "starte den Finanzchef"
  ("find the profit margins", "do the numbers", "is this profitable", "break-even",
  "unit economics", "how much do I need to start", "run the CFO").
argument-hint: "[Pfad zu zahlen.json]"
---

# gruender-finanzen

Die Person, die fragt: "Und was kostet das?" Margen entscheiden, ob aus einer guten
Idee ein Geschäft wird. Dieser Skill findet sie, und jede Zahl lässt sich auf eine
Eingabe zurückführen.

Werkzeug in diesem Ordner:

```bash
python3 "${CLAUDE_SKILL_DIR}/unit_economics.py" gruender/zahlen.json --out gruender/finanzen.md
```

## Schritt 1: sammle die Eingaben

Schreib `gruender/zahlen.json` (Aufbau: `example.json` in diesem Ordner, ein
Matcha-Café mit Laufkundschaft in München). Es braucht:

| Feld | Was hineingehört |
| --- | --- |
| `unit` | was ein Verkauf ist: eine Tasse, eine Bestellung, ein Kundenmonat, ein Platz |
| `unit_plural` | optional: die Mehrzahl für den Bericht („Tassen“). Fehlt sie, steht die Einzahl da |
| `price` | Preis pro Einheit vor Steuern |
| `variable` | die Kosten EINER Einheit: Zutaten, Verpackung, Versand, Kartengebühren, Provisionen pro Verkauf |
| `fixed_monthly` | was du jeden Monat zahlst, egal was passiert: Miete, Gehälter, Software, Versicherung |
| `startup` | einmalige Ausgaben vor der Eröffnung: Kautionen, Ausbau, Ausstattung, erste Ware, Startwerbung |
| `plan_per_day` | die Menge, sobald der Betrieb läuft |
| `ramp_per_day` | 12 Zahlen: die realistische Menge in jedem Monat des ersten Jahres |
| `capacity_per_day` | das Meiste, was du an einem Tag physisch verkaufen kannst, falls es eine Grenze gibt |

Woher die Zahlen kommen, in dieser Reihenfolge:

1. Die eigenen Angebote, Rechnungen, Mietverträge und Preislisten des Nutzers.
2. Öffentliche Preise, die der Nutzer nachprüfen kann (die Preisliste eines
   Lieferanten, die Anzeige eines Vermieters, die veröffentlichten Gebühren eines
   Zahlungsanbieters). Schreib die Quelle neben die Zahl in
   `gruender/finanzen-quellen.md`.
3. Deine Schätzung, klar als Schätzung gekennzeichnet, mit der Begründung. Stelle
   eine Schätzung nie als Tatsache dar.

Frag den Nutzer nach allem, was nur er weiß (genannte Miete, Löhne, die er zahlen
wird). Nimm den Preis aus `gruender/preis.md` oder `gruender/pitch.md`, falls diese
existieren.

**Im Anlauf lügen Pläne.** Monat 1 entspricht fast nie der Planmenge. Wenn das
Käuferpanel gelaufen ist, prüfe den Anlauf mit seiner Kaufquote und den
Erstkäufen im ersten Monat auf Plausibilität (`gruender/panel/ergebnis.md`) und sag,
wie du das gemacht hast.

## Schritt 2: lass es laufen

```bash
python3 "${CLAUDE_SKILL_DIR}/unit_economics.py" gruender/zahlen.json --out gruender/finanzen.md
```

Es schreibt: die Tabelle pro Einheit und den Deckungsbeitrag (was jeder Verkauf nach
seinen eigenen Kosten übrig lässt), die Fixkosten, den Break-even in Einheiten pro
Tag, die Gewinnmarge bei der Planmenge, das erste Jahr Monat für Monat, den
operativen Gewinn des ersten Jahres und das Ergebnis nach den Startkosten, das Geld,
das gebraucht wird, bevor es sich selbst trägt, den Monat, in dem das Startgeld
zurückverdient ist, und eine Was-wäre-wenn-Tabelle (Preis -10 %, Menge -20 %,
Stückkosten +15 %). Es warnt bei einem Preis unter den variablen Kosten, einem
Break-even über der Kapazität, einem Verlustjahr 1 und einer Amortisation nach mehr
als 12 Monaten.

Was-wäre-wenn, ohne die Datei zu ändern:

```bash
python3 "${CLAUDE_SKILL_DIR}/unit_economics.py" gruender/zahlen.json --price 7.00
python3 "${CLAUDE_SKILL_DIR}/unit_economics.py" gruender/zahlen.json --volume 0.8
```

## Schritt 3: die Notiz des Finanzchefs

Füge oben in `gruender/finanzen.md` einen kurzen Abschnitt in einfachen Worten hinzu:

- **Die Marge**: die Gewinnmarge beim Plan und der Deckungsbeitrag pro Einheit.
- **Die Linie, die du im Auge behältst**: die eine Kostenposition oder Annahme, die
  das Ergebnis am meisten bewegt (meist der Anlauf, die Miete oder der Preis), samt
  dem Was-wäre-wenn, das es belegt.
- **Geld**: wie viel Geld der Gründer braucht, bevor es sich selbst trägt.
- **Drei Wege, die Marge zu verbessern**, jeweils mit der Zahl, die sich ändert, und
  um wie viel (rechne das Was-wäre-wenn, rate nicht).
- Ob die Bedingungen des Vorstands zum Geld (`gruender/vorstand.md`) erfüllt sind.

## Regeln

- Jede Zahl in deiner Notiz stammt aus der Ausgabe des Werkzeugs oder aus einer
  Eingabe, die du benennen kannst.
- Der Umsatz ist vor Steuern; sag, falls der Markt des Nutzers noch Umsatzsteuer
  daraufschlägt.
- Keine Finanz-, Steuer- oder Rechtsberatung. Sag einmal, dass ein Steuerberater die
  Struktur, die Lohnkosten und die Steuern prüfen sollte, bevor Geld fließt.

## Ergebnis

`gruender/zahlen.json`, `gruender/finanzen.md`, `gruender/finanzen-quellen.md`. Als
Nächstes: `/gruender-plan` nutzt diese Zahlen für das Verdikt; `/gruender-preis`,
wenn die Marge dünn ist.
