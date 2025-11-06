# Plugin Manifest Shape

A plugin manifest describes the contract between the kernel and the plugin.  The global plugin contract (`plugin.contract.v1`) defines the following fields:

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

The `contract` field specifies the compatibility range that a plugin supports.  The `conformance.tests` list points to the contract, behavior, or performance tests that must pass for the plugin to be considered compatible.
