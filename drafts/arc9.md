# arc9

主模型載入[編輯契約](references/output.md)，並啟動一位獨立 sub-agent `reviewer` 讀取[審查契約](references/review.md)。契約路徑均相對本 SKILL.md 解析為絕對路徑。

```ts
const mode = "read-only"

interface 任務輸入 {
  本次任務: string // 使用者的原始需求，沿用原文
}

interface 審查輸入 extends 任務輸入 {
  材料: string[] // 本次提供或允許讀取的內容、路徑與驗證證據，供審查取用
  已接受的限制: string[] // 含已接受的調整，作為方案的判定條件
  授權範圍: string // 限定審查者可讀取的對象與可進行的唯讀查證
  審查要求?: string[] // 使用者明示的範圍、證據門檻與必查項目，據以安排審查
}

const 本次任務 = 使用者原始需求
const input: 審查輸入 = 整理審查輸入(本次任務)
const context: 編輯脈絡 = 整理編輯脈絡(本次任務)
const reviewer = 啟動審查者({ fork_turns: "none", 契約路徑: 審查契約路徑, input })
const result: 審查輸出 = 取得審查結果(reviewer)
const 交付: 編輯輸出 = 依編輯契約編輯({ context, result })
```

- 派送時一併交代 `審查輸入` 的欄位用途。
- 編輯時若需要補證或重新分析，交回同一位 `reviewer`，依更新結果重新編輯。
- 啟動、讀取契約或取得結果失敗時，回報受阻。
