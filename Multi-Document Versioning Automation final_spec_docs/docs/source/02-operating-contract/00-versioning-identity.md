# Versioning & Identity

* **ULID** is minted at first creation and never changes. Renames create aliases; keys are **never reused**.
* **SemVer** applies to the **doc content**. CI enforces bump on meaningful changes; ledger records events.
* **One-artifact rule** (optional): PR must touch only one Doc Card or source doc per change set for clarity.
