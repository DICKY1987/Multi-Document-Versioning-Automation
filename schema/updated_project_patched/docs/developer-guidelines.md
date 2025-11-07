# Developer Guidelines (issue 35)

These guidelines help ensure consistency across contributions to
the modular plugin ecosystem. Adhering to these practices will
improve quality, maintainability, and readability.

## Coding Standards

* Follow PEP 8 for Python and StandardJS for JavaScript/TypeScript.
* Use descriptive names for variables, functions, and files.
* Keep functions small and focused; avoid deep nesting.
* Document public functions and classes using docstrings.

## Workflow

* Start from the appropriate plugin template under `five Modular
  Plugin Templates.txt` and `Common scaffold & deliverables (for every
  template).txt`.
* Write or update unit tests alongside your code. Tests live in
  `tests/` and follow the naming convention `test_<op>.py`.
* Run `pytest` and `nox -s schema` before opening a pull request.
* Create a feature branch for your work and open a pull request
  targeting `main`. Tag the appropriate teams in `CODEOWNERS`.

## Documentation

* Update relevant README files and examples when you change
  operation contracts or behavior.
* All new operations must include input/output schemas, examples,
  and a test skeleton.
* Use the migration template when introducing breaking changes.

## Review Process

* At least two approvals are required for merging into `main`.
* Reviewers must check that the contributor followed these
  guidelines, that tests pass, and that documentation is up to date.

## Tooling

* Use `nox` sessions for running tests and schema validations.
* Use `scripts/generate_plugin_files.py` to generate derived
  artifacts from plugin specs.
* Use `scripts/validate_readme.py` to ensure documentation examples
  conform to schemas.