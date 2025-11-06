# CLI Surface

Commands are implemented as plugins and follow a common JSON I/O envelope (`{ ok, artifacts, messages, errors }`). All commands support `--dry-run` and `--out <path>`.

Available commands:

* `id mint --key <doc_key> --owner <team> [--doc-type <type>]`
* `id rekey --ulid <ulid> --new-key <key>`
* `id deprecate --ulid <ulid> --reason "<text>" --date YYYY-MM-DD`
* `id consolidate --target <ulid> --sources <ulid,ulid,...>`
* `id mfid.update --ulid <ulid> --algo blake3|sha256 [--normalize on|off]`
* `id registry.build [--roots docs/,plans/]`
* `id ledger.append --type <EVENT> --ulid <ulid> --data <json>`
* `id validate card --path <card.yaml>`
* `docs migrate --roots docs/,plans/ --owner <team> --key-strategy <slug|map:file> [--commit]`
