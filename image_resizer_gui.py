import os
import shutil
import tempfile
import zipfile
from tkinter import Tk, Label, Entry, Button, StringVar, filedialog, messagebox, ttk, Frame
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title('画像リサイズツール')
        self.root.geometry('480x300')
        self.file_path = StringVar()
        self.width = StringVar(value='330')
        self.height = StringVar(value='330')
        self.status = StringVar()

        # ドラッグ＆ドロップ対応
        self.dnd_frame = Frame(root, width=400, height=60, bg='#e0e0e0')
        self.dnd_frame.place(x=40, y=20)
        self.dnd_frame_label = Label(self.dnd_frame, text='ここにフォルダまたはzipファイルをドロップ', bg='#e0e0e0')
        self.dnd_frame_label.pack(expand=True, fill='both')
        self.dnd_frame.drop_target_register(DND_FILES)
        self.dnd_frame.dnd_bind('<<Drop>>', self.handle_drop)

        # 解像度入力
        Label(root, text='幅(px):').place(x=60, y=100)
        Entry(root, textvariable=self.width, width=6).place(x=110, y=100)
        Label(root, text='高さ(px):').place(x=180, y=100)
        Entry(root, textvariable=self.height, width=6).place(x=240, y=100)

        # ファイルパス表示
        Label(root, textvariable=self.file_path, fg='blue').place(x=40, y=140)

        # 実行ボタン
        Button(root, text='リサイズ実行', command=self.run_resize).place(x=190, y=180)

        # 進捗バー
        self.progress = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
        self.progress.place(x=40, y=220)

        # ステータス
        Label(root, textvariable=self.status, fg='red').place(x=40, y=250)

    def handle_drop(self, event):
        path = event.data.strip('{}')  # Windowsでパスが{}で囲まれる場合がある
        self.file_path.set(path)
        self.status.set('')

    def run_resize(self):
        path = self.file_path.get()
        if not path:
            self.status.set('ファイルまたはフォルダを選択してください')
            return
        try:
            width = int(self.width.get())
            height = int(self.height.get())
        except ValueError:
            self.status.set('幅・高さは整数で入力してください')
            return
        self.status.set('処理中...')
        self.root.update_idletasks()
        try:
            if os.path.isdir(path):
                self.process_folder(path, width, height)
            elif zipfile.is_zipfile(path):
                self.process_zip(path, width, height)
            else:
                self.status.set('フォルダまたはzipファイルを選択してください')
                return
            self.status.set('完了')
        except Exception as e:
            self.status.set(f'エラー: {e}')

    def process_folder(self, folder_path, width, height):
        out_dir = f'{folder_path}_out'
        os.makedirs(out_dir, exist_ok=True)
        png_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(folder_path) for f in filenames if f.lower().endswith('.png')]
        total = len(png_files)
        if total == 0:
            self.status.set('pngファイルが見つかりません')
            return
        self.progress['maximum'] = total
        for i, f in enumerate(png_files, 1):
            rel_path = os.path.relpath(f, folder_path)
            out_path = os.path.join(out_dir, rel_path)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with Image.open(f) as img:
                img = img.resize((width, height), Image.LANCZOS)
                img.save(out_path)
            self.progress['value'] = i
            self.root.update_idletasks()
        self.progress['value'] = 0

    def process_zip(self, zip_path, width, height):
        base = os.path.splitext(zip_path)[0]
        out_zip = base + '_out.zip'
        with tempfile.TemporaryDirectory() as tmpdir:
            with zipfile.ZipFile(zip_path, 'r') as zin:
                zin.extractall(tmpdir)
            self.process_folder(tmpdir, width, height)
            # 再圧縮
            with zipfile.ZipFile(out_zip, 'w', zipfile.ZIP_DEFLATED) as zout:
                for root, dirs, files in os.walk(f'{tmpdir}_out'):
                    for file in files:
                        abs_path = os.path.join(root, file)
                        arcname = os.path.relpath(abs_path, f'{tmpdir}_out')
                        zout.write(abs_path, arcname)

if __name__ == '__main__':
    try:
        from tkinterdnd2 import TkinterDnD
    except ImportError:
        import sys
        sys.exit('tkinterdnd2が必要です。pip install tkinterdnd2 でインストールしてください。')
    root = TkinterDnD.Tk()
    app = ImageResizerApp(root)
    root.mainloop()
