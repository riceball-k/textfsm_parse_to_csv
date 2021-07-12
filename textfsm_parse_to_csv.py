import argparse
import csv
import datetime
import json
import sys
import tkinter
import tkinter.filedialog as fd
from pathlib import Path

import textfsm

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('template', type=str, nargs='?', help='textfsmテンプレートファイル')
    parser.add_argument('filenames', metavar='logfile', type=str, nargs='*', help='ログファイル')
    parser.add_argument('-j', '--json', help="JSON形式で出力", action="store_true")
    args = parser.parse_args()

    # テンプレートファイル名指定
    if args.template is None:
        tkinter.Tk().withdraw()
        template_filename = fd.askopenfilename(
            title='テンプレートファイルを選択',
            filetypes=[('テンプレート', '*.textfsm;*.template'), ('すべて', '*.*')],
            initialdir=Path.cwd(),
        )
        if template_filename == '':
            sys.exit(0)
    else:
        template_filename = args.template

    # ログファイル名指定
    if args.filenames == []:
        tkinter.Tk().withdraw()
        log_filenames = fd.askopenfilenames(
            title='ログファイルを選択',
            filetypes=[('ログファイル', '*.log'), ('すべて', '*.*')],
            initialdir=Path.cwd(),
        )
        if log_filenames == '':
            sys.exit(0)
    else:
        import glob
        log_filenames = []
        for pattern in args.filenames:
            log_filenames.extend(glob.glob(pattern))

    for filename in log_filenames:
        # テンプレート読み込み
        with open(template_filename, 'rt') as f:
            try:
                table = textfsm.TextFSM(f)
            except textfsm.TextFSMTemplateError as e:
                print(f'\n{e}')
                break

        # ログ読み込み & パース
        log_filename = Path(filename)
        with log_filename.open('rt') as f:
            print(f' input: "{log_filename}"')
            read_data = f.read()

        if args.json:
            data = table.ParseTextToDicts(read_data)
            # JSONファイル名作成、ログファイルの保存場所に作成
            output_filename = log_filename.parent / (
                log_filename.stem + datetime.datetime.now().strftime('_%Y%m%d_%H%M%S.json')
            )
            # JSONファイル出力
            with output_filename.open('wt', encoding='utf-8') as f:
                print(f'output: "{output_filename}"')
                output = json.dump(data, f, indent=4)
        else:
            data = table.ParseText(read_data)
            # CSVファイル名作成、ログファイルの保存場所に作成
            output_filename = log_filename.parent / (
                log_filename.stem + datetime.datetime.now().strftime('_%Y%m%d_%H%M%S.csv')
            )
            # CSVファイル出力
            with output_filename.open('wt', newline='') as f:
                print(f'output: "{output_filename}"')
                output = csv.writer(f)
                output.writerow(table.header)
                for row in data:
                    row = [','.join(col) if type(col) is list else col for col in row]
                    output.writerow(row)

    input('\nEnterを押して終了')
