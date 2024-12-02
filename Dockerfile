# ベースイメージ
FROM python:3.12-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なシステムパッケージをインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 依存関係ファイルをコピー
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# コンテナがリッスンするポートを指定
EXPOSE 8080

# アプリケーションの起動
CMD ["python", "main.py"]
