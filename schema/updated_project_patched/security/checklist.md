# Security Checklist (issue 17)

Use this checklist when reviewing a plugin for release. All items
must be addressed before merging to main:

1. **SBOM:** Ensure SBOMs are generated and signed; verify no
   critical or high vulnerabilities exceed budgets.
2. **Secrets:** Confirm no secrets or credentials are present in
   code or configuration files.
3. **Policies:** Validate retention, redaction, and slsa policies
   are referenced and up to date.
4. **Threat Model:** Review the threat model for updates and
   document any changes.
5. **Tests:** Ensure state‑change safety tests and observability
   conformance tests pass in CI.
6. **Permissions:** Review plugin manifest for appropriate
   permissions and actions; deny by default must be true.
7. **Migration:** For breaking changes or deprecation, verify
   migration guides and announcements are prepared.