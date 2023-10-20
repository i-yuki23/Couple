# Pythonイメージをベースにする
FROM python:3.11

# 作業ディレクトリを設定
WORKDIR /app

# requirements.txtを先にコピーして依存関係をインストール
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY . .

# ポート5000を公開
EXPOSE 5000

# Flaskアプリを起動するコマンドを設定
CMD ["python", "app.py"]