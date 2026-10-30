#!/usr/bin/env python3
"""Render an agent-roundtable team from team.config.yaml into a staging folder.

Deterministic: the same framework, config and repo render the same files, so
/init-team and /sync-team can show an honest diff and re-runs are no-ops.

Usage:
  python3 -I render.py --framework <dir> --repo <dir> --config <file> --out <dir>
                       [--alongside <relpath>]... [--skip <relpath>]...

  --alongside  write ours next to an existing hand-written file as <relpath>.roundtable
  --skip       don't render this output at all (keep the project's file)

Needs PyYAML. Writes nothing outside --out. Prints a JSON summary on stdout.
"""
import argparse, json, os, re, sys, unicodedata

try:
    import yaml
except ImportError:
    sys.exit("render.py needs PyYAML: python3 -m pip install --user pyyaml")

ORDER = ["architect", "product-owner", "product-manager", "security", "qa", "frontend",
         "backend-domain", "backend-app", "devops", "docs", "copy", "marketing", "steward"]
TIERS = ["fast", "balanced", "strong", "strongest"]
WHEN = {
    "always": "every PR",
    "code": "every PR that changes code or tests",
    "behaviour": "every PR that changes behaviour",
    "ui": "every PR that changes a user-facing surface",
    "product": "PRs that change product rules, pricing or user-facing claims",
    "contract": "PRs that change a contract",
    "infra": "PRs that change infra or pipelines",
}
GENERATED = "agent-roundtable:generated"
LOCAL_RE = re.compile(r"<!-- agent-roundtable:local:start -->.*?<!-- agent-roundtable:local:end -->", re.S)
BLOCK_RE = re.compile(r"<!-- agent-roundtable:start.*?<!-- agent-roundtable:end -->", re.S)
DEFAULT_LOCAL = ("<!-- agent-roundtable:local:start -->\n"
                 "<!-- Project-specific additions for this agent go here; /init-team and /sync-team keep this block. -->\n"
                 "<!-- agent-roundtable:local:end -->")

ap = argparse.ArgumentParser()
ap.add_argument("--framework", required=True)
ap.add_argument("--repo", required=True)
ap.add_argument("--config", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--alongside", action="append", default=[])
ap.add_argument("--skip", action="append", default=[])
args = ap.parse_args()
FW, REPO, OUT = args.framework, args.repo, args.out


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def fw(*parts):
    return os.path.join(FW, *parts)


outputs = []


def emit(rel, text, mode=None):
    if rel in args.skip:
        return
    target = rel + ".roundtable" if rel in args.alongside else rel
    path = os.path.join(OUT, target)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text if text.endswith("\n") else text + "\n")
    if mode:
        os.chmod(path, mode)
    outputs.append(target)


def front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise SystemExit(f"no front matter in {text[:40]!r}")
    return yaml.safe_load(m.group(1)), text[m.end():]


# ---------------------------------------------------------------- config
cfg = yaml.safe_load(read(args.config))
VERSION = read(fw("VERSION")).strip()
cfg.setdefault("template", {})
cfg["template"].setdefault("repo", "rmjoia/agent-roundtable")
cfg["template"]["version"] = VERSION

owner = (cfg.get("owner") or {}).get("title", "the owner")
models = {"fast": "haiku", "balanced": "sonnet", "strong": "opus", "strongest": "opus", **(cfg.get("models") or {})}
conv = cfg.get("conventions") or {}
size = {"soft_lines": 800, "soft_files": 25, "hard_lines": 1500, "hard_files": 40, **(conv.get("size") or {})}
trailer_pattern = conv.get("trailer", "Agent: <name> (<model>)")
policy = conv.get("push_policy", "owner-only")
paths = cfg.get("paths") or {}
stack = cfg.get("stack") or {}
i18n = cfg.get("i18n") or {}
retro = {"cadence": "weekly", "label": "retro", **(cfg.get("retro") or {})}
gates = (cfg.get("gates") or {}).get("pre_commit") or []
packs = cfg.get("packs") or ["neutral"]

theme_id = cfg["theme"]
theme_path = fw("themes", "local", theme_id[6:] + ".yaml") if theme_id.startswith("local/") else fw("themes", theme_id + ".yaml")
if theme_id.startswith("local/") and not os.path.exists(theme_path):
    theme_path = os.path.join(REPO, "themes", "local", theme_id[6:] + ".yaml")
