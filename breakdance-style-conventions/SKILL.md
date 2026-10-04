---
name: "breakdance-style-conventions"
description: "Vanessa's personal conventions for naming CSS selectors, structuring reusable styles, and handling images/fonts when building or styling Breakdance sites. Always consult this skill before creating new Breakdance selectors, global variables, hero sections, or background images, or before placing, restyling or replacing Brighter BD Elements (Scos_* review card, FAQs and the rest) — even on greenfield builds and even if not explicitly asked about naming or conventions. This is a living document — when Vanessa states a new preference in conversation, add it here rather than treating this list as final."
---

# Breakdance Style & Build Conventions

This captures Vanessa's personal build conventions for Breakdance sites, so they're applied consistently without her having to restate them each time. This file is expected to grow — when she gives a new rule in conversation, append it to the relevant section below (or add a new section) rather than waiting for a full rewrite.

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

Some classes don't belong to the site's design system at all — they're written by a plugin for its own tracking or functionality (Google Analytics data-attribute selectors, LiteSpeed Cache's own lazy-load-control classes, etc.). Don't rename these, don't fold them into the site prefix, don't reclassify them as utilities. They're a separate category entirely: leave exactly as found. If unsure whether something is plugin-native vs. part of the design system, ask rather than assume — infrastructure classes can look similar to genuine one-off utilities at a glance. These include `ga-*` prefixed selectors.

## 6. Scales — extend, don't fork

If a size/spacing/weight scale already exists using one mechanism (e.g. a numbered set of classes all built with `clamp()`), and a new value is needed at the small or large end, add the next step in that same scale using the same mechanism. Don't solve the same need with a parallel class built a different way (e.g. a plain fixed-px class sitting right below a clamp-based scale, covering the gap the scale should have covered itself). One scale, one mechanism, extended as needed — not two systems quietly doing the same job.

## 7. Retire workarounds when a better native option exists

