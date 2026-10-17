# masters-lenses

[繁體中文](README.md)

`$masters-lens` is a manually invoked skill for read-only engineering reviews. It uses materials supplied or permitted by the task, works backward from delivery requirements, and traces concrete operations to their causes. Its guiding principle is to make illegal states unrepresentable. It provides an overall judgment, supporting evidence, and necessary changes.

## Cases

These four CSV import proposals cover process structure, tenant isolation, admission capacity, and delivery requirements.

| Proposed system | Review response |
|---|---|
| CSV imports run about twice a week, with at most 500 rows each. The proposal adds a factory for future formats and a queue; an old job can overwrite corrected data. | Do not implement as proposed. Keep CSV parsing, an import service, and the database. Bind each job to fixed content and commit customer updates with completion status in one transaction. Define what “newer” means; if acceptance order determines it, allocate sequence numbers in the database and enforce updates atomically. Measure before choosing background execution. |
| Tenants may import only their own files. The API accepts a path string, which the file service later normalizes. | Trace a path traversal that lets the worker read another tenant’s file, import it into the caller’s tenant, and expose it through queries. Remove caller-selected paths and derive the source from a trusted tenant identity and a fixed filename. |
| Twenty jobs arrive per second while two finish. Accepted jobs may wait at most 30 seconds. The proposal only enlarges the queue. | Reject queue expansion alone. Reserve capacity atomically at admission and reject excess work. Persist the job and pending message in one transaction, with a sender responsible for recovery. Track the original job and use idempotent retries. Jobs must start or explicitly fail within 30 seconds. |
| A single CSV flow already implements versioning, transactions, retries, and capacity control. The supplied validation records satisfy the requirements. | Support delivery within the stated scope, citing input validation, fixed content and versions, database locking and atomic updates, transactional results and recovery, and existing measurements. No substantive new issue is identified. |

[Full case materials and answers](examples/masters-lens/README.md).

## Usage

A shared contract defines inputs, outputs, evidence, and how judgments apply to candidate designs. Named scenarios anchored by nine experts provide observation methods selected for the current problem. When a candidate changes, recheck the operations and judgments that depend on the changed parts. See [SKILL.md](dist/skills/masters-lens/SKILL.md) for the full methods.

After installation, invoke it in the current task discussion:

```text
$masters-lens Review this proposal and identify any necessary changes.
```

An explicitly requested output language takes precedence. Otherwise, the response follows the main language and writing form of the current user request. Default length is 250–400 body characters for Chinese or 150–250 words for English, in at most three bullet points. The response covers the judgment, evidence, and any unknowns or next steps that affect the decision, without greetings or an opening preamble. The current task may specify different output requirements. Counting rules and optional fields are defined in the [shared skill contract](dist/skills/masters-lens/SKILL.md).

[Full answers and execution records for Chinese requests, English requests, and an explicit language override](examples/masters-lens/language/README.md).

## Installation

[Download the ZIP](dist/masters-lenses.zip), extract it, and place the `masters-lens` folder in Codex’s skills directory. The default Windows location is `C:\Users\<username>\.codex\skills\`. If `CODEX_HOME` is set, use its `skills` subdirectory. Invoke `$masters-lens` on the next turn.

You can also provide the path to [SKILL.md](dist/skills/masters-lens/SKILL.md) and ask the model to read and use it.

## Validation and maintenance

Packaging checks verify consistency among the source, generated files, ZIP, license, and manual invocation policy. See the [maintenance instructions](MAINTENANCE.md) for the source and rebuild commands.

## License

This project uses the [MIT License](LICENSE).
