<!-- omit in toc -->
# TextFSM Parse to CSV

入力ファイルをTextFSMでパースしてCSVファイル（またはJSONファイル）に出力する

## 必要なモジュール

- TextFSM

Python3.10 以上が必要

## 使用方法

```bash
usage: textfsm_parse_to_csv.py [-h] [-j] [-o directory] [-t template] [logfile ...]

positional arguments:
  logfile               target logfiles

options:
  -h, --help            show this help message and exit
  -j, --json            Output in JSON Format
  -o directory, --output directory
                        Output directory
  -t template, --template template
                        TextFSM Template
```

- `-t template` および `logfile` が省略された場合、ファイルダイアログで選択（複数ファイルを選択可能）
- テンプレートファイルは複数指定可能（`-t` オプションを複数指定する）
- デフォルトではCSV形式で出力するが、`-j` `--json`オプションをつけるとJSON形式で出力する
- 出力ファイル名は `ログファイル名_テンプレートファイル名.(csv|json)`
  - ログファイル名・テンプレートファイル名の拡張子部分は出力ファイル名から削除される
- 出力ファイルは `logfile` と同一ディレクトリに保存される
  - `-o` `--output` で出力先ディレクトリを指定可能（ディレクトリは存在すること）
- テンプレートファイル名とログファイル名はワイルドカード指定可

## 補足事項

TextFSMのValueで `List` optionが指定されたものは、CSV形式では ",（カンマ）" で結合される。
