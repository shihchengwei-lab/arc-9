# 維護說明

## 來源與成品

用途、案例與安裝方式見 [README](README.md)。本文件說明重建與維護方式。

[drafts/arc9.md](drafts/arc9.md) 是完整提示詞的唯一維護來源，包含共用契約與具名場景；不要直接修改 `dist/` 中的產物。

[封裝腳本](scripts/package_skills.py) 維護呼叫名稱與介面描述，為完整來源加上 SKILL.md 識別資訊，另產生 agents/openai.yaml。單一成品名稱為 `arc9`，設定 `allow_implicit_invocation: false`，維持使用者明確呼叫。

成品目錄與 ZIP 均只含 `arc9`，內有 SKILL.md、agents/openai.yaml 與 LICENSE，共 3 個檔案。授權文字來自根目錄 LICENSE。封裝程式、測試與研究材料不進入 ZIP；腳本不安裝、發布或呼叫模型。

同一份產物集合決定 ZIP 與 `dist/skills/` 的內容。重建會清除 `dist/skills/` 中不在集合內的過期檔案與資料夾，以及改名前的 `dist/masters-lenses.zip`；其他位置不受影響。已提交的舊版提示詞與案例可由 Git 歷史查閱；本機研究快照不進入成品。

## 重建與檢查

在專案根目錄執行：

```powershell
python -B -X utf8 scripts/package_skills.py
python -B -X utf8 scripts/package_skills.py --check
python -B -X utf8 -m unittest discover -s tests -v
```

只需 Python 標準函式庫。ZIP 檔案時間固定，讓相同來源在同一環境產生相同位元組；`--check` 可檢查成品與 ZIP 是否偏離來源，不寫檔。`-B` 避免測試產生 Python 快取。

五個封裝測試涵蓋：完整定稿內容、手動政策與 MIT 授權、目錄與 ZIP 內容一致、成品或 ZIP 被改動時檢查失敗、舊成品與場景函式庫殘留偵測、重建清除過期產物，以及相同來源重建一致。`--check` 偵測差異但不覆寫或刪除檔案。這些檢查不證明模型判斷品質或安裝後的 Host 行為。

## 提交範圍

提交維護來源、封裝腳本、可重跑測試、說明與成品。研究素材、一次性實驗及交接紀錄由 .gitignore 排除，保留在本機；維護流程不依賴這些檔案。
