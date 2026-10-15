#!/usr/bin/env python3
"""Stückrechnung (Unit Economics) für gruender-finanzen. Nur Standardbibliothek, kein Netzwerk.

Liest eine JSON-Datei mit dem Geschäft und gibt die Zahlen aus, die ein Finanzchef prüft, bevor
auch nur ein Euro ausgegeben wird: was eine Einheit einbringt, die echte Marge bei der geplanten
Menge, wie viele Einheiten pro Tag für den Break-even nötig sind, wie Jahr 1 Monat für Monat
aussieht und wie lange es dauert, das Startgeld zu verdienen.

    python3 unit_economics.py gruender/zahlen.json
    python3 unit_economics.py gruender/zahlen.json --out gruender/finanzen.md
    python3 unit_economics.py gruender/zahlen.json --json
    python3 unit_economics.py gruender/zahlen.json --price 7.00 --volume 0.8

Die Eingabe (siehe example.json in diesem Ordner):

    business          Name, für den Bericht
    unit              was du je einmal verkaufst: "Tasse", "Bestellung", "Kundenmonat"
    unit_plural       optional: Mehrzahl für den Bericht ("Tassen"); fehlt sie, steht die Einzahl
    price             Preis je Einheit, vor Steuern
    variable          [{label, cost}]  Kosten EINER Einheit: Zutaten, Verpackung,
                      Versand, Kartengebühren, eine Provision je Einheit
    fixed_monthly     [{label, cost}]  Kosten, die jeden Monat anfallen, egal was du verkaufst:
                      Miete, Gehälter, Software, Versicherung
    startup           [{label, cost}]  einmalige Ausgaben vor der Eröffnung
    days_per_month    Verkaufstage im Monat (Standard 30)
    capacity_per_day  die meisten Einheiten pro Tag, die du körperlich verkaufen kannst (optional)
    plan_per_day      die Menge, die du einplanst, wenn der Betrieb läuft
    ramp_per_day      12 Zahlen: Einheiten pro Tag in jedem Monat von Jahr 1
                      (optional; Standard = plan_per_day in jedem Monat)

Jede Zahl im Bericht stammt aus dieser Datei. Nichts wird nachgeschlagen oder geschätzt.
Fehlt ein Feld, sagt das Werkzeug es, statt etwas zu ergänzen.

--price und --volume rechnen ein Was-wäre-wenn, ohne die Datei zu ändern: --price ersetzt den
Preis, --volume skaliert jede Menge (0.8 = 20 Prozent weniger Verkäufe).
"""

import argparse
import json
import math
import sys


class NumbersError(Exception):
    pass


def _de(v, decimals):
    """Deutsche Schreibweise: Punkt als Tausendertrenner, Komma als Dezimalzeichen. Nur Anzeige."""
    s = "{:,.{d}f}".format(v, d=decimals)
    return s.replace(",", "\0").replace(".", ",").replace("\0", ".")


def _money(v):
    sign = "-" if v < 0 else ""
    return "%s%s €" % (sign, _de(abs(v), 2))


def _whole(v):
    sign = "-" if v < 0 else ""
    return "%s%s €" % (sign, _de(abs(round(v)), 0))


def _sum(items, field):
    total = 0.0
    for i, it in enumerate(items or []):
        if not isinstance(it, dict) or "cost" not in it:
            raise NumbersError("%s[%d] braucht ein 'cost'" % (field, i))
        try:
            total += float(it["cost"])
        except (TypeError, ValueError):
            raise NumbersError("%s[%d].cost ist keine Zahl: %r" % (field, i, it["cost"]))
    return total


def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        raise NumbersError("Datei nicht gefunden: %s" % path)
    except json.JSONDecodeError as e:
        raise NumbersError("%s ist kein gültiges JSON: %s" % (path, e))


