# arc9 neutral-profile language calibration — 2026-10-22

3/3 language requests met the recorded language criteria. Each used a fresh main model and exactly one independent reviewer.

[Inputs and complete outputs](../../examples/masters-lens/finalized-2026-10-22/neutral-language/README.md) · [Recorded usage](../../examples/masters-lens/finalized-2026-10-22/neutral-language/results.json) · [Original 13-request suite](arc9-finalized-2026-10-22.md)

## Why this follow-up exists

The original suite used ignore-user-config and a zero project-document limit, but recorded inputs still contained the host global AGENTS.md, including a Traditional-Chinese directive. Its English-request opening was Chinese while the final answer was English. That condition cannot isolate the skill's default language behavior.

This calibration uses a separate CODEX_HOME with no AGENTS files. [Official instruction-discovery guidance](https://learn.chatgpt.com/docs/agent-configuration/agents-md) documents the global instruction scope under CODEX_HOME. Absence of injected AGENTS blocks was checked in all six actual root/reviewer input logs, rather than inferred from command flags.

The skill snapshot, model (gpt-6.1-sol), effort (xhigh), CLI (0.159.1), input bytes and dispatch text match the original language requests; only the profile and run-directory paths differ. Each profile/case was attempted once. The initial 13 responses are retained and are not replaced by these new results.

## Results

| Request | Language result | Seconds | Input + output tokens |
|---|---|---:|---:|
| [language-chinese](../../examples/masters-lens/finalized-2026-10-22/neutral-language/language-chinese/answer.md) | pass | 248.937 | 337,128 |
| [language-english](../../examples/masters-lens/finalized-2026-10-22/neutral-language/language-english/answer.md) | pass | 319.531 | 298,627 |
| [language-override](../../examples/masters-lens/finalized-2026-10-22/neutral-language/language-override/answer.md) | pass | 212.594 | 225,269 |


### language-chinese

The initial progress messages and final response are Traditional Chinese. The response preserves the stale-write and recovery findings; detailed mechanisms, prerequisites and verification-method statements are in the appendix. Both model inputs contain zero injected AGENTS instruction blocks.

> 不建議照原案直接實作。

> 架構可以縮小。

### language-english

The first progress message, later progress updates and final answer are English even though the proposal material is Chinese. The final answer retains the stale-overwrite and recovery findings and puts candidate arrangements and their conditions in the supporting appendix. Both actual model inputs contain zero injected AGENTS instruction blocks.

> I’ll read the proposal and the $arc9 skill

> Do not implement this proposal as written.

> A smaller CSV import feature is reasonable.

### language-override

The request is English and explicitly asks for Traditional Chinese. All progress messages and the final answer are Traditional Chinese; the final answer retains the stale-overwrite and recovery findings and groups detailed mechanisms, optional improvements and verification qualifications in the appendix. Both actual model inputs contain zero injected AGENTS instruction blocks. This is a language check; it does not give an additional pass score for required-arrangement classification.

> 我會先讀取指定的任務檔與 arc9 技能內容

> 不建議照原案直接實作。

> 以下附錄提供判斷依據、成立條件與驗證方式。

## Cost

This cohort used 821,208 input tokens, including 676,736 cached input, and 39,816 output tokens including 15,872 reasoning tokens. Input plus output totals 861,024; complete workflow times sum to 781.062 seconds.

Median complete workflow: 248.937 seconds and 298,627 input-plus-output tokens. Root and reviewer usage is counted once per unique thread, and waits are included in wall time.

Including the original suite, the work comprises 16 requests / 32 unique threads, 4,330,508 total tokens, and 3340.030 seconds of complete workflow time. The two profiles remain separate in the results and medians.
