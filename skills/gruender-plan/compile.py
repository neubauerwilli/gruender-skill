#!/usr/bin/env python3
"""Stellt den Businessplan für gruender-plan zusammen. Nur Standardbibliothek, kein Netzwerk.

Liest alles, was die anderen zehn Skills in gruender/ geschrieben haben, und setzt daraus ein
Dokument zusammen, gruender/businessplan.md, mit einem Verdikt oben. Das Verdikt wird aus den
Zahlen berechnet, nie von Hand geschrieben:

    Profitabel     jede Prüfung, zu der Daten vorliegen, besteht
    Noch nicht     mindestens eine Prüfung fällt durch (jeder Fehlschlag steht mit seiner Zahl da)
    Unvollständig  es gibt noch keine Zahlen (starte zuerst gruender-finanzen)

Die Prüfungen:
    1. jede Einheit verdient Geld vor den Fixkosten      (gruender/zahlen.json)
    2. Jahr 1 macht einen Betriebsgewinn                  (gruender/zahlen.json)
    3. der Break-even passt in die Kapazität, falls eine Kapazität angegeben ist
    4. genug vom Käuferpanel kauft                        (gruender/panel/ergebnis.json, --min-buy-rate, Standard 25%)

    python3 compile.py                      # liest ./gruender, schreibt ./gruender/businessplan.md
    python3 compile.py --dir pfad/zu/gruender --min-buy-rate 0.3
    python3 compile.py --check              # gibt nur das Verdikt aus; Exit 0 (Profitabel) oder 1
"""

import argparse
import importlib.util
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SECTIONS = [  # (Datei in gruender/, Überschrift, welcher Skill sie schreibt)
    ("zusammenfassung.md", "Zusammenfassung", "gruender-plan"),
    ("vorstand.md", "Was der Vorstand sagte", "gruender-vorstand"),
    ("konkurrenz.md", "Die Konkurrenz", "gruender-konkurrenz"),
    ("panel/ergebnis.md", "Das Käuferpanel", "gruender-kunden"),
    ("preis.md", "Preisgestaltung", "gruender-preis"),
    ("angebot.md", "Das Angebot", "gruender-angebot"),
    ("finanzen.md", "Die Zahlen", "gruender-finanzen"),
    ("marketing.md", "Marketing", "gruender-marketing"),
    ("marke.md", "Marke", "gruender-marke"),
    ("betrieb.md", "Betrieb", "gruender-betrieb"),
    ("start.md", "Startplan", "gruender-start"),
]


def _de(v, decimals=0):
    """Deutsche Schreibweise: Punkt als Tausendertrenner, Komma als Dezimalzeichen. Nur Anzeige."""
    s = "{:,.{d}f}".format(v, d=decimals)
    return s.replace(",", "\0").replace(".", ",").replace("\0", ".")


