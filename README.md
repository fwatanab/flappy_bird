# Flappy Bird (Kivy)

Kivy を用いて実装した Flappy Bird 風のシンプルなゲームです。  
メニュー画面からゲームを開始し、スペースキーやクリックで鳥を操作してパイプの間を通り抜けます。

---

## 動作環境

- macOS / Windows / Linux
- Python 3.11 系（動作確認済み）
- Kivy 2.3.0

---

## セットアップ

### リポジトリからクローン

```bash
git clone https://github.com/fwatanab/flappy_bird.git
cd flappy_bird
```

### 仮想環境を作成して依存関係をインストール

```bash
# プロジェクト直下で
python3 -m venv venv
source venv/bin/activate   # Windows の場合: venv\Scripts\activate

# pip を最新化
pip install -U pip setuptools wheel

# 必要パッケージのインストール
pip install -r requirements.txt
```

---

## 実行方法
```bash
python3 src/main.py
```
---

## 遊び方

- スペースキー または マウスクリック で鳥を羽ばたかせます
- パイプの間を通り抜けるとスコアが加算されます
- 画面外に出たりパイプに当たるとゲームオーバーです
- メニュー画面からゲームを開始できます

---

## 特徴

- Kivy によるクロスプラットフォーム対応
- メニュー画面とゲーム画面の切り替え
- ウィンドウサイズに応じた描画（モバイルではフルスクリーン）


