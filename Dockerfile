# ベースイメージの指定
FROM python:3.11-slim

# 作業ディレクトリの設定
WORKDIR /app

# 必要なライブラリのインストール
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードのコピー
COPY main.py main.py

# ポートの指定
EXPOSE 80

# アプリケーションの起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
