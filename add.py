import nest_asyncio
from pyngrok import ngrok
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# 1. ngrokの認証（ここにあなたのトークンを貼る）
NGROK_AUTH_TOKEN = "ngrokのAuthtokenを貼り付ける"
ngrok.set_auth_token(NGROK_AUTH_TOKEN)

# 2. FastAPIのアプリ設定
app = FastAPI()

# JavaScriptからのアクセスを許可（CORS設定）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Numbers(BaseModel):
    num1: float
    num2: float

@app.post("/add")
def add_numbers(data: Numbers):
    return {"sum": data.num1 + data.num2}

# 3. トンネルを開いてサーバーを起動
# 公開用のURLを発行
public_url = ngrok.connect(8000)
print(f"★★★ 公開URLはこちら: {public_url} ★★★")
print("※ このURLをJavaScriptのfetch部分に貼り付けてください")

# Colabでasyncioを動かすための設定
nest_asyncio.apply()

# 修正前
# uvicorn.run(app, host="0.0.0.0", port=8000)

# この1行だけだと，エラー（RuntimeError: asyncio.run() cannot be called from a running event loop）が発生．
# これは、Google Colab特有の現象で，Colab自体が既にPythonを動かすための「ループ（イベントループ）」を持っているため、
# その中でさらに新しくループを作ろうとすると「もう動いてるよ！」と怒られてしまうから。



# 修正後（Colab用）
import asyncio
config = uvicorn.Config(app, host="0.0.0.0", port=8000)
server = uvicorn.Server(config)
await server.serve()

# 上記修正で直る理由：
# Colabのセルは await（待機）という命令を直接受け付けることができる特殊な環境なので，
# uvicorn.run という「全部おまかせ」の命令ではなく、await server.serve() という
# 「今のループを使ってサーバーを開始してね」という丁寧な命令に変えることで、エラーを回避できる。

# 実行した後の状態について
# この修正をして実行すると、セルがずっと「実行中（ぐるぐる）」の状態になり，それで正解！
# 実行中: サーバーが起きていて、JavaScriptからのリクエストを待っている状態。
# 停止（再生ボタンが戻る）: サーバーが寝てしまった状態。通信できない。
