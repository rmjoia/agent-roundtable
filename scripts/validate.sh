#!/usr/bin/env bash
# Local checks for the template itself (this repo runs no GitHub Actions).
# Needs python3 with PyYAML; jsonschema is used when installed.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

python3 -I - <<'PY'
import glob, sys, re, yaml
ok = True
def fail(msg):
    global ok; ok = False; print("✗", msg)

roles = {}
for f in sorted(glob.glob("roles/*.md")):
    if f.endswith("README.md"): continue
    text = open(f, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m: fail(f"{f}: no front matter"); continue
    fm = yaml.safe_load(m.group(1))
    rid = f.split("/")[-1][:-3]
    if fm.get("id") != rid: fail(f"{f}: id {fm.get('id')} != file name")
    for k in ("title", "version", "default_tier", "summary"):
        if k not in fm: fail(f"{f}: missing {k}")
    if fm.get("default_tier") not in ("fast", "balanced", "strong", "strongest"): fail(f"{f}: bad tier")
    roles[rid] = fm
if "architect" not in roles or not roles["architect"].get("required"): fail("architect must exist and be required")

for f in sorted(glob.glob("themes/*.yaml")) + sorted(glob.glob("themes/local/*.yaml")):
    t = yaml.safe_load(open(f, encoding="utf-8"))
    missing = set(roles) - set(t.get("roles", {}))
    if not f.startswith("themes/local/") and missing: fail(f"{f}: missing roles {sorted(missing)}")
    extra = set(t.get("roles", {})) - set(roles)
    if extra: fail(f"{f}: unknown roles {sorted(extra)}")
    names = [v["name"].lower() for v in t["roles"].values()]
    if len(names) != len(set(names)): fail(f"{f}: duplicate names")
    if not t.get("source"): fail(f"{f}: no source")

schema = yaml.safe_load(open("team.config.schema.yaml"))
configs = ["team.config.example.yaml"] + glob.glob("examples/*/team.config.yaml")
try:
    import jsonschema
    for c in configs:
        try: jsonschema.validate(yaml.safe_load(open(c)), schema)
        except jsonschema.ValidationError as e: fail(f"{c}: {e.message}")
except ImportError:
    print("… jsonschema not installed; config files only parsed")
    for c in configs: yaml.safe_load(open(c))

for f in glob.glob("examples/*/.claude/agents/*.md"):
    text = open(f, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m: fail(f"{f}: no front matter"); continue
    fm = yaml.safe_load(m.group(1))
    for k in ("name", "description", "model"):
        if k not in fm: fail(f"{f}: missing {k}")
    if "{{" in text: fail(f"{f}: unrendered placeholder")

print("✓ roles, themes, configs and examples valid" if ok else "")
sys.exit(0 if ok else 1)
PY

for f in templates/hooks/commit-msg templates/hooks/install-hooks.sh scripts/*.sh examples/*/scripts/git-hooks/* examples/*/scripts/*.sh; do
  [ -f "$f" ] && bash -n "$f"
done
echo "✓ shell syntax"
bash scripts/scrub-check.sh
