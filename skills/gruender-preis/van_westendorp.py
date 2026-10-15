#!/usr/bin/env python3
"""Preissensibilität (Van Westendorp) für gruender-preis. Nur Standardbibliothek.

Jeder Käufer im Panel beantwortet vier Fragen: bei welchem Preis es zu billig wäre, um ihm zu
trauen, ein Schnäppchen, langsam teuer und zu teuer zum Kaufen. Zusammen ergeben die vier
Antworten eine akzeptable Preisspanne und den Preis, der die wenigsten Menschen unzufrieden lässt.

    python3 van_westendorp.py gruender/panel/antworten
    python3 van_westendorp.py preise.csv --out gruender/preiskurve.md
    python3 van_westendorp.py gruender/panel/antworten --json

Die Eingabe ist entweder der Antworten-Ordner des Panels (eine JSON je Käufer, geschrieben von
gruender-kunden) oder eine CSV mit den Spalten too_cheap, cheap, expensive, too_expensive (eine
Zeile je Befragtem; weitere Spalten werden ignoriert). Wer eine der vier Zahlen nicht nennt oder
sie in falscher Reihenfolge nennt (zu billig muss die niedrigste sein, zu teuer die höchste), wird
aussortiert und mitgezählt.

Die vier Punkte, die das Werkzeug ausgibt:

    PMC  Point of Marginal Cheapness      darunter halten zu viele es für zu billig
    PME  Point of Marginal Expensiveness  darüber halten zu viele es für zu teuer
    OPP  Optimal Price Point              gleich viele sagen "zu billig" wie "zu teuer"
    IPP  Indifference Price Point         gleich viele sagen "Schnäppchen" wie "teuer"

PMC bis PME ist die akzeptable Spanne. Das sind Antworten simulierter Käufer: Nutze die Spanne,
um zu wählen, was du TESTEST, und teste es dann mit echten Menschen.
"""

import argparse
import csv
import glob
import json
import os
import sys

KEYS = ("too_cheap", "cheap", "expensive", "too_expensive")


class PricingError(Exception):
    pass


def _f(v):
    s = str(v).replace("€", "").replace("$", "").strip()
    # deutsche Schreibweise zulassen: "4,50" und "1.234,50" (Komma = Dezimalzeichen)
    if "," in s:
        if s.rfind(",") > s.rfind(".") and len(s.split(",")[-1]) != 3:
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    try:
        x = float(s)
    except (TypeError, ValueError):
        return None
    return x if x > 0 else None


