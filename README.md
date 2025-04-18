# 画像リサイズGUIツール（Python/tkinter）

## 概要
フォルダまたはzipファイル内のすべてのPNG画像を、指定したサイズ（初期値: 330x330px）に一括リサイズするWindows向けオフラインツールです。
GUIでドラッグ＆ドロップ操作に対応しています。

## 特徴
- フォルダまたはzipファイルをドラッグ＆ドロップで選択
- PNG画像のみ対象
- 解像度は幅・高さを指定可能（初期値: 330x330）
- 出力は「入力名+out」フォルダまたはzipとして、元と同じ階層に保存
- 進捗バー・エラー表示あり

## 必要環境
- Python 3.7以降（Windows推奨）
- pipで以下のパッケージをインストール

```
pip install -r requirements.txt
```

## 使い方
1. `image_resizer_gui.py` を実行します。
2. ウィンドウにフォルダまたはzipファイルをドラッグ＆ドロップします。
3. 必要に応じて幅・高さを変更します。
4. 「リサイズ実行」ボタンを押します。
5. 入力と同じ階層に「入力名+out」フォルダまたはzipが作成され、リサイズ済み画像が出力されます。

## 注意事項
- 入力はPNG画像のみ対応です。
- zip入力の場合、フォルダ構造も維持して再圧縮されます。
- tkinterdnd2が必要です。インストールされていない場合は `pip install tkinterdnd2` を実行してください。

## ライセンス
MIT License（改変・商用利用可）
