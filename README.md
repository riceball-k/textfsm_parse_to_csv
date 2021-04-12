TextFSM Parse to CSV
====================

入力ファイルをTextFSMでパースしてCSVファイルに出力するだけの汎用プログラム

前提
----

textfsmをインストールしておくこと

```
> pip install textfsm
>
```

使用方法
--------

```
> textfsm_parse_to_csv.py [-h] [template] [logfile [logfile ...]]
```

- `logfile`が省略された場合、ファイルダイアログで選択（複数ファイル選択可能）
- `template`も省略された場合、ファイルダイアログで選択（1つだけ選択可能）
  - `template`選択後、`logfile`をファイルダイアログで選択する。
- 出力ファイル名は `ファイル名_yyyymmdd_hhmmss.csv`
  - `logfile`と同一ディレクトリに出力する。

補足事項
--------

`List`optionが指定された`Value`については、",(カンマ）"で結合して出力する。
