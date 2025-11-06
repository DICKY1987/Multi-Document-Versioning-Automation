# Implementation Notes

* Prefer **hexagonal** internals in each plugin for testability.  Modularity and separation (acquisition/transform/validation/orchestration) keeps the code deterministic and maintainable.
* Use **PBS→DDS→File‑Map→RTM** templates under `/plan` to keep deliverables first and verification executable.
