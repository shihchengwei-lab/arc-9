# 維護說明

## 來源與成品

用途、案例與安裝方式見 [README](README.md)。本文件說明重建與維護方式。

[drafts/arc9.md](drafts/arc9.md) 維護入口與唯讀 CLI 啟動方式。[第一層](drafts/references/review.md) 維護審查契約與具名場景，[第二層](drafts/references/output.md) 維護輸出編輯契約。各項規則在其負責的來源維護，修改後重建 `dist/`。

入口把使用者原始請求與可用材料交給獨立的 CLI 會話，並把審查契約原樣複製到該會話的暫存工作目錄。初審與補查讀取同一份副本，檔案寫入由唯讀沙箱阻止。審查者按問題選用具名場景查證並形成結論，需要交叉核對時可用裁決表。主模型收到結果後編輯正文與附錄。

[封裝腳本](scripts/package_skills.py) 維護呼叫名稱與介面描述，為入口加上 SKILL.md 識別資訊，複製兩份參考文件，另產生 agents/openai.yaml。單一成品名稱為 `arc9`，設定 `allow_implicit_invocation: false`，維持使用者明確呼叫。

成品目錄與 ZIP 均只含 `arc9`，內有 SKILL.md、references/review.md、references/output.md、agents/openai.yaml 與 LICENSE，共 5 個檔案。授權文字來自根目錄 LICENSE。封裝程式、測試與研究材料不進入 ZIP；腳本不安裝、發布或呼叫模型。

同一份產物集合決定 ZIP 與 `dist/skills/` 的內容。重建只清除 `dist/skills/` 中不在集合內的過期檔案與資料夾，以及改名前的 `dist/masters-lenses.zip`。重建與 `--check` 都會先檢查成品路徑，按實際大小寫比對檔名。遇到目錄連結、符號連結，或 Windows 會去掉尾端空格或句點的成品名稱時停止。寫入時以同目錄的新檔替換成品，避免改寫與成品共用內容的硬連結。重建期間由單一程序管理成品目錄。

## 重建與檢查

在專案根目錄執行：

```powershell
python -B -X utf8 scripts/package_skills.py
python -B -X utf8 scripts/package_skills.py --check
python -B -X utf8 -m unittest discover -s tests -v
```

只需 Python 標準函式庫。ZIP 檔案時間固定，讓相同來源在同一環境產生相同位元組；`--check` 可檢查成品與 ZIP 是否偏離來源，不寫檔。`-B` 避免測試產生 Python 快取。

封裝測試涵蓋來源與成品一致、手動政策與 MIT 授權、缺少來源時保留既有成品、檢查差異與過期成品、重建可重現，以及 Windows 目錄連結、檔名別名、大小寫和外部硬連結。

## 案例

[CSV 匯入案例](examples/csv-import/README.md)收錄四份題目與完整回答。更新案例時，用同一組題目重跑，再依新回答更新中英文 README 的摘要。
