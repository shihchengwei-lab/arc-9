# 舊版 CSV 三組對照：執行紀錄

## 日期與設定

2026-09-07，以修正後的比較方式重新執行。三個獨立 subagent 各回答一次，未繼承主對話（`fork_turns="none"`），未看到其他組回答；本輪未重抽或改寫回答。三組沿用主代理模型設定，沒有覆寫模型或推理設定；工具沒有回傳可供核對的模型版本與隨機種子。

共同輸入包含中性的審查要求、相同材料與問題，要求繁體中文、250–400 字、最多三個重點。只有角色組加上「你是資深工程師」；單濾鏡組只使用 simplicity，雙濾鏡組使用 simplicity 與 reliability。輸出全文照錄。以讀取 SKILL.md 使用濾鏡。

本輪比較角色提示與濾鏡兩種引導方式。前次讓所有組別都帶角色提示，紀錄保留於 Git 歷史 `40efcca`；本頁對應本輪三份回答。

| 組別 | 實際派送提示詞 | 回答全文 | 額外材料 |
|---|---|---|---|
| 角色提示（無濾鏡） | [提示詞](baseline-prompt.txt) | [原文](baseline.md) | 無 |
| 單一濾鏡 | [提示詞](single-prompt.txt) | [原文](single.md) | [simplicity](https://github.com/shihchengwei-lab/masters-lenses/blob/4e80ebcd2f7f1d4fb524841459e4b5d47e7fe2b4/dist/skills/simplicity/SKILL.md) |
| 雙濾鏡 | [提示詞](dual-prompt.txt) | [原文](dual.md) | simplicity 與 [reliability](https://github.com/shihchengwei-lab/masters-lenses/blob/4e80ebcd2f7f1d4fb524841459e4b5d47e7fe2b4/dist/skills/reliability/SKILL.md) |

[共同材料與問題](input.md)。所有組別都被要求不讀取指定範圍以外的檔案、不修改檔案。

## 判讀與執行範圍

三組都指出預留格式的複雜度、佇列需要量測、舊工作覆寫與完成狀態的風險，也都區分交易與更新順序的保護。

這是虛構方案的單次提示對照。紀錄包含派送提示詞與回答，未執行回答中的技術建議；沒有獨立評分、多次重跑、正確率或使用者理解程度量測，也未測試安裝後的 `$` 介面。

## 來源與圖片重建

濾鏡來源版本：`4e80ebcd2f7f1d4fb524841459e4b5d47e7fe2b4`。

測試時 SKILL.md 的 SHA-256：

- simplicity：`AFF159F7BB65011C80919E39919F2BCC4253E5397EA0B1DD0F40ECA6D7CD79C0`
- reliability：`D2C9F2204F44D28C3B00DEB56AA92B366AF526664A6185B2DEEC2ED4A151C5F5`

圖片是編輯整理的重點摘要，搭配各組回答的視覺呈現；每張附一句逐字原文摘錄，腳本會核對摘錄存在於原文。可在 Windows、已安裝 Pillow 與微軟正黑體的環境重建：

```powershell
python -B -X utf8 scripts/render_readme_examples.py
```

重建圖片不會重新呼叫模型。
