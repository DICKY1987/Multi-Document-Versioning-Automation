# Plugin Contract

The global plugin contract (plugin.contract.v1) defines required manifest fields:

```yaml
apiVersion: plugin.contract.v1
key: PLG_DOCS_VALIDATE
version: 0.3.0
contract: ">=1.0 <2.0"
capabilities: ["validate"]
config_schema: "schemas/validate.config.schema.json"
inputs:
  - name: source_map
    schema: "schemas/docs.scan.out.schema.json"
outputs:
  - name: report
    schema: "schemas/validate.report.schema.json"
conformance:
  tests:
    - "tests/unit/test_validate.py"
    - "tests/behavior/docs_registry.feature::validation"
```

(Contracts + compatibility ranges + conformance kit.)
