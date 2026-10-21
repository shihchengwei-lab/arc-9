- **Do not implement the proposal as written.** The CSV import feature is worth building, but an older import can restart and overwrite corrected customer details. That directly breaks a stated product requirement.
- **Fix update priority and recovery first.** Define which upload takes precedence, enforce that rule whenever customer data is saved, and explain how interrupted imports reach a reliable, visible outcome.
- **Start with fewer components.** Only CSV is currently needed. Future JSON/Excel support has no stated justification; the queue and background worker need evidence that their added complexity is worthwhile. The current workload alone does not establish whether direct processing would be fast enough.

**Appendix: evidence, necessary changes, and limits**

The review uses only the [supplied proposal](C:/Users/kk789/Desktop/masters-lenses/experiments/arc9-final-readme-2026-10-22/inputs/language-english.md) and the specified skill folder. These are findings from the design, **not results from running software**.

| Check | Finding and implication |
|---|---|
| An older import restarts after a correction | Import A stops; corrected import B saves a new phone number; A restarts and restores the old number. The proposal permits this sequence. A unique email identifies the customer, and `job_id` identifies the import; neither identifies which data should win. |
| Two imports update the same customer | Their writes can interleave. The system needs an explicit priority rule that applies during every update, including retries. |
| Customer updates finish before the completion marker is saved | An interruption leaves the data written but the import not marked complete. Recovery is unspecified. This does **not** establish that completion is reported prematurely or that the import will remain stuck permanently. |
| A completed import is delivered again | Handling is unspecified. A repeat must not restore values superseded by a newer correction. Retrying an import should reuse its original contents; uploading corrections should create a new import. |
| Processing through the existing backend | No timing measurements or acceptable waiting time were supplied. Test representative files of up to 500 rows before choosing this approach. |

**One possible priority rule:** if later accepted uploads should take precedence, assign each import an increasing number and remember the last accepted number for each customer. The database must check the number and save the update together, rejecting older updates. This recommendation depends on accepting upload order as the meaning of “newer.”

Another option is strict processing in upload order, with recovery rules preventing older imports from being reapplied after newer ones. Merely running one import at a time is insufficient.

**Completion needs a clear meaning.** Define how interrupted imports recover and whether “completed” includes rows skipped because a newer correction already superseded them. Optionally, show the number skipped and the reason; that does not require live progress for every row.

Saving all customer changes and the completion marker in one database operation—where everything succeeds or everything is rolled back—could simplify recovery. It is optional, depends on acceptable database performance, and does not by itself prevent an older import from overwriting a newer correction.

The proposal already describes customer matching, import identifiers, a completion marker, and a CSV processing path. Those provide useful foundations, but no implementation or tests were supplied. Keep responsibility for checking CSV contents and saving customers clear; postpone the format-selection factory until another format is actually needed.