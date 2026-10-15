---
name: gruender-plan
description: >-
  Dein Businessplaner. Fasst alles zusammen, was die anderen Gründer-Skills
  geschrieben haben (das Urteil des Vorstands, die Konkurrenz, das Kundenpanel, Preis,
  Angebot, die Zahlen des Finanzchefs, Marketing, Marke, Betrieb und den Startplan),
  in einem Businessplan mit einem Verdikt ganz oben, das aus den Zahlen berechnet und
  nie von Hand geschrieben wird: Profitabel, Noch nicht (mit den durchgefallenen
  Zahlen) oder Unvollständig. Ergänzt eine Zusammenfassung und eine einseitige Fassung
  für Partner, Kreditgeber oder Investoren. Nutze ihn, wenn der Nutzer sagt "schreib
  meinen Businessplan", "fass alles zusammen", "ist das profitabel", "gib mir den
  Plan" oder am Ende des Gründer-Pakets (englisch: "write my business plan", "put it
  all together", "is it profitable", "give me the plan").
argument-hint: "[--min-buy-rate 0.25]"
---

# gruender-plan

Der letzte Schritt. Ein Dokument, nach dem ein Gründer handeln oder das er an einen
Partner oder Kreditgeber weitergeben kann, gebaut ausschließlich aus dem, was das Paket
gefunden hat.

Werkzeug in diesem Ordner:

```bash
python3 "${CLAUDE_SKILL_DIR}/compile.py" --dir gruender
```

## Schritt 1: sehen, was da ist

```bash
python3 "${CLAUDE_SKILL_DIR}/compile.py" --dir gruender --check
```

gibt das Verdikt und jede Prüfung aus. Die Prüfungen, alle berechnet:

1. Jede Einheit verdient Geld vor den Fixkosten (`gruender/zahlen.json`).
2. Jahr 1 macht einen operativen Gewinn.
3. Der Break-even passt in die Kapazität, falls eine Kapazität angegeben wurde.
4. Genug simulierte Käufer kaufen (`gruender/panel/ergebnis.json`; Standardschwelle
   25 %, änderbar mit `--min-buy-rate`, und sag, warum).

Gibt es keine Zahlen, lautet das Verdikt Unvollständig: biete an, `/gruender-finanzen`
auszuführen. Nenne die übrigen fehlenden Abschnitte mit dem Skill, der den jeweiligen
füllt. Fülle einen fehlenden Abschnitt nicht selbst aus Vermutungen.

## Schritt 2: die Zusammenfassung

Schreibe `gruender/zusammenfassung.md`, eine halbe Seite, in einfachen Worten:

- Was das Geschäft ist und für wen, in zwei Sätzen.
- Das Verdikt und die drei Zahlen dahinter (Marge, Break-even, Jahr 1).
- Worin sich Kundenpanel und Vorstand einig waren und wo sie sich widersprochen haben.
- Das größte Risiko und was dagegen getan wird.
- Was der Gründer zum Start braucht (Bargeld vom Finanzchef, der erste Test aus dem
  Startplan).
- Das Eine, was diese Woche zu tun ist.

Lautet das Verdikt Noch nicht, beginnt die Zusammenfassung mit dem, was sich ändern
muss, und welcher Skill es ändert. Nie eine durchgefallene Prüfung abschwächen.

## Schritt 3: zusammenstellen

```bash
python3 "${CLAUDE_SKILL_DIR}/compile.py" --dir gruender
```

schreibt `gruender/businessplan.md`: Titel, das Verdikt mit seinen Prüfungen, die
Tabelle der Kernzahlen, die Idee, dann jeden Abschnitt, den das Paket erzeugt hat
(Zusammenfassung, Vorstand, Konkurrenz, Panel, Preis, Angebot, Zahlen, Marketing,
Marke, Betrieb, Start), und was noch nicht erledigt ist.

## Schritt 4: der Onepager

Schreibe `gruender/onepager.md` für jemanden, der in zwei Minuten entscheidet: das
Problem, der Kunde, das Angebot und der Preis, die Zahlentabelle, die Belege
(Panel-Ergebnis, Abstand zur Konkurrenz, ein eventueller echter Test), wofür das Geld
gebraucht wird, und die Bitte. Dieselben Zahlen wie im Plan, Wort für Wort.

## Regeln

- Das Verdikt kommt von `compile.py`. Schreibe nie Profitabel von Hand und runde nie
  eine durchgefallene Zahl zu einer bestandenen auf.
- Sag es einmal und deutlich: Das Panel besteht aus simulierten Käufern und die Zahlen
  sind Prognosen; echte Kunden und echte Angebote bestätigen sie. Keine Finanz-,
  Rechts- oder Steuerberatung.
- Will der Nutzer ein PDF oder eine Präsentation, biete an, den Plan zu exportieren,
  aber behalte das Markdown als maßgebliche Quelle.

## Ergebnis

`gruender/zusammenfassung.md`, `gruender/businessplan.md`, `gruender/onepager.md`.
Nenne dem Nutzer dann das Verdikt in einer Zeile und das Eine, was diese Woche zu tun
ist.
