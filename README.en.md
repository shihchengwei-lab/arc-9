![Architecture Review Core 9](docs/images/arc9-hero.png)

# arc-9

[繁體中文](README.md)

A proposal can look workable while leaving gaps in data updates, permissions, or recovery after interruption.

`$arc9` is a manually invoked skill for read-only engineering reviews. It traces actual operations, explains whether a proposal needs changes, and identifies where to change it and why. When a proposal already meets the requirements, it says so.

Its guiding principle is to make illegal states unrepresentable: arrange data and operations so that states forbidden by the requirements cannot be created. Reviews use materials supplied or permitted by the task and do not change code, files, settings, or external state.

## Representative cases

These summaries come from reviews of four CSV import proposals.

| Proposed system | Review finding |
|---|---|
| Small imports get a factory for future formats and a queue; old jobs can overwrite corrections. | Simplify the flow and measure execution time. Confirm which updates should take precedence, then enforce that order during writes. |
| The API checks a path prefix, but the file service interprets the path differently. | Identify the cross-tenant read and derive both source and destination from a trusted tenant identity. |
| Twenty jobs arrive per second while two finish, with a maximum wait of 30 seconds. | A larger queue cannot meet the commitment. Limit acceptance and handle resubmissions and recovery. |
| A simple import flow permits resubmission to overwrite data; transactions and verification records meet the requirements. | Ready to ship, with no changes required before delivery. |

## Get started

1. [Download the ZIP](dist/arc-9.zip), extract it, and place the `arc9` folder in Codex’s skills directory. The default Windows location is `C:\Users\<username>\.codex\skills\`. If `CODEX_HOME` is set, use its `skills` subdirectory.
2. On the next turn, invoke it in the current task discussion:

```text
$arc9 Review this proposal and identify any necessary changes.
```

The response briefly covers the judgment, evidence, and any unknowns or next steps that affect the decision. It follows the request’s language by default; you can specify a different language or length.

You can also provide the path to a downloaded [SKILL.md](dist/skills/arc9/SKILL.md) and ask the model to read and use it.

## Full cases and records

- Four CSV proposals: [Materials and full answers](examples/masters-lens/README.md) · [Execution records](examples/masters-lens/execution.md)
- Updated requirements and resolved issues: [Full answers for six states](examples/masters-lens/contracts/README.md) · [Execution records](examples/masters-lens/contracts/execution.md)
- Language and length: [Three request scenarios](examples/masters-lens/language/README.md) · [Execution records](examples/masters-lens/language/execution.md)

See the [maintenance instructions](MAINTENANCE.md) for prompt sources, packaging checks, and rebuild commands.

## License

This project uses the [MIT License](LICENSE).
