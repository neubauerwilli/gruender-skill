"""Lädt ein Werkzeug aus einem Skill-Ordner (die Ordnernamen enthalten Bindestriche)."""

import importlib.util
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(ROOT, "skills")


def load(folder, name):
    path = os.path.join(SKILLS_DIR, folder, name + ".py")
    spec = importlib.util.spec_from_file_location("gruender_" + name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def example(folder, name):
    return os.path.join(SKILLS_DIR, folder, name)
