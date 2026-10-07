---
name: breakdance-style-conventions
description: Vanessa's personal conventions for naming CSS selectors and design-token variables, structuring reusable styles, and handling images/fonts on Breakdance builds. Consult before creating new selectors, global variables, hero sections, or background images — including greenfield builds, even if naming wasn't asked about. Living document: append new preferences here as Vanessa states them, don't wait for a rewrite.
---

# Breakdance Style & Build Conventions (loader)

This skill is a loader. The conventions themselves live in one canonical file on GitHub, so every copy stays current without re-uploading.

**Canonical:** https://raw.githubusercontent.com/brighterwebsites/breakdance_extras/main/breakdance-style-conventions/SKILL.md

## On first use in a conversation

Load the canonical file once per conversation, then follow it as if it were this skill. Don't re-fetch on later uses in the same conversation.

Try in this order and stop at the first that works:

1. **Claude Code with a local copy:** if a non-`anthropic-skills:` skill named `breakdance-style-conventions` is available, use that one instead of this loader. It's a git checkout of the same file, pulled at session start.
2. **Web fetch:** fetch the canonical URL above.
3. **Code execution:** `curl -fsSL <canonical URL>` in the sandbox.
4. **Fallback:** read `snapshot.md` in this skill's folder. Say once that you're working from the snapshot (its date is on its first line), because it may be behind the canonical file.

## Adding or changing a rule

Edit the canonical file in the GitHub repo, not this loader. In claude.ai, where you can't push, give Vanessa the exact text and section to add so she can commit it.
