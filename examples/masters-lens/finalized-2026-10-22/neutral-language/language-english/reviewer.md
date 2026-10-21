```yaml
output:
  context:
    task: >
      Assess whether the CSV import proposal is worth implementing as proposed.
      Explain the assessment in English for a reader with no software engineering background.
    purpose: Review summary.
    authorization: Read-only assessment; no implementation.
    accepted_constraints:
      - Read only the task file and the arc9 skill folder.
      - No network access or file changes.
      - No additional accepted adjustments.
    materials_read:
      - inputs/language-english.md
      - variants/B/SKILL.md
      - variants/B/references/review.md
    evidence:
      F1: >
        Five people use the internal tool. Imports occur about twice weekly,
        with no more than 500 rows each.
      F2: >
        CSV is the only current format. No other format is scheduled.
      F3: >
        There is one backend and one relational database. Email uniquely
        identifies a customer; matching imports update name and phone.
      F4: >
        Proposed flow: ImportController → ImportService →
        ImportStrategyFactory → CsvImportStrategy → CustomerRepository,
        plus a message queue and background worker.
      F5: >
        Each import has a job_id. The worker commits each customer separately,
        then records completed in a separate write. Interruption causes
        redelivery of the entire job. Corrected uploads are allowed, different
        jobs may run concurrently, and there are no per-row progress records
        or data version fields.
      F6: >
        Users must be able to see completion, retry after failure, and have
        corrected customer information protected from older jobs.

  result:
    task_answer:
      overall_judgment: >
        Do not implement the proposal as written. It can let an older import
        overwrite a correction, including when the older import is retried.
        A smaller CSV import feature is a reasonable direction, provided its
        rules for corrections, retries, and completion are made reliable first.
        The stated workload does not establish a need for the proposed
        future-format factory or background-processing infrastructure.

      key_evidence_and_applicability:
        - judgment: The proposal does not protect corrected customer information.
          basis: F3, F5, F6.
          explanation: >
            An old import can stop, a corrected upload can update a customer,
            and the old import can then restart and write its old values over
            the correction. Two concurrently running imports can produce the
            same result without any interruption.
          scope: >
            Applies when jobs contain the same email and an older job writes
            after the correction. Independent customers are unaffected by this
            particular conflict.

        - judgment: A job_id alone does not prevent that overwrite.
          basis: F5.
          explanation: >
            The supplied design gives the job an identity, but specifies no
            rule at the customer write that rejects an older job. Recognizing
            the job and deciding whether its data may replace current data
            are different responsibilities.

        - judgment: The separate completion write creates a recovery boundary.
          basis: F5.
          explanation: >
            A worker can stop after some customer writes, or after every
            customer write but before recording completion. The retry then
            repeats earlier work. These states need truthful reporting and
            safe recovery.
          qualification: >
            Separate commits do not by themselves prove a product violation.
            Repeating assignments of the same values can be harmless if
            nothing newer has intervened. The definite violation is the
            permitted overwrite of newer corrections.

        - judgment: The extra format-selection machinery lacks a current justification.
          basis: F2, F4.
          explanation: >
            There is only one format and no scheduled second format. The
            proposal adds places to follow and maintain before it provides
            a demonstrated benefit.
          qualification: >
            Separating CSV parsing from customer-update rules can still be
            useful. Removing the factory does not require putting everything
            into one large function.

        - judgment: Background processing remains a conditional choice.
          basis: F1, F4.
          explanation: >
            A queue introduces another handoff, duplicate deliveries, job
            status management, and recovery work. Small, infrequent uploads
            make a direct approach worth checking first.
          qualification: >
            Row count and weekly frequency do not establish execution time.
            No timing measurements or response-time limits were supplied,
            so this review cannot guarantee that processing during the
            original request will be fast enough.

      task_gaps:
        G1:
          condition: >
            Older work must not overwrite corrected customer information,
            including during retries and concurrent imports.
          status: Unmet.
          basis: F3, F5, F6.
          impact: >
            Users can successfully correct a customer and later see the
            wrong information return.

        G2:
          condition: >
            Completion and failure reporting must remain meaningful after
            interruptions and retries.
          status: Partly specified; recovery behavior needs confirmation.
          basis: F5, F6.
          unknown: >
            The material specifies completed and whole-job redelivery, but
            does not define what the user sees during partial processing,
            an uncertain outcome, or a failed attempt.
          impact: >
            This prevents a complete assessment of the failure experience.
            It does not weaken the definite rejection based on G1.

        G3:
          condition: >
            The chosen execution method must fit the acceptable waiting
            time and the existing system's operating limits.
          status: Pending evidence.
          basis: F1, F4.
          unknown: >
            Actual import duration, acceptable waiting time, request limits,
            and database locking costs.
          impact: >
            Determines whether direct processing is sufficient or background
            processing is justified. It does not change the need to fix G1.

        G4:
          condition: >
            The implementation needs an unambiguous rule for which upload
            is newer and how overlapping input is treated.
          status: Pending product decision.
          basis: F3, F5, F6.
          unknown: >
            The exact precedence rule, treatment of duplicate emails within
            one file, and handling of invalid rows are not specified.
          impact: >
            These decisions affect concrete implementation and completion
            wording. The current design is unsafe under the ordinary
            interpretation that a later correction should prevail.

      necessary_arrangements:
        A1:
          source_condition: G1.
          arrangement: >
            Give each accepted upload a fixed order value, assigned and
            recorded by the database. Reuse that value on every retry.
            A corrected upload receives a newer value. Store the order of
            the last applied import with each customer, and make the
            database change the customer's values only when the incoming
            upload is permitted by that order.
          responsibility:
            upload_registration: >
              Establish the immutable upload identity, contents, and order.
            customer_database_write: >
              Compare the incoming order with the stored order and update
              the values and order together in one indivisible operation.
          why_it_addresses_the_cause: >
            An old processor can still run, but its database write cannot
            replace a customer already updated by a newer correction.
          premises:
            - >
              Product accepts database-assigned upload order as the precedence
              rule. If another rule is required, encode that rule instead.
            - Retries use the original upload contents and original order.
            - Every import path obeys the same database write rule.
            - >
              The database supports the required atomic comparison and update.
          alternatives: >
            Strictly finishing or permanently superseding all older work
            before allowing newer work is another possible arrangement.
            It must also prevent delayed or resumed older processors from
            writing. Merely allowing one worker at a time is insufficient
            if an old job can be retried after a correction.

        A2:
          source_condition: G2.
          arrangement: >
            Define explicit job outcomes and their meaning, including an
            incomplete or uncertain state. Record completion only when the
            chosen processing rules have resolved the entire file. Preserve
            a completed result against stale attempts to report failure.
          responsibility: >
            The import coordinator owns job state and recovery; the database
            must enforce any state transitions that competing attempts can
            otherwise race.
          premises: >
            Completion must distinguish successful processing from a promise
            that every uploaded value is still current. A newer correction
            may legitimately supersede an older upload.

        A3:
          source_condition: G2.
          arrangement: >
            Prefer evaluating a single database transaction that applies the
            accepted customer changes and records completion together. A
            transaction makes those changes succeed or roll back together.
            Serialize duplicate attempts for the same job and recheck its
            completed state before doing work.
          why_it_helps: >
            A crash then leaves either no committed import changes or a
            completed job. A replay of a completed job can return its existing
            result instead of writing customers again.
          premises:
            - >
              Whole-file acceptance is the chosen behavior, with invalid
              input resolved before changes are committed.
            - >
              The database supports the transaction, and measured duration
              and locking effects are acceptable.
          alternative: >
            Retain separate row commits if partial results are an intentional
            product choice. Keep A1, make repeated processing of the same
            immutable input safe, report partial or uncertain outcomes
            truthfully, and record completion after all rows are resolved.
            Per-row checkpoints can reduce repeated work but are not
            inherently necessary for the stated requirements.
          qualification: >
            Whole-file atomicity is a simplifying candidate, not an explicit
            requirement in the supplied product request. It also does not
            replace A1: an older transaction can otherwise commit after
            a newer one and overwrite it.

        A4:
          source_condition: G3.
          arrangement: >
            Measure a representative maximum-size import in the existing
            backend and database, including normal customer activity.
            Compare its duration and blocking effects with the accepted
            waiting time and request limits.
          decision: >
            Use direct processing if it fits. Retain a queue and background
            worker if the evidence calls for them, carrying A1 and A2 across
            that boundary.
          qualification: >
            Moving work into the background changes how the user waits;
            it does not remove the database work or its contention.

        A5:
          source_condition: G4.
          arrangement: >
            Decide and document the upload-precedence rule, invalid-row
            behavior, duplicate-email behavior within a file, and the meaning
            of completion when newer corrections have superseded some rows.
          candidate: >
            Later registered uploads win for each email; retries retain
            their original registration order; reject ambiguous duplicate
            emails and invalid input before applying a whole-file import.
          qualification: >
            This is a concrete candidate policy, not a fact or an additional
            user requirement.

    specified_content:
      - requirement: Assess whether the proposal is worth implementing as proposed.
        response: >
          No. Fix the stale-write rule before implementation, simplify the
          format handling, and choose background processing using actual
          timing evidence.
        material_sources: F1–F6.
      - requirement: English explanation for a nontechnical reader.
        response: >
          Lead with the visible risk: an older upload can undo a user's
          correction. Describe extra components through their maintenance
          and recovery costs, and reserve implementation details for the
          appendix.
      - requirement: Read-only review within the permitted materials.
        response: >
          Only the listed task and skill files were read. No files were
          modified, no network was accessed, and no implementation was attempted.

    review_material:
      condition_results:
        satisfied:
          - condition: Existing email identifies the customer to update.
            source: F3.
            basis: The table has a unique email key and matching imports update name and phone.
            scope_and_premises: >
              Establishes customer identity for the stated normal path.
              It does not establish which competing update should win.

          - condition: Completion can be recorded on an uninterrupted successful attempt.
            source: F5, F6.
            basis: The worker records completed after writing every row.
            scope_and_premises: >
              All row commits and the later status write succeed.
              This does not resolve interrupted or competing attempts.

          - condition: Interrupted jobs have a mechanism for another attempt.
            source: F5, F6.
            basis: The queue redelivers the entire job after interruption.
            scope_and_premises: >
              Establishes a retry mechanism, not safe behavior in the
              presence of newer customer information.

        unmet:
          - condition: Older work cannot replace corrected customer information.
            source: F6.
            basis: F3 and F5 permit the counterexamples in the validation records.
            impact: Corrections can be silently undone.
            arrangements: A1, with A2–A3 governing recovery.
            applicability: Jobs overlap on an email and execute out of upload order.

        pending:
          - condition: Failure and uncertain outcomes are visible and understandable.
            source: F6.
            unknown: Status semantics and recovery transitions beyond completed.
            decision_impact: G2.
            arrangement: A2 and the selected A3 alternative.

          - condition: Execution fits operational and user waiting limits.
            source: The decision between direct and background execution.
            unknown: Measured time, request limits, and contention.
            decision_impact: G3.
            arrangement: A4.

          - condition: Input precedence and completion have precise meanings.
            source: F3, F5, F6.
            unknown: G4.
            decision_impact: Required to finalize the corrected implementation.
            arrangement: A5.

      formed_observations:
        O1:
          observation: >
            Job identity, customer identity, and update precedence are
            separate facts. Neither an email key nor a job_id supplies all three.
          basis: F3, F5.
          applicability: Current proposal and either corrected execution method.

        O2:
          observation: >
            Checking an upload's age only before processing is insufficient.
            A correction can commit between that check and the old write.
          basis: F5 permits concurrency.
          applicability: >
            Any arrangement relying on an application-level check followed
            by an unconstrained customer update.
          consequence: >
            Enforce precedence at the database operation that changes
            the customer, using an atomic comparison and update.

        O3:
          observation: >
            A transaction around the entire file can simplify recovery,
            but cannot by itself establish newer-upload precedence.
          basis: >
            Atomicity determines whether changes commit together; the
            material provides no rule controlling which job commits last.
          applicability: A3.

        O4:
          observation: >
            A queue or a single worker is not a substitute for a precedence rule.
          basis: F5 permits replay of older work.
          applicability: >
            Designs in which an old job can be delivered or retried after
            a newer correction.

        O5:
          observation: >
            The parser knows how CSV becomes rows; the import coordinator
            knows upload and job rules; the customer database operation can
            constrain competing writes.
          basis: F3–F6 and A1–A3.
          consequence: >
            Keep those responsibilities clear without requiring a factory
            for formats that have no scheduled use.

        O6:
          observation: >
            No evidence establishes a speed benefit from the proposed layers
            or a need for background processing.
          basis: F1, F2, F4; no measurements supplied.
          qualification: >
            This is absence of justification, not proof that either approach
            will meet a particular response-time target.

      judgments_and_attached_basis:
        J1:
          judgment: Reject direct implementation of the current proposal.
          basis: G1; validation V1 and V2.
          scope_and_premises: Overlapping customer emails across old and corrected jobs.

        J2:
          judgment: Defer the format-selection factory.
          basis: F2 and F4.
          scope_and_premises: No accepted second-format requirement.

        J3:
          judgment: Prefer checking the simpler execution path before adding a queue.
          basis: F1, F4, O6.
          scope_and_premises: Conditional on A4; no performance guarantee asserted.

        J4:
          judgment: Make precedence enforcement independent of execution placement.
          basis: O1–O4.
          scope_and_premises: >
            Required whether processing is direct, queued, whole-file,
            or incremental.

        J5:
          judgment: Avoid demanding per-row progress solely because retries exist.
          basis: >
            With immutable input and the atomic precedence rule, replay can
            safely repeat work; no product requirement demands row-by-row progress.
          scope_and_premises: >
            Any side effects beyond the supplied customer assignments would
            need separate analysis. None are specified in the material.

      optional_improvements:
        - improvement: Add a clear count of processed and superseded rows.
          purpose: Explain why an older job can finish without changing newer customer values.
          premises: >
            Needed only if the selected user experience benefits from these
            details. The essential requirement is truthful completion wording.

        - improvement: Add per-row checkpoints.
          purpose: Reduce repeated processing if incremental imports become costly.
          premises: >
            Not needed solely to satisfy this small workload. Requires
            evidence that repeated work is a meaningful cost.

        - improvement: Introduce additional format implementations when a real second format arrives.
          purpose: Share demonstrated common rules while keeping parsing separate.
          premises: >
            Reassess the actual formats and their differing rules then;
            do not assume all formats need the same abstraction now.

      complete_validation_data:
        method: >
          Logical execution traces derived from the supplied design.
          No program, database, timing test, or implementation was available
          or executed. Candidate traces validate the stated guarantees only
          under their listed premises.

        original_proposal:
          V1:
            case: An interrupted old job overwrites a correction.
            initial_state: Customer email e has phone 100.
            steps:
              - Old job A contains phone 111 and writes it.
              - A stops before the job is recorded completed.
              - Corrected job B writes phone 222 and completes.
              - The queue redelivers A.
              - A writes phone 111 again.
            outcome: Customer e ends with the old value 111.
            violated_condition: F6 protection of corrected customer information.
            missing_guarantee: A customer write cannot reject stale job A.

          V2:
            case: Concurrent jobs overwrite a correction without any retry.
            steps:
              - Older A and corrected B contain the same email.
              - B writes the corrected value.
              - A reaches that email later and writes the old value.
            outcome: The older value wins.
            violated_condition: Same as V1.
            missing_guarantee: Cross-job precedence at the customer update.
            relationship: Same root cause as V1, not a separate architectural defect.

          V3:
            case: Interruption after a partial import.
            steps:
              - A commits rows 1 through k.
              - A stops before the remaining rows and completion write.
              - The queue redelivers all of A.
            outcome: Some customer changes exist while the job remains incomplete.
            interpretation: >
              Partial state is permitted by the proposal. It is not by itself
              forbidden by F6. Safe replay and truthful status must account for it.

          V4:
            case: Interruption between final customer write and completion.
            steps:
              - A commits every customer row.
              - A stops before the separate completed write.
              - A is redelivered and repeats its customer writes.
            outcome: Customer writes can all exist without a completed marker.
            interpretation: >
              The original marker does not imply a known outcome before retry.
              Repetition is harmless only if its effects are safe, including
              with respect to later corrections.

          V5:
            case: Replay with no intervening changes.
            steps:
              - A writes fixed name and phone values.
              - A repeats exactly those assignments.
            outcome: The same customer values can result.
            interpretation: >
              Replay is not automatically corrupting. This limits the criticism
              and isolates the newer-correction conflict as the decisive failure.

        corrected_candidate:
          premises:
            - A1 precedence is enforced atomically at every import customer write.
            - >
              Job contents and upload order are immutable; corrected uploads
              are new jobs with newer order.
            - >
              For whole-file processing, customer changes and completion share
              a database transaction.
            - >
              Duplicate attempts serialize on the durable job record and recheck completion.
            - >
              Completion means the file has been resolved, with any newer
              corrections preserved; it does not promise its values remain current forever.

          V6:
            case: New correction writes first.
            steps:
              - B has a newer order than A and updates email e.
              - A later attempts to update e.
            outcome: The database rejects or skips A's stale replacement.
            preserved_condition: Corrected information remains.

          V7:
            case: Old job writes first.
            steps:
              - A updates email e.
              - Newer B then updates e.
            outcome: B's corrected information becomes current.
            preserved_condition: Same precedence rule as V6, regardless of execution order.

          V8:
            case: Correction occurs between an early check and an old update.
            steps:
              - A performs an early check.
              - B commits a newer correction.
              - A reaches its customer write.
            outcome: >
              The atomic database condition sees the newer order and refuses
              the stale replacement.
            preserved_condition: No check-then-write race.
            warning: An unconstrained update after only an early check would fail this case.

          V9:
            case: Whole-file attempt stops before commit.
            outcome: >
              Customer changes and completed state roll back together.
              A retry uses the same job identity, order, and contents.
            preserved_condition: No partially committed whole-file result.
            limitation: Requires the selected transaction arrangement.

          V10:
            case: Whole-file commit succeeds but acknowledgement is lost.
            outcome: >
              The durable job is already completed. A serialized retry
              returns that result without rewriting customers.
            preserved_condition: Safe recovery from an uncertain response.

          V11:
            case: Two attempts for the same job overlap.
            outcome: >
              The job record serializes the attempts. The later attempt
              observes completion or proceeds after the earlier attempt rolls back.
            preserved_condition: Duplicate deliveries cannot independently reapply a completed job.

          V12:
            case: Different jobs overlap and hold database locks.
            outcome: >
              Precedence remains correct if A1 is implemented atomically.
              Transactions may wait or be aborted by the database.
            remaining_obligation: >
              Handle aborted attempts using the same identity and order.
              Validate acceptable waiting and locking costs under A4.
            qualification: Correctness does not establish acceptable performance.

          V13:
            case: Incremental alternative retries old rows.
            outcome: >
              Repeated rows use the same immutable input and order;
              rows already superseded by newer uploads cannot be overwritten.
              The job remains incomplete until the whole file is resolved.
            preserved_condition: Safe retry without mandatory per-row checkpoints.
            limitation: >
              Partial customer changes remain visible, so that behavior and
              status wording must be accepted.

        evidence_that_would_change_the_choice:
          - >
            A genuine scheduled second format could justify revisiting format abstractions.
          - >
            Measured import time beyond accepted waiting or request limits
            could justify background processing.
          - >
            Unacceptable whole-file locking or a requirement to retain valid
            rows despite invalid rows could favor incremental processing.
          - >
            A different accepted precedence policy would change A1's comparison
            rule, while leaving the need to enforce that rule at the write intact.
```

The decisive conclusion requires no further evidence: the stated proposal permits an older job to undo a correction. The unknowns affect the replacement design, not that conclusion.