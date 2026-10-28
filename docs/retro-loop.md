# Retro loop

The team improves its own prompts. That is the point of the loop.

## Feedback in every report
Every agent report ends with `## Feedback`: friction, missing context in the brief, tool limits, unclear hand-overs, a suggested process change. "None" is allowed; omission isn't.

## The retro log
One GitHub issue per period, `Retro log — <period>`, labelled `retro`. The architect adds one comment per return: agent, task, model, whether it bounced at review, and the feedback verbatim. The architect also logs its own observations: lane slips with their post-mortem, briefs that were wrong, re-dispatches, findings that right-first-time should have prevented, bugs found after merge, the owner's corrections.

## The retrospective
On the agreed cadence (weekly by default) and at each milestone, the architect sends the owner a retro brief: what worked, what didn't, root causes, and proposed changes with their owner. Approved changes route by domain:
- personas, roster, templates → the ways-of-working steward;
- backlog items → the product owner;
- pipeline and hook checks → DevOps.

Each gets an issue; the next retro checks it landed.

## Rules for rules
- A fix needed twice becomes a line in the brief template.
- A rule that no feedback or incident touched across two retros is a candidate for removal. Every rule costs every agent attention on every task.
- Model tiers adapt: a task type that bounces at review moves up a tier; one that never bounces is tried a tier lower. The security review never goes below the strongest tier.

## Measures
First-time quality (findings per PR, by author), rework (review rounds, re-dispatches), lane discipline, honesty (a gate reported as passed that wasn't run), model fit, and flow (lead time, deploy frequency, change-failure rate).
