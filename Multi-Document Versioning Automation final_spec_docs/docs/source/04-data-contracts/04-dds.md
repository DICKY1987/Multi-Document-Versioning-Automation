# Deliverable Definition Sheet (DDS)

A DDS defines a deliverable and its acceptance criteria.  Example:

```yaml
id: DEL-DOCS-MGMT
name: "Automated Documentation & Versioning"
purpose: "Docs-as-code pipeline with versioning & proof"
acceptance:
  - id: AC-DOCS-001
    gherkin: |
      Feature: Docs registry
        Scenario: Registry completeness
          Given committed Doc Cards and source files
          When docs.registry.build runs
          Then every Doc Card path exists
          And every active doc appears in registry with current semver
evidence:
  tests: ["tests/behavior/docs_registry.feature::complete_registry"]
  reports: ["reports/docs-validate.xml"]
```

DDS files live under `/plan/deliverables/` and link PBS, tests, and evidence.
