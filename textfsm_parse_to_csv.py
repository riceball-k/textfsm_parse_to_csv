import argparse
import csv
import json
import re
from collections.abc import Iterable
from datetime import datetime as dt
from glob import glob
from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
from tkinter.messagebox import showerror, showinfo
from typing import Any

from textfsm import TextFSM, TextFSMTemplateError

wildcard = re.compile(r"[*?]|\[.+?\]")


class DirNotFoundError(FileNotFoundError):
    pass


class Abort(Exception):
    pass


class Glob:
    """重複排除に対応したGlobクラス"""

    def __init__(self, pattern: str | Iterable[str]):
        self.files = set()  # 生成済みフルパスファイル名の集合
        if isinstance(pattern, str):
            self.pattern = (pattern,)
        else:
            self.pattern = pattern
        # patternの妥当性確認
        for path in self.pattern:
            if not (Path(path).is_file() or wildcard.search(path)):
                raise FileNotFoundError(f"file not found: '{path}'")

    def is_new_file(self, file: Path):
        """未生成のファイル名ならTrue"""
        if (absolute := file.absolute()) not in self.files:
            self.files.add(absolute)
            return True
        else:
            return False

    def __iter__(self):
        """重複を排除したフルパスファイル名イテレータ"""
        self.files.clear()
        for path in self.pattern:
            if (file := Path(path)).is_file():
                if self.is_new_file(file):
                    yield file
            else:
                for file in map(Path, glob(path, recursive=True)):
                    if self.is_new_file(file):
                        yield file


def read_argument():
    """コマンドライン引数の読み込み"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-j", "--json", action="store_true", help="Output in JSON Format"
    )
    parser.add_argument(
        "-o", "--output", metavar="directory", type=Path, help="Output directory"
    )
    parser.add_argument(
        "-t", "--template", metavar="template", action="append", help="TextFSM Template"
    )
    parser.add_argument("logfile", nargs="*", help="target logfiles")
    args = parser.parse_args()

    # コマンドラインオプションのチェック
    if args.output:
        if not (args.output.exists() and args.output.is_dir()):
            raise DirNotFoundError(f"directory not found: '{args.output}'")
    if args.template:
        Glob(args.template)
    if args.logfile:
        Glob(args.logfile)

    return args


def select_file(args: argparse.Namespace):
    # テンプレートファイル選択
    if not args.template:
        Tk().withdraw()
        args.template = askopenfilenames(
            title="テンプレートファイルを選択（複数選択可）",
            filetypes=[("テンプレート", "*.textfsm;*.template"), ("すべて", "*.*")],
            initialdir=".",
        )
        if not args.template:
            raise Abort

    # ログファイル選択
    if not args.logfile:
        Tk().withdraw()
        args.logfile = askopenfilenames(
            title="ログファイルを選択（複数選択可）",
            filetypes=[("ログファイル", "*.log"), ("すべて", "*.*")],
            initialdir=".",
        )
        if not args.logfile:
            raise Abort


def to_str(text: str | Iterable[str]):
    return text if isinstance(text, str) else ",".join(text)


class LogFile:
    """ログファイル管理クラス"""

    def __init__(self, file: Path):
        self.file = file
        self.option = dict(encoding="ascii", errors="surrogateescape")
        self.text = file.read_text(**self.option)

    @property
    def name(self):
        return str(self.file)

    def parse(self, template: Path, output_dir: Path | None = None, to_json=False):
        """ファイルのパース結果をファイル出力する

        Args:
            template (Path): TextFSMテンプレートファイル
            path (Path | None): 出力先ディレクトリ、Noneなら
            to_json (bool, optional): True...JSON形式、False...CSV形式
        """
        # パース
        try:
            with template.open("r", encoding="utf-8") as f:
                fsm = TextFSM(f)
            table: list[dict[str, Any]] = fsm.ParseTextToDicts(self.text)
        except TextFSMTemplateError as e:
            raise TextFSMTemplateError(f"'{template.name}'\n\n{e}")

        # outputファイル名作成
        filename = self.file.stem + dt.now().strftime(f"_{template.stem}_%Y%m%d_%H%M%S")
        if output_dir is None:
            output_file = self.file.parent / filename
        else:
            output_file = output_dir / filename

        # ファイル出力
        if to_json:
            # JSON形式
            output_file = output_file.with_suffix(".json")
            output_file.write_text(json.dumps(table, indent=4), **self.option)
        else:
            # CSV形式
            output_file = output_file.with_suffix(".csv")
            with output_file.open("w", newline="", **self.option) as f:  # type: ignore
                writer = csv.DictWriter(f, fieldnames=fsm.header)
                writer.writeheader()
                for row in table:
                    writer.writerow({k: to_str(v) for k, v in row.items()})
        print(f"output: '{output_file.absolute()}'")


def main():
    args = read_argument()
    select_file(args)

    # 順次パース&出力
    i = j = 0
    for i, logfile in enumerate(map(LogFile, Glob(args.logfile)), 1):
        print(f"input: '{logfile.file}'")
        for j, template in enumerate(Glob(args.template), 1):
            logfile.parse(template, args.output, args.json)

    showinfo("完了", f"{i} logfiles\n{j} templates\n{i * j} output files")


if __name__ == "__main__":
    try:
        main()
    except DirNotFoundError as error:
        showerror("ディレクトリエラー", str(error))
    except FileNotFoundError as error:
        showerror("ファイルエラー", str(error))
    except TextFSMTemplateError as error:
        showerror("テンプレートエラー", str(error))
    except Abort:
        pass
