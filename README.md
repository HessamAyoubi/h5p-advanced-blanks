# H5P Advanced Blanks

> **Lingonex version.** This is Lingonex's own copy of
> [sr258/h5p-advanced-blanks](https://github.com/sr258/h5p-advanced-blanks) (MIT, by
> S. Rettig), kept with its full history; the original is the `upstream` remote.
>
> | | Upstream | Lingonex |
> |---|---|---|
> | Version | 1.1.0 | **1.1.1** |
> | "Case sensitive" default | off | **on** |
> | "Auto-check" default | off | **on** |
>
> Only the defaults differ: German exercises are case-sensitive (nouns), and the
> exercise is meant to be checked blank by blank. Existing content keeps whatever it
> was saved with; the defaults apply to new content.
>
> **Installed on** academy.lingonex.de and, since 2026-10-27, lingonex.de: both
> `H5P.AdvancedBlanks` 1.1.1, byte-identical to `releases/H5P.AdvancedBlanks-1.1.1.h5p`.
> That package also carries **H5P.Question 1.4.8**, which this library needs in exactly
> version 1.4 and which a fresh site does not have (lingonex.de only had 1.5). Install it
> through *H5P Content → Libraries → Upload Libraries*.
>
> `dist/` is a build output and not committed (see `.gitignore`): rebuild with
> `npm ci` and `npm run build:prod`. The release package holds the `dist/` that is live.

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