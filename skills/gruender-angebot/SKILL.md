---
name: gruender-angebot
description: >-
  Baut ein Angebot, zu dem man kaum Nein sagen kann (Builds an offer too good to
  refuse). Listet jedes Problem auf, das der Käufer auf dem Weg zum gewünschten
  Ergebnis hat, macht aus jedem eine Lösung, kürzt auf das, was billig zu liefern
  und für den Käufer wertvoll ist, und schnürt es mit ehrlichen Boni, einer Garantie,
  die der Finanzchef sich leisten kann, echter Dringlichkeit und einem klaren Namen
  zusammen. Bewertet es mit der Wertgleichung (Ergebnis, Wahrscheinlichkeit, Zeit,
  Aufwand) und testet es erneut im schnellen Käuferpanel. Nutze es, wenn der Nutzer
  sagt "mach mein Angebot besser", "warum kauft das keiner", "was soll alles drin
  sein", "Garantie", "Boni", "unwiderstehliches Angebot" oder "Grand Slam Offer"
  ("make my offer better", "why won't people buy", "what should I include",
  "guarantee", "bonuses", "grand slam offer"), oder nachdem das Panel gezeigt hat,
  dass Leute abspringen (after the panel shows people passing).
argument-hint: "[was du verkaufst]"
---

# gruender-angebot

Die meisten Unternehmen verkaufen ein Produkt. Gute verkaufen ein Angebot: das
Produkt plus alles, was das Kaufen zu einem leichten Ja macht. Dieser Skill baut
das und nutzt dafür die Angebots-Linse in `../gruender-vorstand/lenses.md` als
Methode (eine Zusammenfassung des Frameworks aus Alex Hormozis *$100M Offers*;
stelle sie nie als seine Worte dar).

## Schritt 1: lies, was schon bekannt ist

- `gruender/idee.md` und `gruender/pitch.md`: was heute verkauft wird.
- `gruender/panel/ergebnis.md`: warum Käufer abspringen, in ihren Worten. Das ist
  das Rohmaterial: Auf jeden der wichtigsten Einwände soll etwas im Angebot
  antworten.
- `gruender/zahlen.json`: was jedes Extra kostet, damit das Paket profitabel bleibt.
- `gruender/vorstand.md`: die Bedingungen des Vorstands.

## Schritt 2: die Problemliste

Schreib jedes Hindernis zwischen dem Käufer und dem gewünschten Ergebnis auf, in den
Worten des Käufers: vor dem Kauf (Zweifel, Preis, Aufwand beim Wechseln), währenddessen
(Warten, Lernen, Umstände), danach (hält es, was passiert, wenn es scheitert). Ziel
sind 15 bis 30. Hol zuerst die Einwände aus dem Panel und die Beschwerden über die
Konkurrenz.

## Schritt 3: Lösungen, gekürzt und gebündelt

Mach aus jedem Problem eine Lösung (ein Merkmal, eine Leistung, eine Garantie, ein
Format). Bewerte jede nach Wert für den Käufer (1 bis 5) und Lieferkosten (1 bis 5,
aus den Zahlen des Finanzchefs). Behalte hohen Wert bei niedrigen Kosten. Bündle den
Rest zu:

- **Dem Kern**: die Sache selbst, beschrieben über das Ergebnis, nicht über die
  Zutaten.
- **Boni**: zwei oder drei, jeder räumt genau einen konkreten Einwand aus.
- **Der Garantie**: was passiert, wenn das Angebot nicht hält, was es verspricht.
  Rechne vor dem Versprechen mit dem Werkzeug des Finanzchefs durch, was sie bei einer
  realistischen Inanspruchnahme kostet.
- **Dringlichkeit und Knappheit**: nur, wenn sie wahr sind (eine Startwoche, eine
  begrenzte erste Charge). Nie einen falschen Countdown oder ein "nur noch 3
  verfügbar".
- **Dem Namen**: ein klarer, konkreter Name für das Angebot, nicht für die Firma.

## Schritt 4: bewerte es

Nach der Wertgleichung, vorher und nachher, je 1 bis 10: Traumergebnis, gefühlte
Wahrscheinlichkeit, es zu bekommen, Zeit bis zum Ergebnis, Aufwand und Verzicht.
Sag, welches Element des Pakets welche Bewertung bewegt.

## Schritt 5: teste es erneut

Schreib das neue Angebot in `gruender/pitch.md` (den alten Stand behältst du als
`gruender/pitch-v1.md`) und starte `/gruender-kunden --quick` mit demselben Seed.
Berichte die Kaufquote vorher und nachher und welche Einwände weggefallen sind. Hat
sich nichts bewegt, sag das: Dann liegt das Problem vielleicht am Markt oder am Preis,
nicht am Angebot.

## Regeln

- Jedes Versprechen muss einlösbar und bezahlbar sein; prüfe die Kosten mit dem
  Finanzchef.
- Keine gefälschten Bewertungen, Referenzen, Knappheit, Rabatte oder "bekannt aus".
- Halte dich bei Garantien und Werbeaussagen (besonders Gesundheitsversprechen) an die
  Werbe- und Verbraucherschutzregeln des Marktes des Nutzers. Das ist keine
  Rechtsberatung.

## Ergebnis

`gruender/angebot.md` (Problemliste, das Paket, Kosten, die Wertgleichungs-Bewertungen,
das Ergebnis des erneuten Tests) und die aktualisierte `gruender/pitch.md`. Als
Nächstes: `/gruender-finanzen`, um die Zahlen mit dem Paket neu zu rechnen, dann
`/gruender-marketing`.