theme = yaml.safe_load(read(theme_path))["roles"]
neutral = yaml.safe_load(read(fw("themes", "neutral.yaml")))["roles"]


def slugify(name):
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")


# ---------------------------------------------------------------- roles
roles = {}
for rid in ORDER:
    rc = (cfg.get("roles") or {}).get(rid)
    if rid == "architect":
        rc = rc or {}
    if rc is None or not rc.get("enabled", True):
        continue
    fm, body = front_matter(read(fw("roles", rid + ".md")))
    themed = theme.get(rid) or {}
    name = rc.get("name") or themed.get("name") or neutral[rid]["name"]
    flavour = "" if rc.get("name") else themed.get("flavour", "")
    personality = "" if rc.get("name") else themed.get("personality", "")
    tier = rc.get("tier") or fm["default_tier"]
    floor = fm.get("tier_floor")
    if floor and TIERS.index(tier) < TIERS.index(floor):
        tier = floor
    roles[rid] = dict(fm=fm, body=body, Name=name, slug=slugify(name), flavour=flavour, personality=personality,
                      tier=tier, model=models[tier], rc=rc)

slugs = [r["slug"] for r in roles.values()]
dupes = sorted({s for s in slugs if slugs.count(s) > 1})
if dupes:
    raise SystemExit(f"duplicate agent names: {dupes}; set roles.<id>.name to make them unique")


def name_of(rid):
    return roles[rid]["Name"] if rid in roles else owner


def cap(text):
    return text[:1].upper() + text[1:]


def resolve_lanes(rid):
    r = roles[rid]
    raw = list(r["rc"].get("lanes") or r["fm"].get("default_lanes") or []) + list(r["rc"].get("extra_lanes") or [])
    lanes = []
    for glob in raw:
        keys = re.findall(r"\{\{paths\.([a-z0-9_]+)\}\}", glob)
        if any(paths.get(k) in (None, "", "none") for k in keys):
            continue
        for k in keys:
            glob = glob.replace("{{paths.%s}}" % k, paths[k].rstrip("/"))
        if glob not in lanes:
            lanes.append(glob)
    includes = [g for g in lanes if not g.startswith("!")]
    prefixes = [g.split("*")[0] for g in includes]
    # An exclusion only means something if it sits inside an included path.
    return [g for g in lanes if not g.startswith("!") or any(g[1:].startswith(p) for p in prefixes)]


def lane_bullets(lanes):
    return "\n".join(f"  - except `{g[1:]}`" if g.startswith("!") else f"  - `{g}`" for g in lanes)


def lane_inline(lanes):
    return ", ".join(f"except `{g[1:]}`" if g.startswith("!") else f"`{g}`" for g in lanes)


def hand_overs(rid):
    items = []
    for target, what in (roles[rid]["fm"].get("hands_over") or {}).items():
        what = subst(what)
        if target == "*":
            items.append(what)
        elif target in roles:
            items.append(f"{what} → {roles[target]['Name']}")
        else:
            items.append(f"{what} → {owner} (role not enabled)")
    return items


def gates_for(lanes):
    prefixes = [g.split("*")[0] for g in lanes if not g.startswith("!")]
    hits = [g for g in gates if any(re.search(g["paths"], p) for p in prefixes)]
    if not hits:
        return "  - the project's checks for what you changed"
    return "\n".join(f"  - `cd {g.get('cwd', '.')} && {g['run']}`" for g in hits)


PUSH = {
    "owner-only": (
        "You never push, open PRs or merge. When a branch is ready, give {{owner}} the summary and the exact "
        "commands; {{owner}} pushes, opens the PR and merges.",
        "{{owner}} pushes and opens the PR; no agent, the architect included, pushes, opens PRs or merges.",
    ),
    "architect-on-merge-approval": (
        "You push, open PRs and apply labels. You merge only on {{owner}}'s explicit \"merge #N\" for that PR; "
        "approval for one PR never extends to another. Specialists never push, open PRs or merge.",
        "{{role:architect}} pushes, opens the PR and applies the labels; specialists never push, open PRs or merge.",
    ),
}


def stack_text(key):
    value = stack.get(key)
    return "the project's stack" if value in (None, "", "none") else value


