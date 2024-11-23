# ベースイメージの指定
FROM python:3.11-slim

# 作業ディレクトリの設定
WORKDIR /app

# 必要なライブラリのインストール
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# アプリケーションコードのコピー
COPY . /app/

# ポートの指定
EXPOSE 8080

# アプリケーションの起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
