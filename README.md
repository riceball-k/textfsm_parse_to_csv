TextFSM Parse to CSV
====================

入力ファイルをTextFSMでパースしてCSVファイル（またはJSONファイル）に出力する

必要なモジュール
----------------

- Python (3.9.4で確認)
- TextFSM

使用方法
--------

```bash
usage: textfsm_parse_to_csv.py [-h] [-j] [template] [logfile ...]

positional arguments:
  template    textfsmテンプレートファイル
  logfile     ログファイル

optional arguments:
  -h, --help  show this help message and exit
  -j, --json  JSON形式で出力
```

- `logfile`が省略された場合、ファイルダイアログで選択（複数ファイル選択可能）
- `template`も省略された場合、ファイルダイアログで選択（1つだけ選択可能）
  - `template`選択後、`logfile`をファイルダイアログで選択する。
- 出力ファイル名は `ファイル名_yyyymmdd_hhmmss.(csv|json)`
  - `logfile`と同一ディレクトリに出力する。

補足事項
--------

CSVで出力する場合、`List`optionが指定された`Value`については、",（カンマ）"で結合して出力する。