def _load_unit_economics():
    path = os.path.join(HERE, "..", "gruender-finanzen", "unit_economics.py")
    spec = importlib.util.spec_from_file_location("gruender_unit_economics", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read().strip()
    except FileNotFoundError:
        return None


def _strip_h1(text):
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    # Überschriften eine Ebene tiefer, damit sie unter der Abschnittsüberschrift stehen
    return "\n".join(("#" + l) if l.startswith("#") else l for l in lines).strip()


def verdict(d, min_buy_rate=0.25):
    """Gibt (Verdikt, Prüfungen, Zahlen, Panel) zurück. Prüfungen = [(ok, Text)]."""
    checks = []
    numbers = panel = None
    raw = _read(os.path.join(d, "zahlen.json"))
    if raw:
        ue = _load_unit_economics()
        numbers = ue.analyse(json.loads(raw))
        u = numbers["unit"]
        up = numbers.get("unit_plural", u)
        c = numbers["contribution"]
        checks.append((c > 0, "Pro %s bleiben vor den Fixkosten %s übrig (%.0f%% Deckungsbeitrag)." % (
            u, _de(c, 2) + " €", numbers["contribution_pct"] * 100)
                       if c > 0 else "Pro %s gehen vor den Fixkosten %s VERLOREN." % (u, _de(-c, 2) + " €")))
        y = numbers["year1_profit"]
        checks.append((y > 0, "Betriebsgewinn Jahr 1: %s €." % _de(y) if y > 0
                       else "Betriebs-VERLUST Jahr 1: %s €." % _de(-y)))
        be, cap = numbers["breakeven_per_day"], numbers["capacity_per_day"]
        if cap is not None:
            fits = not math.isinf(be) and be <= float(cap)
            checks.append((fits, "Der Break-even liegt bei %s pro Tag, die Kapazität bei %s." % (
                "nie erreicht" if math.isinf(be) else "%s %s" % (_de(math.ceil(be)), up), cap)))
    raw = _read(os.path.join(d, "panel", "ergebnis.json"))
    if raw:
        panel = json.loads(raw)
        r = panel["buy_rate"]
        checks.append((r >= min_buy_rate, "%d von %d simulierten Käufern kaufen (%.0f%%, die Hürde liegt bei %.0f%%)." % (
            panel["buys"], panel["answered"], r * 100, min_buy_rate * 100)))
    if numbers is None:
        v = "Unvollständig"
    elif all(ok for ok, _ in checks):
        v = "Profitabel"
    else:
        v = "Noch nicht"
    return v, checks, numbers, panel


def compile_plan(d, min_buy_rate=0.25):
    idea = _read(os.path.join(d, "idee.md"))
    name = None
    if idea:
        first = idea.splitlines()[0]
        name = first[2:].strip() if first.startswith("# ") else None
    v, checks, numbers, panel = verdict(d, min_buy_rate)
    title = name or (numbers["business"] if numbers and numbers.get("business") else "Dein Geschäft")
    L = ["# %s · Businessplan" % title, ""]
    L.append("**Verdikt: %s**" % v)
    L.append("")
    for ok, text in checks:
        L.append("- %s %s" % ("✓" if ok else "✗", text))
    if v == "Unvollständig":
        L.append("- Noch keine Zahlen. Starte /gruender-finanzen und kompiliere dann erneut.")
    L.append("")
    if numbers:
        be = numbers["breakeven_per_day"]
        up = numbers.get("unit_plural", numbers["unit"])
        L += ["| Kennzahl | |", "| --- | ---: |",
              "| Preis | %s € je %s |" % (_de(numbers["price"], 2), numbers["unit"]),
              "| Gewinnmarge beim Plan | %.0f%% je %s |" % (numbers["margin_at_plan"] * 100, numbers["unit"]),
              "| Break-even | %s pro Tag |" % ("nie" if math.isinf(be) else "%s %s" % (_de(math.ceil(be)), up)),
              "| Betriebsgewinn Jahr 1 | %s € |" % _de(numbers["year1_profit"]),
              "| Startausgaben | %s € |" % _de(numbers["startup"]),
              "| Bargeld, bis es sich selbst trägt | %s € |" % _de(numbers["cash_needed"]),
              "| Startgeld wieder verdient | %s |" % ("Monat %d" % numbers["payback_month"] if numbers["payback_month"] else "nicht in Jahr 1")]
        if panel:
            L.append("| Käuferpanel | %d kaufen · %d lehnen ab |" % (panel["buys"], panel["passes"]))
        L.append("")
    if idea:
        L += ["## Die Idee", "", _strip_h1(idea), ""]
    missing = []
    for fname, heading, skill in SECTIONS:
        text = _read(os.path.join(d, fname))
        if text:
            L += ["## %s" % heading, "", _strip_h1(text), ""]
        else:
            missing.append((heading, skill))
    if missing:
        L += ["## Noch offen", ""]
        for heading, skill in missing:
            L.append("- %s: starte /%s" % (heading, skill))
        L.append("")
    L.append("_Das Panel besteht aus simulierten Käufern, und die Zahlen sind Hochrechnungen aus deinen Eingaben. Bestätige die"
             " Nachfrage mit echten Kunden und die Kosten mit echten Angeboten, bevor du Geld ausgibst. Keine Finanz-, Rechts- oder Steuerberatung._")
    return v, "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--dir", default="gruender", help="Arbeitsordner mit den Ergebnissen der Skills (Standard: gruender)")
    ap.add_argument("--min-buy-rate", type=float, default=0.25, help="Mindest-Kaufquote des Panels (Standard 0.25)")
    ap.add_argument("--check", action="store_true", help="nur das Verdikt ausgeben; Exit 0, wenn Profitabel")
    ap.add_argument("--out", help="Standard: <dir>/businessplan.md")
    a = ap.parse_args(argv)
    if not os.path.isdir(a.dir):
        print("Fehler: Hier gibt es keinen Ordner %s/. Führe zuerst die anderen Gründer-Skills aus." % a.dir, file=sys.stderr)
        return 2
    v, text = compile_plan(a.dir, a.min_buy_rate)
    if a.check:
        _, checks, _, _ = verdict(a.dir, a.min_buy_rate)
        print("Verdikt: %s" % v)
        for ok, t in checks:
            print("  %s %s" % ("✓" if ok else "✗", t))
        return 0 if v == "Profitabel" else 1
    out = a.out or os.path.join(a.dir, "businessplan.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("Verdikt: %s. Geschrieben: %s" % (v, out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
