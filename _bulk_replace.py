"""Bulk find/replace + page rename for Pakenham Plumbers scaffold."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SELF_NAME = Path(__file__).name

REPLACEMENTS = [
    ("https://geelongroofrestorations.com.au", "https://pakenhamplumbers.com.au"),
    ("geelongroofrestorations.com.au", "pakenhamplumbers.com.au"),
    ("geelongroofrestorations", "pakenhamplumbers"),
    ("Geelong Roof Restorations", "Pakenham Plumbers &amp; Pergolas"),
    ("Geelong roof restoration", "Pakenham decking &amp; pergola"),
    ("Geelong&rsquo;s specialist", "Pakenham&rsquo;s specialist"),
    ("Geelong&rsquo;s", "Pakenham&rsquo;s"),
    ("Greater Geelong", "Cardinia Shire"),
    ("Surf Coast Shire", "Cardinia Hills"),
    ("Bellarine", "Officer"),
    ("Surf Coast", "Cardinia Hills"),
    ("Geelong, the Bellarine and the Surf Coast", "Pakenham, Officer and the Cardinia Hills"),
    ("Geelong, the Bellarine, and the Surf Coast", "Pakenham, Officer, and the Cardinia Hills"),
    ("Bell Park", "Nar Nar Goon"),
    ("Corio", "Garfield"),
    ("Ocean Grove", "Heritage Springs"),
    ("Torquay", "Gembrook"),
    ("Geelong", "Pakenham"),
    ('"3220"', '"3810"'),
    ("VIC 3220", "VIC 3810"),
    ("3220", "3810"),
    ("-38.1499", "-38.0814"),
    ("144.3617", "145.4842"),
    ("Roof Restoration Services", "Decking, Pergola &amp; Outdoor Living Services"),
    ("roof restoration & replacement contractors", "decking, pergola &amp; outdoor living specialists"),
    ("Roof restoration", "Decking"),
    ("roof restoration", "decking project"),
    ("Roof Restoration", "Decking"),
    ("ROOF RESTORATION", "DECKING &amp; PERGOLAS"),
    ("specialist roof restoration", "specialist decking"),
    ("free roof inspections", "free design consultations"),
    ("Free roof inspections", "Free design consultations"),
    ("Free Inspection", "Free Consultation"),
    ("free inspection", "free consultation"),
    ("RoofingContractor", "GeneralContractor"),
    ("Roof Cleaning &amp; Pressure Washing", "Timber Decking"),
    ("Roof Painting &amp; Sealing", "Composite Decking"),
    ("Tile Restoration &amp; Repointing", "Pergolas &amp; Verandas"),
    ("Metal Roof Restoration", "Alfresco &amp; Outdoor Kitchens"),
    ("Gutter Replacement", "Deck Restoration"),
    ("Roof cleaning &amp; pressure washing", "Timber decking"),
    ("Roof painting &amp; sealing", "Composite decking"),
    ("Tile restoration &amp; repointing", "Pergolas &amp; verandas"),
    ("Metal roof restoration", "Alfresco &amp; outdoor kitchens"),
    ("Gutter replacement", "Deck restoration"),
    ("Roof Cleaning", "Timber"),
    ("Roof Painting", "Composite"),
    ("Tile Restoration", "Pergolas"),
    ("Metal Restoration", "Alfresco"),
    ("/services/roof-cleaning/", "/services/gas-fitting/"),
    ("/services/roof-painting/", "/services/blocked-drains/"),
    ("/services/tile-restoration/", "/services/burst-leaking-pipes/"),
    ("/services/metal-restoration/", "/services/emergency-plumber/"),
    ("/services/gutter-replacement/", "/services/hot-water-systems/"),
    ("/newtown/", "/officer/"),
    ("/belmont/", "/cardinia-lakes/"),
    ("/highton/", "/lakeside/"),
    ("/armstrong-creek/", "/heritage-springs/"),
    ("/lara/", "/beaconsfield/"),
    ("/greater-geelong/", "/cardinia-shire/"),
    ("Newtown", "Officer"),
    ("Belmont", "Cardinia Lakes"),
    ("Highton", "Lakeside"),
    ("Armstrong Creek", "Heritage Springs"),
    ("Lara", "Beaconsfield"),
    ("quotes@geelongroofrestorations.com.au", "quotes@pakenhamplumbers.com.au"),
    (">G</text>", ">P</text>"),
]

EXTENSIONS = {".astro", ".md", ".toml", ".mjs", ".json", ".xml", ".txt", ".html", ".css", ".js"}

def patch_file(p):
    try:
        s = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    out = s
    for old, new in REPLACEMENTS:
        out = out.replace(old, new)
    if out != s:
        p.write_text(out, encoding="utf-8")
        return True
    return False

def main():
    PAGES = ROOT / "src" / "pages"
    for old, new in [
        ("newtown.astro", "officer.astro"),
        ("belmont.astro", "beaconsfield.astro"),
        ("highton.astro", "cockatoo.astro"),
        ("armstrong-creek.astro", "emerald.astro"),
        ("lara.astro", "pakenham-upper.astro"),
        ("greater-geelong.astro", "cardinia-shire.astro"),
    ]:
        o, n = PAGES / old, PAGES / new
        if o.exists() and not n.exists():
            o.rename(n); print(f"renamed: {old} -> {new}")

    SVC = PAGES / "services"
    for old, new in [
        ("roof-cleaning.astro", "timber-decking.astro"),
        ("roof-painting.astro", "composite-decking.astro"),
        ("tile-restoration.astro", "pergolas.astro"),
        ("metal-restoration.astro", "alfresco-outdoor-kitchens.astro"),
        ("gutter-replacement.astro", "deck-restoration.astro"),
    ]:
        o, n = SVC / old, SVC / new
        if o.exists() and not n.exists():
            o.rename(n); print(f"renamed: {old} -> {new}")

    changed = 0
    for p in ROOT.rglob("*"):
        if not p.is_file(): continue
        if p.suffix not in EXTENSIONS: continue
        if "node_modules" in p.parts or "dist" in p.parts: continue
        if p.name == SELF_NAME: continue
        if patch_file(p):
            changed += 1

    pkg = ROOT / "package.json"
    if pkg.exists():
        s = pkg.read_text(encoding="utf-8")
        s = s.replace('"name": "geelongroofrestorations"', '"name": "pakenhamplumbers"')
        pkg.write_text(s, encoding="utf-8")

    print(f"Done. {changed} files patched.")

if __name__ == "__main__":
    main()
