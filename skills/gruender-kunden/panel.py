#!/usr/bin/env python3
"""Das Käuferpanel für gruender-kunden. Nur Standardbibliothek, kein Netzwerk.

Es erledigt die Buchführung für einen Schwarm simulierter Käufer: Es teilt aus deinem
Zielkundenprofil (Einkommen, Alter, Kaufverhalten, Einwand) je Käufer eine Personenkarte aus,
schreibt je Käufer ein Briefing, das ein Unteragent beantwortet, prüft die Antworten und zählt,
wer kauft, wer nicht und warum.

    python3 panel.py init --customer gruender/kunde.json --pitch gruender/pitch.md [--n 100] [--seed 7]
    python3 panel.py prompts [--wave 10]     # ein Briefing je Käufer, der noch fehlt, in Wellen aufgelistet
    python3 panel.py check                   # welche Antworten fehlen oder kaputt sind
    python3 panel.py save P003 < antwort.txt # die eigene JSON-Antwort eines Käufers ablegen, die er ausgegeben statt geschrieben hat
    python3 panel.py tally [--out gruender/panel/ergebnis.md]
    python3 panel.py status

Der Stand liegt in gruender/panel/ (mit --dir änderbar): panel.json, personas.json,
briefs/<id>.md, antworten/<id>.json, ergebnis.md, ergebnis.json.

Das Werkzeug antwortet nie für einen Käufer. Jede Zahl in ergebnis.md wird aus den Antwortdateien
gezählt, die die Unteragenten geschrieben haben. Simulierte Käufer sind ein schneller, billiger Weg,
Einwände und Schwachstellen zu finden. Sie sind keine Kunden: Bestätige, was wichtig ist, mit echten
Menschen (Vorverkauf, Warteliste, eine Landingpage mit Preis).
"""

import argparse
import json
import os
import random
import sys

FIRST_NAMES = [
    "Anna", "Lukas", "Sophie", "Jonas", "Leonie", "Felix", "Mia", "Paul", "Hannah", "Maximilian", "Lena", "Elias",
    "Emilia", "Ben", "Clara", "Noah", "Johanna", "Moritz", "Laura", "Tim", "Marie", "Jan", "Katharina", "David",
    "Lisa", "Simon", "Julia", "Philipp", "Sarah", "Tobias", "Nele", "Florian", "Amelie", "Niklas", "Franziska",
    "Fabian", "Charlotte", "Sebastian", "Theresa", "Alexander", "Vanessa", "Leon", "Annika", "Matthias", "Carina",
    "Stefan", "Lara", "Kilian", "Sabrina", "Dominik", "Melanie", "Benedikt", "Jana", "Andreas", "Pia", "Christian",
    "Nina", "Patrick", "Eva", "Michael", "Svenja", "Daniel", "Miriam", "Marco", "Helena", "Tom", "Alina", "Robin",
    "Kathrin", "Yannick", "Isabel", "Luca", "Verena", "Henrik", "Celina", "Oliver", "Denise", "Raphael", "Karolina",
    "Jakob", "Lea", "Stephan", "Tamara", "Valentin", "Elif", "Emre", "Aylin", "Can", "Zeynep", "Mehmet", "Leyla",
    "Murat", "Selin", "Ali", "Ayse", "Marlene", "Konstantin", "Greta", "Anton", "Ida", "Linus", "Frieda", "Emil",
    "Mathilda", "Jannis", "Luisa", "Ole", "Josefine", "Ferdinand", "Rebecca", "Joshua", "Antonia", "Samuel", "Pauline",
    "Vincent", "Viktoria", "Erik", "Maja", "Nick", "Sandra", "Marvin", "Bettina", "Gregor", "Silke",
]
REASONS = ["price", "habit", "need", "trust", "quality", "convenience", "timing", "values", "other"]
# Die reason_code-Werte bleiben englisch (Vertrag mit den Antwortdateien). Hier stehen ihre deutschen Namen
# für Briefing und Bericht.
REASONS_DE = {
    "price": "Preis", "habit": "Gewohnheit", "need": "Bedarf", "trust": "Vertrauen", "quality": "Qualität",
    "convenience": "Bequemlichkeit", "timing": "Zeitpunkt", "values": "Werte", "other": "Sonstiges",
}
ANSWER_FIELDS = {"id", "buys", "reason_code", "reason"}
WAVE = 10