def read(path):
    """Gibt (rows, dropped) zurück; rows sind (too_cheap, cheap, expensive, too_expensive)."""
    raw = []
    if os.path.isdir(path):
        for fp in sorted(glob.glob(os.path.join(path, "*.json"))):
            try:
                with open(fp, encoding="utf-8") as fh:
                    a = json.load(fh)
            except (json.JSONDecodeError, UnicodeDecodeError):
                raw.append(None)
                continue
            raw.append(tuple(_f(a.get("price_" + k)) for k in KEYS))
    elif path.endswith(".csv"):
        with open(path, newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                raw.append(tuple(_f(r.get(k)) for k in KEYS))
    else:
        raise PricingError("gib den Antworten-Ordner des Panels oder eine .csv an")
    rows, dropped = [], 0
    for r in raw:
        if r is None or any(v is None for v in r) or not (r[0] <= r[1] <= r[2] <= r[3]):
            dropped += 1
            continue
        rows.append(r)
    return rows, dropped


def curves(rows, grid):
    n = float(len(rows))
    tc = [sum(1 for r in rows if r[0] >= p) / n for p in grid]          # zu billig bei p (fällt)
    ch = [sum(1 for r in rows if r[1] >= p) / n for p in grid]          # Schnäppchen bei p (fällt)
    ex = [sum(1 for r in rows if r[2] <= p) / n for p in grid]          # teuer bei p (steigt)
    te = [sum(1 for r in rows if r[3] <= p) / n for p in grid]          # zu teuer bei p (steigt)
    return tc, ch, ex, te


def cross(grid, falling, rising):
    """Erster Preis, bei dem die steigende Kurve die fallende trifft (lineare Interpolation)."""
    for i in range(1, len(grid)):
        d0 = rising[i - 1] - falling[i - 1]
        d1 = rising[i] - falling[i]
        if d0 <= 0 <= d1 and d1 != d0:
            t = -d0 / (d1 - d0)
            return grid[i - 1] + t * (grid[i] - grid[i - 1])
        if d0 == 0:
            return grid[i - 1]
    return None


def analyse(rows, step=None):
    if len(rows) < 5:
        raise PricingError("mindestens 5 vollständige Antworten nötig (vorhanden: %d)" % len(rows))
    lo = min(r[0] for r in rows)
    hi = max(r[3] for r in rows)
    step = step or max(0.01, round((hi - lo) / 400, 2))
    grid, p = [], lo
    while p <= hi + 1e-9:
        grid.append(round(p, 4))
        p += step
    tc, ch, ex, te = curves(rows, grid)
    not_cheap = [1 - v for v in ch]
    not_exp = [1 - v for v in ex]
    pts = {
        "PMC": cross(grid, tc, not_cheap),
        "PME": cross(grid, not_exp, te),
        "OPP": cross(grid, tc, te),
        "IPP": cross(grid, ch, ex),
    }
    return {"n": len(rows), "points": pts, "range": [pts["PMC"], pts["PME"]],
            "median": {k: sorted(r[i] for r in rows)[len(rows) // 2] for i, k in enumerate(KEYS)}}


def report(res, dropped, price=None):
    # Anzeige in deutscher Schreibweise: Komma als Dezimalzeichen, Euro-Zeichen hinten
    m = lambda v: "k. A." if v is None else ("%.2f €" % v).replace(".", ",")
    p = res["points"]
    L = ["# Preissensibilität", "",
         "%d vollständige Antworten%s. Simulierte Käufer: Nutze das, um zu wählen, was du testest, nicht als letztes Wort." % (
             res["n"], (", %d aussortiert (unvollständig oder in falscher Reihenfolge)" % dropped) if dropped else ""), "",
         "| Punkt | Preis | Bedeutung |", "| --- | ---: | --- |",
         "| PMC | %s | darunter halten zu viele es für zu billig, um gut zu sein |" % m(p["PMC"]),
         "| OPP | %s | gleich viele sagen zu billig wie zu teuer: der geringste Widerstand |" % m(p["OPP"]),
         "| IPP | %s | gleich viele nennen es ein Schnäppchen wie teuer |" % m(p["IPP"]),
         "| PME | %s | darüber sagen zu viele, es ist zu teuer zum Kaufen |" % m(p["PME"]), "",
         "**Akzeptable Spanne: %s bis %s.**" % (m(p["PMC"]), m(p["PME"])), ""]
    md = res["median"]
    L.append("Mittlere Antworten (Median): zu billig %s, Schnäppchen %s, wird teuer %s, zu teuer %s." % (
        m(md["too_cheap"]), m(md["cheap"]), m(md["expensive"]), m(md["too_expensive"])))
    if price is not None and p["PMC"] is not None and p["PME"] is not None:
        where = "innerhalb" if p["PMC"] <= price <= p["PME"] else ("unterhalb" if price < p["PMC"] else "oberhalb")
        L += ["", "Dein aktueller Preis, %s, liegt **%s** der akzeptablen Spanne." % (m(price), where)]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("source", help="der Antworten-Ordner des Panels oder eine CSV")
    ap.add_argument("--price", type=float, help="dein aktueller Preis, um ihn auf der Spanne einzuordnen")
    ap.add_argument("--out", help="Bericht hierhin schreiben (Markdown)")
    ap.add_argument("--json", action="store_true", help="die Zahlen als JSON ausgeben")
    a = ap.parse_args(argv)
    try:
        rows, dropped = read(a.source)
        res = analyse(rows)
    except (PricingError, FileNotFoundError) as e:
        print("Fehler: %s" % e, file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(dict(res, dropped=dropped), indent=1))
        return 0
    text = report(res, dropped, a.price)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("geschrieben: %s" % a.out)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
