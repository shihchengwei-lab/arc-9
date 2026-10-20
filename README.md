![Architecture Review Core 9](docs/images/arc9-hero.png)

# arc-9

[English](README.en.md)

方案看起來可行，資料更新、權限或中斷重試仍可能留下缺口。

`$arc9` 是手動呼叫的唯讀工程審查 skill。它沿實際操作追查問題，說明方案是否需要改動、該改哪裡，以及判斷的依據。方案已符合需求時，也會直接說明。

它以「使非法狀態無法被表達」為最高原則：調整資料與操作的安排，讓違反需求的狀態無法建立。審查只讀取任務提供或允許讀取的材料，不修改程式、檔案、設定或外部狀態。

## 代表案例

以下摘要取自四個 CSV 匯入方案的審查回答。

| 題目中的方案 | 審查重點 |
|---|---|
| 小量匯入預先加入多格式工廠與佇列，舊工作還能覆寫修正資料。 | 先簡化流程、量測耗時；確認新舊資料的優先規則，再讓寫入遵守它。 |
| API 檢查路徑前綴，開檔時卻用另一種路徑解讀。 | 找出跨租戶讀檔路徑，改由可信租戶身分決定來源與寫入對象。 |
| 每秒到達 20 個工作、完成 2 個，卻要求等待不超過 30 秒。 | 擴大佇列無法履行承諾；需要限制受理量，並處理重送與中斷恢復。 |
| 簡單匯入流程允許重送覆寫，交易與驗證紀錄也符合需求。 | 判定可交付，沒有交付前必要改動。 |

## 開始使用

1. [下載 ZIP](dist/arc-9.zip)，解壓縮後將 `arc9` 資料夾放入 Codex 的 skills 目錄。Windows 預設位置為 `C:\Users\<使用者名稱>\.codex\skills\`；已設定 `CODEX_HOME` 時，使用該目錄下的 `skills`。
2. 下個回合，在目前的任務討論中呼叫：

```text
$arc9 請檢查目前方案有哪些必要改動。
```

回答會簡短交代判斷、依據，以及影響決策的未知與必要下一步。預設跟隨請求語言，也可指定語言與篇幅。

也可以提供已下載的 [SKILL.md](dist/skills/arc9/SKILL.md) 路徑，請模型讀取並使用。

## 完整案例與紀錄

- 四個 CSV 方案：[題目與完整回答](examples/masters-lens/README.md) · [執行紀錄](examples/masters-lens/execution.md)
- 需求更新與問題修正：[六個狀態的完整回答](examples/masters-lens/contracts/README.md) · [執行紀錄](examples/masters-lens/contracts/execution.md)
- 語言與篇幅：[三種請求情境](examples/masters-lens/language/README.md) · [執行紀錄](examples/masters-lens/language/execution.md)

提示詞來源、封裝檢查與重建方式見[維護說明](MAINTENANCE.md)。

## 授權

本專案採用 [MIT License](LICENSE)。
