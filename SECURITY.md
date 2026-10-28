# Security policy

## Reporting a vulnerability

Please report security issues **privately** through this repository's **Security → Report a vulnerability** form (GitHub private vulnerability reporting). Don't open a public issue.

Include what you found, where (file and line, or the generated output), and how it could be abused. You'll get an acknowledgement within 7 days and a plan within 30.

## Scope

This repo ships prompts, templates and shell scripts that run inside other people's projects. In scope:
- generated hooks or scripts that could execute unintended commands, leak secrets, or be bypassed;
- prompts or commands that could lead an agent to exfiltrate data, push, merge or publish without the owner's approval, or widen its own permissions;
- the upstream contribution design leaking project data to the template;
- anything in the shipped themes, packs or examples that should not be public.

Out of scope: vulnerabilities in Claude Code itself (report to [Anthropic](https://www.anthropic.com/responsible-disclosure-policy)) or in the projects that adopt this template.

## Supported versions

The latest release. Fixes are released as a new version; run `/sync-team` to pick them up.
