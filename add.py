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
# uvicorn.run(app, host="0.0.0.0", port=8000)
import asyncio
config = uvicorn.Config(app, host="0.0.0.0", port=8000)
server = uvicorn.Server(config)
await server.serve()
