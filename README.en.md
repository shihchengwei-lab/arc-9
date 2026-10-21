![Architecture Review Core 9](docs/images/arc9-hero.png)

# arc-9

[繁體中文](README.md)

A proposal can look workable while allowing old data to overwrite corrections, exposing someone else’s files, or failing when interrupted work is retried.

`$arc9` is a review tool you invoke manually in Codex. It traces data and operations, explains whether a proposal meets its requirements, and identifies what needs to change and why. When the proposal already meets the requirements, it says so.

Reviews look for changes to data, permissions and operations that prevent the failure from occurring. They only read materials you supply or permit, without changing code, files, settings or other systems.

## Results, cost and limitations

- **Results:** In the ten review scenarios tested on 2026-10-22, arc9 correctly judged whether each proposal met its specified requirements, including after requirements changed or defects were fixed.
- **Cost:** The median complete review took about 3 minutes 40 seconds. Median combined usage of the assistant and independent reviewer was about 239,000 tokens. Tokens measure text processed by a model; this count includes repeated and cached content.
- **Known limitations:** In one case, it treated an optional wording change as required, adding unnecessary work to the recommendation. In another, it repeated information about the review process, making the answer longer.

The [verification report](tests/reports/arc9-finalized-2026-10-22.md) contains individual results, model settings and usage calculations. The [language test report](tests/reports/arc9-language-neutral-2026-10-22.md) records Chinese requests, English requests and an explicit request for Traditional Chinese.

## Representative cases

These summaries come from this round’s reviews of four CSV import proposals. [Complete inputs and answers](examples/masters-lens/finalized-2026-10-22/README.md)

| Proposed system | What the review found |
|---|---|
| Small imports get support for unneeded formats and a queue; old jobs can overwrite later corrections. | Trace how old data can replace a correction. Decide which update takes precedence, then use measured execution time to decide whether a queue is needed. |
| The system checks an authorized directory, but opening the file can reach someone else’s directory. | Derive the permitted data scope from the signed-in identity and enforce that same scope when opening files. |
| Twenty jobs arrive per second while two finish, with a maximum wait of 30 seconds. | A larger queue cannot meet the commitment. Limit acceptance and handle resubmissions and interrupted work. |
| The requirements accept resubmissions overwriting data, and data updates and load verification meet those requirements. | Ready to ship, with no additional changes required. |

## Get started

The host must be able to start an independent AI reviewer, called a sub-agent. It examines the proposal, and the assistant in your conversation then edits the review into a summary and appendix.

1. [Download the ZIP](dist/arc-9.zip), extract it, and place the `arc9` folder in Codex’s skills directory. The default Windows location is `C:\Users\<username>\.codex\skills\`. If you set a different Codex data directory with `CODEX_HOME`, use its `skills` subdirectory.
2. On the next turn, invoke it in the current task discussion:

```text
$arc9 Review this proposal and identify any necessary changes.
```

The body gives the judgment, reasons and necessary changes. Detailed analysis and optional improvements go in the appendix. Responses follow the request’s language by default; you can specify another language or length.

You can also provide the full path to [SKILL.md](dist/skills/arc9/SKILL.md) and ask the model to read and use it. Keep the complete `arc9` folder, including `references`.

See the [maintenance instructions](MAINTENANCE.md) for prompt sources, packaging checks and rebuild commands.

## License

This project uses the [MIT License](LICENSE).
