---
name: obsidian-markdown
description: Create and edit Obsidian Flavored Markdown with wikilinks, embeds, callouts, properties, and other Obsidian-specific syntax. Use when working with .md files in Obsidian, or when the user mentions wikilinks, callouts, frontmatter, tags, embeds, or Obsidian notes.
---

# Obsidian Flavored Markdown Skill

Create and edit valid Obsidian Flavored Markdown. Obsidian extends CommonMark and GFM with wikilinks, embeds, callouts, properties, comments, and other syntax. This skill covers only Obsidian-specific extensions -- standard Markdown (headings, bold, italic, lists, quotes, code blocks, tables) is assumed knowledge.

<HARD-GATE>
Règles NON-NÉGOCIABLES pour les notes Obsidian :
1. `[[wikilinks]]` pour les notes internes du vault UNIQUEMENT — liens Markdown `[text](url)` pour les URLs externes
2. Frontmatter YAML valide au début de chaque note (au minimum `tags` et/ou `aliases`)
3. Block IDs (`^block-id`) sur une ligne SÉPARÉE pour les listes et quotes
4. JAMAIS de HTML dans les notes Obsidian — utiliser la syntaxe Obsidian native
</HARD-GATE>

## CHECKLIST OBLIGATOIRE

1. **Frontmatter** — Ajouter propriétés (title, tags, aliases) en YAML au début
2. **Contenu** — Rédiger avec Markdown standard + extensions Obsidian
3. **Liens** — `[[wikilinks]]` pour notes du vault, `[text](url)` pour externe
4. **Embeds** — `![[embed]]` pour intégrer notes, images, PDFs
5. **Callouts** — `> [!type]` pour structurer l'information
6. **Vérification** — Confirmer le rendu en reading view Obsidian

---

## Workflow: Creating an Obsidian Note

1. **Add frontmatter** with properties (title, tags, aliases) at the top of the file. See [PROPERTIES.md](references/PROPERTIES.md) for all property types.
2. **Write content** using standard Markdown for structure, plus Obsidian-specific syntax below.
3. **Link related notes** using wikilinks (`[[Note]]`) for internal vault connections, or standard Markdown links for external URLs.
4. **Embed content** from other notes, images, or PDFs using the `![[embed]]` syntax. See [EMBEDS.md](references/EMBEDS.md) for all embed types.
5. **Add callouts** for highlighted information using `> [!type]` syntax. See [CALLOUTS.md](references/CALLOUTS.md) for all callout types.
6. **Verify** the note renders correctly in Obsidian's reading view.

> When choosing between wikilinks and Markdown links: use `[[wikilinks]]` for notes within the vault (Obsidian tracks renames automatically) and `[text](url)` for external URLs only.

## Internal Links (Wikilinks)

```markdown
[[Note Name]]                          Link to note
[[Note Name|Display Text]]             Custom display text
[[Note Name#Heading]]                  Link to heading
[[Note Name#^block-id]]                Link to block
[[#Heading in same note]]              Same-note heading link
```

Define a block ID by appending `^block-id` to any paragraph:

```markdown
This paragraph can be linked to. ^my-block-id
```

For lists and quotes, place the block ID on a separate line after the block:

```markdown
> A quote block

^quote-id
```

## Embeds

Prefix any wikilink with `!` to embed its content inline:

```markdown
![[Note Name]]                         Embed full note
![[Note Name#Heading]]                 Embed section
![[image.png]]                         Embed image
![[image.png|300]]                     Embed image with width
![[document.pdf#page=3]]               Embed PDF page
```

See [EMBEDS.md](references/EMBEDS.md) for audio, video, search embeds, and external images.

## Callouts

```markdown
> [!note]
> Basic callout.

> [!warning] Custom Title
> Callout with a custom title.

> [!faq]- Collapsed by default
> Foldable callout (- collapsed, + expanded).
```

Common types: `note`, `tip`, `warning`, `info`, `example`, `quote`, `bug`, `danger`, `success`, `failure`, `question`, `abstract`, `todo`.

