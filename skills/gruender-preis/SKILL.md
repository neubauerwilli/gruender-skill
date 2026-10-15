---
name: gruender-preis
description: >-
  Findet den Preis, den Käufer wirklich zahlen. Liest die vier Preisantworten pro
  Käufer aus dem Kundenpanel zu einer Preisempfindlichkeitsspanne nach Van
  Westendorp (zu billig, ein Schnäppchen, wird teuer, zu teuer), stellt sie dem
  gegenüber, was Wettbewerber wirklich verlangen, und der Marge des Finanzchefs,
  und empfiehlt einen Preis, eine Preisleiter (gut / besser / am besten) und ein
  Eröffnungsangebot zum Testen. Nutze den Skill, wenn der Nutzer sagt "was soll ich
  verlangen", "bepreise das", "ist 6,50 € zu teuer", "Preisstrategie", "welcher
  Preis", oder nach dem Kundenpanel. Englische Auslöser: "how much should I
  charge", "price this", "is $X too expensive", "pricing strategy", "what price".
argument-hint: "[aktueller Preis]"
---

# gruender-preis

Der Preis ist der schnellste Hebel für die Marge und der, den Gründer am meisten
raten. Dieser Skill legt ihn anhand von drei prüfbaren Dingen fest: was Käufer
gesagt haben, was Wettbewerber verlangen und was das Business verdienen muss.

Werkzeug in diesem Ordner:

```bash
python3 "${CLAUDE_SKILL_DIR}/van_westendorp.py" gruender/panel/antworten --price 6.50 --out gruender/preiskurve.md
```

## Schritt 1: was Käufer gesagt haben

Ist `/gruender-kunden` gelaufen, hat jeder Käufer vier Preisfragen beantwortet. Lass
das Werkzeug über `gruender/panel/antworten` laufen (oder über eine CSV mit den
Spalten `too_cheap, cheap, expensive, too_expensive` aus echten Umfragen, die
simulierte Antworten jedes Mal schlagen). Es meldet:

| Punkt | Bedeutung |
| --- | --- |
| PMC | darunter halten zu viele es für zu billig, um gut zu sein |
| OPP | der Preis mit dem geringsten Widerstand in beide Richtungen |
| IPP | wo genauso viele es ein Schnäppchen nennen wie teuer |
| PME | darüber werden zu viele gar nicht kaufen |

PMC bis PME ist die akzeptable Spanne. Ist das Panel nicht gelaufen, sag das und
biete an, zuerst `/gruender-kunden --quick` laufen zu lassen. Erfinde keine Spanne.

## Schritt 2: was Wettbewerber verlangen

Aus `gruender/konkurrenz.md` (oder schlage sie jetzt nach, auf ihren eigenen
öffentlichen Preisseiten, mit Links): der Preis der nächsten Ersatzprodukte für
dieselbe Aufgabe. Halte fest, was jeder Preis enthält, damit du Gleiches mit
Gleichem vergleichst. Ein Matcha Latte wird mit anderen Matcha Lattes und dem
Kaffee verglichen, den er ersetzt, nicht mit einem Teebeutel.

## Schritt 3: was das Business braucht

Aus `gruender/zahlen.json`: die variablen Kosten pro Einheit und der Break-even.
Lass das Werkzeug des Finanzchefs bei zwei oder drei Kandidatenpreisen laufen, um
Marge und Break-even jeweils zu sehen:

```bash
python3 "${CLAUDE_SKILL_DIR}/../gruender-finanzen/unit_economics.py" gruender/zahlen.json --price 7.00
```

## Schritt 4: entscheiden

Schreibe `gruender/preis.md`:

1. **Der Preis** und warum: wo er in der akzeptablen Spanne liegt, im Vergleich zu
   den Wettbewerbern, und die Marge, die er ergibt (aus dem Werkzeug, nicht
   geraten).
2. **Die Leiter**, falls das Business eine haben kann: gut / besser / am besten
   (Größe, Paket, Abo, Mitgliedschaft) mit einem Grund, jede Stufe hochzusteigen.
3. **Das Eröffnungsangebot**: ein Einstiegspreis oder Bonus zum Start, der Käufer
   nicht darauf abrichtet, auf Rabatte zu warten, mit Enddatum.
4. **Was mit echten Käufern zu testen ist**: zwei Preise innerhalb der Spanne und
   wie man sie testet (zwei Landingpages, ein Vorverkauf zu jedem, A/B auf der
   Speisetafel).
5. Die wörtlichen Preiseinwände des Panels (die drei häufigsten), damit das
   Marketing sie beantworten kann.

## Regeln

- Preisantworten simulierter Käufer legen fest, was getestet wird. Sie sind kein
  Beweis.
- Preise nie unter den variablen Kosten, um Kunden zu "kaufen", ohne es zu sagen und
  ohne zu sagen, wie lange sich das Business das laut Finanzchef leisten kann.
- Keine falschen Anker: kein "statt 9,00 €" für einen Preis, der nie verlangt wurde.

## Ergebnis

`gruender/preiskurve.md`, `gruender/preis.md`. Hat sich der Preis geändert,
aktualisiere `gruender/zahlen.json` und lass `/gruender-finanzen` erneut laufen.
Als Nächstes: `/gruender-angebot`.
