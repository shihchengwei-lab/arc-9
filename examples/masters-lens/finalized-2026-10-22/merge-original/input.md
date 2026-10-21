# 任務
審查目前版本的檔案下載與刪除：授權的對象是否就是實際操作的對象？哪些改動建議仍有必要？

# 已確認的承諾與範圍
下載必須具有實際檔案的read權限；刪除必須具有實際檔案的delete權限。兩個權限獨立決定。不能用對A的權限讀取或刪除B。
檔案ID及storage_key由服務持有；同一次操作期間映射不變。以下handle直接指向該檔案，操作期間不會改指別的檔案。沒有其他本次需要審查的解析、並行或權限變動條件。

# 既有版本
下載入口收route_file_id和body_storage_key。先依route_file_id取得檔案A並檢查read權限，再開啟body_storage_key的檔案；使用者能獨立指定兩個值。
刪除入口收route_file_id和body_delete_file_id。先依route_file_id取得檔案A並檢查delete權限，再刪除body_delete_file_id所指的檔案；使用者能獨立指定兩個值。
既有測試身分U對A有read和delete，對B兩者都沒有。既有版本中，route指A、body指B時，下載取得B，刪除也會刪除B。

# 目前版本
兩個入口都維持既有版本。

# 驗證紀錄
上述U仍能以A通過授權而對B操作。
