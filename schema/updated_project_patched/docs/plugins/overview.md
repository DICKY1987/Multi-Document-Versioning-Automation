# Plugin Ecosystem Documentation (issue 20)

This directory is intended for generated documentation about each
plugin in the ecosystem. For every plugin, the release process
should generate a markdown file under `docs/plugins/<plugin_key>.md`
containing front matter, usage examples, schema references, and
operational health details. A table of all plugins and their
versions should be generated and published as part of the docs
site.

Plugins must ensure that their `README_PLUGIN.md` front matter
includes `derived_from_spec: true` and that examples are kept
current via automated tests. The release pipeline should package
these docs and deploy them to the static site.