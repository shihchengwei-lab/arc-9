# Finalized arc9 verification — 2026-10-22

The finalized skill matched the expected overall verdict in 10/10 proposal/contract scenarios. Each of the 13 requests used a fresh main model and exactly one independent reviewer.

The verdict score concerns whether the supplied proposal meets its commitments. Required-arrangement classification and editorial routing are assessed separately and have exceptions, recorded below.

This suite retained the host global AGENTS.md, including its Traditional-Chinese directive. Its three language cases are observations under that profile, not isolated default-language tests. The [neutral-profile language calibration](arc9-language-neutral-2026-10-22.md) is reported separately, preserving all original responses.

Median full-workflow time: 220.3 seconds. Median input-plus-output usage across both models: 238,747 tokens.

[All inputs, final responses and reviewer outputs](../../examples/masters-lens/finalized-2026-10-22/README.md) · [Machine-readable results](../../examples/masters-lens/finalized-2026-10-22/results.json)

## Conditions and scope

- Model gpt-6.1-sol, reasoning effort xhigh, Codex CLI 0.159.1, on Windows.
- One attempt per request, in the pre-recorded order; no answers were selected by repeated sampling.
- The thirteen requests comprise four CSV proposals, six contract states, and three language variations of the same CSV material. They are targeted supplied-material checks, not thirteen unrelated systems.
- The actual finalized installation was snapshotted before execution. Source, package and installed copies matched. The full entry/reviewer/editor workflow ran for every request; the first-layer output was not precomputed.
- The host provided a read-only fixture reader. Both roles read the relevant contract and current input. Exactly one reviewer was launched with fork_turns=none and did not delegate further.
- config.toml was ignored and project_doc_max_bytes was set to zero. Other skills, memories, plugins, hooks, web, shell and image/browser tools were disabled; the code-mode host and multi-agent support remained enabled.
- Audit of the actual recorded model inputs found the global AGENTS.md in all 26 threads. The English-request opening was Traditional Chinese while its final response was English. The global language directive prevents attributing this opening to the skill alone. The follow-up uses a distinct CODEX_HOME without AGENTS, consistent with [OpenAI's instruction-discovery guidance](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
- Existing input fixtures were copied without changing their contents. Expected relationships were frozen before the first run and were not supplied to the tested models.
- The root agent assessed complete responses against those criteria, accepting valid alternative arrangements. Output-routing observations are reported separately from task-judgment checks.
- No application described by the fixtures was executed. Claims concern the supplied-material review outputs.
- This round validates the finalized version. No fresh baseline was run, and it is not used to claim an improvement over earlier versions.

## Results

| Request | Verdict | Required arrangements | Language observation | Output routing | Seconds | Total tokens |
|---|---|---|---|---|---:|---:|
| [csv](../../examples/masters-lens/finalized-2026-10-22/csv/answer.md) | pass | source overlap | pass | see notes | 261.968 | 268,900 |
| [security](../../examples/masters-lens/finalized-2026-10-22/security/answer.md) | pass | supported | pass | pass | 144.141 | 231,804 |
| [overload](../../examples/masters-lens/finalized-2026-10-22/overload/answer.md) | pass | supported | pass | pass | 275.906 | 296,621 |
| [complete](../../examples/masters-lens/finalized-2026-10-22/complete/answer.md) | pass | supported | pass | partial | 266.594 | 473,290 |
| [authority-base](../../examples/masters-lens/finalized-2026-10-22/authority-base/answer.md) | pass | supported | pass | pass | 144.938 | 277,312 |
| [authority-memo](../../examples/masters-lens/finalized-2026-10-22/authority-memo/answer.md) | pass | extra memo rewrite | pass | follows source | 160.110 | 238,747 |
| [authority-authorized](../../examples/masters-lens/finalized-2026-10-22/authority-authorized/answer.md) | pass | supported | pass | pass | 113.875 | 195,101 |
| [merge-original](../../examples/masters-lens/finalized-2026-10-22/merge-original/answer.md) | pass | supported | pass | pass | 220.312 | 226,522 |
| [merge-read-fixed](../../examples/masters-lens/finalized-2026-10-22/merge-read-fixed/answer.md) | pass | supported | pass | pass | 150.985 | 270,233 |
| [merge-both-fixed](../../examples/masters-lens/finalized-2026-10-22/merge-both-fixed/answer.md) | pass | supported | pass | pass | 99.406 | 229,251 |
| [language-chinese](../../examples/masters-lens/finalized-2026-10-22/language-chinese/answer.md) | pass | supported (policy choices) | pass | see notes | 250.312 | 193,269 |
| [language-english](../../examples/masters-lens/finalized-2026-10-22/language-english/answer.md) | pass | source classifies simplification as required | not isolated | see notes | 221.812 | 349,134 |
| [language-override](../../examples/masters-lens/finalized-2026-10-22/language-override/answer.md) | pass | supported (candidate policy) | pass | see notes | 248.609 | 219,300 |

## Recorded observations


### csv

Correctly rejects direct implementation because retries can overwrite corrections and completion state can diverge from committed data. A simplification recommendation appears in both reviewer task-answer and optional-improvement sections and in the edited main body; detailed candidate arrangements and prerequisites are in the appendix.

> 舊工作再被重送，就可能把修正覆蓋回去。

> 目前逐筆寫入、最後另標完成，可能留下部分更新

> 架構可以先簡化。

### security

Optional narrowing of the background service account and verification/process qualifications are in the explicit appendix; the required source-binding repair remains in the main body.

> /tenants/A/../B/customers.csv

> 固定寫入 A，並不能保證來源也是 A。

> 交付前必須限制實際讀取的檔案來源

### overload

The response rejects a queue-size-only change, traces false acceptance and duplicate submissions, and proposes bounded/durable admission. Capacity arithmetic, verification conditions and remaining evidence needs are in the appendix; decision-level quantities remain in the body.

> 活動結束時也估計累積約 2,160 件未完成工作

> 可靠接下工作才回覆 202

> 前端等待時持續查詢原工作

### complete

Correctly accepts the supplied implementation and accepted overwrite/replay semantics; the reviewer reports no task gap or necessary arrangement. Optional boundary-test documentation and unused mechanisms are in the appendix. Editorial limitation: the second body bullet repeats an unrequested verification-method qualification after the first bullet already says the decision relies on supplied implementation and verification records.

> 可以交付。

> 未發現交付前必須修正的實質缺口。

> 本次未直接檢查程式或重新執行測試。

### authority-base

Retains task-selected R1 and the 30-second deadline, recognizes 45-second noncompliance, and requires implementation improvement plus same-condition verification. An authorized move to R2 is treated as a conditional alternative in the appendix, not a requirement change already granted.

> 本次指定 R1，要求受理後 30 秒內可下載

> 實際時間至少縮短 15 秒

> 須另獲明確同意

### authority-memo

Correctly retains R1 and rejects an implementation memo as authority to relax the deadline. Classification exception: the reviewer includes rewriting the memo in its Necessary arrangements field, and the editor carries it into the main body. The stated commitment concerns completion within 30 seconds; rewriting the memo does not close the 45-versus-30-second gap. This is recorded separately from the correct noncompliance verdict.

> 新增備註不能把標準改成 60 秒。

> 將備註更正為「目前 45 秒，未達 R1 的 30 秒要求」

### authority-authorized

Fresh complete-workflow regression passes: the reviewer reports no gap and no necessary arrangement under task-selected R2; the editor puts the optional memo rewrite and its non-prerequisite qualification together after the appendix boundary. The body retains the 60-second authority and 45-second compliance evidence.

> 沒有必須調整的安排。

> 可選的文字改善：將備註改為

> 並非達標的必要條件

### merge-original

Finds both mismatches and their shared cause while preserving independently determined read/delete permissions. Accepts either authoritative input if authorization and use bind to the same object. Optional wrappers, alternative details, and verification/process qualifications are confined to the appendix.

> 目前下載與刪除都仍可越權。

> 下載檢查該檔案的讀取權限，刪除檢查該檔案的刪除權限。

> 兩種修法擇一即可

### merge-read-fixed

Drops the repaired download defect and keeps only the deletion mismatch as requiring a repair. Mixed-permission test cases and explicit rejection of obsolete fields are classified as optional improvements in the appendix, with their purpose and conditions.

> 目前下載已修正，刪除仍有漏洞。

> 必要改動在刪除入口。

> 目前缺口在檔案對象錯配，沒有證據顯示兩項權限被合併

### merge-both-fixed

Recognizes both bindings are fixed, keeps read/delete independently authorized, and removes both historical defects. The reviewer reports no remaining gap or necessary arrangement. Supporting test cases and the verification-method qualification are placed in the appendix.

> 目前下載與刪除都符合要求，沒有本次仍須追加的必要改動。

> 未滿足：無。待確認且影響本次判斷的條件：無。必要安排：無。

### language-chinese

Uses Traditional Chinese and preserves the CSV rejection, stale-retry counterexample, and ordering/recovery concerns. As in the CSV request, a general simplification recommendation remains in the body, while candidate mechanisms and conditions are in the appendix. The reviewer also derives unspecified duplicate-row/error policies from understandable completion/retry results and calls for settling those choices before implementation.

> 不值得照原案直接實作。

> 僅限制同時執行，或讓整份檔案一起成功、一起取消，都不足以防止舊資料覆蓋。

> 可選的簡化及其前提

### language-english

The final response is English and correctly rejects the proposal, with candidate mechanisms and their conditions in the appendix. The initial main-model progress message is Traditional Chinese. Prompt audit found an injected global AGENTS directive requiring Traditional Chinese despite ignore-user-config and project_doc_max_bytes=0, so this run does not isolate default language behavior. The reviewer also labels scope simplification as a necessary adjustment; that is recorded separately from the correct rejection verdict.

> Do not implement the proposal as written.

> Fix update priority and recovery first.

> 我會依指定的 arc9 技能進行唯讀審查

### language-override

The English request explicitly asks for Traditional Chinese; the final response is Traditional Chinese and preserves the stale-retry, recovery and scope findings. It states the priority and transaction prerequisites in the appendix rather than treating atomicity alone as a stale-write fix. This host-profile run also contains the existing global Traditional-Chinese directive.

> 不建議照原案直接實作。

> 系統必須能阻止舊資料覆蓋新資料

> 材料並未要求整份匯入必須全部成功或全部失敗

## Cost accounting

Wall time spans CLI launch through exit, including reviewer execution and waits. Each unique main/reviewer thread contributes its last cumulative usage once. Output includes reasoning; cached input is a subset of input.

| Metric | Entire round |
|---|---:|
| Requests / unique threads | 13 / 26 |
| Input tokens | 3,361,241 |
| Cached input subset | 2,745,472 |
| Output tokens, including reasoning | 108,243 |
| Reasoning output subset | 45,904 |
| Input plus output | 3,469,484 |
| Sum of complete workflow times | 2558.968 seconds |
| Median complete workflow time | 220.312 seconds |
| Time range | 99.406–275.906 seconds |

Token counts include cached and repeated context. They are recorded model usage, not a currency estimate. Per-thread and per-request values appear in the linked results.

## Tested artifact and records

The public [skill snapshot](../../examples/masters-lens/finalized-2026-10-22/skill/SKILL.md), [criteria](../../examples/masters-lens/finalized-2026-10-22/criteria.json), inputs and verbatim outputs identify what was tested. File digests, run times and thread IDs are in the results file. The package SHA-256 is ab8b99828860c2bbb052b3fc855b170f39263326207bdfc9ffe25fa9ec5891cb.

The evidence directory preserves original file bytes, including line endings, with a local attributes file.

Raw CLI events, stderr, original session logs, read-audit records and the frozen execution manifest remain in the private local experiment directory. Public records contain the actual final responses, reviewer outputs and user-visible main-model messages, without internal reasoning traces or account configuration.
