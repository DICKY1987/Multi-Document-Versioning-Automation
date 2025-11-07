# Plugin Lifecycle Management (issue 24)

This document extends the plugin lifecycle policy to include runtime
mechanics. It defines how plugins are discovered, initialized,
activated/deactivated, and gracefully shut down. It also covers
state persistence and hot reloads.

## Discovery

Plugins are discovered by scanning the `plugins/` directory for
`plugin.spec.json` files. The key from the spec becomes the plugin
identifier. The `generate_plugin_files.py` script generates
`manifest.json` files consumed by the kernel.

## Initialization Order

Plugins declare dependencies via a hypothetical `depends_on` field
in their manifest. The kernel topologically sorts plugins and
initializes them in dependency order. Circular dependencies are
rejected at load time.

## Activation & Deactivation

Plugins may be enabled or disabled via feature flags. A disabled
plugin will not register its operations with the kernel. Runtime
config changes trigger reloading of the plugin; the kernel calls
the plugin's `deactivate()` method, then `activate()` to reapply
configuration. Handlers should be written to tolerate activation
and deactivation idempotently.

## State Persistence

Plugins should avoid global mutable state. When needed, state must
be scoped to a run context and persisted via the kernel API
(e.g., using provided storage services) rather than in-memory
variables. This makes hot-reload and scaling safe.

## Hot Reload

During development, plugins may support hot reload triggered by
file change detection. The kernel reinitializes the plugin using
the activation protocol described above. Plugins should guard
long‑running tasks and timers so they do not leak across reloads.