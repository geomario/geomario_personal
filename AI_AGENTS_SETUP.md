# AI agents setup: instructions, skills and Spec Kit

How to set this repo up so **Claude Code** and **GitHub Copilot** (and Cursor, Codex…) work
well in it, using the same layout as `brain_frontend_extension`, where it's already done and
tested. Step 1 is done; steps 2 and 3 are still to do, in that order.

Checked against the official docs on 2026-10-28 (updated 2026-10-29). These tools change
often, so re-check the links at the bottom if something behaves differently.

---

## The three pieces

| Piece | What it is | Where it lives |
| --- | --- | --- |
| **Instructions** | The project's rules, read at the start of every chat: what the project is, how to run it, what never to do | `AGENTS.md` (+ a one-line `CLAUDE.md`) |
| **Skills** | Reusable expert instructions for one topic (e.g. "Django security"), loaded when relevant or called with `/name` | `.agents/skills/` (+ links in `.claude/skills/`) |
| **Spec Kit** | A workflow for building features from a written spec: describe → plan → tasks → implement | `.specify/` + `.claude/skills/speckit-*` |

### Who reads what

| | Claude Code | Copilot |
| --- | --- | --- |
| `AGENTS.md` | ✅ through `CLAUDE.md` (directly too since v2.1.277, but only when there is no `CLAUDE.md`) | ✅ |
| `CLAUDE.md` | ✅ | only with a VS Code setting |
| Skills in `.claude/skills/` | ✅ (the only folder it reads) | ✅ |
| Skills in `.agents/skills/` | ❌ | ✅ (also Cursor, Codex, Gemini CLI) |
| Skills in `.github/skills/` | ❌ | ✅ |

That's why the layout is:

- **Instructions written once** in `AGENTS.md`; `CLAUDE.md` contains the line
  `@AGENTS.md`, which makes Claude Code import it. Put shared rules in `AGENTS.md`; only
  Claude-specific notes would go below the import in `CLAUDE.md`.
- **Skills stored once** in `.agents/skills/`; `.claude/skills/<name>` is a **symlink** to
  each one (not a copy). Claude follows the link; Copilot reads both folders but shows each
  skill only once (checked in VS Code on 2026-10-28).

---

## Step 1: AGENTS.md and CLAUDE.md (done)

`AGENTS.md` describes the project as it is (database-backed content, Docker for
development, the production deploy) and its rules; `CLAUDE.md` is the single line
`@AGENTS.md`. The README was corrected first, because assistants believe whatever these
files say. Keep both up to date whenever how things work changes.

**Check it works** (from the repo root, in a terminal):

```sh
claude -p "Without reading files: what does AGENTS.md say about migrations? One line."
```

If it answers from your rules, the import works.

---

## Step 2: skills

### How to find skills