Some existing classes exist because a cleaner native way to do the same thing wasn't known or available yet at the time — not because the class solves something the builder can't otherwise do (e.g. a set of "span N columns" utility classes applied per child, built before realising the grid's own column-template setting on the parent does the same job directly). When rebuilding and a workaround like this is identified, don't preserve it or reclassify it as a utility — retire it and use the proper native mechanism instead. Worth asking if unsure whether something is a genuine reusable utility or a workaround that's since been superseded.

## 8. Agency-wide shared components — separate prefix from site-specific work

Components built once and reused across multiple client sites (not specific to any one site) get their own agency-level prefix (`bw-`), distinct from any individual site's prefix and distinct from generic unprefixed utilities. This is a third naming tier, not a variant of the other two: site prefix = specific to this site's content/structure; `bw-` = shared agency component library; no prefix = generic single-purpose utility usable anywhere.

## 9. Elements — prefer Fundamental elements

Prefer Fundamental elements (F-Text, F-Text Link and the rest of the Fundamental set) over the standard Essential elements wherever a Fundamental element can do the job. They output cleaner markup, which is easier for AI to work with, and the MCP's element lookups miss some basic standard blocks. Don't recommend switching away from Fundamentals to dodge a builder bug; work around the bug instead (see section 10) and expect Breakdance to fix it.

### Mixed-content sites — basic vs fundamental elements


Breakdance 3.x has two element families, and sites built before or across the betas usually contain both.

- **Fundamentals** render with a `bde-f-` class (`bde-f-container`, `bde-f-text`, `bde-f-image`). They ship **no default CSS**: what you write is what renders.
- **Basic elements** render with a plain `bde-` class (`bde-div`, `bde-text`, `bde-column`, `bde-section`). They ship **hidden base CSS** that does not appear in the element's design panel or its custom CSS field.

The one that causes most of the trouble:

```css
.bde-div { display:flex; flex-direction:column; align-items:flex-start; text-align:left; max-width:100%; position:relative; background-size:cover; }
```

This means a class that only sets `display:flex` on a basic Div still lays out as a column. Its children also shrink to their content width, and `justify-content: space-between` appears to do nothing.

**How to tell which family an element belongs to:** check the rendered class (`bde-f-` or `bde-`). In the element tree, fundamentals usually hold registered selectors (by ID). Older basic elements often hold loose class strings, and some of those are not registered selectors at all.

#### Before styling — check

1. **Read the hidden defaults.** Render the post or template with its CSS included, then read `element_default_css` for every basic element type you are about to style.
   - As of beta 9, the per-element CSS lookup returns Div, Text, Image, RichText and TextLink as "missing" (bug reported), so don't rely on it for those.
   - Custom elements (Brighter BD Elements) and other built-ins return correctly.
2. **Check every class you will touch.** Is it a registered selector? Is it used anywhere else on the site?
   - If a class is unregistered, scope a nested rule under a registered parent. Don't register a new global class just to style it.
   - **Before reusing an existing class on a new or rebuilt element, expand it and inspect its nested children** (`& > div`, `& > div:first-child` and so on), not just its own properties. Nested rules don't show on the element, and they reapply the old structure's layout to whatever the new element contains. On early-beta sites, assume a reused class carries baggage until you've checked.
3. **Read existing selector properties back before changing them.** Importing a selector replaces its properties; it does not merge.

#### While styling — declare, don't inherit

Any class applied to a basic element must restate every layout property that the element's defaults set: `display`, `flex-direction`, `align-items` and `width` (plus `justify-content` where it matters).

Never write `display:flex` on its own against a basic Div. The explicit declarations win whatever the element type, so the rule still holds if the wrapper is later swapped to a fundamental.

#### After styling — verify

1. Read the selectors back. The import should report no dropped properties, other than ones you removed on purpose.
2. Check the result visually against a real record. For templates, render with a real product or post as context.
3. Purge LiteSpeed before judging the frontend.

#### When to swap or rebuild instead of restyling

| Situation | Approach |
| --- | --- |
| Restyling a block that works structurally | Keep the basic elements and apply "declare, don't inherit". This is the lowest-risk option on live sites and the default. |
| Restructuring that block anyway, or fighting the basic wrapper's defaults on more than a few properties | Swap the wrapper to a fundamental Container, move the children into it, and give it a fresh role-named class. Reuse an existing class only if fundamentals already use it. |
| The section is being redesigned, not just restyled | Rebuild it from fundamentals, and delete the old section in the same pass. |

**Exception: retired Brighter BD Elements always get replaced, never restyled in place.** See section 14.

#### Naming — don't encode the element family

Don't use family-specific prefixes such as `cns_f_` or `cns_b_`. The reasoning is the same as in section 1: a name says what a selector *is*, not how it is currently built.

- The family is already visible in the rendered class (`bde-f-` or `bde-`), so the name doesn't need to carry it.
- A family prefix becomes wrong the moment a wrapper is swapped.
- To track migration progress, use selector collections or folders.

*Origin: CNS single-product template, Oct 2026. The price block and specs box were shrinking and stacking because of the `.bde-div` defaults. Fixed with explicit layout declarations; no rebuild was needed.*

## 10. Design tokens — Variables are the single source of truth

**Every token is a registered global variable.** Colours, spacing, radius, type sizes, weights, line heights, letter spacing, shadows, motion and font families live in Global Settings > Variables, so they can be picked in the builder.

**Colours are Variables, not the Global Colours palette.** Register every colour as a colour variable. On existing sites, move palette colours into Variables (same names and values), then empty the palette once everything is migrated. The palette is likely to be deprecated: once its colours are removed, new colours can't be added to it in the builder.

**Keep the global stylesheet as empty as possible.** Don't define tokens in a `:root {}` block in Global Settings > Code, and don't load fonts with `@import`: registering a font as a font-family variable makes Breakdance load it. Move any remaining global CSS (base element styles, form and button styling) into global selectors, so it's visible and editable in the selector panel. Leave only what can't live anywhere else, such as `@keyframes`.

**Variable-type mismatch workaround (`-t` pointer variables).** Some builder controls only list one variable type: for example, F-Text's font-weight control takes text (T) variables while F-Text Link's takes number (#) variables, even though both are the same CSS property. Until Breakdance fixes it:
- The `#` variable is the single source of truth and holds the value (`--cns-fw-semibold: 600`).
- A matching text variable with a `-t` suffix holds only a pointer to it (`--cns-fw-semibold-t: var(--cns-fw-semibold)`), kept in a separate "(T aliases)" collection.
- Never put a value in a `-t` variable; only ever change the `#` one.
- Use the same pattern, suffix and collection anywhere else the mismatch shows up. When Breakdance fixes it, delete the aliases collection.

## 11. Breakpoints — optimise down to 350px

Active mobile users typically sit at 393px down to 375px. Optimise layouts down to 350px, and add a custom 350px breakpoint below Phone Portrait (479px) on new sites and rebuilds.

## 12. Editing safety

**Deleting a selector strips its class from every element.** Breakdance stores an element's classes as selector IDs, so deleting a selector that is in use removes that class from every element using it. Never delete a selector that is used on any element. To retire a duplicate or generic class that's in use, rename it within its component's rename pass, so the elements are updated in the same edit.

**Reload the builder before editing after an AI change.** The builder saves its whole in-memory copy of selectors and variables, so a tab opened before an AI or MCP change can overwrite that change on save. Refresh the builder before testing or editing whenever changes have been made outside it.

**Snapshot before bulk changes.** Before deleting or bulk-editing selectors or variables, export the raw Breakdance options (selectors, variables, collections, global settings) to a JSON file outside the web root, so a single option can be restored without a full database restore.

**Purge after writes.** After any write that changes CSS output, purge the LiteSpeed cache so the live site picks up the regenerated Breakdance CSS.

## 13. Colour naming — semantic only, single tier

**Name colours by the job they do, never by what they look like.** A colour variable's name must stay true if its value changes later. `--pfs-primary` survives a rebrand from orange to teal; `--pfs-orange` becomes a lie the moment it changes. So no hue or shade words in colour variable names: no `blue`, `orange`, `sand`, `charcoal`, `navy`, `forest`, and no numbered shade scales (`-100`…`-900`) either.

**One tier.** The semantic variable holds the value directly (`--pfs-primary: #e8541f`). Don't build a raw palette tier underneath that semantic variables point to — it doubles the number of variables for no gain on a small-business site. Only exception: a site that's already set up two-tier — follow what's there rather than restructuring it.

**Pattern:** `--{prefix}-{role}` with an optional `-{variant}` for state or strength.

Core roles (use these names; add only what the site actually needs):
- `primary` — main brand colour (buttons, key links, brand moments)
- `on-primary` — text/icons sitting on `primary`
- `accent` — secondary highlight (badges, small emphasis, hover moments)
- `on-accent` — text/icons sitting on `accent`
- `text` — body text
- `text-muted` — secondary text, captions, meta
- `heading` — only if headings differ from `text`
- `bg` — page background
- `surface` — cards, panels sitting on `bg`
- `surface-alt` — alternating section band
- `inverse-bg` / `on-inverse` — dark (or contrasting) sections and the text on them
- `border` — dividers, input borders
- `success`, `warning`, `error` — form and status feedback, when needed

Variants describe state or strength, not lightness: `primary-hover`, `primary-soft` (tint used for backgrounds), `primary-strong`. Each variant stores its own value — don't create a hidden raw tier to derive them.

**Same rule for utility classes.** A colour utility references the role, not the hue: `.bg-surface-alt`, `.text-muted` — not `.bg-beige`, `.text-grey`. (Lightness modifiers like `.bg-dark-10` from section 1 are fine; they describe an adjustment, not a hue.)

## 14. Brighter BD Elements — replace retired ones, handle SCOS elements with care

### Plugin versions differ between sites

Around 12 client sites run the Brighter BD Elements plugin, and they aren't on the same version. Versions were never tracked properly in the plugin, so the header comment and version number don't reliably tell you what code a site is running. Don't assume a site matches the git repo (`brighterwebsites/bd-brighter-elements`), or that two sites match each other. Bringing every site up to the current version isn't practical: it would mean diffing roughly 12 installs by hand. So the working rule is to converge each site *as you touch it*, not all at once.

### Current vs retired elements

Current. These are fine to use on new builds and rebuilds:

- `Scos_*` (Aggregate Review, Breadcrumbs, FAQs, Review Card, TL;DR). They output SCOS data and schema, so there's no fundamental equivalent. See the cautions below.
- `Accordion_Content_Extended`
- `TableRows`, `Table_Cell`, `Table_Text`
- `Text_Extended`

**Retired. Never place these:** `Definition`, `Definitions_Box`, `Description_Text`, `Extended_Wrapper`, `Section_Simple`, `Summary`.
- Fundamental elements replaced them.
- From plugin v0.3.5 they're hidden from the builder's Add panel (`addPanelRules => ['alwaysHide' => true]`), but they stay registered so existing pages keep rendering.
- Sites on older plugin versions will still show them in the Add panel.
- MCP element lookups may still list them on any version.

### When you find a retired element on a page — replace it with fundamentals

This is the default, not an option. Don't restyle a retired element in place, even when the block works. Its CSS and markup depend on whichever plugin version that site happens to have, so any fix only holds for that one site.

1. Note the element's current visual result (screenshot or render) and the classes and selectors it carries.
2. Rebuild the block from fundamental elements. Apply the existing role-named classes only if section 9's "check before reusing a class" passes. Otherwise create a fresh role-named class.
3. Delete the retired element in the same pass, so the page never holds both versions.
4. Verify the result against the original render, then purge LiteSpeed.

Track progress per site with selector folders or collections, not with naming (section 1).

**Only delete a retired element's folder from a site's plugin once nothing on that site uses it any more.** Deleting it breaks every page that still contains one.

### SCOS elements — check the live version before styling

The `Scos_*` elements also differ between sites. Their HTML structure and default CSS have changed between plugin versions, and some design-panel controls don't work on some versions. **Review Card** and **FAQs** have changed the most. Before editing their design-panel options or targeting them with selectors:

1. **Read the rendered markup on *this* site.** Render the page, or call `preview-element`, and read the actual classes and nesting. Don't write selectors from the git repo's `html.twig`, or from another site's markup.
2. **Read that site's element default CSS** (`element_default_css`). It may differ from the repo's `default.css`.
3. **Don't trust a design-panel control just because it exists.** After changing one, check the rendered CSS to confirm it actually took effect. If it didn't, style through a selector scoped to the element's real rendered classes, and note the broken control for the plugin backlog.
4. **Don't copy SCOS selectors between sites** without repeating steps 1–2 on the target site. A selector written for one version's structure can match nothing on another version, or match the wrong thing.

*This section is an interim note. Revisit it once the plugin has a reliable version marker and the sites have been brought onto a known version.*