def subst(text, rid=None):
    text = text.replace("{{shared_rules}}", read(fw("templates", "shared-rules.md")).rstrip("\n"))
    text = text.replace("{{push_policy}}", PUSH[policy][0]).replace("{{push_policy_short}}", PUSH[policy][1])
    if rid:
        r = roles[rid]
        lanes = resolve_lanes(rid)
        text = text.replace("{{Name}}", r["Name"]).replace("{{name}}", r["slug"])
        text = text.replace("{{flavour}}", r["flavour"])
        if r["personality"]:
            text = text.replace("{{personality}}", r["personality"])
        else:  # no personality: drop the heading with its slot
            text = re.sub(r"^#+ Your personality\n\{\{personality\}\}\n\n", "", text, flags=re.M)
        text = text.replace("{{lanes}}", lane_bullets(lanes) or "  - nothing in the repo")
        text = text.replace("{{hands_over}}", "\n".join(f"  - {h}" for h in hand_overs(rid)))
        text = text.replace("{{gates}}", gates_for(lanes))
        text = text.replace("{{trailer}}", trailer_pattern.replace("<name>", r["slug"]).replace("<model>", r["model"]))
        text = text.replace("{{model}}", r["model"])
    text = text.replace("{{trailer_example}}", trailer_pattern)
    text = text.replace("{{project}}", cfg["project"]["name"])
    text = text.replace("{{template.version}}", VERSION).replace("{{template.repo}}", cfg["template"]["repo"])
    text = text.replace("{{packs_path}}", "docs/conventions/neutral")
    text = re.sub(r"\{\{role:([a-z-]+)\}\}", lambda m: name_of(m.group(1)), text)
    text = re.sub(r"\{\{role_slug:([a-z-]+)\}\}", lambda m: roles[m.group(1)]["slug"], text)
    for k, v in models.items():
        text = text.replace("{{models.%s}}" % k, v)
    for k, v in size.items():
        text = text.replace("{{size.%s}}" % k, str(v))
    for k, v in retro.items():
        text = text.replace("{{retro.%s}}" % k, str(v))
    text = re.sub(r"\{\{stack\.([a-z0-9]+)\}\}", lambda m: stack_text(m.group(1)), text)
    text = text.replace("{{i18n.languages}}", ", ".join(i18n.get("languages") or []) or "the project's language")
    text = text.replace("{{i18n.source}}", i18n.get("source") or (i18n.get("languages") or ["the source language"])[0])
    # {{owner}} at the start of a sentence, list item or table cell is capitalised.
    text = re.sub(r"(^|[.!?]\s+|^\s*[-*]\s+|\|\s+(\*\*)?)\{\{owner\}\}", lambda m: m.group(1) + cap(owner), text, flags=re.M)
    return text.replace("{{owner}}", owner)


def tagline(rid):
    return subst(roles[rid]["fm"]["tagline"])


def render_directive(line):
    """Carry out a '<!-- render: ... -->' line. Returns replacement text ('' drops the line)."""
    if "one bullet per enabled role except the architect" in line:
        return "\n".join(f"- **{r['Name']}** ({r['fm']['title']}, `{r['model']}`): {tagline(rid)}"
                         for rid, r in roles.items() if rid != "architect")
    if "one row per enabled role:" in line:
        return "\n".join(
            f"| {r['fm']['title']} | **{r['Name']}**{' (main Claude Code session)' if rid == 'architect' else ''} | {tagline(rid)} |"
            for rid, r in roles.items())
    if "one row per enabled role except the architect, with its resolved lanes" in line:
        rows = []
        for rid, r in roles.items():
            if rid == "architect":
                continue
            writes = ("**nothing in the repo**: strategies and verdicts go back in the report"
                      if r["fm"].get("read_only") else lane_inline(resolve_lanes(rid)))
            rows.append(f"| {r['Name']} | {writes} | {'; '.join(hand_overs(rid))} |")
        return "\n".join(rows)
    if "one line listing each enabled agent and its tier" in line:
        return ("Per agent (the architect runs on your session's model): "
                + " · ".join(f"{r['Name']} {r['tier']} → `{r['model']}`" for rid, r in roles.items() if rid != "architect"))
    if "one row per entry in review_gates" in line:
        rows = []
        for g in cfg.get("review_gates") or []:
            reviewers = [x for x in g["reviewers"] if x == "consumer" or x in roles]
            if not reviewers:
                continue
            label = g.get("label") or cap(g["id"].replace("-", " "))
            who = ", ".join("the consuming agent" if x == "consumer" else f"**{name_of(x)}**" for x in reviewers)
            rows.append(f"| {label} | {who} | {WHEN[g['when']]} | {g.get('lens', '')} |")
        return "\n".join(rows)
    if "Every user-facing string has keys in" in line:
        langs = i18n.get("languages") or []
        return f"- [ ] Every user-facing string has keys in {', '.join(langs)}" if len(langs) > 1 else ""
    raise SystemExit("unhandled render directive: " + line.strip())


