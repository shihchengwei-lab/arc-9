# masters-lens：四案執行紀錄

## 受測版本與材料

四個 CSV 匯入方案的題目、回答與執行資料如下。題目中的實作、效能數字與驗證通過紀錄是提供給代理的材料。

| 案例 | 測試時版本庫 HEAD | 實際受測內容 |
|---|---|---|
| CSV 匯入、租戶資料隔離、過載與受理 | `62971aa380010cf3fb79a56ba48b63535dc243da` | [受測 SKILL.md](skill-snapshot.md) |
| 接受重送覆寫的簡單方案 | `f4d5b8faf4a8c7bfcdc0ab8d1901f5f3d8f2935a` | [受測 SKILL.md](language/skill-snapshot.md)，與語言測試使用相同內容 |

## 派送與執行

四案各建立一個獨立代理，使用 `fork_turns=none`，沿用主代理模型與推理設定，沒有指定覆寫。前三案的紀錄未提供精確模型版本與 seed；第四案讀得的執行標籤為 `gpt-6.1-sol`、推理設定 `xhigh`，未取得不可變模型版本或 seed。篇幅與格式由受測 skill 提供。

前三案派送文字如下，`<案例>` 分別替換為 `csv`、`security`、`overload`：

```text
請讀取 C:\Users\kk789\Desktop\masters-lenses\experiments\restored-methods-four-cases-2026-10-17\<案例>\input.md 與 C:\Users\kk789\Desktop\masters-lenses\experiments\restored-methods-four-cases-2026-10-17\skills\masters-lens\SKILL.md，使用 $masters-lens 回答題目。
```

第四案派送文字：

```text
請讀取 C:\Users\kk789\Desktop\masters-lenses\experiments\accepted-overwrite-single-case-2026-10-18\input.md 與 C:\Users\kk789\Desktop\masters-lenses\experiments\accepted-overwrite-single-case-2026-10-18\skill-snapshot.md，使用 $masters-lens 回答題目。
```

各案一次嘗試、一份最終回答。過載案在同一 session 接續，共兩個回合；其餘各一回合。過載案接續前尚無最終回答，於 UTC `2026-10-17T15:46:54.098Z` 送出：

```text
接續原本尚未完成的任務，完成最後回答。
```

下表時間均為 UTC 2026-10-17：

| 案例 | session ID | 派送 | 最終回答 |
|---|---|---|---|
| CSV 匯入 | `01a14a87-b382-7070-abd3-80bceb8fa44f` | 15:42:49.546 | 15:43:31.037 |
| 租戶資料隔離 | `01a14a87-d0eb-7793-8bac-f2d5d93bce70` | 15:42:57.187 | 15:43:25.156 |
| 過載與受理 | `01a14a87-e12f-73b1-a66a-755141c80cd5` | 15:43:01.296 | 15:47:08.210 |
| 接受重送覆寫的簡單方案 | `01a14af3-7a03-7922-82e9-9999e0ca5eb7` | 17:40:32.869 | 17:41:01.447 |

## 回答與篇幅

| 案例 | 題目 | 完整回答 | 正文字元 |
|---|---|---|---|
| CSV 匯入 | [材料與問題](csv/input.md) | [原文](csv/answer.md) | 301 |
| 租戶資料隔離 | [材料與問題](security/input.md) | [原文](security/answer.md) | 321 |
| 過載與受理 | [材料與問題](overload/input.md) | [原文](overload/answer.md) | 296 |
| 接受重送覆寫的簡單方案 | [材料與問題](complete/input.md) | [原文](complete/answer.md) | 327 |

計數依受測 skill，排除空白與 Markdown 排版標記，保留正文識別字的底線。四份最終回答均以繁體中文、三個條列呈現，符合 250–400 字元，沒有客套話或開場白。第四案執行過程另有一則讀取後進度說明，保留於本機工具紀錄，未計入 final_answer 篇幅。

## 檔案識別與核對

下表為各案固定內容的 SHA-256：

| 檔案 | SHA-256 |
|---|---|
| [前三案受測 SKILL.md](skill-snapshot.md) | `8E4E3F6A01A087B058C5D0AC296AC4574A61A92C9417CB2B406149D5BC95C399` |
| [第四案受測 SKILL.md](language/skill-snapshot.md) | `6DA793818BB33EB18A9E77E4854EB7E16D1D63AE7149E8BCC038C5AF8A81A7AF` |
| [csv/input.md](csv/input.md) | `76A8B5B2806D8F7B3EF388867C8805F09FADC3D17005607596113FD5FAFA8069` |
| [csv/answer.md](csv/answer.md) | `FED135853E34A235608AAF7E8DD1204914DC1464B107EB9D88FD3EC225D674AF` |
| [security/input.md](security/input.md) | `E17079F30AB7ACB359DD9AEC96BD785A16A1C0D0D8BE70E99C28BDFD457E2D3D` |
| [security/answer.md](security/answer.md) | `A114BB314F8E4DED5FD5D6A07B69A25D7ADBB8B6B99C3E5F78FF46B9503DC341` |
| [overload/input.md](overload/input.md) | `8548B7C81D32CAEFCCE1881EBAB06480A792B14D649C7BA93BD97BB6DAF0A6D9` |
| [overload/answer.md](overload/answer.md) | `2D0E9CAAD2AF8D50A232A56870DF6EFC3469A4E1BC8C61564E17C36A182F17D2` |
| [complete/input.md](complete/input.md) | `DB86977F3E676591BD32619E86E6361F729D41EE43FF45700E74EE84C29C5B28` |
| [complete/answer.md](complete/answer.md) | `9259ED958B9987D06385511CE8CCB64C0CA45FEA16F838F42F19963227C85362` |
| 前三案當時封裝 ZIP（保存在本機原始紀錄） | `08B77FFD5D565963742F9B3C265A245CDDC5DC7815AE5E04CB039BD999199D2D` |
| 第四案當時封裝 ZIP | `3389F295DE3A6FC94775AE3449F2D45CC4E077EF74F4B4622E74099558D7FCCE` |

前三案當輪封裝重建、成品檢查、五項封裝單元測試、官方 quick_validate 與 git diff --check 通過；受測快照、當時成品與 ZIP 內容一致。

第四案的受測快照、成品與 ZIP 內的 SKILL.md 內容一致。代理只執行兩次 `Get-Content -Raw`，讀取題目與快照。公開題目與回答逐位元組複製自本機原始紀錄；回答與 session 的 final_answer 及 task_complete 原文一致。

完整工具呼叫與結果、派送與接收紀錄、檔案識別及唯讀核對清單保留於本機：

- 前三案：`experiments/restored-methods-four-cases-2026-10-17/`，另含過載案的接續紀錄與前版比較。
- 第四案：`experiments/accepted-overwrite-single-case-2026-10-18/`，包含派送前評估計畫、凍結紀錄及 `transcript.jsonl`。
