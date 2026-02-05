#### Empirical

# Test Impact Analyzer

Test Impact Analyzer is a tool that identifies **which Playwright tests are impacted**
by a specific Git commit in the `flash-tests` repository.

It helps developers, reviewers, and CI systems quickly understand the scope of a change
without running or reviewing the entire test suite.

---

## What Is an Impacted Test?

A test is considered impacted if:

- **Added** – a new test appears in the commit
- **Removed** – a test is deleted in the commit
- **Modified** – an existing test’s code changes

Tests are identified using Playwright syntax:

## Technologies used
- FastAPI
- Node.js
- Git
- Conda
- Uvicorn

## Running the CLI
node cli/index.js --commit 45433fd --repo /path/to/flash-tests
