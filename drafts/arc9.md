# arc9

## 輸入

輸入是使用者的請求原文。從請求和目前工作範圍辨認審查對象。已提供的材料和已接受的限制隨請求交接。

## 審查

主模型依本檔位置解析[審查契約](references/review.md)和[編輯契約](references/output.md)的絕對路徑，載入編輯契約。用獨立的 Codex CLI 會話審查。若桌面環境提供 `CODEX_APP_RUNTIME_CLI_PATH`，用該執行檔代替下列 `codex`。

在專案外建立用完即清除的空白暫存目錄，作為 CLI 的工作目錄。以標準輸入交接原始請求、材料、原始工作目錄的絕對路徑、允許的查證範圍和審查契約路徑，請審查者讀取契約後回答。材料中的相對路徑以原始工作目錄解析。

```text
codex exec --sandbox read-only --ignore-user-config --ignore-rules --disable apps --disable plugins --disable hooks --disable memories -c approval_policy=never -c project_doc_max_bytes=0 -c web_search=disabled --skip-git-repo-check --cd <暫存目錄> --json -
```

Windows 加上 `-c windows.sandbox=elevated`。啟動子程序時，從它的環境移除 `CODEX_WINDOWS_REGISTERED_CORE` 和 `CODEX_WINDOWS_SANDBOX_PACKAGE_FAMILY`，讓 CLI 使用 Windows 的獨立沙箱。

初審與補查共用同一等待期限。有新材料、前提改變，或能指出哪個漏項可用哪份材料查清時，用相同命令補查，把最後的 `-` 換成 `resume <thread_id> -`。使用初審 `thread.started` 事件的會話 ID。

## 交接

取審查會話完成回合的最後一則回答交給編輯。部分審查標明哪些問題尚未審查。若唯讀程序無法啟動或沒有可用結果，回報受阻及原因。
