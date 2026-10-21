# arc9

主模型載入[編輯契約](references/output.md)；必須啟動一個獨立 sub-agent `reviewer`（`fork_turns="none"`），令其讀取[審查契約](references/review.md)。路徑均相對本 SKILL.md 解析為絕對路徑。

```text
mode := read-only
reviewer.input := {
  本次任務: 使用者原始需求,
  材料: 本次任務提供或允許讀取的內容、路徑及驗證證據,
  已接受的限制: 含已接受的調整,
  授權範圍,
  讀者背景?,
  文件用途?,
  本次明確輸出要求?
}
審查執行者 := reviewer

{正文, 附錄} := 主模型依編輯契約分區編輯(reviewer.output)
交付 := {正文, 附錄}

補證 ∨ 重新分析 ⇒ 交回 reviewer → 依更新結果重新分區編輯
啟動、讀取契約或取得結果失敗 ⇒ 回報受阻
```