See [CALLOUTS.md](references/CALLOUTS.md) for the full list with aliases, nesting, and custom CSS callouts.

## Properties (Frontmatter)

```yaml
---
title: My Note
date: 2024-01-15
tags:
  - project
  - active
aliases:
  - Alternative Name
cssclasses:
  - custom-class
---
```

Default properties: `tags` (searchable labels), `aliases` (alternative note names for link suggestions), `cssclasses` (CSS classes for styling).

See [PROPERTIES.md](references/PROPERTIES.md) for all property types, tag syntax rules, and advanced usage.

## Tags

```markdown
#tag                    Inline tag
#nested/tag             Nested tag with hierarchy
```

Tags can contain letters, numbers (not first character), underscores, hyphens, and forward slashes. Tags can also be defined in frontmatter under the `tags` property.

## Comments

```markdown
This is visible %%but this is hidden%% text.

%%
This entire block is hidden in reading view.
%%
```

## Obsidian-Specific Formatting

```markdown
==Highlighted text==                   Highlight syntax
```

## Math (LaTeX)

```markdown
Inline: $e^{i\pi} + 1 = 0$

Block:
$$
\frac{a}{b} = c
$$
```

## Diagrams (Mermaid)

````markdown
```mermaid
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Do this]
    B -->|No| D[Do that]
```
````

To link Mermaid nodes to Obsidian notes, add `class NodeName internal-link;`.

## Footnotes

```markdown
Text with a footnote[^1].

[^1]: Footnote content.

Inline footnote.^[This is inline.]
```

## Complete Example

````markdown
---
title: Project Alpha
date: 2024-01-15
tags:
  - project
  - active
status: in-progress
---

# Project Alpha

This project aims to [[improve workflow]] using modern techniques.

> [!important] Key Deadline
> The first milestone is due on ==January 30th==.

## Tasks

- [x] Initial planning
- [ ] Development phase
  - [ ] Backend implementation
  - [ ] Frontend design

## Notes

The algorithm uses $O(n \log n)$ sorting. See [[Algorithm Notes#Sorting]] for details.

![[Architecture Diagram.png|600]]

Reviewed in [[Meeting Notes 2024-01-10#Decisions]].
````

## References

- [Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown)
- [Internal links](https://help.obsidian.md/links)
- [Embed files](https://help.obsidian.md/embeds)
- [Callouts](https://help.obsidian.md/callouts)
- [Properties](https://help.obsidian.md/properties)

---

## ANTI-PATTERNS

| Excuse | Réalité |
|--------|---------|
| "Les liens Markdown standards suffisent dans un vault" | Utiliser `[[wikilinks]]` pour les notes internes — Obsidian suit les renommages automatiquement. Liens Markdown uniquement pour URLs externes. |
| "Le frontmatter c'est optionnel" | Les propriétés (tags, aliases, dates) sont ESSENTIELLES pour les Bases, la recherche et l'organisation du vault. |
| "Les callouts c'est du décor" | Les callouts structurent l'information (warning, tip, important). Ils améliorent la lisibilité en reading view. |
| "Un seul format de bloc ID suffit" | Pour les listes et quotes, le `^block-id` doit être sur une ligne SÉPARÉE après le bloc. Syntaxe différente des paragraphes. |

## CROSS-LINKS

| Contexte | Skill |
|----------|-------|
| Fichiers .canvas | `json-canvas` |
| Fichiers .base | `obsidian-bases` |
| CLI Obsidian | `obsidian-cli` |
| Intégration vault | MCP `mcp-obsidian` |

## ÉVOLUTION

Après chaque création de note Obsidian :
- Si un callout type manque → l'ajouter à la liste des types courants
- Si un pattern de frontmatter est récurrent → créer un template
- Si une syntaxe Obsidian évolue → mettre à jour les exemples

Seuils : si > 3 erreurs de syntaxe sur les mêmes éléments → ajouter un exemple explicite.
