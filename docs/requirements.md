# Requirements and cost

## What you need

- **[Claude Code](https://code.claude.com/docs/en/overview)**, in the terminal, an IDE extension or the desktop app.
- **An account that can run Claude Code**: a Claude subscription (Pro, Max, Team or Enterprise), an Anthropic Console (API) account, or a supported cloud provider (Amazon Bedrock, Google Vertex AI, Microsoft Foundry). See [pricing](https://claude.com/pricing) and the [third-party integrations](https://code.claude.com/docs/en/third-party-integrations) page.
- **Git**, and the **GitHub CLI** (`gh`) if you want labels and PRs handled from the session.
- **Python 3 with PyYAML** for `scripts/render.py`, which turns your config and the role templates into files the same way every time. Most machines that run AI tooling have it; if yours doesn't, `/init-team` offers to install PyYAML (`python3 -m pip install --user pyyaml`) or renders by hand from the same rules, which works but may vary slightly between runs.
- `bash` for the generated hooks.

## This framework runs on subagents

Every specialist is a Claude Code [subagent](https://code.claude.com/docs/en/sub-agents) (`.claude/agents/*.md`). The architect, your main session, dispatches them through the Agent tool. The Claude Code docs don't restrict subagents to a particular plan: they work wherever Claude Code does. What matters is **usage**:

- Subagent requests **count toward the same usage limits** as your main conversation, and each subagent spends tokens of its own while it runs.
- One reviewed change typically runs several agents: the builder, then security, QA, plan alignment and docs reviews. Expect a multiple of what a single session would use.

**Recommendation:** for day-to-day use, run this on a plan with generous limits (Max, Team or Enterprise) or with API billing, where you pay per token and can set spend limits. On Pro, you can still use it: enable fewer roles, put routine reviews on the `fast` or `balanced` tier, and expect to hit limits sooner.

## Model tiers

Roles name a **tier**, not a model. `team.config.yaml` maps tiers to Claude Code model aliases:

```yaml
models:
  fast: haiku        # mechanical, fully specified work
  balanced: sonnet   # writing from clear sources, routine reviews
  strong: opus       # building with TDD, design, tricky reviews
  strongest: opus    # security reviews; set to the strongest model your plan offers
```

If your plan or provider doesn't offer a model, map that tier to one it does. Your organisation's `availableModels` setting can also restrict which models agents may use.

## Keeping cost down

- **Enable only the roles you need.** Only the architect is required.
- **The cheapest tier that gets it right first time.** A review bounce costs more than the stronger model would have. Log the tier of each dispatch on the retro issue and adapt at each retro.
- **Short reports.** Agents report in ≤ 300 words and put details on the issue or PR, which keeps the architect's context (and every later turn) small.
- **At most two agents in parallel** unless their paths are disjoint.
- **Batch reviews**: one review dispatch can cover several PRs.