class PanelError(Exception):
    pass


def _de(v):
    """Ganze Zahl in deutscher Schreibweise (Tausenderpunkt). Nur Anzeige."""
    return "{:,}".format(int(v)).replace(",", ".")


# ── Austeilen ───────────────────────────────────────────────────────────────────
def _quota(items, n, key="share"):
    """Verteilt n genau nach den Anteilen auf die Einträge (größter Rest)."""
    total = sum(float(it.get(key, 1)) for it in items) or 1.0
    raw = [n * float(it.get(key, 1)) / total for it in items]
    counts = [int(r) for r in raw]
    order = sorted(range(len(items)), key=lambda i: raw[i] - counts[i], reverse=True)
    for i in order[: n - sum(counts)]:
        counts[i] += 1
    return counts


def validate_customer(c):
    for k in ("business", "target", "segments", "behaviours", "objections"):
        if k not in c or c[k] in ("", [], None):
            raise PanelError("kunde.json braucht '%s'" % k)
    for s in c["segments"]:
        if "name" not in s or "income" not in s or len(s["income"]) != 2:
            raise PanelError("jedes Segment braucht einen Namen und ein Einkommen [niedrig, hoch]")
    for b in c["behaviours"]:
        if "name" not in b:
            raise PanelError("jedes Kaufverhalten braucht einen Namen")


