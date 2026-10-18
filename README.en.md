![Architecture Review Core 9](docs/images/arc9-hero.png)

# arc-9

[繁體中文](README.md)

`$arc9` is a manually invoked skill for read-only engineering reviews. It traces an operation from input to result, explains whether a proposal needs changes, and identifies where to change it and why.

Its guiding principle is to make illegal states unrepresentable. It prioritizes changes to data and operations that prevent states forbidden by the requirements. Reviews use materials supplied or permitted by the task and do not change code, files, settings, or external state.

## Cases

These are summaries of reviews of four CSV import proposals.

| Proposed system | Review judgment and recommendations |
|---|---|
| CSV imports run about twice a week, with at most 500 rows each. The proposal adds a factory for future formats and a queue; an old job can overwrite corrected data. | Do not implement as proposed. Keep CSV parsing, an import service, and the database; measure execution time before choosing background processing. First confirm whether later acceptance should take precedence. If so, assign sequence numbers at acceptance, keep the CSV input fixed, and reject older sequence numbers atomically during writes. Commit the batch and completion status together; retries use the original job and input. |
| Tenants may import only their own files. The API checks the path string’s prefix, while the file service normalizes the path before opening it. | `/tenants/A/../B/customers.csv` passes A’s prefix check but opens B’s file. The worker then imports B’s data into A, where A can query it. Remove caller-selected paths, derive the fixed source path from a trusted tenant identity, and use that same source to determine the destination tenant. |
| Twenty jobs arrive per second while two finish. Accepted jobs may wait at most 30 seconds. The proposal only enlarges the queue. | Cannot ship as proposed. A larger queue adds no processing capacity, and frontend resubmissions amplify the load. Reject work the service cannot handle; when accepting it, atomically save the job and the information needed to resume delivery, for example, with a transactional outbox. Track the original job and deduplicate resubmissions. Accepted jobs must start or explicitly fail by the deadline; verify the one-second response and 30-second waiting requirements. |
| A five-person internal tool imports CSV files in a single transaction. Resubmission applies the file again, including an older file overwriting corrections. | Ready to ship. Writes use fixed parsed data after validation; the batch transaction and unique constraint maintain data integrity. Resubmission and conflicting-write order follow the accepted requirements. Failure and an unconfirmed outcome have explicit representations. The supplied timing, memory, and overload-rejection records meet this release's budget. |

[Full case materials and answers](examples/masters-lens/README.md).

## Usage

The model selects methods for the current problem: tracing how data is processed, which other jobs a stalled operation holds up, whether data changes after validation, and what an interruption and retry leave behind. It also compares how different layers interpret the same input and checks execution time and resource use. These methods appear as scenarios named after nine engineers in [SKILL.md](dist/skills/arc9/SKILL.md).

When the proposal changes, it rechecks the affected steps against the original requirements.

After installation, invoke it in the current task discussion:

```text
$arc9 Review this proposal and identify any necessary changes.
```

An explicitly requested output language takes precedence. Otherwise, the response follows the main language and writing form of the current user request. Default length is 250–400 body characters for Chinese or 150–250 words for English, in at most three bullet points. The response covers the judgment, evidence, and any unknowns or next steps that affect the decision, without greetings or an opening preamble. The current task may specify different output requirements. Counting rules and optional fields are defined in the [shared skill contract](dist/skills/arc9/SKILL.md).

[Full answers and execution records for Chinese requests, English requests, and an explicit language override](examples/masters-lens/language/README.md).

## Installation

[Download the ZIP](dist/arc-9.zip), extract it, and place the `arc9` folder in Codex’s skills directory. The default Windows location is `C:\Users\<username>\.codex\skills\`. If `CODEX_HOME` is set, use its `skills` subdirectory. Invoke `$arc9` on the next turn.

You can also provide the path to [SKILL.md](dist/skills/arc9/SKILL.md) and ask the model to read and use it.

## Validation and maintenance

Packaging checks confirm that the generated SKILL.md contains the full prompt, the ZIP matches the generated directory, and the package includes the MIT license and manual invocation setting. See the [maintenance instructions](MAINTENANCE.md) for the source and rebuild commands.

## License

This project uses the [MIT License](LICENSE).
