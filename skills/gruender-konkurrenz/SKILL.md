---
name: gruender-konkurrenz
description: >-
  Kartiert jeden Wettbewerber und die Lücke, die er lässt. Findet direkte und
  indirekte Wettbewerber sowie die Ersatzlösungen, die ein Käufer stattdessen
  nutzen würde, nur aus öffentlichen Quellen, und hält fest, was jeder verkauft,
  zu welchem Preis, wie er sich positioniert und worüber sich seine Kunden in
  öffentlichen Bewertungen beschweren, jede Tatsache mit Link. Endet mit einer
  Positionierungskarte und der Lücke, die das neue Business besetzen kann. Nutze
  den Skill, wenn der Nutzer sagt "wer sind meine Wettbewerber", "ist der Markt
  überfüllt", "was gibt es sonst noch", "Konkurrenzanalyse", "finde die Lücke",
  "gegen wen trete ich an". Englische Auslöser: "who are my competitors", "is this
  market crowded", "what else is out there", "competitor analysis", "find the gap",
  "who am I up against".
argument-hint: "[Stadt oder Markt]"
---

# gruender-konkurrenz

Jeder Käufer löst dieses Problem schon irgendwie. Dieser Skill findet heraus, wie,
was sie dafür zahlen und was sie daran hassen, damit das neue Business mit einer
Lücke startet statt mit einer Vermutung.

## Die Regeln

- **Nur öffentliche Quellen, jede Tatsache mit Link.** Websites, Preisseiten,
  Speisekarten, App-Store- und Google-Maps-Einträge, Bewertungsseiten, Reddit,
  Nachrichten. Ist eine Quelle nicht erreichbar, sag das. Erfinde nie einen
  Wettbewerber, einen Preis, eine Bewertung oder eine Rezension.
- **Lesen, nicht abgreifen.** Lies Seiten so, wie es ein Mensch tun würde. Halte
  dich an die Nutzungsbedingungen jeder Seite.
- **Zitate sind wörtlich**, kurz und mit Link. Sie sind Recherche, nie
  Kundenstimmen für die Werbung.

## Schritt 1: wer ist da

Aus `gruender/idee.md` (schreibe sie zuerst, falls sie fehlt; siehe
`/gruender-vorstand` Schritt 0):

| Typ | Was es bedeutet | Beispiel für ein Matcha-Café |
| --- | --- | --- |
| Direkt | verkauft dasselbe an denselben Käufer | andere Matcha-Bars in Laufnähe |
| Indirekt | ein anderes Produkt für dieselbe Aufgabe | die Kaffeeläden in derselben Straße |
| Ersatz | wie Käufer es ohne ein Unternehmen lösen | Matcha-Pulver für zu Hause, Fertiggetränke aus der Dose |

Peile 5 bis 10 direkte und indirekte Wettbewerber an, dazu die wichtigsten
Ersatzlösungen. Suche bei einem lokalen Business auf der Karte genau im Gebiet; bei
einem Online-Business so, wie ein Käufer suchen würde ("bester <Sache> für
<wen>", "<Sache> Alternative").

## Schritt 2: die Fakten

Eine Zeile pro Wettbewerber in `gruender/konkurrenz.csv`:

`name,type,url,location_or_channel,price_of_comparable_item,what_it_sells,positioning_line,rating,review_count,source_date`

`positioning_line` ist ihre eigene Überschrift oder ihr Slogan, kopiert. Der Preis
gilt für den Artikel, der dem am nächsten kommt, was das neue Business verkauft,
mit dem, was er enthält.

## Schritt 3: was ihre Kunden sagen

Lies bei den besten 3 bis 5 die Bewertungen (zuerst 1 bis 3 Sterne, dann die
4-Sterne-Bewertungen nach dem Muster "super, aber …"). Halte wiederkehrende
Beschwerden als Themen fest, mit Anzahl und ein bis zwei verlinkten Zitaten je
Thema. Markiere ein Thema als dünn, wenn es unter drei Bewertungen hat.

## Schritt 4: die Karte und die Lücke

Schreibe `gruender/konkurrenz.md`:

1. Die Tabelle (aus der CSV), sortiert danach, wie direkt jeder konkurriert.
2. Preisspanne: niedrigster, mittlerer und höchster Preis für den vergleichbaren
   Artikel.
3. Eine Positionierungskarte als Text: zwei Achsen, die für diesen Käufer zählen
   (Preis und Bequemlichkeit, Qualität und Tempo …), und wo jeder Wettbewerber
   steht.
4. Die Beschwerden, gerankt, mit Links.
5. **Die Lücke**: was niemand gut macht und dieses Business könnte, belegt mit der
   Evidenz. Gibt es keine Lücke, sag das klar; das ist das nützlichste Ergebnis,
   das dieser Skill liefern kann.
6. Die Bedrohung: wer das neue Business am schnellsten kopieren könnte und wie.

## Ergebnis

`gruender/konkurrenz.csv`, `gruender/konkurrenz.md`. Als Nächstes:
`/gruender-kunden` nutzt die Beschwerden, um echte Einwände zu schreiben;
`/gruender-preis` nutzt die Preisspanne.
