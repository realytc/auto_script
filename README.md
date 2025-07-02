## 📍 Repo 目的

試作 ACY 網站的註冊驗面自動化測試。

## 📜 Command Line 說明

1. 對終端機下指令 `pytest 目錄/檔案` 會自動加上`-sv` 參數，告訴 pytest 回報詳細的測試結果並列出打印的關鍵資料。
   - 若要移除預設參數，可至 _pytest.ini_ 初始檔，移除設定`addopts= -sv`。
   - `-s` 表示終端機會顯示 `print()` 資料。
   - `-v` 表示終端機會顯示測試詳情與錯誤內容。
2. 環境參數 `--env=uat` 與 `--env=prod`，可切換執行環境。
   - 預設執行環境為 `UAT`。
   - 指令範例: `pytest --env=prod tests/test_register_reg` 表示在 `PROD`環境執行腳本。
   - 相關代碼在 _configs.py_ 和 _conftest.py_。
3. 裝置參數，可切換執行裝置。
   - 預設執行裝置為 `desktop`。
   - 指令範例: `pytest --device=mobile`。
   - 參數選項： desktop / mobile / tablet
   - 相關代碼在 _configs.py_

## 🔢 檢閱測試覆蓋率報告

1. 下載 pytest-cov 套件，下載指令 `pip install pytest-cov`
2. 執行腳本時，對終端機下指令 `pytest --cov --cov-report=html 目錄/檔案` 執行測試。
   - 範例: `pytest --cov --cov-report=html tests/test_register_reg.py`。
3. pytest 會更新 _.coverage_ 檔案與 _htmlcov_ 目錄和檔案，若皆無會自動創建。
4. 進入 _htmlcov_ 目錄，桌面打開 _index.html_(或~.html)的檔案，可檢視測試覆蓋率。

## 📖 檢閱報錯日誌

1. 每次執行測試後，會 **自動儲存 pytest 報錯內容**。
   - 自動建立 `error_log` 目錄（若已存在，則不重複建立）。
   - 在該目錄下建立 `error_執行時間.log` 檔案。
   - 可使用記事本或任何文字編輯器開啟 `.log` 檔，檢視錯誤日誌。
   - 功能設定於 `conftest.py`。

2. 每次執行測試後，會 **自動儲存執行 log 內容**。
   - 自動建立 `log` 目錄（若已存在，則不重複建立）。
   - 每次執行會產生帶有當日時間戳的獨立 log 檔。
   - 當日執行多次，log都會新增在同一檔案中。
   - 可使用記事本開啟 `.log` 檔，檢視詳細執行過程。


`<參考>`: https://docs.pytest.org/en/stable/reference/reference.html#pytest.hookspec.pytest_runtest_makereport

## 📁 專案目錄結構

```
auto_test/                                 # 專案根目錄
├── __pycache__/                           # Python執行時產生的快取
├── .idea/                                 # PyCharm專案設定資料夾
├── .pytest_cache/                         # pytest執行後的快取資料
├── error_log/                             # 自訂錯誤日誌輸出目錄
├── htmlcov/                               # coverage執行產生的HTML報告
├── pages/                                 # Page Object 模組
│   ├── __pycache__/                       # pages快取
│   ├── __init__.py                        # 讓 pages 成為Python套件
│   └── register.py                        # 註冊頁的Page Object
├── tests/                                 # 測試腳本和設定
│   ├── __pycache__/                       # tests快取
│   ├── configs.py                         # 環境設定、測試資料
│   ├── conftest.py                        # pytest fixture配置
│   └── test_register_reg.py               # 註冊頁測試案例
├── utils/                                 # 共用工具
│   ├── __pycache__/                       # utils快取
│   └── logger.py                          # 自訂logger封裝
├── venv/                                  # Python虛擬環境
├── .coverage                              # coverage執行結果檔
├── .gitignore                             # git忽略規則
├── pytest.ini                             # pytest全域設定

```
