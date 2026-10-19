# arc9：六個契約狀態的執行紀錄

[題目與完整回答](cases.md) · [案例索引](README.md)

## 受測版本

測試日期：2026-10-19。測前版本庫 HEAD 為 `e8bd262caf2ad2a2b3b15ecf1382c176c97625ae`；實際受測內容取自當時工作目錄，以快照識別。

| 版本 | 受測快照 | SHA-256 |
|---|---|---|
| 前版 | [SKILL.md](../skill-snapshot.md) | `A39570883F8A697F2D524686E9DEB72E2A980ECFA1B769C310DDE9D1D4DAB5E9` |
| 新版 | [SKILL.md](skill-snapshot.md) | `DA65836AB5297C659503F93B2752B789281D670D0A36B8DD434D57CF8A5D2B1C` |

新版修改兩處共用內容：將任務承諾與事實依據的更新來源分開；合併同一成因的發現時，保留各項判斷的依據、適用候選與前提。

## 題目與預期關係

六個狀態於推論前固定。報表組維持相同實作與 45 秒量測，改變實作備註或任務指定規格；檔案組維持相同權限條件，逐步修正下載與刪除的對象綁定。題目中的實作與驗證紀錄是提供給模型的材料。

| 狀態 | 測前預期關係 | 前版 | 新版 |
|---|---|---|---|
| [authority-base](cases.md#authority-base) | 仍以 R1 的 30 秒判定不符合。 | 通過 | 通過 |
| [authority-memo](cases.md#authority-memo) | 實作備註不改變指定規格，仍不符合。 | 通過 | 通過 |
| [authority-authorized](cases.md#authority-authorized) | 本次指定 R2，以 60 秒判定符合。 | 通過 | 通過 |
| [merge-original](cases.md#merge-original) | 保留下載與刪除兩項問題及各自權限。 | 通過 | 通過 |
| [merge-read-fixed](cases.md#merge-read-fixed) | 下載已修正，只保留刪除缺陷。 | 通過 | 通過 |
| [merge-both-fixed](cases.md#merge-both-fixed) | 對象綁定問題已消除，不保留舊缺陷。 | 通過 | 通過 |

兩版均符合六個狀態的預期關係，本次未測出兩處文字修改帶來的行為改善。兩版在全部修正後皆不保留舊缺陷；新版另建議補測只有 read 或只有 delete 的身分，並明確區分為驗證補強。

## 派送與執行

使用 Codex CLI 0.159.1，模型 `gpt-6.1-sol`、推理設定 `xhigh`。每個狀態分別輸入獨立對話；同狀態的兩版題目相同，只替換嵌入的 skill 全文。版本順序交錯，各狀態、各版本一次，共 12 次。各次 exit code 均為 0。

派送格式如下；語言、篇幅與輸出格式由 skill 提供。

```text
請使用本訊息提供的 arc9 審查指示，回答案例中的問題。

【arc9 審查指示】
<該版本的受測 skill 全文>

【案例材料與問題】
<該狀態的完整題目>
```

原生執行檔後接下列共用引數，再接 `--output-last-message <回答檔路徑> -`；派送全文由標準輸入送入。

```json
[
  "exec",
  "--ignore-user-config",
  "--ephemeral",
  "--json",
  "--color",
  "never",
  "--model",
  "gpt-6.1-sol",
  "--sandbox",
  "read-only",
  "--skip-git-repo-check",
  "--cd",
  "C:\\Users\\kk789\\Desktop\\masters-lenses\\experiments\\contract-flow-six-cases-2026-10-19\\run-cwd",
  "-c",
  "model_reasoning_effort=\"xhigh\"",
  "-c",
  "project_doc_max_bytes=0",
  "-c",
  "web_search=\"disabled\"",
  "-c",
  "approval_policy=\"never\"",
  "--enable",
  "skip_host_skill_discovery",
  "--disable",
  "apps",
  "--disable",
  "plugins",
  "--disable",
  "hooks",
  "--disable",
  "memories",
  "--disable",
  "skill_search",
  "--disable",
  "multi_agent",
  "--disable",
  "shell_tool",
  "--disable",
  "view_image",
  "--disable",
  "image_generation",
  "--disable",
  "code_mode_host",
  "--disable",
  "browser_use",
  "--disable",
  "computer_use"
]
```

執行期間停用使用者設定、其他 skills、記憶、工具、網路與 hooks。每次均收到兩則啟動訊息，分別涉及 `skip_host_skill_discovery` 與停用的 code-mode host，原文保存於事件紀錄；12 次均有 `turn.completed`，沒有 `turn.failed`、頂層執行錯誤或工具呼叫。

下表依實際執行順序排列；時間為 UTC。

| 狀態 | 版本 | 開始 | 結束 | thread ID |
|---|---|---|---|---|
| authority-base | previous | 2026-10-19T06:55:19.143377+00:00 | 2026-10-19T06:55:50.966246+00:00 | `01a152f1-790e-7683-86b5-e2365d2f1194` |
| authority-base | current | 2026-10-19T06:55:50.968396+00:00 | 2026-10-19T06:56:20.814014+00:00 | `01a152f1-f527-7903-8743-a6f7f6003ff1` |
| authority-memo | current | 2026-10-19T06:56:20.815932+00:00 | 2026-10-19T06:56:47.586652+00:00 | `01a152f2-69b9-78f0-9571-1d3c0a0cc2c8` |
| authority-memo | previous | 2026-10-19T06:56:47.587567+00:00 | 2026-10-19T06:57:20.572337+00:00 | `01a152f2-d24e-72d0-b4b4-5a40f5bb812d` |
| authority-authorized | previous | 2026-10-19T06:57:20.574311+00:00 | 2026-10-19T06:57:35.015092+00:00 | `01a152f3-531a-7e21-9856-0922bc5d879c` |
| authority-authorized | current | 2026-10-19T06:57:35.017090+00:00 | 2026-10-19T06:58:01.915099+00:00 | `01a152f3-8b90-7872-a617-e67b8312a80a` |
| merge-original | current | 2026-10-19T06:58:01.917095+00:00 | 2026-10-19T06:58:52.378728+00:00 | `01a152f3-f4aa-75b3-96fc-a3d88fa9c006` |
| merge-original | previous | 2026-10-19T06:58:52.380644+00:00 | 2026-10-19T06:59:26.964808+00:00 | `01a152f4-b9df-7831-9b8e-c7b5eb065eeb` |
| merge-read-fixed | previous | 2026-10-19T06:59:26.966199+00:00 | 2026-10-19T06:59:54.591609+00:00 | `01a152f5-40d4-7460-a241-dbceddc7958b` |
| merge-read-fixed | current | 2026-10-19T06:59:54.594529+00:00 | 2026-10-19T07:00:25.219372+00:00 | `01a152f5-acd0-7130-90ec-4b14a15da46d` |
| merge-both-fixed | current | 2026-10-19T07:00:25.221374+00:00 | 2026-10-19T07:01:04.459770+00:00 | `01a152f6-2478-7781-9a2b-de9438b63696` |
| merge-both-fixed | previous | 2026-10-19T07:01:04.460762+00:00 | 2026-10-19T07:01:32.339035+00:00 | `01a152f6-bdb3-70f3-8ca3-16bd842e16e8` |

主代理依測前預期關係閱讀完整回答判定。12 份回答均為繁體中文、250–400 個非空白正文字元、三個條列，沒有開場或中途訊息，未逐位列出大師。

## 用量

| 狀態 | 版本 | 輸入 token | 快取輸入 | 輸出 token | 其中推理 token | 秒 | 正文字元 |
|---|---|---:|---:|---:|---:|---:|---:|
| authority-base | previous | 13894 | 0 | 1096 | 801 | 31.812 | 322 |
| authority-base | current | 13946 | 0 | 1122 | 858 | 29.844 | 285 |
| authority-memo | previous | 13945 | 0 | 1224 | 948 | 32.985 | 302 |
| authority-memo | current | 13997 | 0 | 987 | 712 | 26.765 | 294 |
| authority-authorized | previous | 13945 | 0 | 910 | 630 | 14.437 | 302 |
| authority-authorized | current | 13997 | 0 | 1059 | 791 | 26.906 | 293 |
| merge-original | previous | 14055 | 0 | 1297 | 1034 | 34.578 | 352 |
| merge-original | current | 14107 | 9856 | 1828 | 1552 | 50.469 | 368 |
| merge-read-fixed | previous | 14130 | 0 | 1020 | 754 | 27.625 | 344 |
| merge-read-fixed | current | 14182 | 0 | 1268 | 1002 | 30.625 | 313 |
| merge-both-fixed | previous | 14191 | 9856 | 1041 | 754 | 27.875 | 329 |
| merge-both-fixed | current | 14243 | 0 | 1430 | 1169 | 39.25 | 313 |

| 合計 | 前版 | 新版 |
|---|---:|---:|
| 輸入 token | 84160 | 84472 |
| 快取輸入 token | 9856 | 9856 |
| 輸出 token（含推理） | 6588 | 7694 |
| 推理 token | 4921 | 6084 |
| 輸入＋輸出 token | 90748 | 92166 |
| 執行秒數 | 169.312 | 203.859 |

輸出 token 已包含推理 token，快取輸入為輸入 token 的一部分。新版輸入加輸出為 92,166，前版為 90,748；這次單次觀察增加 1.6%。

## 檔案識別與原始紀錄

當次封裝 ZIP SHA-256：`873869BFD60A62EBC3BAD8FA34128424FC1B95DD004702C0E75823688CE0BE82`；其中 SKILL.md 與新版受測快照一致。

本機原始資料位於 `experiments/contract-flow-six-cases-2026-10-19/`：

- `frozen.json`、`expected.json`：測前固定的材料雜湊、執行順序與預期關係。
- `attempts.jsonl`：12 次實際指令、時間與結束狀態。
- 各狀態目錄的 `input.md`、`previous-prompt.txt`、`current-prompt.txt`、兩版 `*-answer.md`、`*-events.jsonl`、`*-stderr.txt` 與 `*-result.json`：題目、派送全文、回答及原始執行輸出。
- `assessment.json`、`results.json`、`final-verification.json`、`execution.md`：判定引句、用量、檔案核對與結果。
- `previous-skill.md`、`current-skill.md`、`run_once.py`、`summarize.py`：受測內容及當次執行、彙整腳本。

測前 `frozen.json` SHA-256：`2623B670708B91A71A6133B86D54B6529D46E8BF45A657CC4603592CA2CA740D`。
測前 `expected.json` SHA-256：`2C19B0358CDAA0DC6F96A030CF89A81898363DE59888C2AC3F5F379CA88CF95A`。

公開題目與兩版回答收錄於 [cases.md](cases.md)，以原文嵌入，僅增加章節與排版；下表雜湊識別原始 UTF-8 檔案的完整位元組。

| 狀態 | 原始檔案 | SHA-256 |
|---|---|---|
| authority-base | `input.md` | `CEC0717F97B81810DE71CC2B17152B52B51EF0D8884AB1AF7AF1BA038405809E` |
| authority-base | `previous-answer.md` | `4A90CD1A4956AFE28DD3038B61F9ADB409B32738F28342BB918FCADE174ED0C8` |
| authority-base | `current-answer.md` | `19DBE156D8674A886789833188815DB9ABEA377698F93CE7A0F66D023A64FE7E` |
| authority-base | `previous-prompt.txt` | `516DABF31178873EBB623D14B6288DB97A21E6054D47D69D12AA1CBA5CAA37F6` |
| authority-base | `current-prompt.txt` | `D5577686E93E886A855F4A3D2DD3AC7D42EE92BA4F469FF56955410656870284` |
| authority-memo | `input.md` | `848B4482A034B0054CF7DB1A13D5F61F80F00D3DC835434E6D793B77039153AF` |
| authority-memo | `previous-answer.md` | `0E0785C5EFA7E308A70788D891AAF0B08451C23F891B5E66CE7144585F5BA4A0` |
| authority-memo | `current-answer.md` | `8E5FDFEAFC29B354FCA4F095815078C9CFD2CBC0CEFDFE51CBA5AD148B956C6F` |
| authority-memo | `previous-prompt.txt` | `73555D692A83F44123CF54C3D2BCAF80325158835CC0E3D8BC7B0ABFAB1DCCF6` |
| authority-memo | `current-prompt.txt` | `0FE15AE8F8238DEA60C58AD6051DD30347BF745097FD3EF43E27AE5CF23AF228` |
| authority-authorized | `input.md` | `F2941BF05F451BBA43A3B249A3CCC3E94FB9493DC28FB57AD811885A22E08117` |
| authority-authorized | `previous-answer.md` | `0A5F63F01CB31936DD91A825CA6947B72417D6F7ECAC6FCD941DFDA3A02A8FEB` |
| authority-authorized | `current-answer.md` | `BDE5F4A5606BB40FCD46976FE24B27176F7416487C63DEE633CB0D030BABB359` |
| authority-authorized | `previous-prompt.txt` | `BB915254663658C82E5B1CC266C521D9A03F68115000CDD69A46EBEE1451926C` |
| authority-authorized | `current-prompt.txt` | `AB6F0A53C2E7BF0C77ED1161E0479813C545B38A57B540EB939CC18E8B6067D0` |
| merge-original | `input.md` | `4D14EA32509AD8A8D0F476F3FDA20D6556604AA3A8941A24186B18E41B775B43` |
| merge-original | `previous-answer.md` | `2558801DC02AEBF02B895D18C5C81440925896D1C8FA7D4AD9C7472871726B82` |
| merge-original | `current-answer.md` | `333CE8BDA3A32545307E0591A4EFFC755349F6CC2303AC58A95491B2F2C5AA50` |
| merge-original | `previous-prompt.txt` | `57E93BA9065E814F38BB3222C148A960806B223D8F10E94D6FF4BC32404B0681` |
| merge-original | `current-prompt.txt` | `B2DBB9F6F3BD94547670EB816BDB6ED7A6944EBBF3230B3E9CD5B0617901165A` |
| merge-read-fixed | `input.md` | `5D5A0292651B48912F5BB7FB1BEC10580566A87141F125F878C87A2276ED62D0` |
| merge-read-fixed | `previous-answer.md` | `2F062B0CF50710C29B99C4CDD8873E2B43DC3CCD81922AE5B8911D189900AE60` |
| merge-read-fixed | `current-answer.md` | `18F61C089B60E765163E47D83E613C811D9EC07E28B528C6C1AFE47D89C53104` |
| merge-read-fixed | `previous-prompt.txt` | `5DC57B5AE6F515CAB62B3FC6FEB416FBFDAA94134BB9970ED7D48A9C7D477ED6` |
| merge-read-fixed | `current-prompt.txt` | `5100B871FA0A1B1D3FD01270FCE3399F6FB413BE333284F149CEB45734029AF7` |
| merge-both-fixed | `input.md` | `15EF66201C3A301C853DCBD081E9979BEB94C8D5FB2D2662770F1372E5733BD2` |
| merge-both-fixed | `previous-answer.md` | `CAEB20243972151E825162F49E15C709611A5C4033D635418C5AE5E9E484C31A` |
| merge-both-fixed | `current-answer.md` | `DF355BC6EBB4380E509195A1C812D404092EF5D96248A34A8CD17E8D6433466F` |
| merge-both-fixed | `previous-prompt.txt` | `AC5B8D0A7C13D46AD3071D322585641BFC2CCB6EE628208432BCA30267C6BE77` |
| merge-both-fixed | `current-prompt.txt` | `86D22B3FF3590E9B425EDFAB28D447995304A1709D4D47C78217EE71C5E61398` |

測試結束時，22 份凍結材料、31 份受版本控制檔案與三份安裝檔案均與測前相同。當時工作目錄已有來源與封裝的三項未提交變更。這輪測試使用獨立狀態輸入，未接續前一狀態的對話歷史。
