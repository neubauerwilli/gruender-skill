---
name: gruender-vorstand
description: >-
  Dein Vorstand. Legt eine Geschäftsidee einem dreiköpfigen Vorstand vor, jedes
  Mitglied ein Unteragent, der die Idee durch genau ein veröffentlichtes Framework
  liest: die Angebots-Linse (nach Alex Hormozis $100M Offers), die Monopol-Linse
  (nach Peter Thiels Zero to One) und die Produkt-Linse (nach Walter Isaacsons
  Biografie über Steve Jobs). Jedes Mitglied bewertet die Idee, nennt die Risiken,
  die sie töten würden, und stimmt ab: investieren, investieren wenn, oder ablehnen.
  Nutze den Skill, wenn der Nutzer sagt "teste meine Geschäftsidee", "würde das
  funktionieren", "nimm das auseinander", "was würde ein Vorstand sagen", "ist das
  ein gutes Business", oder das Gründer-Paket mit einer neuen Idee startet. Englische
  Auslöser: "test my business idea", "would this work", "pressure-test this", "what
  would a board say", "is this a good business", "start the founder pack".
argument-hint: "<die Geschäftsidee, oder leer lassen, dann gilt das Gespräch>"
---

# gruender-vorstand

Die erste Sitzung. Bevor jemand eine Website baut oder einen Mietvertrag
unterschreibt, nehmen drei Vorstandsmitglieder die Idee aus jeweils anderer
Richtung auseinander und stimmen ab.

Was der Nutzer nach `/gruender-vorstand` getippt hat: `$ARGUMENTS`. Ist das leer,
nimm die Idee aus dem Gespräch.

## Die Regel zu den drei Namen

Die Linsen sind Zusammenfassungen **veröffentlichter Frameworks**, mehr nicht. Die
Vorstandsmitglieder sind nicht diese Personen, sprechen nie als sie, zitieren sie
nie und behaupten nie, sie würden etwas gutheißen. Schreibe "die Angebots-Linse",
nie "Alex Hormozi sagt". Fragt der Nutzer, was einer von ihnen wirklich denkt,
sag, dass du nur ihre öffentlichen Frameworks anwenden kannst.

## Schritt 0: die Ideen-Datei

Alles im Gründer-Paket liest `gruender/idee.md` im Projekt des Nutzers. Gibt es
sie nicht, schreibe sie jetzt aus dem Gespräch:

```markdown
# <Name des Unternehmens oder ein Arbeitstitel>

- Was es ist: ein Satz.
- Für wen es ist: der Zielkunde, so konkret, wie der Nutzer ihn machen kann.
- Was es verkauft, zu welchem Preis: das Kernprodukt und sein Preis.
- Wo und wie: Stadt oder online, wie Kunden es finden, wie es geliefert wird.
- Budget und Rahmen: Geld, Zeit, Fähigkeiten, alles, was schon entschieden ist.
```

Fehlen Name, Kunde, Produkt oder Preis, frag danach (höchstens drei Fragen in
einer Nachricht) und schreibe dann die Datei. Erfinde kein Budget, keine
Marktgröße und keinen Wettbewerber.

## Schritt 1: den Vorstand briefen

Schreibe `gruender/vorstand/brief.md`: die Ideen-Datei plus alles andere, was der
Nutzer gesagt hat und was ein Fremder wissen müsste. **Unteragenten sehen dieses
Gespräch nicht**, deshalb muss der Brief für sich allein stehen. Gib deine eigene
Meinung zur Idee nicht hinein.

## Schritt 2: einberufen

Starte drei Unteragenten in EINER Nachricht (Agent-Werkzeug, `subagent_type:
general-purpose`, einer pro Mitglied), jedem gesagt: `Lies gruender/vorstand/brief.md
und die lenses.md von gruender-vorstand (Pfad unten), wende NUR die Linse <Linse>
an und schreibe dein Memo nach gruender/vorstand/<linse>.md.` Die Linsen-Datei ist
`lenses.md` im Ordner dieses Skills (`${CLAUDE_SKILL_DIR}/lenses.md`; wird dieser
Pfad nicht aufgelöst, nimm das Basisverzeichnis, das Claude Code für diesen Skill
ausgegeben hat). Die Linsen heißen `angebot`, `monopol` und `produkt`.

Jedes Memo in dieser Form:

```markdown
# <Linse>-Linse
Punkte: <1 bis 10> | Votum: investieren / investieren, wenn … / ablehnen
## Was stark ist
## Was die Idee töten würde (die drei wichtigsten, gefährlichste zuerst)
## Die Fragen, die ich dem Gründer stellen würde
## Bei "investieren, wenn …": die Bedingungen
```

## Schritt 3: die Zusammenfassung des Vorsitzenden

Lies die drei Memos (sie sind kurz) und schreibe `gruender/vorstand.md`:

1. Die Abstimmung, z. B. "2 mal investieren, wenn …, 1 mal ablehnen", und die
   Durchschnittspunktzahl.
2. Die Risiken, die mehr als ein Mitglied genannt hat: Sie stehen zuerst.
3. Alle Bedingungen, zusammengeführt, als Checkliste, die der Rest des Pakets
   abhaken kann (der Finanzchef, das Kundenpanel und der Preis prüfen die meisten).
4. Ein Absatz: die stärkste Version dieses Business, die der Vorstand sieht. Sie
   kann von dem abweichen, was der Nutzer vorgestellt hat; sag das offen.

Behalte die Meinungsverschiedenheiten der Mitglieder bei. Ein Vorstand, der sich
in allem einig ist, hat seine Arbeit nicht gemacht.

## Regeln

- Bewerte das Business, nicht den Gründer.
- Keine erfundenen Fakten. Braucht eine Linse eine Zahl, die noch niemand hat
  (Marktgröße, Kosten für die Gewinnung eines Kunden), nenne sie als offene Frage
  und sag, welcher Skill sie beantwortet (`/gruender-konkurrenz`,
  `/gruender-kunden`, `/gruender-finanzen`).
- Ein "ablehnen" ist ein Ergebnis, kein Scheitern. Sag es klar.

## Ergebnis

`gruender/idee.md`, `gruender/vorstand/` (Brief und drei Memos),
`gruender/vorstand.md`. Nenne dann die Abstimmung in einer Zeile und schlage den
nächsten Schritt vor: `/gruender-konkurrenz`, um zu sehen, wer schon da ist, oder
`/gruender-kunden`, um die Idee 100 simulierten Käufern vorzulegen.

## Wohin das Paket als Nächstes geht

```
vorstand -> konkurrenz -> kunden -> preis -> angebot -> finanzen -> marketing -> marke -> betrieb -> start -> plan
```

Jeder Skill läuft auch allein; jeder liest, was schon in `gruender/` liegt.
