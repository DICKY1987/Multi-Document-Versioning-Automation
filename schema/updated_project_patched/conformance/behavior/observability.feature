# Behavior test for observability (issue 12)

Feature: Observability
  All operations must emit structured telemetry with required
  OpenTelemetry attributes. This behavior test describes the
  expected trace spans and attributes that must be present in
  emitted logs during a plugin run.

  Scenario: Operation emits telemetry
    Given a plugin operation "doc.parse_front_matter"
    When the operation completes successfully
    Then a log entry or span MUST include the following attributes:
      | key                 | description                          |
      | plugin_key          | The key of the plugin                |
      | plugin_version      | Version of the plugin                |
      | op_key              | Operation identifier                 |
      | event_id            | ULID/UUIDv7 for this event           |
      | level               | Log level (debug/info/warn/error)    |
      | ts                  | Timestamp (RFC3339 or epoch)         |
    And the log entry MUST be structured (e.g. JSON)