def analyse(spec, price=None, volume=1.0):
    """Gibt ein Dict mit jeder Zahl des Berichts zurück. Reine Funktion, leicht zu testen."""
    if "price" not in spec and price is None:
        raise NumbersError("'price' fehlt")
    p = float(price if price is not None else spec["price"])
    if p <= 0:
        raise NumbersError("der Preis muss über null liegen")
    days = float(spec.get("days_per_month", 30))
    var = _sum(spec.get("variable"), "variable")
    fixed = _sum(spec.get("fixed_monthly"), "fixed_monthly")
    startup = _sum(spec.get("startup"), "startup")

    if "plan_per_day" not in spec and "ramp_per_day" not in spec:
        raise NumbersError("gib 'plan_per_day' oder 'ramp_per_day' (12 Zahlen) an")
    plan = float(spec.get("plan_per_day", 0)) * volume
    ramp = spec.get("ramp_per_day")
    if ramp is None:
        ramp = [plan] * 12
    else:
        if len(ramp) != 12:
            raise NumbersError("'ramp_per_day' braucht 12 Zahlen, eine je Monat (bekommen: %d)" % len(ramp))
        ramp = [float(v) * volume for v in ramp]
    if not plan:
        plan = ramp[-1]

    contribution = p - var
    contribution_pct = contribution / p
    breakeven_day = math.inf if contribution <= 0 else fixed / (contribution * days)
    plan_units_month = plan * days
    margin_at_plan = (contribution - (fixed / plan_units_month if plan_units_month else math.inf)) / p

    months = []
    cumulative = -startup
    payback_month = None
    for m, per_day in enumerate(ramp, start=1):
        units = per_day * days
        revenue = units * p
        variable_cost = units * var
        profit = revenue - variable_cost - fixed
        cumulative += profit
        if payback_month is None and cumulative >= 0:
            payback_month = m
        months.append({"month": m, "per_day": per_day, "units": units, "revenue": revenue,
                       "variable": variable_cost, "fixed": fixed, "profit": profit,
                       "cumulative": cumulative})
    year_profit = sum(m["profit"] for m in months)
    year_revenue = sum(m["revenue"] for m in months)
    # das Bargeld, das du brauchst: Startgeld plus das tiefste Loch, das die Monatsverluste graben
    lowest = min([-startup] + [m["cumulative"] for m in months])
    cash_needed = -lowest

    unit = spec.get("unit", "Einheit")
    unit_plural = spec.get("unit_plural", unit)
    capacity = spec.get("capacity_per_day")
    flags = []
    if contribution <= 0:
        flags.append("Jede Einheit verliert Geld, noch vor Miete und Gehältern: Der Preis liegt unter den variablen Kosten.")
    if capacity is not None and breakeven_day > float(capacity):
        flags.append("Der Break-even braucht %.0f %s pro Tag, aber die Kapazität liegt bei %s." % (breakeven_day, unit_plural, capacity))
    if capacity is not None and plan > float(capacity):
        flags.append("Der Plan (%.0f pro Tag) liegt über der Kapazität (%s)." % (plan, capacity))
    if year_profit < 0:
        flags.append("Jahr 1 macht im Betrieb Verlust (%s)." % _whole(year_profit))
    if payback_month is None:
        flags.append("Die Startausgaben sind in Jahr 1 nicht wieder verdient.")

    return {
        "business": spec.get("business", ""), "unit": unit, "unit_plural": unit_plural,
        "price": p, "variable_per_unit": var, "contribution": contribution,
        "contribution_pct": contribution_pct, "fixed_monthly": fixed, "startup": startup,
        "plan_per_day": plan, "margin_at_plan": margin_at_plan, "breakeven_per_day": breakeven_day,
        "capacity_per_day": capacity, "year1_revenue": year_revenue, "year1_profit": year_profit,
        "year1_after_startup": year_profit - startup, "payback_month": payback_month,
        "cash_needed": cash_needed, "months": months, "flags": flags,
        "variable_items": spec.get("variable", []), "fixed_items": spec.get("fixed_monthly", []),
        "startup_items": spec.get("startup", []),
    }


def sensitivity(spec):
    """Die drei Was-wäre-wenn, die jeder Plan überstehen sollte."""
    base = analyse(spec)
    rows = [("Basisplan", base)]
    rows.append(("Preis -10%", analyse(spec, price=base["price"] * 0.9)))
    rows.append(("Menge -20%", analyse(spec, volume=0.8)))
    worse = json.loads(json.dumps(spec))
    for it in worse.get("variable", []):
        it["cost"] = float(it["cost"]) * 1.15
    rows.append(("Stückkosten +15%", analyse(worse)))
    return rows