- Browse [skills.sh](https://skills.sh), the public directory, with install counts.
- Or search from the terminal: `npx skills find django` (also try `python`, `postgres`,
  `docker`, `security`).
- Prefer **official** sources (the company behind the tool). Community skills can be good,
  but **read every file before committing**: skills run with the assistant's permissions.

### Candidates for this repo

From `npx skills find` on 2026-10-28 (install counts change):

| Skill | Source | Official? | What for |
| --- | --- | --- | --- |
| `web-design-guidelines` | `vercel-labs/agent-skills` | ✅ Vercel | Reviews HTML/CSS/UI for accessibility and UX. Works on any site, including Django templates. **First to install** |
| `agent-browser` | `vercel-labs/agent-browser` | ✅ Vercel | Lets the assistant open the site in Chrome to click through and check it (needs `npm i -g agent-browser`) |
| `terraform-style-guide` | `hashicorp/agent-skills` | ✅ HashiCorp | Conventions for `infra/` (already used in `brain_frontend_extension`) |
| `multi-stage-dockerfile` | `github/awesome-copilot` | ✅ GitHub's collection | Smaller, safer Dockerfiles. Low priority: the Dockerfile is already small |
| `django-patterns`, `django-security` | `affaan-m/ecc` | ⚠️ community | Django conventions and security checks. Popular (12-13K installs), but review carefully |

Not worth it here: `supabase-postgres-best-practices` (four small tables, no query
tuning needed).

### How to install (always for both assistants)

```sh
npx skills add vercel-labs/agent-skills --skill web-design-guidelines -a claude-code -a github-copilot
npx skills list     # each skill should show "Claude Code, GitHub Copilot"
```

Using both `-a` flags is what creates the layout above: real files in `.agents/skills/`, a
link in `.claude/skills/`, and the source + content hash recorded in `skills-lock.json`.
Commit all three. Install **one skill at a time**, read its files, try it, then commit.

To use one: call it by name (`/web-design-guidelines review the homepage template`), or just
describe the task and the assistant loads the relevant skill itself.

> [!NOTE]
> **Windows:** symlinks in git need Developer Mode (or admin) and
> `git config core.symlinks true` before cloning; otherwise Claude Code won't see the skills.

---

## Step 3: Spec Kit

[Spec Kit](https://github.com/github/spec-kit) (by GitHub) turns "build feature X" into a
written spec first, then a plan, then tasks, then code, so the assistant builds what you
actually meant and you can review each stage.

### Install (once per machine)

Needs Python 3.11+ and [uv](https://docs.astral.sh/uv/):

```sh
uv tool install specify-cli
specify --version
```

### Add it to this repo

Commit everything first and work on a branch: `--force` may replace files at paths Spec Kit
manages, so you want a clean diff to review.

```sh
git switch -c chore/spec-kit
specify init --here --force --integration claude
git status          # review every new file before committing
```

- Use **only the `claude` integration**. It installs the commands as skills in
  `.claude/skills/speckit-*`, which Copilot also reads, so one install serves both
  assistants.
- **Don't** also add the `copilot` integration: it would put copies in `.github/skills/`
  (duplicates in Copilot), and Spec Kit marks it as not safe to combine with another.
- Leave the `speckit-*` folders where Spec Kit puts them (don't move them to
  `.agents/skills`); its updater manages them.
- It also adds `.specify/` (templates, scripts and the constitution). Commit it.

> [!WARNING]
> Spec Kit may write to `CLAUDE.md`: older versions rewrote it during `/speckit-plan`,
> newer ones keep a marked section in the agent's context file. Not confirmed for the
> current release. After `specify init` and after the first `/speckit-plan`, run
> `git diff CLAUDE.md`: it should still start with `@AGENTS.md`, and any project facts
> Spec Kit added belong in `AGENTS.md` instead.

### The workflow

Run these in the assistant's chat (Claude Code or Copilot agent mode), not the terminal:

| Command | What it does |
| --- | --- |
| `/speckit-constitution` | Once per project: the principles every spec is checked against. Base it on `AGENTS.md`'s rules; don't duplicate them |
| `/speckit-specify <feature>` | Writes the spec: what and why, user stories, requirements. No code yet |
| `/speckit-clarify` | Optional: asks up to 5 questions about unclear parts and updates the spec |
| `/speckit-plan` | Technical plan: how it will be built in this codebase |
| `/speckit-checklist` | Optional: checks the spec itself is complete and clear |
| `/speckit-tasks` | Breaks the plan into ordered tasks (`tasks.md`) |
| `/speckit-analyze` | Optional, read-only: checks spec, plan and tasks agree before coding |
| `/speckit-implement` | Builds the tasks |
| `/speckit-converge` | Checks the code against spec/plan/tasks and adds anything missed |

Spec Kit's docs write them as `/speckit.specify`; with the skills layout you type
`/speckit-specify`. Review the spec and the plan before running implement: that's where
the value is.

### Check it works

- In Claude Code: type `/speckit` and the commands should be listed.
- In VS Code Copilot Chat (**Agent** mode): type `/` and the same `speckit-*` commands should
  appear, each once.
- Try it on something small first, e.g. `/speckit-specify add a contact form` through
  `/speckit-plan`, and read what it produced.

---

## Quick checklist

- [x] README matches reality (database or not)
- [x] `AGENTS.md` written; `CLAUDE.md` = `@AGENTS.md`; `claude -p` test answers from it
- [ ] Skills installed one by one with `-a claude-code -a github-copilot`, files reviewed,
      `npx skills list` shows both assistants
- [ ] Copilot's `/` menu shows each skill once
- [ ] Spec Kit installed on a branch with `--integration claude` only; diff reviewed,
      `CLAUDE.md` still starts with `@AGENTS.md`
- [ ] Constitution written from `AGENTS.md`
- [ ] One small feature tried through specify → plan

## Reference

- Working example: `brain_frontend_extension` (`AGENTS.md`, `CLAUDE.md`, `.agents/skills/`,
  `.claude/skills/`, `skills-lock.json`, README section "Working with AI agents")
- [GitHub Docs: agent skills](https://docs.github.com/en/copilot/concepts/customizations/agent-skills)
- [VS Code: agent skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [VS Code: custom instructions (AGENTS.md)](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- [Claude Code: skills](https://code.claude.com/docs/en/skills)
- [Claude Code: memory and AGENTS.md](https://code.claude.com/docs/en/memory)
- [skills CLI](https://github.com/vercel-labs/skills) · [skills.sh directory](https://skills.sh)
- [Spec Kit](https://github.com/github/spec-kit) ·
  [existing projects](https://github.github.io/spec-kit/guides/existing-projects.html) ·
  [commands](https://github.github.io/spec-kit/reference/agentic-sdd.html) ·
  [Claude integration](https://github.github.io/spec-kit/integrations/claude.html) ·
  [Copilot integration](https://github.github.io/spec-kit/integrations/copilot.html)
