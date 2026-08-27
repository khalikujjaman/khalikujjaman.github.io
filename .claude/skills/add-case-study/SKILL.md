---
name: add-case-study
description: Add or edit a project case study on mohammadkhalikujjaman.com. Use when the user has new engineering project work — a report, test campaign, simulation or thesis chapter — to publish on the portfolio site.
---

# Add a case study to the portfolio site

The site is a single page, `index.html`. Case studies are `<article class="project-card">`
elements inside `<div class="project-grid">` in `<section id="work">`. Adding one is an
edit to that file, not a new page.

## Before writing anything

Ask for, and do not proceed without:

1. The source document (report PDF, test summary, or thesis chapter).
2. One image — test rig photograph, plot, or contour. No stock imagery, no renders of
   equipment that was not used.
3. Whether the work was solo or a team, and if a team, what the user personally did.

## Hard rules

- **Every case study carries a number in the `result-box`.** A measured value, a
  percentage, a count, a tolerance. If the work produced no number, it is not ready to
  publish — say so rather than writing a qualitative summary.
- **Never invent a tool, metric or result.** Only what appears in the source document.
  If the report says OpenFOAM and FLORIS, do not add ANSYS. If a value is a publication
  result rather than the user's own measurement, label it as such in the text.
- **Team work gets a `project-contribution` line.** State the team size and the user's
  own scope, conservatively. Solo work omits the element entirely.
- **British English.** No motivational phrasing, no "passionate about", no adjectives
  doing work that a number should do.
- **The `result-box` states an engineering outcome, including the negative one.**
  A test that failed to qualify a material is a result. Say what the evidence prevented
  as well as what it supported.

## Template

Copy this exactly. `NN` is the zero-padded index, one higher than the current last card.

```html
<article id="project-NN" class="project-card project-N">
  <div class="project-image">
    <img src="/projects/SLUG.webp"
         alt="DESCRIPTION OF WHAT IS ACTUALLY VISIBLE"
         width="1400" height="820" loading="lazy">
    <span class="project-index">0<!-- -->N</span>
  </div>
  <div class="project-body">
    <p class="project-kicker">Team of N - CONTEXT</p>
    <h3>TITLE — under 60 characters, no colon</h3>
    <p class="project-summary">What was done and how, in two sentences. Method first.</p>
    <div class="result-box">
      <span>Engineering outcome</span>
      <p>The result, with its number and its limitation.</p>
    </div>
    <ul class="tag-list" aria-label="TITLE methods and tools">
      <li>METHOD</li><li>TOOL</li><li>DOMAIN</li><li>NUMERIC SPEC</li>
    </ul>
    <p class="project-contribution">Team of N · My contribution: SCOPE.</p>
    <a class="text-link" href="/docs/REPORT-NAME.pdf">Read the report</a>
  </div>
</article>
```

Tag list: three to four items, one of which is numeric (`2.57 GPa contact`,
`65 vessels`, `23 trials`).

## Every addition touches four things

1. The `<article>` in `<div class="project-grid">`.
2. The project nav directly above the grid — add a matching
   `<a href="/#project-NN"><small>NN</small><span>SHORT LABEL</span>…</a>`
   with the same chevron `<svg>` as its siblings.
3. `/docs/REPORT-NAME.pdf` and `/projects/SLUG.webp` placed on disk. Hyphenated,
   lowercase, descriptive filenames — these appear in search results.
4. `sitemap.xml` — update `<lastmod>` on the homepage entry.

## Image handling

Convert to `.webp`, 1400×820, quality 82. Strip EXIF. If the source is a screenshot of a
plot, crop the whitespace first. Alt text describes what is in the frame, not what the
project is about.

## After the edit

Serve locally (`python3 -m http.server` in the site root) and confirm: the new card
renders in the grid, the nav anchor scrolls to it, the PDF link resolves, and no other
card's index shifted. Then report what changed. Do not deploy.