def render(text, rid=None):
    text = re.sub(r"<!-- Render notes \(removed from output\):.*?-->\n", "", text, flags=re.S)
    lines = []
    for line in text.split("\n"):
        if line.strip().startswith("<!-- render:"):
            replacement = render_directive(line)
            if replacement:
                lines.append(replacement)
        else:
            lines.append(line)
    return subst("\n".join(lines), rid)


def existing(rel):
    path = os.path.join(REPO, rel)
    return read(path) if os.path.exists(path) else None


# ---------------------------------------------------------------- outputs
notes = []

def with_template_version(raw):
    """Set template.version in the config text without reformatting it (comments survive)."""
    block = re.search(r"^template:[ \t]*\n((?:[ \t]+.*\n?)*)", raw, re.M)
    if block is None:
        return re.sub(r"^(version:.*\n)", lambda m: m.group(1) + f"\ntemplate:\n  repo: {cfg['template']['repo']}\n  version: \"{VERSION}\"\n",
                      raw, count=1, flags=re.M)
    body = block.group(1)
    if re.search(r"^[ \t]+version:", body, re.M):
        body = re.sub(r"^([ \t]+version:).*$", lambda m: f'{m.group(1)} "{VERSION}"', body, count=1, flags=re.M)
    else:
        body = body.rstrip("\n") + f'\n  version: "{VERSION}"\n'
    return raw[:block.start(1)] + body + raw[block.end(1):]


emit("team.config.yaml", with_template_version(read(args.config)))

for rid, r in roles.items():
    if r["fm"].get("renders_to") == "claude-md":
        continue
    rel = f".claude/agents/{r['slug']}.md"
    current = existing(rel)
    if current is not None and GENERATED not in current and rel not in args.skip + args.alongside:
        notes.append(f"{rel} exists and was written by hand: pass --skip or --alongside, or move its content into the local block")
    includes = [g for g in resolve_lanes(rid) if not g.startswith("!")]
    lanes = ", ".join(includes[:3]) + (", …" if len(includes) > 3 else "") if includes else "nothing in the repo (read-only)"
    description = f"{subst(' '.join(r['fm']['summary'].split()))} Lanes: {lanes}."
    head = ["---", f"name: {r['slug']}",
            "description: " + json.dumps(description, ensure_ascii=False),
            f"model: {r['model']}"]
    if r["fm"].get("read_only"):
        head.append("tools: Read, Grep, Glob, Bash, WebFetch, WebSearch")
    head.append("---")
    marker = (f"<!-- {GENERATED} role={rid} role_version={r['fm']['version']} template={VERSION}: "
              "edit team.config.yaml or the local section below, then re-run /init-team -->")
    match = LOCAL_RE.search(current or "")
    local = match.group(0) if match else DEFAULT_LOCAL
    emit(rel, "\n".join(head) + "\n" + marker + "\n\n" + render(r["body"].strip("\n"), rid) + "\n\n" + local + "\n")

block = render(read(fw("templates", "claude-team-section.md.tmpl"))).rstrip("\n")
block = block.replace("{{architect_body}}", render(roles["architect"]["body"].strip("\n"), "architect"))
current = existing("CLAUDE.md")
if current is None:
    rows = "\n".join(f"| {k} | {v} |" for k, v in stack.items() if v not in (None, "", "none"))
    intro = f"# {cfg['project']['name']}\n\n{cfg['project'].get('domain', '')}\n"
    if rows:
        intro += f"\n| Layer | Choice |\n|---|---|\n{rows}\n"
    claude = intro + "\n" + block + "\n"
