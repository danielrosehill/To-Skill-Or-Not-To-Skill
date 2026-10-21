---
name: install-heuristic
description: Install, update or remove the "to skill or not to skill" heuristic in the user-level instruction files of the user's AI coding agents (Claude Code, Codex, Gemini CLI, Qwen Code, opencode). User level only, never project level. Use when the user says "install the skill heuristic", "add skill-or-not to my CLAUDE.md", "propagate the heuristic to my agents", or "update the heuristic block".
---

# Install the heuristic at user level

The heuristic in `snippet/heuristic.md` is a standing habit, so it belongs in the
**user-level** instruction file of each agent. That makes it apply in every project.
Never put it in a project's `CLAUDE.md` or `AGENTS.md`.

## Steps

1. Find the plugin checkout. If `${CLAUDE_PLUGIN_ROOT}` is unset (for example, when
   the skill was read from a catalogue), clone
   `https://github.com/danielrosehill/To-Skill-Or-Not-To-Skill` or use an existing
   local clone.
2. Preview the change:

   ```bash
   python3 -I <root>/scripts/install.py --dry-run
   ```

   This prints a JSON report. With no `--agent` flag, the script targets every
   agent whose config directory exists.
3. Show the user which files will change. Then run the same command without
   `--dry-run`. Before changing a file, the script writes a timestamped `.bak-`
   copy next to it.
4. Report the paths from the JSON output.

## Options

| Flag | Effect |
| --- | --- |
| `--agent claude codex …` | Only these agents (`--list` shows the known ones and their paths) |
| `--file PATH` | Another user-level file. Refused if it is inside a git repo, unless `--force` is passed |
| `--remove` | Remove the marked block |
| `--dry-run` | Report without writing |

The block sits between `<!-- BEGIN to-skill-or-not-to-skill -->` and
`<!-- END to-skill-or-not-to-skill -->`. Running the script again replaces the block
in place, so it is also the update path. Don't hand-edit inside the markers.

If the user's instruction file is generated from a source (for example, a build
target), add the heuristic to that source rather than to the generated file. Say so
instead of injecting the block.
