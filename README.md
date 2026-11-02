# H5P Advanced Blanks

> **Lingonex version.** This is Lingonex's own copy of
> [sr258/h5p-advanced-blanks](https://github.com/sr258/h5p-advanced-blanks) (MIT, by
> S. Rettig), kept with its full history; the original is the `upstream` remote.
>
> | | Upstream | Lingonex |
> |---|---|---|
> | Version | 1.1.0 | **1.1.2** |
> | "Case sensitive" default | off | **on** |
> | "Auto-check" default | off | **on** |
> | Text field while typing | fixed width, text scrolls | **grows with the text** (1.1.2) |
>
> German exercises are case-sensitive (nouns), and the exercise is meant to be checked
> blank by blank. Existing content keeps the settings it was saved with; the defaults
> apply to new content. A field starts as wide as the longest correct answer rounded up
> to the next 10 characters (upstream behaviour) and, from 1.1.2, widens as the student
> types past that, so they always see what they wrote. Site CSS must not cap its width
> at a fixed size (`max-width: 100%` keeps it inside its row).
>
> **Installed:** 1.1.1 on academy.lingonex.de and, since 2026-10-27, lingonex.de,
> byte-identical to `releases/H5P.AdvancedBlanks-1.1.1.h5p`. 1.1.2 is built
> (`releases/H5P.AdvancedBlanks-1.1.2.h5p`) and not installed yet. Each package also
> carries **H5P.Question 1.4.8**, which this library needs in exactly version 1.4 and
> which a fresh site does not have (lingonex.de only had 1.5). Install through
> *H5P Content → Libraries → Upload Libraries*.
>
> **Releasing:** `dist/` is a build output and not committed (see `.gitignore`).
> Webpack 4 needs the old OpenSSL provider on current Node, and the `cp` in the build
> script needs a POSIX shell, so on Windows PowerShell:
> `$env:NODE_OPTIONS = '--openssl-legacy-provider'; npm run build:prod` (the `cp` step
> only refreshes `dist/ractive.min.js`, which does not change). Then bump
> `patchVersion` in `library.json` and run
> `python -I tools/make-release.py releases/<previous>.h5p`.

This is an advanced 'Fill the blanks' content type for h5p. In addition to most of the features of the regular 'Fill the blanks' content type it supports:

* The content creator can specify a feedback text message that should be displayed to the users when they enter a certain incorrect answer.
* The content creator can specify parts of the text that should be highlighted when the users enter a certain incorrect answer. ("signal words")
* The content creator can use text snippets to avoid retyping the same feedback message over and over.
* User are given more detailed feedback when they make spelling mistake.

It's main use is for foreign language learning, where you can give the users individual hints, why certain tenses or word forms can't be used in this case. While it is possible to have a 'Check' button at the end, it makes more sense to use the auto-check setting as the user is guided through the 'fill the blanks' exercise blank by blank.

## Architecture

This content type uses parts of h5p-blanks but is not based on it, as it was ported over from a widget written by the author for LearningApps.org. It uses a MVC style architecture with Ractive as the library responsible for creating the views. It is written in TypeScript.

## Getting started

Grab all the modules:

```bash
npm install
```

Build project with debug info:

```bash
npm run build
```

Build project in production mode:
```bash
npm run build:prod
```

Copy all relevant files to ``dist`` directory
```bash
npm run dist
```