def report(spec, a):
    u = a["unit"]
    up = a["unit_plural"]
    L = []
    L.append("# Stückrechnung: %s" % (a["business"] or "dein Geschäft"))
    L.append("")
    L.append("Jede Zahl unten stammt aus der Eingabedatei. Nichts wird nachgeschlagen oder geschätzt.")
    L.append("")
    L.append("## Eine Einheit: %s" % u)
    L.append("")
    L.append("| Posten | je %s |" % u)
    L.append("| --- | ---: |")
    L.append("| Preis | %s |" % _money(a["price"]))
    for it in a["variable_items"]:
        L.append("| %s | -%s |" % (it.get("label", "Kosten"), _money(float(it["cost"]))))
    L.append("| **Deckungsbeitrag** (was jede Einheit für die Fixkosten übrig lässt) | **%s** (%.0f%%) |"
             % (_money(a["contribution"]), a["contribution_pct"] * 100))
    L.append("")
    L.append("## Die Marge, auf die es ankommt")
    L.append("")
    L.append("Fixkosten: %s im Monat (%s)." % (_whole(a["fixed_monthly"]), ", ".join(
        "%s %s" % (it.get("label", "Kosten"), _whole(float(it["cost"]))) for it in a["fixed_items"]) or "keine angegeben"))
    L.append("")
    be = a["breakeven_per_day"]
    L.append("- **Break-even: %s pro Tag.** Darunter verlierst du jeden Monat Geld." % (
        "nie (jede Einheit verliert Geld)" if math.isinf(be) else "%s %s" % (_de(math.ceil(be), 0), up)))
    L.append("- **Gewinnmarge bei deinem Plan** (%s pro Tag): **%.0f%%** von jedem Verkauf, nach allen Kosten." % (
        _de(a["plan_per_day"], 0), a["margin_at_plan"] * 100))
    if a["capacity_per_day"] is not None:
        L.append("- Kapazität: %s pro Tag." % a["capacity_per_day"])
    L.append("")
    L.append("## Jahr 1, Monat für Monat")
    L.append("")
    L.append("| Monat | %s pro Tag | Umsatz | Gewinn | kumuliert (nach %s Startgeld) |" % (up, _whole(a["startup"])))
    L.append("| ---: | ---: | ---: | ---: | ---: |")
    for m in a["months"]:
        L.append("| %d | %s | %s | %s | %s |" % (m["month"], _de(m["per_day"], 0), _whole(m["revenue"]),
                                             _whole(m["profit"]), _whole(m["cumulative"])))
    L.append("")
    L.append("- **Betriebsgewinn Jahr 1: %s** bei %s Umsatz." % (_whole(a["year1_profit"]), _whole(a["year1_revenue"])))
    L.append("- Nach den %s Startausgaben: %s." % (_whole(a["startup"]), _whole(a["year1_after_startup"])))
    L.append("- Startgeld wieder verdient: %s." % ("Monat %d" % a["payback_month"] if a["payback_month"] else "nicht in Jahr 1"))
    L.append("- Bargeld, das du brauchst, bis es sich selbst trägt: **%s**." % _whole(a["cash_needed"]))
    L.append("")
    L.append("## Was wäre wenn")
    L.append("")
    L.append("| Szenario | Marge beim Plan | Break-even pro Tag | Gewinn Jahr 1 |")
    L.append("| --- | ---: | ---: | ---: |")
    for name, s in sensitivity(spec):
        be = s["breakeven_per_day"]
        L.append("| %s | %.0f%% | %s | %s |" % (name, s["margin_at_plan"] * 100,
                                              "nie" if math.isinf(be) else _de(math.ceil(be), 0),
                                              _whole(s["year1_profit"])))
    L.append("")
    if a["flags"]:
        L.append("## Warnzeichen")
        L.append("")
        for f in a["flags"]:
            L.append("- %s" % f)
    else:
        L.append("Keine Warnzeichen in diesen Zahlen. Sie sind nur so gut wie die Eingaben: Prüfe jede Kostenzeile an einem echten Angebot.")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("numbers", help="die zahlen.json des Geschäfts")
    ap.add_argument("--out", help="Bericht hierhin schreiben (Markdown)")
    ap.add_argument("--json", action="store_true", help="die Zahlen als JSON ausgeben")
    ap.add_argument("--price", type=float, help="Preis für das Was-wäre-wenn")
    ap.add_argument("--volume", type=float, default=1.0, help="Mengenfaktor für das Was-wäre-wenn")
    args = ap.parse_args(argv)
    try:
        spec = load(args.numbers)
        if args.price is not None:
            spec = dict(spec, price=args.price)
        if args.volume != 1.0:
            spec = dict(spec)
            if "plan_per_day" in spec:
                spec["plan_per_day"] = float(spec["plan_per_day"]) * args.volume
            if "ramp_per_day" in spec:
                spec["ramp_per_day"] = [float(v) * args.volume for v in spec["ramp_per_day"]]
        a = analyse(spec)
    except NumbersError as e:
        print("Fehler: %s" % e, file=sys.stderr)
        return 2
    if args.json:
        out = {k: v for k, v in a.items() if not k.endswith("_items")}
        out["breakeven_per_day"] = None if math.isinf(out["breakeven_per_day"]) else out["breakeven_per_day"]
        print(json.dumps(out, indent=1, ensure_ascii=False))
        return 0
    text = report(spec, a)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("geschrieben: %s" % args.out)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
