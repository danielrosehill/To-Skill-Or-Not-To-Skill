---
name: skill-or-not
description: Decide whether a task should become a reusable skill before doing it as a one-off. Runs the five-step checklist (repeatable? automatable? already in our library? already written by someone else? otherwise create it) and acts on the verdict. Use when the user says "should this be a skill", "is this a skill candidate", "run the skill checklist", "to skill or not to skill", or "I think this is replicable".
---

# To skill or not to skill

Run the checklist below against the task in front of you, which is either the one the
user just described or the one they point at. Work through the steps in order and stop
at the first exit. Record the evidence for each answer, not just yes or no.

## 1. Is it repeatable?

Look at two things:

- **Shape.** Would anyone plausibly do this only once? Tasks like "reconcile this
  month's invoices", "triage this inbox" or "check this site on mobile" recur by
  their nature. Tasks like "rename this one file" do not.
- **History.** Check the agent's memory, past sessions, shell history, and the
  current repo for earlier runs of the same pattern. Two earlier occurrences settle
  it.

Lean towards yes. If the answer is clearly no, **exit: do the task.**

## 2. Can it be automated or assisted?

Can available tools do the task, in whole or in part? That includes MCP servers,
APIs, browser automation, the shell, or written guidance an agent could follow step
by step. Partial counts: a skill that does the lookup and leaves the decision to the
user still pays off. Set the bar low.

If nothing about it can be automated or guided, **exit: do the task.**

## 3. Is it already in the library?

Skill discovery should already have surfaced a matching skill. If it didn't, search
explicitly before you conclude nothing exists:

- the skills and plugins installed in this session;
- the user's plugin catalogue or marketplaces (public, private, third-party), using
  whatever search tool the environment provides;
- the local clones of the user's plugin repos.

A search that returns nothing may be blind rather than conclusive: the wrong index,
an empty index, or a tool that can't see that namespace. Make sure the search
actually reaches the library before you trust a miss.

If you find a match, **exit: use that skill for the task.** If it needs a small fix
to fit, fix it in its plugin repo and note that.

## 4. Has someone else already written it?

Search public sources for third-party skills, plugins, or boilerplates covering the
workflow: official vendor plugins, public marketplaces, GitHub. Then judge how
personal the workflow is:

- **Fits as-is.** Add it to the user's third-party collection as a pointer to the
  upstream repo, pinned to a ref. Don't copy it. Then use it for the task. **Exit.**
- **Close, but the workflow is individual.** Use it as the base for step 5 and credit
  the upstream in the new skill.
- **Nothing suitable.** Go to step 5.

## 5. Create it

1. **Pick the plugin.** It goes in the public plugin if nothing in it is personal:
   no names, accounts, hosts, or internal infrastructure. Otherwise it goes in the
   private one. A skill that would only be public after depersonalising can ship
   publicly in a generic form, with the specifics kept in a private sibling.
2. **Write the skill.** Follow the conventions of the target plugin. Don't invent
   new ones.
3. **Deploy it** the way the user's plugins normally go live, for example push and
   index or sync. Then confirm the skill is actually discoverable.
4. **Validate it on the real task.** Run the one-off task you were about to do
   through the new skill. Fix whatever that run exposes before you call the skill
   done.

## Approval

Steps 1–4 are read-only, so go ahead with them. Creating a skill, publishing it, or
adding it to a collection follows the user's standing approval rules. If none are
known, state the verdict and the plan in two lines and ask once.

## Report

Finish with a short verdict, for example:

```
skill-or-not: step 5 → new skill `invoice-reconcile` in <private plugin>
evidence: monthly pattern (3 prior sessions); the vendor API covers it
first run: <task> completed through the skill
```
