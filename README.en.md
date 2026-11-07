![Architecture Review Core 9](docs/images/arc9-hero.png)

# arc-9

[繁體中文](README.md)

A proposal can look workable while allowing old data to overwrite corrections, exposing someone else’s files, or failing when interrupted work is retried.

`$arc9` is a review tool you invoke manually in Codex. It traces data and operations, explains whether a proposal meets its requirements, and identifies what needs to change and why. When the proposal already meets the requirements, it says so.

Reviews look for changes to data, permissions and operations that prevent the failure from occurring. They only read materials you supply or permit, without changing code, files, settings or other systems.

## Representative cases

See the [full inputs and answers](examples/csv-import/README.md) for the four CSV import cases.

| Proposed system | What the review found |
|---|---|
| A small import adds support for more formats and a queue. Retrying an old job can overwrite a later correction. | Decide which update takes precedence and keep data writes consistent with the completion record. Use measurements to decide whether background processing is needed. |
| The system checks an authorized directory, but opening the file can reach someone else’s directory. | Use the signed-in tenant to determine which file to open, and handle pending jobs that still carry the old paths. |
| Twenty jobs arrive per second while two finish, with a maximum wait of 30 seconds. | Limit intake to available processing capacity. Acknowledge acceptance only when the system can reliably take responsibility for the job. |
| The requirements allow resubmissions to overwrite data and require 1–500 rows per CSV file. | The overwrite policy is acceptable. Delivery remains unconfirmed because the evidence does not show rejection of files with 0 or 501 rows. |

## Get started

Use a Codex environment that supports independent reviewers (sub-agents).

1. [Download the ZIP](dist/arc-9.zip), extract it, and place the `arc9` folder in Codex’s skills directory. The default Windows location is `C:\Users\<username>\.codex\skills\`. If you set a different Codex data directory with `CODEX_HOME`, use its `skills` subdirectory.
2. On the next turn, invoke it in the current task discussion:

```text
$arc9 Review this proposal and identify any necessary changes.
```

The response explains the verdict, reasons and next steps, separating required fixes from questions that need verification. It follows the request’s language by default. You can specify a language or length.

You can also provide the full path to [SKILL.md](dist/skills/arc9/SKILL.md) and ask the model to read and use it. Keep the complete `arc9` folder, including `references`.

See the [maintenance instructions](MAINTENANCE.md) for rebuild and test commands.

## License

This project uses the [MIT License](LICENSE).
