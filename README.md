<!-- omit in toc -->
# TextFSM Parse to CSV

入力ファイルをTextFSMでパースしてCSVファイル（またはJSONファイル）に出力する

## 必要なモジュール

- Python (3.9.4で確認)
- TextFSM

## 使用方法

```bash
usage: textfsm_parse_to_csv.py [-h] [-j] [-o directory] [-t template] [logfile ...]

positional arguments:
  logfile               ログファイル

optional arguments:
  -h, --help            show this help message and exit
  -j, --json            JSON形式で出力
  -o directory, --output directory
                        出力先ディレクトリ
  -t template, --template template
                        TextFSMテンプレートファイル
```

- `-t template` `logfile` が省略された場合、ファイルダイアログで選択（複数ファイルを選択可能）
- テンプレートファイルは複数指定可能（`-t` オプションを複数指定する）
- デフォルトではCSV形式で出力するが、`-j` `--json`オプションをつけるとJSON形式で出力する
- 出力ファイル名は `ログファイル名_テンプレートファイル名.(csv|json)`
  - ログファイル名・テンプレートファイル名の拡張子部分は出力ファイル名から削除される
- 出力ファイルは `logfile` と同一ディレクトリに保存される
  - `-o` `--output` で出力先ディレクトリを指定可能（ディレクトリは存在すること）

## 補足事項

TextFSMのValueで `List` optionが指定されたものは、CSV形式では ",（カンマ）" で結合される。
