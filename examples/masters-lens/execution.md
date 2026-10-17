# masters-lens：四案執行紀錄

## 受測版本與材料

2026-10-17，使用現有 CSV 匯入、租戶資料隔離、過載受理與完整方案四份題目，審查恢復九位大師具體方法後的單檔版。題目中的效能數字與驗證通過紀錄是給定材料，本輪沒有執行題目所描述的匯入系統。

受測內容見 [SKILL.md 快照](skill-snapshot.md)，SHA-256 為：

```text
8E4E3F6A01A087B058C5D0AC296AC4574A61A92C9417CB2B406149D5BC95C399
```

提示詞與封裝在派送前固定，快照與當時的 `dist/skills/masters-lens/SKILL.md`、ZIP 內容相同。測試時的版本庫 HEAD 為 `62971aa380010cf3fb79a56ba48b63535dc243da`，實際受測內容為工作目錄的固定快照。[metadata.json](metadata.json) 保存來源、受測內容與封裝的識別，以及各案派送與回答資料。

## 派送與設定

每案建立一個獨立代理任務，派送文字如下，案例目錄分別為 `csv`、`security`、`overload`、`complete`：

```text
請讀取 C:\Users\kk789\Desktop\masters-lenses\experiments\restored-methods-four-cases-2026-10-17\<案例>\input.md 與 C:\Users\kk789\Desktop\masters-lenses\experiments\restored-methods-four-cases-2026-10-17\skills\masters-lens\SKILL.md，使用 $masters-lens 回答題目。
```

四個任務均使用 `fork_turns=none`，沿用主代理模型與推理設定，沒有指定覆寫；工具未提供精確模型版本與 seed。派送只有題目與 skill 路徑，共通契約由 skill 提供。

CSV、資安與過載先派送。收到使用者繼續指示時，CSV 與資安已有最終回答，過載尚未完成，完整案尚未派送。其後首次派送完整案，並對過載的同一原任務送出：

```text
接續原本尚未完成的任務，完成最後回答。
```

過載的同一 session 有兩個回合與一份最終回答；其他三案各一個回合與一份最終回答。每案各一次嘗試，沒有補抽。各案實際派送、接收、最終回答的 UTC 時間與 session ID 見 [metadata.json](metadata.json)。

四案工具結果均包含完整題目與受測 SKILL.md。完整案另用一次工具計算草擬回答字元。公開完整回答直接保存各 session 的唯一 `final_answer` 原文。本機受測目錄另保留完整工具呼叫與結果、派送及接續紀錄、前版回答與比較。

## 回答與輸出契約

| 案例 | 題目 | 完整回答 | 正文字元 | 條列項目 |
|---|---|---|---|---|
| CSV 匯入 | [材料與問題](csv/input.md) | [原文](csv/answer.md) | 301 | 3 |
| 租戶資料隔離 | [材料與問題](security/input.md) | [原文](security/answer.md) | 321 | 3 |
| 過載與受理 | [材料與問題](overload/input.md) | [原文](overload/answer.md) | 296 | 3 |
| 已完成驗證的方案 | [材料與問題](complete/input.md) | [原文](complete/answer.md) | 279 | 3 |

計數依 skill，排除空白與 Markdown 排版標記，保留正文識別字的底線。四份均以繁體中文、全文三個條列呈現，符合 250–400 字元，沒有客套話或開場白。

CSV 回答反對直接加入格式工廠與佇列，將工作內容、版本順序與完成狀態接到資料庫安排；「較新」先列為待定政策。資安回答推導出完整跨租戶外洩路徑，取消任意來源路徑。過載回答提出原子容量保留、工作與待送訊息同交易、補送與原工作追蹤。完整案依既有規則、驗證及量測支持交付，沒有新增問題。

## 檔案與封裝核對

四案完成後、保存回答之前，37 個專案檔案與 183 個受測目錄檔案的清單及 SHA-256 與派送前相同；清單檔本身不計入。已安裝 skill 與前版實驗目錄也未變更。

封裝重建、成品檢查、五項封裝單元測試、官方 quick_validate 與 git diff --check 均通過。ZIP 只含 SKILL.md、agents/openai.yaml、LICENSE 三個檔案；來源、成品、受測快照與 ZIP 一致，手動呼叫政策與授權不變。ZIP 的 SHA-256 為：

```text
08B77FFD5D565963742F9B3C265A245CDDC5DC7815AE5E04CB039BD999199D2D
```
