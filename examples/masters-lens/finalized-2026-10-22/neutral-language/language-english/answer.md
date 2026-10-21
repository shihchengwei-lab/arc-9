- **Do not implement this proposal as written.** An older import can run after a corrected upload and replace the correction with outdated information.
- **A smaller CSV import feature is reasonable.** Support for unplanned formats adds maintenance work. Background processing needs justification from measured waiting times.
- **Resolve correction priority, safe retries, and completion reporting first.** A job number identifies an import; it does not stop that import from overwriting newer data. See the supporting appendix below.

The supporting appendix draws only on the [supplied proposal](C:/Users/kk789/Desktop/masters-lenses/experiments/arc9-final-readme-language-neutral-2026-10-22/inputs/language-english.md). These are reasoned failure scenarios, not results from running software.

**Why the current design fails:** an old import writes phone number `111` and stops before recording completion. A corrected upload then saves `222`. When the old import restarts, it writes `111` again. Both jobs followed the proposed rules, but the correction was lost. The same problem can happen when two imports run together, even without an interruption.

Saving each customer separately creates another recovery problem: some or all customer changes can be saved while the job still appears incomplete. That arrangement can work, but it needs clear reporting and safe repetition. Repeating identical values is harmless when nothing newer has intervened; retries themselves are not the decisive defect.

**A workable smaller design would need these rules:**

| Area | Suggested arrangement and conditions |
|---|---|
| Which upload wins | Agree that later accepted uploads take priority for each email, or choose another explicit rule. Give each upload a permanent order number; retries retain its original number and contents. |
| Protecting corrections | Store the last applied upload order with each customer. The database must check that order and save the customer’s details together, as one indivisible operation. Every import path must follow this rule. Checking only before processing leaves a gap in which another upload can intervene. |
| Completion and retries | Define what users see while work is incomplete, failed, or uncertain. Once a job is completed, retries should return its recorded result. Competing attempts must not change a completed job back to failed. |
| Saving a whole file | Consider one database transaction: a group of changes that either all save or all roll back. Include both customer changes and completion in that group, and prevent duplicate attempts for the same job from proceeding together. This simplifies recovery, provided whole-file acceptance and database waiting times are acceptable. |
| Keeping separate customer saves | This remains an alternative if partial results are intentional. It still needs correction protection, safe repetition, and truthful status until every row has been resolved. Recording progress for each row is not inherently required. |
| Keeping the structure small | Separate reading CSV, managing the import, and updating customers. Defer the component that selects between formats until another format has a real requirement. |
| Choosing background processing | Measure a representative 500-row import during normal system use. Compare its duration and database blocking with acceptable waiting times and request limits. Keep the queue and background worker if those measurements justify them. |

A whole-file transaction, a queue, or a single worker **does not by itself protect corrections**. An older job could still run after a newer one unless the priority rule prevents its writes.

The interruption and concurrency checks behind this recommendation are:

| Scenario | Current proposal or required corrected behavior |
|---|---|
| Old job retries after a correction | Current proposal allows the old values to return. |
| Old and corrected jobs run together | Current proposal allows whichever writes later to win, including the older job. |
| Job stops partway through | Some customer changes remain saved. Recovery must acknowledge and safely handle that partial result. |
| All rows save, but completion does not | The job can appear incomplete and repeat work already done. |
| Identical work repeats without intervening changes | The resulting customer values can remain correct. |
| Newer upload writes before the older one | The proposed database priority rule must reject or skip the older replacement. |
| Older upload writes first | The newer upload must subsequently replace it. |
| Correction arrives between an early check and an old write | The check within the database write must still prevent the overwrite. |
| Whole-file transaction stops before saving | Both customer changes and completion must roll back. |
| Whole-file save succeeds but its response is lost | A retry must find the completed result and return it without rewriting customers. |
| Two attempts process the same job | One must wait, then recheck whether the job already completed. |
| Different jobs compete for database access | Priority protection must remain correct; waits and aborted attempts need handling and measurement. |
| Separate-row processing repeats old rows | Newer corrections must survive, while the job remains incomplete until every row is resolved. |

Before implementation, the product decisions still needed are the precise upload-priority rule, treatment of invalid rows and repeated emails within one file, and what “completed” means when newer uploads have superseded some values. Completion should mean the file has been resolved, not that its values will remain current forever.

Optional additions have narrower purposes:

| Addition | Purpose and when it helps |
|---|---|
| Counts of applied and superseded rows | Explain why an older completed import did not replace newer values, if users need that detail. |
| Per-row progress records | Reduce repeated work if measurements show that repetition is costly. |
| Support for additional formats | Reconsider shared format-handling machinery when a second format is actually scheduled. |

The missing timing evidence affects which simpler implementation to choose. It does not change the finding that the current proposal can undo corrections.