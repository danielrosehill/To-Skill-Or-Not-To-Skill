#!/usr/bin/env python3
"""Install the "to skill or not to skill" heuristic into user-level agent instructions.

    python3 -I install.py [--agent NAME ...] [--file PATH ...] [--remove] [--dry-run] [--force]
    python3 -I install.py --list

With no --agent/--file, targets every known agent whose config dir exists. The block
is delimited by markers, so re-running replaces it in place. Each changed file gets a
.bak-<timestamp> copy first. Project-level files (anything inside a git work tree) are
refused unless --force. Prints a JSON report on stdout.
"""
import argparse, json, os, re, shutil, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
SNIPPET = os.path.join(HERE, "..", "snippet", "heuristic.md")
BEGIN = "<!-- BEGIN to-skill-or-not-to-skill -->"
END = "<!-- END to-skill-or-not-to-skill -->"

# agent -> (config dir that proves it is installed, user-level instruction file)
AGENTS = {
    "claude": ("~/.claude", "~/.claude/CLAUDE.md"),
    "codex": ("~/.codex", "~/.codex/AGENTS.md"),
    "gemini": ("~/.gemini", "~/.gemini/GEMINI.md"),
    "qwen": ("~/.qwen", "~/.qwen/QWEN.md"),
    "opencode": ("~/.config/opencode", "~/.config/opencode/AGENTS.md"),
}


def expand(p):
    return os.path.abspath(os.path.expanduser(p))


def in_git_tree(path):
    d = os.path.dirname(path)
    while not os.path.isdir(d):
        d = os.path.dirname(d)
    r = subprocess.run(["git", "-C", d, "rev-parse", "--is-inside-work-tree"],
                       capture_output=True, text=True)
    return r.returncode == 0 and r.stdout.strip() == "true"


def apply(path, block, remove, dry):
    text = open(path).read() if os.path.exists(path) else ""
    pat = re.compile(r"\n*" + re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?", re.S)
    if remove:
        if not pat.search(text):
            return "absent"
        new, status = pat.sub("\n", text, count=1).rstrip("\n") + "\n", "removed"
    elif pat.search(text):
        new = pat.sub(lambda m: "\n\n" + block + "\n", text, count=1).lstrip("\n")
        status = "unchanged" if new == text else "replaced"
    else:
        new = (text.rstrip("\n") + "\n\n" if text.strip() else "") + block + "\n"
        status = "appended"
    if new != text and not dry:
        if os.path.exists(path):
            shutil.copy2(path, path + ".bak-" + time.strftime("%Y%m%d%H%M%S"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").write(new)
    return status


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", nargs="+", choices=sorted(AGENTS))
    ap.add_argument("--file", nargs="+", default=[])
    ap.add_argument("--remove", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="allow files inside a git work tree")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()

    if a.list:
        print(json.dumps({n: {"file": f, "detected": os.path.isdir(expand(d))}
                          for n, (d, f) in AGENTS.items()}, indent=2))
        return

    if a.agent:
        names = a.agent
    elif a.file:
        names = []
    else:
        names = [n for n, (d, _) in AGENTS.items() if os.path.isdir(expand(d))]
    targets = [(n, expand(AGENTS[n][1])) for n in names] + [("file", expand(f)) for f in a.file]

    block = BEGIN + "\n" + open(SNIPPET).read().rstrip("\n") + "\n" + END
    rep = {"dry_run": a.dry_run, "action": "remove" if a.remove else "install", "targets": []}
    for name, path in targets:
        if not a.force and in_git_tree(path):
            status = "refused: inside a git work tree (project level); use --force"
        else:
            status = apply(path, block, a.remove, a.dry_run)
        rep["targets"].append({"agent": name, "file": path, "status": status})
    if not targets:
        rep["note"] = "no agent config dirs found; pass --agent or --file"
    print(json.dumps(rep, indent=2))


if __name__ == "__main__":
    main()
