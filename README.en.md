![Architecture Review Core 9](docs/images/arc9-hero.png)

# arc-9

[繁體中文](README.md)

`$arc9` is a manually invoked skill for read-only engineering reviews. It traces an operation from input to result, explains whether a proposal needs changes, and identifies where to change it and why.

Its guiding principle is to make illegal states unrepresentable. It prioritizes changes to data and operations that prevent states forbidden by the requirements. Reviews use materials supplied or permitted by the task and do not change code, files, settings, or external state.

## Cases

These are summaries of reviews of four CSV import proposals.

| Proposed system | Review judgment and recommendations |
|---|---|
| CSV imports run about twice a week, with at most 500 rows each. The proposal adds a factory for future formats and a queue; an old job can overwrite corrected data. | Do not implement as proposed. Keep CSV parsing, an import service, and the database. Bind each job to fixed content and commit customer updates with completion status in one transaction. Define “newer” first. If acceptance order determines it, allocate sequence numbers in the database and allow only newer jobs to update customer data at the write boundary. Measure execution time before choosing background processing. |
| Tenants may import only their own files. The API checks the path string’s prefix, while the file service normalizes the path before opening it. | `/tenants/A/../B/customers.csv` passes A’s prefix check but opens B’s file. The worker then imports B’s data into A, where A can query it. Remove caller-selected paths and derive the source from a trusted tenant identity and a fixed filename. |
| Twenty jobs arrive per second while two finish. Accepted jobs may wait at most 30 seconds. The proposal only enlarges the queue. | A larger queue cannot meet the waiting limit. Check and reserve capacity atomically at admission, and reject excess work. Save the job and pending message in one database transaction, then have a recovery sender deliver the message to the queue. The frontend tracks the original job, and retries return that same job. Accepted jobs must start or explicitly fail within 30 seconds. |
| A five-person internal tool imports CSV files in a single transaction. Resubmission applies the file again, including an older file overwriting corrections. | Supports delivery. Validation precedes writes; a failed transaction rolls back the batch, and the unique constraint preserves customer uniqueness. Resubmission and conflicting writes follow the accepted behavior. The supplied timing, memory, and overload-rejection records also meet this release's requirements. |

[Full case materials and answers](examples/masters-lens/README.md).

## Usage

The model selects methods for the current problem: following a record through processing, examining what happens after an interruption and retry, comparing how different layers interpret the same input, or checking execution time and resource use. These methods appear as scenarios named after nine engineers in [SKILL.md](dist/skills/arc9/SKILL.md).

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
