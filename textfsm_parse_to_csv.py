import textfsm
from pathlib import Path
import sys
import csv
import datetime
import tkinter.filedialog as fd
import tkinter
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('template', type=str, nargs='?', help='textfsmテンプレートファイル')
    parser.add_argument('filenames', metavar='logfile', type=str, nargs='*', help='ログファイル')
    args = parser.parse_args()

    # テンプレートファイル名指定
    tkinter.Tk().withdraw()
    if args.template is None:
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
        log_filenames = fd.askopenfilenames(
            title='ログファイルを選択',
            filetypes=[('ログファイル', '*.log'), ('すべて', '*.*')],
            initialdir=Path.cwd(),
        )
        if log_filenames == []:
            sys.exit(0)
    else:
        import glob
        log_filenames = []
        for pattern in args.filenames:
            log_filenames.extend(glob.glob(pattern))

    for filename in log_filenames:
        log_filename = Path(filename)
        # CSVファイル名作成、ログファイルの保存場所に作成
        output_filename = log_filename.parent / (
            log_filename.stem + datetime.datetime.now().strftime('_%Y%m%d_%H%M%S.csv')
        )
        print(f'出力: "{output_filename}"')

        # テンプレート読み込み
        with open(template_filename, 'rt') as f:
            table = textfsm.TextFSM(f)

        # ログ読み込み & パース
        with log_filename.open('rt') as f:
            data = table.ParseText(f.read())

        # CSVファイル出力
        with output_filename.open('wt', newline='') as f:
            output = csv.writer(f)
            output.writerow(table.header)
            for row in data:
                row = [','.join(col) if type(col) is list else col for col in row]
                output.writerow(row)
