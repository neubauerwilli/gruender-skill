import json
import os
import re
import unittest

from _load import ROOT, SKILLS_DIR

SKILLS = ["gruender-vorstand", "gruender-marketing", "gruender-finanzen", "gruender-kunden", "gruender-start",
          "gruender-preis", "gruender-angebot", "gruender-konkurrenz", "gruender-marke", "gruender-betrieb",
          "gruender-plan"]
ABOUT = ("Elf kostenlose Claude-Skills auf Deutsch, die dein Business testen, bevor du startest: ein Vorstand nach "
         "den Frameworks von Hormozi, Thiel und Jobs, ein Marketingchef, ein Finanzchef und ein Kundenpanel aus "
         "100 KI-Käufern. Kostenlos, MIT.")
EN_DASH = chr(0x2013)


def frontmatter(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return (m.group(1) if m else ""), text


EM = chr(0x2014)  # built in code so this file does not trip its own check


def text_files():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for f in files:
            if f.endswith((".md", ".py", ".json", ".txt")) or f in ("LICENSE", ".gitignore"):
                yield os.path.join(base, f)


class Repo(unittest.TestCase):
    def test_eleven_skill_folders(self):
        found = sorted(d for d in os.listdir(SKILLS_DIR) if os.path.isfile(os.path.join(SKILLS_DIR, d, "SKILL.md")))
        self.assertEqual(found, sorted(SKILLS))

    def test_frontmatter_name_and_description(self):
        for s in SKILLS:
            fm, text = frontmatter(os.path.join(SKILLS_DIR, s, "SKILL.md"))
            self.assertIn("name: %s\n" % s, fm + "\n", s)
            self.assertRegex(fm, r"description: ", s)
            self.assertGreater(len(fm), 300, "%s description is too thin" % s)
            self.assertGreater(len(text.splitlines()), 60, s)

    def test_tools_named_in_skills_exist(self):
        for s in SKILLS:
            _, text = frontmatter(os.path.join(SKILLS_DIR, s, "SKILL.md"))
            for tool in re.findall(r"\$\{CLAUDE_SKILL_DIR\}/([\w.\-/]+\.(?:py|md))", text):
                self.assertTrue(os.path.exists(os.path.normpath(os.path.join(SKILLS_DIR, s, tool))), "%s: %s" % (s, tool))

    def test_plugin_manifests(self):
        with open(os.path.join(ROOT, ".claude-plugin", "plugin.json"), encoding="utf-8") as fh:
            plugin = json.load(fh)
        self.assertEqual(plugin["name"], "gruender-skill")
        self.assertEqual(plugin["description"], ABOUT)
        self.assertEqual(plugin["license"], "MIT")
        with open(os.path.join(ROOT, ".claude-plugin", "marketplace.json"), encoding="utf-8") as fh:
            market = json.load(fh)
        self.assertEqual(market["name"], "gruender-skill")
        self.assertEqual(market["plugins"][0]["name"], "gruender-skill")
        self.assertEqual(market["plugins"][0]["source"], "./")

    def test_license_keeps_original_copyright(self):
        with open(os.path.join(ROOT, "LICENSE"), encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn("Copyright (c) 2026 Jake Schincariol", text)
        self.assertIn("MIT License", text)

    def test_readme_carries_the_reel_copy(self):
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
            readme = " ".join(fh.read().split())
        self.assertTrue(readme.startswith("# Der Gründer-Skill"))
        for line in (
            "Elf Claude-Skills auf Deutsch, die dein Business testen, bevor du startest. Kostenlos, MIT, keine "
            "Anmeldung, kein API-Schlüssel, nichts zu verbinden.",
            "Und einer ist das Kundenpanel: Er baut dir 100 KI-Käufer aus deiner Zielgruppe und schickt dein "
            "Business durch 100 Kaufsituationen.",
            "Füge den Link zu diesem Repo in Claude ein und sag `install skill`",
            "/plugin marketplace add neubauerwilli/gruender-skill",
            "/plugin install gruender-skill@gruender-skill",
            "## Kleingedrucktes",
            "https://github.com/Jakeschincariol/founder-skill",
        ):
            self.assertIn(line, readme)
        for s in SKILLS:
            self.assertIn("`skills/%s`" % s, readme)

    def test_examples_parse(self):
        for rel in ("gruender-finanzen/example.json", "gruender-kunden/kunde.example.json"):
            with open(os.path.join(SKILLS_DIR, rel), encoding="utf-8") as fh:
                json.load(fh)

    def test_no_em_dashes(self):
        for path in text_files():
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
                self.assertNotIn(EM, text, os.path.relpath(path, ROOT))
                self.assertNotIn(EN_DASH, text, os.path.relpath(path, ROOT))

    def test_no_english_skill_names_left(self):
        for path in text_files():
            if os.path.basename(path) in ("README.md", "LICENSE", "test_repo.py"):
                continue
            with open(path, encoding="utf-8") as fh:
                self.assertNotRegex(fh.read(), r"founder[-/]", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    unittest.main()
