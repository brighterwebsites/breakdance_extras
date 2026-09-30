---
name: breakdance-style-conventions
description: conventions for naming CSS selectors, structuring reusable styles, and handling images/fonts when building or styling Breakdance sites. Always consult this skill before creating new Breakdance selectors, global variables, hero sections, or background images — even on greenfield builds and even if not explicitly asked about naming or conventions. This is a living document — when Vanessa states a new preference in conversation, add it here rather than treating this list as final.
---
 
# Breakdance Style & Build Conventions
 
This captures Vanessa's personal build conventions for Breakdance sites, so they're applied consistently without having to restate them each time. This file is expected to grow — when she gives a new rule in conversation, append it to the relevant section below (or add a new section) rather than waiting for a full rewrite.
 
## 1. Selector naming & prefixing
 
**Global prefix per site.** Every site gets one short prefix (e.g. `gs_` for Guerilla Steel), applied to semantic/component-level selectors — anything that names a section or component specific to *this* site's content structure (`gs_hero`, `gs_hero-title`, `gs_card`).
 
**Functional/utility modifiers stay unprefixed.** Small, single-purpose classes that do one CSS job and aren't tied to this site's specific content — e.g. `.right` (align-self: right), `.bg-dark-10` (background 10% darker, may also lift paired text color) — do NOT get the site prefix.
 
**The test to apply:** would this exact class, doing this exact thing, make sense unchanged on a completely different site?
- Yes → it's a utility. No prefix.
- No, because it names something specific to this site's content or structure → it's semantic. Prefix it.
**Why this matters practically, not just tidiness:** Vanessa uses the prefix as a workflow signal while building — she experiments freely with unprefixed classes, then adds the prefix only to what she decides to keep. Anything left unprefixed at cleanup time is safe to delete. Don't prefix speculative/in-progress classes prematurely; that removes the signal.
 
**Sub-element naming — BEM double-underscore.** For compound/child names within a semantic component, use double-underscore to denote a sub-element: `gs_project__wrapper`, `gs_project__card`, `gs_project__overlay`. Apply this consistently once a component has more than one named part — don't invent a different separator (single hyphen, camelCase) for the same relationship.
 
**One prefix per site, permanently — don't repurpose it to track migration or build status.** If a site needs to distinguish old vs. new selectors during a rebuild or migration (e.g. tracking what's been touched since a platform upgrade), use Breakdance's selector folder/organisation feature for that — don't invent a second or temporary prefix (like an interim `xx_` variant) to encode that information into the name itself. Names should only ever encode what the selector *is*; where it stands in a migration is a filing/organisation concern, not a naming concern.
 
## 2. Reusability — don't duplicate identical patterns per page
 
Before creating a page-scoped selector (e.g. `gs_home-hero`), check whether an identical style pattern already exists elsewhere on the site. If it's the same, reuse the general-purpose selector (`gs_hero`) instead of creating a near-duplicate under a page-specific name. Page-level prefixing on a selector should only happen when that page's version is *actually* different from the general pattern — not by default.
 
## 3. Background images — never use CSS background-image
 
Hero and section background images must not be implemented as a CSS `background-image`. Use an actual image element instead, so:
- `fetchpriority` and `decoding` (sync/async) attributes can be set appropriately
- Lazy loading is explicitly turned **off** in the element's design settings for above-the-fold/hero images
This is a hard rule, not a default-with-exceptions — apply it every time a hero or above-fold section needs a background image.
 
## 4. Hero section fonts — max 2 styles
 
Hero sections should use a maximum of **2 font styles**, counting font-weight as a distinct style (e.g. Barlow Condensed Bold + Inter Regular = 2, not 1). This cap exists specifically so every font used in the hero can be preloaded — don't introduce a third weight or family in a hero section even if it "just" needs a lighter touch somewhere.
 
## 5. Third-party / infrastructure classes — leave untouched
 
Some classes don't belong to the site's design system at all — they're written by a plugin for its own tracking or functionality (Google Analytics data-attribute selectors, LiteSpeed Cache's own lazy-load-control classes, etc.). Don't rename these, don't fold them into the site prefix, don't reclassify them as utilities. They're a separate category entirely: leave exactly as found. If unsure whether something is plugin-native vs. part of the design system, ask rather than assume — infrastructure classes can look similar to genuine one-off utilities at a glance. These include ga-* prefix selectors 
 
## 6. Scales — extend, don't fork
 
If a size/spacing/weight scale already exists using one mechanism (e.g. a numbered set of classes all built with `clamp()`), and a new value is needed at the small or large end, add the next step in that same scale using the same mechanism. Don't solve the same need with a parallel class built a different way (e.g. a plain fixed-px class sitting right below a clamp-based scale, covering the gap the scale should have covered itself). One scale, one mechanism, extended as needed — not two systems quietly doing the same job.
 
## 7. Retire workarounds when a better native option exists
 
Some existing classes exist because a cleaner native way to do the same thing wasn't known or available yet at the time — not because the class solves something the builder can't otherwise do (e.g. a set of "span N columns" utility classes applied per child, built before realising the grid's own column-template setting on the parent does the same job directly). When rebuilding and a workaround like this is identified, don't preserve it or reclassify it as a utility — retire it and use the proper native mechanism instead. Worth asking if unsure whether something is a genuine reusable utility or a workaround that's since been superseded.
 
## 8. Agency-wide shared components — separate prefix from site-specific work
 
Components built once and reused across multiple client sites (not specific to any one site) get their own agency-level prefix (`bw-`), distinct from any individual site's prefix and distinct from generic unprefixed utilities. This is a third naming tier, not a variant of the other two: site prefix = specific to this site's content/structure; `bw-` = shared agency component library; no prefix = generic single-purpose utility usable anywhere.
 
## Open / not yet decided
 
- **Color token naming convention** — Vanessa is still working out a standard pattern (semantic/role-based naming — primary, secondary, neutral, accent — layered over a raw palette tier, roughly following Tier 1 raw hues → Tier 2 semantic aliases). Not locked yet. Do not assume or invent a color-naming scheme in the absence of site-specific instruction — ask, or use whatever convention that site's design system already has, until this section is filled in.
