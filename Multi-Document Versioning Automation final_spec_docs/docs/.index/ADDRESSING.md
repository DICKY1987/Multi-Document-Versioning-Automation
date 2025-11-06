# Addressing Scheme

This repository uses stable URIs to uniquely identify volumes, sections, and paragraphs within the documentation suite.  Edits should reference these addresses in commit messages and pull requests.

* `spec://<VOLUME>/<section_key>#<paragraph_anchor>` points to a specific paragraph within a section.  For example, `spec://ARCH/1.1#p-2` locates the second paragraph of section 1.1 in the Architecture volume.
* `specid://<ULID>` points to an exact ID defined in the suite index.  Use this form when the numeric key may change but the ULID remains stable.

When adding or modifying content, update the sidecar files and the suite index so that these addresses remain accurate.
