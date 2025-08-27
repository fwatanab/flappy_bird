""" Flappy Bird 設定ファイル """

# 基本設定
GAME_TITLE = "Flappy Bird"
FPS = 60
SCROLL_SPEED = 200
GRAVITY = -0.5
FLAP_POWER = 8

# モバイルはフルスクリーン、PCではウィンドウ起動にする想定
FULLSCREEN = False

# 画面サイズとアスペクト比
BASE_WIDTH = 1080
BASE_HEIGHT = 1920
ASPECT_RATIO = BASE_WIDTH / BASE_HEIGHT

# PC起動時の初期ウィンドウ（9:16・スマホ相当）
# 360x640 は一般的な“論理解像度”で扱いやすいサイズ
DEFAULT_WINDOW_WIDTH = 360
DEFAULT_WINDOW_HEIGHT = 640

# タイトル設定
TITLE_SIZE_RATIO = (0.5, 0.15)  # タイトルのサイズ (幅, 高さ)
TITLE_POS_RATIO = (0.5, 0.7)    # タイトルの位置 (X, Y)

# --- Gameplay invariants (window size independent) ---
# 画面の右→左にパイプが横断し切るまでの秒数（大きい画面でも同じ体感速度）
COLUMN_CROSS_SECONDS = 3.0
# パイプのスポーン間隔（秒）
COLUMN_SPAWN_INTERVAL = 1.2
# 上下のギャップは画面高さの比率で一定（例: 22%）
PIPE_GAP_RATIO = 0.22
# 鳥の設定
BIRD_START_RATIO = (0.1, 0.9)  # 開始位置 (X, Y)
BIRD_SIZE_RATIO = (0.05, 0.05) # 鳥のサイズ (幅, 高さ)

# 地面の高さ比率
FLOOR_HEIGHT_RATIO = 0.2

# パイプの設定
PIPE_GAP_RATIO = 0.2        # パイプ間のギャップ比率 (0.25〜0.35)
PIPE_MIN = 0.1              # パイプの最小高さ比率 (0.1〜0.2)
PIPE_SIZE_RATIO = 0.05      # パイプの横幅比率 (0.1〜0.15)
PIPE_START_WIDTH = 1.1      # 最初のパイプの生成位置 (画面外右側)
PIPE_SPAWN_INTERVAL = 1.5   # パイプの生成間隔 (秒)
