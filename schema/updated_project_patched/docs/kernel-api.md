# Kernel API for Plugin Authors (issue 29)

This document describes the kernel APIs available to plugin
developers. It acts as the authoritative reference for services
exposed by the runtime.

## Overview

The kernel exposes a small set of services via a well‑defined API.
Plugins must only interact with the environment through these
interfaces to ensure compatibility and security.

### Filesystem Service (`fs`)

* `fs.read(path)`: returns the contents of a file relative to the
  repository root. Denied unless the plugin declares `fs.read` in
  its allowed actions.
* `fs.write(path, data)`: writes data to a file. Denied unless
  declared.

### Network Service (`net`)

* `net.http(url, method="GET", headers=None, body=None)`: performs
  an HTTP request. Only hosts declared in `net_allowed_hosts` are
  permitted.

### Ledger Service (`ledger`)

* `ledger.record(event_name, payload)`: emits a ledger event. The
  payload must conform to the ledger contract. Returns an
  `event_id`.

### Config Service (`config`)

* `config.get(key, default=None)`: retrieves configuration
  parameters from the plugin’s configuration.

### Scheduler Service (`scheduler`)

* `scheduler.run_at(timestamp, op_key, payload)`: schedule a future
  execution of an operation.

### Telemetry Service (`telemetry`)

* `telemetry.emit(log_entry)`: emits a structured log entry (see
  observability policy).

For more details, consult the runtime source and the kernel
contract. Plugins must not perform operations outside these
services.