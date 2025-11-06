# CI/CD Gates

1. **L0 Static**: markdownlint, link-check, schema lint.
2. **L1 Contract/Unit**: plugin I/O schemas, manifest validation.
3. **L2 Behavior/BDD**: DDS acceptance (Given/When/Then) in CI.
4. **L3 Integration**: full build with hermetic adapters.
5. **L4 Perf/Soak** (optional): build time, page count budgets.
6. **L5 Security/License**: policy checks for embedded assets.
   **Green → auto-publish; Red → quarantine with actionable report.**