def deal(customer, n=100, seed=7):
    """Teilt n Personenkarten aus. Gleicher Kunde + n + Seed = immer dieselben Karten."""
    validate_customer(customer)
    if n < 1:
        raise PanelError("--n muss mindestens 1 sein")
    rng = random.Random(seed)
    age = customer.get("age", [25, 45])
    segs = []
    for s, k in zip(customer["segments"], _quota(customer["segments"], n)):
        segs += [s] * k
    behs = []
    for b, k in zip(customer["behaviours"], _quota(customer["behaviours"], n)):
        behs += [b] * k
    rng.shuffle(segs)
    rng.shuffle(behs)
    names = FIRST_NAMES[:]
    rng.shuffle(names)
    while len(names) < n:
        names += ["%s %d" % (x, len(names) // len(FIRST_NAMES) + 1) for x in FIRST_NAMES]
    objections = customer["objections"]
    habits = customer.get("habits") or []
    cards = []
    for i in range(n):
        s, b = segs[i], behs[i]
        lo, hi = float(s["income"][0]), float(s["income"][1])
        cards.append({
            "id": "P%03d" % (i + 1),
            "name": names[i],
            "age": rng.randint(int(age[0]), int(age[1])),
            "segment": s["name"],
            "income": int(round(rng.uniform(lo, hi), -3)),
            "behaviour": b["name"],
            "behaviour_how": b.get("how", ""),
            "objection": objections[rng.randrange(len(objections))],
            "habit": habits[rng.randrange(len(habits))] if habits else "",
        })
    return cards


# ── Stand ───────────────────────────────────────────────────────────────────────
def _path(d, *p):
    return os.path.join(d, *p)


def _read_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _write_json(path, obj):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def init(d, customer_path, pitch_path, n=100, seed=None):
    try:
        customer = _read_json(customer_path)
    except FileNotFoundError:
        raise PanelError("Datei nicht gefunden: %s" % customer_path)
    try:
        with open(pitch_path, encoding="utf-8") as fh:
            pitch = fh.read().strip()
    except FileNotFoundError:
        raise PanelError("Datei nicht gefunden: %s (schreib zuerst den Pitch: was du verkaufst, den Preis, wo)" % pitch_path)
    if not pitch:
        raise PanelError("der Pitch ist leer")
    if seed is None:
        seed = random.SystemRandom().randrange(1, 10 ** 6)
    cards = deal(customer, n, seed)
    _write_json(_path(d, "panel.json"), {"n": n, "seed": seed, "customer": customer, "pitch": pitch})
    _write_json(_path(d, "personas.json"), cards)
    os.makedirs(_path(d, "briefs"), exist_ok=True)
    os.makedirs(_path(d, "antworten"), exist_ok=True)
    return cards


def load_state(d):
    try:
        return _read_json(_path(d, "panel.json")), _read_json(_path(d, "personas.json"))
    except FileNotFoundError:
        raise PanelError("kein Panel in %s: führe zuerst init aus" % d)


BRIEF = """Du bist ein simulierter Käufer in einem Verbraucherpanel. Ein Gründer will wissen, bevor er Geld ausgibt, ob echte Menschen wie du kaufen würden. Deine Antwort hilft nur, wenn sie ehrlich ist: Die meisten Menschen kaufen die meisten Dinge nicht, und ein höfliches Ja ist schlimmer als ein klares Nein.

=== WER DU BIST ===
{name}, {age}. {segment}. Du verdienst etwa {income_de} € im Jahr.
So kaufst du ein: {behaviour}. {behaviour_how}
{habit_line}Das Erste, was dir bei einem solchen Angebot einfällt: "{objection}"
Du gehörst zu diesen Menschen: {target}.
=== ENDE ===

=== WAS ANGEBOTEN WIRD (du siehst es zum ersten Mal, so wie ein Passant oder jemand, der durch den Feed scrollt) ===
{pitch}
=== ENDE ===

Entscheide so, wie {name} entscheiden würde, mit {name}s Geld, Gewohnheiten und Zweifeln, in einer normalen Woche. Sei nicht gefällig. Erfinde keine Fakten über das Geschäft, die nicht oben stehen.

Antworte auf Deutsch: Alle Textfelder (reason, objection, would_change_my_mind) schreibst du auf Deutsch, in deiner eigenen Stimme. Die JSON-Schlüssel und der reason_code bleiben genau so, wie sie unten stehen. Alle Preise sind Zahlen in Euro.

Lege die Datei {out} mit deinem Werkzeug zum Dateischreiben an (gib die Antwort nicht nur in deiner Antwort aus). Sie enthält NUR dieses JSON, ohne Markdown-Block, ohne sonst etwas:
{{
  "id": "{id}",
  "buys": true oder false,
  "purchases_first_month": wie oft du im ersten Monat kaufen würdest (0, wenn du nicht kaufst),
  "reason_code": einer von {reasons},
  "reason": "warum, in ein bis zwei Sätzen, in deiner eigenen Stimme",
  "objection": "der Zweifel, der für dich am schwersten wiegt, in deinen eigenen Worten",
  "would_change_my_mind": "das Eine, was deine Antwort umkehren würde, oder leer",
  "price_too_cheap": der Preis, bei dem es zu billig wirken würde, um etwas zu taugen (eine Zahl),
  "price_cheap": der Preis, bei dem es sich wie ein Schnäppchen anfühlt (eine Zahl),
  "price_expensive": der Preis, bei dem es anfängt, teuer zu wirken, du aber vielleicht noch kaufst (eine Zahl),
  "price_too_expensive": der Preis, bei dem du es gar nicht mehr kaufen würdest (eine Zahl)
}}

Bedeutung der reason_code-Werte: price = Preis, habit = Gewohnheit, need = Bedarf, trust = Vertrauen, quality = Qualität, convenience = Bequemlichkeit, timing = Zeitpunkt, values = Werte, other = Sonstiges.
"""


def write_briefs(d, wave=WAVE):
    state, cards = load_state(d)
    target = state["customer"]["target"]
    todo = []
    for c in cards:
        out = _path(d, "antworten", c["id"] + ".json")
        if _answer_ok(out, c["id"]) is None:
            continue
        brief = BRIEF.format(pitch=state["pitch"], target=target, out=os.path.abspath(out),
                             habit_line=("Dein Alltag: %s.\n" % c["habit"]) if c.get("habit") else "",
                             reasons=" / ".join(REASONS), income_de=_de(c["income"]), **c)
        bp = _path(d, "briefs", c["id"] + ".md")
        with open(bp, "w", encoding="utf-8") as fh:
            fh.write(brief)
        todo.append((c["id"], os.path.abspath(bp)))
    waves = [todo[i:i + wave] for i in range(0, len(todo), wave)]
    return waves


def _answer_ok(path, pid):
    """None, wenn die Antwortdatei in Ordnung ist, sonst ein kurzer Problemtext."""
    if not os.path.exists(path):
        return "fehlt"
    try:
        a = _read_json(path)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return "kein gültiges JSON"
    missing = ANSWER_FIELDS - set(a)
    if missing:
        return "es fehlt " + ", ".join(sorted(missing))
    if a.get("id") != pid:
        return "id ist %r, erwartet wurde %s" % (a.get("id"), pid)
    if not isinstance(a.get("buys"), bool):
        return "'buys' muss true oder false sein"
    if a.get("reason_code") not in REASONS:
        return "reason_code %r ist keiner von %s" % (a.get("reason_code"), ", ".join(REASONS))
    return None


def save(d, pid, text):
    """Legt die EIGENE Antwort eines Käufers ab, die er ausgegeben statt geschrieben hat. Nie dazu da, für einen Käufer zu antworten."""
    _, cards = load_state(d)
    if pid not in {c["id"] for c in cards}:
        raise PanelError("kein Käufer %s in diesem Panel" % pid)
    start = text.find("{")
    if start < 0:
        raise PanelError("kein JSON-Objekt in der Antwort")
    try:
        obj, _ = json.JSONDecoder().raw_decode(text[start:])
    except json.JSONDecodeError as e:
        raise PanelError("das JSON der Antwort lässt sich nicht lesen: %s" % e)
    path = _path(d, "antworten", pid + ".json")
    _write_json(path, obj)
    prob = _answer_ok(path, pid)
    if prob:
        os.remove(path)
        raise PanelError("die Antwort von %s ist ungültig (%s); starte stattdessen sein Briefing neu" % (pid, prob))
    return path


def check(d):
    _, cards = load_state(d)
    probs = []
    for c in cards:
        p = _answer_ok(_path(d, "antworten", c["id"] + ".json"), c["id"])
        if p:
            probs.append((c["id"], p))
    return probs


# ── Auszählung ──────────────────────────────────────────────────────────────────
def _rate(rows):
    return (sum(1 for r in rows if r["buys"]) / len(rows)) if rows else 0.0


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def tally(d):
    state, cards = load_state(d)
    by_id = {c["id"]: c for c in cards}
    rows, skipped = [], []
    for c in cards:
        path = _path(d, "antworten", c["id"] + ".json")
        p = _answer_ok(path, c["id"])
        if p:
            skipped.append((c["id"], p))
            continue
        a = _read_json(path)
        rows.append(dict(by_id[c["id"]], **{k: v for k, v in a.items() if k != "id"}, id=c["id"]))
    if not rows:
        raise PanelError("noch keine gültigen Antworten: führe zuerst die Briefings aus (panel.py prompts)")

    def group(key):
        out = {}
        for r in rows:
            out.setdefault(r[key], []).append(r)
        return sorted(((k, len(v), _rate(v)) for k, v in out.items()), key=lambda t: -t[2])

    # Einkommen in Dritteln der ausgeteilten Spanne, damit die Bänder in jedem Lauf dasselbe bedeuten
    incomes = sorted(r["income"] for r in rows)
    cut1, cut2 = incomes[len(incomes) // 3], incomes[2 * len(incomes) // 3]
    for r in rows:
        r["income_band"] = ("unter %s €" % _de(cut1)) if r["income"] < cut1 else (
            ("ab %s €" % _de(cut2)) if r["income"] >= cut2 else "%s bis %s €" % (_de(cut1), _de(cut2)))

    no = [r for r in rows if not r["buys"]]
    yes = [r for r in rows if r["buys"]]

    def reasons(rs):
        out = {}
        for r in rs:
            out.setdefault(r["reason_code"], []).append(r)
        return sorted(((k, v) for k, v in out.items()), key=lambda kv: -len(kv[1]))

    def mean(vals):
        vals = [v for v in vals if v is not None]
        return sum(vals) / len(vals) if vals else None

    res = {
        "business": state["customer"]["business"], "seed": state["seed"], "dealt": len(cards),
        "answered": len(rows), "skipped": skipped, "buys": len(yes), "passes": len(no),
        "buy_rate": len(yes) / len(rows),
        "by_segment": group("segment"), "by_behaviour": group("behaviour"), "by_income": group("income_band"),
        "why_not": [(k, len(v), [r["reason"] for r in v[:2]], [r["id"] for r in v[:2]]) for k, v in reasons(no)],
        "why_yes": [(k, len(v), [r["reason"] for r in v[:2]], [r["id"] for r in v[:2]]) for k, v in reasons(yes)],
        "flip": [r["would_change_my_mind"] for r in no if (r.get("would_change_my_mind") or "").strip()],
        "purchases_first_month_per_buyer": mean([_num(r.get("purchases_first_month")) for r in yes]),
        "price_answers": sum(1 for r in rows if all(_num(r.get(k)) is not None for k in
                                                     ("price_too_cheap", "price_cheap", "price_expensive", "price_too_expensive"))),
    }
    return res


def results_md(res):
    pct = lambda v: "%.0f%%" % (v * 100)
    reason = lambda k: REASONS_DE.get(k, k)
    L = ["# Käuferpanel: %s" % res["business"], ""]
    L.append("**%d kaufen · %d lehnen ab** (%s kaufen) von %d simulierten Käufern. Seed %s, die gleichen Karten lassen sich also erneut austeilen."
             % (res["buys"], res["passes"], pct(res["buy_rate"]), res["answered"], res["seed"]))
    if res["skipped"]:
        L.append("")
        L.append("%d von %d Käufern haben keine gültige Antwort und bleiben außen vor: %s." % (
            len(res["skipped"]), res["dealt"], ", ".join("%s (%s)" % s for s in res["skipped"][:10])))
    L.append("")
    L.append("Das sind simulierte Käufer, keine Kunden. Nutze das, um Einwände und Schwachstellen zu finden, und bestätige"
             " die großen mit echten Menschen, bevor du Geld ausgibst.")
    for title, key in (("Nach Segment", "by_segment"), ("Nach Kaufverhalten", "by_behaviour"), ("Nach Einkommen", "by_income")):
        L += ["", "## %s" % title, "", "| Gruppe | Käufer | Kaufquote |", "| --- | ---: | ---: |"]
        for k, n, r in res[key]:
            L.append("| %s | %d | %s%s |" % (k, n, pct(r), "  (wenige Antworten)" if n < 8 else ""))
    L += ["", "## Warum sie ablehnen", "", "| Grund | Käufer | in ihren Worten |", "| --- | ---: | --- |"]
    for k, n, quotes, ids in res["why_not"]:
        L.append("| %s | %d | %s |" % (reason(k), n, " · ".join('„%s“ (%s)' % (q.replace("|", "/"), i) for q, i in zip(quotes, ids))))
    L += ["", "## Warum sie kaufen", "", "| Grund | Käufer | in ihren Worten |", "| --- | ---: | --- |"]
    for k, n, quotes, ids in res["why_yes"]:
        L.append("| %s | %d | %s |" % (reason(k), n, " · ".join('„%s“ (%s)' % (q.replace("|", "/"), i) for q, i in zip(quotes, ids))))
    if res["flip"]:
        L += ["", "## Was ein Nein umkehren würde", ""]
        for f in res["flip"][:12]:
            L.append("- %s" % f)
    if res["purchases_first_month_per_buyer"] is not None:
        L += ["", "Die Käufer sagen, sie würden im ersten Monat im Schnitt **%s-mal** kaufen." %
              ("%.1f" % res["purchases_first_month_per_buyer"]).replace(".", ",")]
    if res["price_answers"]:
        L += ["", "%d Käufer haben alle vier Preisantworten gegeben. Führe van_westendorp.py aus gruender-preis auf dem Antworten-Ordner aus." % res["price_answers"]]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--dir", default=os.path.join("gruender", "panel"), help="Ordner des Panels (Standard: gruender/panel)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("init", help="Käufer austeilen")
    i.add_argument("--customer", required=True, help="Zielkundenprofil (kunde.json)")
    i.add_argument("--pitch", required=True, help="Pitch (pitch.md)")
    i.add_argument("--n", type=int, default=100, help="Anzahl Käufer (Standard 100)")
    i.add_argument("--seed", type=int, help="Seed, damit dieselben Karten erneut ausgeteilt werden")
    p = sub.add_parser("prompts", help="Briefings schreiben und in Wellen auflisten")
    p.add_argument("--wave", type=int, default=WAVE, help="Käufer je Welle (Standard 10)")
    sub.add_parser("check", help="fehlende oder kaputte Antworten zeigen")
    sv = sub.add_parser("save", help="die ausgegebene Antwort eines Käufers von stdin ablegen")
    sv.add_argument("id", help="Käufer-ID, zum Beispiel P003")
    t = sub.add_parser("tally", help="Antworten auszählen")
    t.add_argument("--out", help="Bericht hierhin schreiben (Standard: <dir>/ergebnis.md)")
    sub.add_parser("status", help="Stand des Panels")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "init":
            cards = init(a.dir, a.customer, a.pitch, a.n, a.seed)
            st, _ = load_state(a.dir)
            print("%d Käufer ausgeteilt (Seed %s) in %s. Weiter: panel.py prompts" % (len(cards), st["seed"], a.dir))
        elif a.cmd == "prompts":
            waves = write_briefs(a.dir, a.wave)
            n = sum(len(w) for w in waves)
            if not n:
                print("jeder Käufer hat eine gültige Antwort. Weiter: panel.py tally")
            else:
                print("%d Briefings in %d Wellen zu je bis zu %d. Starte eine Welle nach der anderen:" % (n, len(waves), a.wave))
                for k, w in enumerate(waves, 1):
                    print("Welle %d: %s" % (k, " ".join("%s=%s" % job for job in w)))
        elif a.cmd == "check":
            probs = check(a.dir)
            if not probs:
                print("alle Antworten vorhanden und gültig")
            for pid, prob in probs:
                print("%s: %s" % (pid, prob))
            return 1 if probs else 0
        elif a.cmd == "save":
            print("abgelegt: %s" % save(a.dir, a.id, sys.stdin.read()))
        elif a.cmd == "tally":
            res = tally(a.dir)
            text = results_md(res)
            out = a.out or _path(a.dir, "ergebnis.md")
            with open(out, "w", encoding="utf-8") as fh:
                fh.write(text)
            _write_json(_path(a.dir, "ergebnis.json"), res)
            print("%d kaufen · %d lehnen ab (%.0f%%). Geschrieben: %s" % (res["buys"], res["passes"], res["buy_rate"] * 100, out))
        elif a.cmd == "status":
            st, cards = load_state(a.dir)
            probs = check(a.dir)
            print("%d Käufer ausgeteilt (Seed %s), %d beantwortet, %d offen" % (len(cards), st["seed"], len(cards) - len(probs), len(probs)))
    except PanelError as e:
        print("Fehler: %s" % e, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
