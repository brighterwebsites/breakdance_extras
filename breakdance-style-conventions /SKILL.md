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

## 9. Mixed-content sites — basic vs fundamental elements

Breakdance 3.x has two element families, and sites built before or across the betas usually contain both.

- **Fundamentals** render with a `bde-f-` class (`bde-f-container`, `bde-f-text`, `bde-f-image`). They ship **no default CSS**: what you write is what renders.
- **Basic elements** render with a plain `bde-` class (`bde-div`, `bde-text`, `bde-column`, `bde-section`). They ship **hidden base CSS** that does not appear in the element's design panel or its custom CSS field.

The one that causes most of the trouble:

```css
.bde-div { display:flex; flex-direction:column; align-items:flex-start; text-align:left; max-width:100%; position:relative; background-size:cover; }
```

This means a class that only sets `display:flex` on a basic Div still lays out as a column. Its children also shrink to their content width, and `justify-content: space-between` appears to do nothing.

**How to tell which family an element belongs to:** check the rendered class (`bde-f-` or `bde-`). In the element tree, fundamentals usually hold registered selectors (by ID). Older basic elements often hold loose class strings, and some of those are not registered selectors at all.

### Before styling — check

1. **Read the hidden defaults.** Render the post or template with its CSS included, then read `element_default_css` for every basic element type you are about to style.
   - As of beta 9, the per-element CSS lookup returns Div, Text, Image, RichText and TextLink as "missing" (bug reported), so don't rely on it for those.
   - Custom elements (Brighter BD Elements) and other built-ins return correctly.
2. **Check every class you will touch.** Is it a registered selector? Is it used anywhere else on the site?
   - If a class is unregistered, scope a nested rule under a registered parent. Don't register a new global class just to style it.
   - **Before reusing an existing class on a new or rebuilt element, expand it and inspect its nested children** (`& > div`, `& > div:first-child` and so on), not just its own properties. Nested rules don't show on the element, and they reapply the old structure's layout to whatever the new element contains. On early-beta sites, assume a reused class carries baggage until you've checked.
3. **Read existing selector properties back before changing them.** Importing a selector replaces its properties; it does not merge.

### While styling — declare, don't inherit

Any class applied to a basic element must restate every layout property that the element's defaults set: `display`, `flex-direction`, `align-items` and `width` (plus `justify-content` where it matters).

Never write `display:flex` on its own against a basic Div. The explicit declarations win whatever the element type, so the rule still holds if the wrapper is later swapped to a fundamental.

### After styling — verify

1. Read the selectors back. The import should report no dropped properties, other than ones you removed on purpose.
2. Check the result visually against a real record. For templates, render with a real product or post as context.
3. Purge LiteSpeed before judging the frontend.

### When to swap or rebuild instead of restyling

| Situation | Approach |
| --- | --- |
| Restyling a block that works structurally | Keep the basic elements and apply "declare, don't inherit". This is the lowest-risk option on live sites and the default. |
| Restructuring that block anyway, or fighting the basic wrapper's defaults on more than a few properties | Swap the wrapper to a fundamental Container, move the children into it, and give it a fresh role-named class. Reuse an existing class only if fundamentals already use it. |
| The section is being redesigned, not just restyled | Rebuild it from fundamentals, and delete the old section in the same pass. |

### Naming — don't encode the element family

Don't use family-specific prefixes such as `cns_f_` or `cns_b_`. The reasoning is the same as in section 1: a name says what a selector *is*, not how it is currently built.

- The family is already visible in the rendered class (`bde-f-` or `bde-`), so the name doesn't need to carry it.
- A family prefix becomes wrong the moment a wrapper is swapped.
- To track migration progress, use selector collections or folders.

*Origin: CNS single-product template, Oct 2026. The price block and specs box were shrinking and stacking because of the `.bde-div` defaults. Fixed with explicit layout declarations; no rebuild was needed.*
 
## Open / not yet decided
 
- **Color token naming convention** — Vanessa is still working out a standard pattern (semantic/role-based naming — primary, secondary, neutral, accent — layered over a raw palette tier, roughly following Tier 1 raw hues → Tier 2 semantic aliases). Not locked yet. Do not assume or invent a color-naming scheme in the absence of site-specific instruction — ask, or use whatever convention that site's design system already has, until this section is filled in.
