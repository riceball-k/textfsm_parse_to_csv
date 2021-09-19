import argparse
# import configparser
import csv
import glob
import json
import sys
import tkinter
import tkinter.filedialog as fd
import tkinter.messagebox as messagebox
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional, Union

import textfsm
from itertools import product


def read_argument() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--json', action='store_true',
                        help='JSON形式で出力')
    parser.add_argument('-o', '--output', metavar='directory', type=Path,
                        help='出力先フォルダ')
    parser.add_argument('-t', '--template', metavar='template',
                        action='append',
                        help='TextFSMテンプレートファイル')
    parser.add_argument('logfile', nargs='*',
                        help='ログファイル')
    return parser.parse_args()


class LogFile:
    """ログファイル管理クラス
    """

    def __init__(self, file: Path):
        self.file: Path = file
        try:
            with file.open('rt', encoding='utf-8') as f:
                self._read_data: str = f.read()
        except Exception as e:
            messagebox.showerror('ファイル読込エラー',
                                 f'"{file.name}"\n\n{str(e)}')
            sys.exit()

    def parse(self, template: Path, path: Optional[Path] = None,
              to_json: bool = False) -> None:
        """ファイルのパース結果をファイル出力する

        Args:
            template (Path): TextFSMテンプレートファイル
            path (Optional[Path], optional): 出力先ディレクトリ. Defaults to None.
            to_json (bool, optional): TrueならJSON形式、False（デフォルト）ならCSV形式で出力
        """
        # テンプレート読み込み
        try:
            with template.open('rt', encoding='utf-8') as f:
                table = textfsm.TextFSM(f)
        except Exception as e:
            messagebox.showerror('テンプレートエラー',
                                 f'"{template.name}"\n\n{str(e)}')
            sys.exit()

        # outputファイル名作成
        if path is None:
            path = self.file.parent
        output = path / (f'{self.file.stem}_{template.stem}' +
                         datetime.now().strftime('_%Y%m%d_%H%M%S'))

        # パース実行
        parse_data: Union[List[dict], List[Any]]
        try:
            if to_json:
                # DICT形式でパースしてJSONファイルを出力する
                parse_data = table.ParseTextToDicts(self._read_data)
                output = output.with_suffix('.json')
                with output.open('wt', encoding='utf-8') as f:
                    json.dump(parse_data, f, indent=4)
            else:
                # リスト形式でパースしてCSVファイルを出力する
                parse_data = table.ParseText(self._read_data)
                output = output.with_suffix('.csv')
                with output.open('wt', encoding='utf-8', newline='') as f:
                    csvfile = csv.writer(f)
                    csvfile.writerow(table.header)
                    for row in parse_data:
                        csvfile.writerow(
                            [','.join(col) if type(col) is list else col
                                for col in row]
                        )
        except Exception as e:
            messagebox.showerror('ファイル出力エラー',
                                 f'"{output.name}"\n\n{str(e)}')
            sys.exit()

        print(f'output: "{output.absolute()}"')


if __name__ == '__main__':
    tkinter.Tk().withdraw()
    args = read_argument()

    # 出力先ディレクトリ名取得
    if args.output:
        if not all((args.output.exists(), args.output.is_dir())):
            messagebox.showerror('出力先エラー',
                                 f'出力先ディレクトリがありません\n"{args.output}"')
            sys.exit()

    # テンプレートファイル名取得
    if args.template:
        template_filenames = args.template
    else:
        template_filenames = fd.askopenfilenames(
            title='テンプレートファイルを選択（複数選択可）',
            filetypes=[('テンプレート', '*.textfsm;*.template'), ('すべて', '*.*')],
            initialdir='.',
        )
        if template_filenames == '':
            sys.exit(0)

    # ログファイル名取得
    if args.logfile:
        log_filenames = []
        for name in args.logfile:
            if Path(name).exists():
                log_filenames.append(name)
            else:
                log_filenames.extend(glob.glob(name))
        if not log_filenames:
            messagebox.showerror('ファイル読込エラー',
                                 'ログファイルがありません')
            sys.exit()
    else:
        log_filenames = fd.askopenfilenames(
            title='ログファイルを選択（複数選択可）',
            filetypes=[('ログファイル', '*.log'), ('すべて', '*.*')],
            initialdir='.'
        )
        if log_filenames == '':
            sys.exit()

    # 処理実行
    for i, (logfile, template) in enumerate(
            product((Path(fname) for fname in log_filenames),
                    (Path(fname) for fname in template_filenames)), 1):
        LogFile(logfile).parse(template=template, path=args.output,
                               to_json=args.json)

    messagebox.showinfo('正常終了', f'完了\n{i} ファイル出力')
