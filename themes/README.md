# Themes

A theme gives each role a **name** and a one-line **flavour**, and optionally a short **personality** (a working trait and something they love off duty). Names make a team easier to talk to ("send it to Hermes") and make labels, trailers and reports readable. They change nothing about what a role does: the [role template](../roles/README.md) is canonical.

## Shipped themes

| Theme | Example (architect · security · front end) | Source |
|---|---|---|
| `neutral` | Architect · Security · Frontend | role names, no personas |
| `arthurian` | Arthur · Bors · Galahad | Malory, *Le Morte d'Arthur*; the *Mabinogion* |
| `greek` | Athena · Argus · Iris | Hesiod, *Theogony*; the Homeric Hymns |
| `roman` | Vitruvius · Horatius · Ovid | historical figures of Rome |
| `norse` | Odin · Heimdall · Baldr | the Poetic and Prose Eddas |
| `egyptian` | Imhotep · Wadjet · Hathor | Egyptian mythology and history |
| `astronomy` | Polaris · Sirius · Vega | traditional star and constellation names |

Every shipped theme is drawn from **public-domain** sources.

## Why there are no franchise themes

Names and characters from film, TV and book franchises (Star Wars, Star Trek, Game of Thrones, The Lord of the Rings and the like) are protected by trademark and copyright. Shipping them in an open-source template would expose every adopter to that risk, so this repo doesn't. What you do in your own private repo is your call; see below.

## Write your own

Create `themes/local/<id>.yaml` in your project:

```yaml
id: my-team
title: My team
source: our own names            # say where the names come from
roles:                           # one entry per role you enable; the architect is required
  architect:  { name: Ada,   flavour: "Designs and routes; writes nothing in the repo." }
  security:   { name: Grace, flavour: "Watches every PR for security and privacy." }
  frontend:   { name: Alan,  flavour: "Owns the surface people see.", personality: "Patient; off duty he restores old radios." }  # personality is optional
```

Then set `theme: local/my-team` in `team.config.yaml` and run `/init-team`.

Rules:
- **Names must be unique** within a theme. The slug (lower case, ASCII letters, digits and hyphens) becomes the agent file name and the `agent:<slug>` label.
- **Flavour is one sentence.** It sets tone; it never changes the role's lane or rules.
- **No real living people** and nothing you don't have the right to use.
- A role missing from your theme falls back to the `neutral` name.

You can also override a single name without a whole theme: `roles.<id>.name` in `team.config.yaml`.

## Contribute a theme

Public-domain themes are welcome. Open a PR with the YAML and cite the source in `source:`. See [CONTRIBUTING.md](../CONTRIBUTING.md).
