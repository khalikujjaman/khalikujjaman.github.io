# mohammadkhalikujjaman.com

Personal engineering portfolio. Owner: Mohammad Khalikujjaman, MSc Mechanical
Engineering, Aarhus University, graduating January 2027. The site exists for one
purpose: getting a mechanical R&D / test / validation engineering role in Denmark.

Originally built on ChatGPT Sites (React on Vite, server-rendered). Migrated to a
plain static site. No build step, no framework, no package.json.

## Structure

```
index.html          single page; all sections are anchors
assets/site.css     one stylesheet
projects/*.webp     case-study images, 1400x820
docs/*.pdf          reports and CVs — these URLs are public and linked externally
favicon.svg  social-card.png
sitemap.xml  robots.txt  google*.html   (Search Console verification)
```

## Rules that must not be broken

- **URLs never change.** One page, anchors `#profile #work #research #experience
  #earlier-work #cv #contact`. Every path under `/docs/` and `/projects/` stays exactly
  as it is. These are indexed by Google and linked from job applications. Adding a new
  path is fine; renaming or removing one is not.
- **The `<head>` block is preserved verbatim** on any edit: title, meta description,
  keywords, robots `index, follow`, canonical, Open Graph, Twitter card, and the JSON-LD
  `Person` schema with its `sameAs` array (LinkedIn, ORCID). If a change requires
  touching it, say so first and wait.
- **Never invent a tool, metric, result or credential.** Only what appears in a source
  document the owner has supplied. Publication results are labelled as such and kept
  distinct from the owner's own measurements.
- **British English.** Direct and concrete. No motivational phrasing, no "passionate
  about", no adjective standing in for a number.
- **Engineering leads.** Banking experience (United Commercial Bank, 2022–2025) stays
  one compact entry and is never expanded, never illustrated, and never placed above
  engineering roles.
- **No redesign.** The visual design and semantic class names are settled. Work is
  content, correctness and performance, not appearance.

## House markup

Semantic class names, no utility classes, no inline styles. Existing vocabulary:
`project-card` `project-image` `project-index` `project-body` `project-kicker`
`project-summary` `result-box` `tag-list` `project-contribution` `capability`
`timeline-date` `timeline-place` `research-card` `earlier-item` `text-link`
`button button-primary` `button-ghost`. Reuse these rather than inventing new ones.

Images: `.webp`, 1400x820, quality 82, EXIF stripped, `loading="lazy"`, explicit
`width` and `height`, alt text describing what is visible in the frame.

## Before every deploy

Run `python3 check.py`. It must pass. It verifies every `/docs` and `/projects`
reference resolves on disk, no `<img>` lacks alt text or dimensions, the JSON-LD parses,
and the canonical URL is intact.

Serve locally with `python3 -m http.server 8000` and check the page at 390px width as
well as desktop.

## Adding a case study

Use the `add-case-study` skill in `.claude/skills/`. Do not hand-roll a project card.