elif BLOCK_RE.search(current):
    claude = BLOCK_RE.sub(lambda _: block, current, count=1)
else:
    claude = current.rstrip("\n") + "\n\n" + block + "\n"
emit("CLAUDE.md", claude)

emit("docs/team-roster.md", render(read(fw("templates", "team-roster.md.tmpl"))))
for name in ("task-brief.md", "definition-of-done.md"):
    emit(f"docs/process/{name}", render(read(fw("templates", "process", name))))

for pack in packs:
    src = fw("packs", pack)
    for root, _, files in sorted(os.walk(src)):
        for f in sorted(files):
            rel = os.path.relpath(os.path.join(root, f), src)
            emit(f"docs/conventions/{pack}/{rel}", read(os.path.join(root, f)))

hand_written = []
for rel, src in [(".github/PULL_REQUEST_TEMPLATE.md", fw("templates", "github", "PULL_REQUEST_TEMPLATE.md"))] + [
        (f".github/ISSUE_TEMPLATE/{n}.md", fw("templates", "github", "ISSUE_TEMPLATE", n + ".md"))
        for n in ("story", "task", "bug", "retro-log")]:
    current = existing(rel)
    if current is not None and GENERATED not in current and rel not in args.skip + args.alongside:
        notes.append(f"{rel} exists and was written by hand: replaced; pass --skip or --alongside to keep it")
    emit(rel, render(read(src)))


def bash_quote(value):
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"').replace("$", "\\$").replace("`", "\\`") + '"'


rows = "\n".join(f"gate {bash_quote(g['name'])} {bash_quote(g['paths'])} {bash_quote(g.get('cwd', '.'))} {bash_quote(g['run'])}"
                 for g in gates) or "# no gates configured: add them under gates.pre_commit in team.config.yaml"
for hook in ("pre-commit", "commit-msg"):
    if hook == "commit-msg" and conv.get("commits", "conventional") != "conventional":
        continue
    current = existing(f"scripts/git-hooks/{hook}")
    if current is not None and GENERATED not in current and f"scripts/git-hooks/{hook}" not in args.skip + args.alongside:
        notes.append(f"scripts/git-hooks/{hook} exists and was written by hand: keep its checks as gates")
    emit(f"scripts/git-hooks/{hook}", render(read(fw("templates", "hooks", hook))).replace("{{gates_rows}}", rows), 0o755)
emit("scripts/install-hooks.sh", render(read(fw("templates", "hooks", "install-hooks.sh"))), 0o755)

leftovers = []
for rel in outputs:
    if rel == "team.config.yaml":
        continue  # the owner's own text, copied as written
    text = read(os.path.join(OUT, rel))
    for i, line in enumerate(text.split("\n"), 1):
        if re.search(r"(?<!\$)\{\{", line):
            leftovers.append(f"{rel}:{i}")
if leftovers:
    raise SystemExit("unrendered placeholders: " + ", ".join(leftovers))

# Lane overlaps and gaps, for the owner to resolve.
def globs_overlap(a, b):
    """True when some path could match both globs. Literal prefixes decide; only '**' reaches into subfolders."""
    pa, pb = a.split("*")[0], b.split("*")[0]
    if a == b:
        return True
    if "**" in a and pb.startswith(pa):
        return True
    if "**" in b and pa.startswith(pb):
        return True
    return "*" not in a and "*" not in b and a == b


owned = {rid: [g for g in resolve_lanes(rid) if not g.startswith("!")] for rid in roles}
overlaps = []
for a in owned:
    for b in owned:
        if a < b:
            for ga in owned[a]:
                for gb in owned[b]:
                    if globs_overlap(ga, gb):
                        pa, pb = ga.split("*")[0], gb.split("*")[0]
                        excluded = any(x.startswith("!") and (x[1:].startswith(pa) or x[1:].startswith(pb))
                                       for x in resolve_lanes(a) + resolve_lanes(b))
                        if not excluded:
                            overlaps.append(f"{name_of(a)} `{ga}` ↔ {name_of(b)} `{gb}`")

print(json.dumps({"version": VERSION, "agents": {r["slug"]: rid for rid, r in roles.items()},
                  "outputs": sorted(outputs), "overlaps": overlaps, "notes": notes}, indent=2, ensure_ascii=False))
