# M3 新譜情報収集ツール

## 概要

M3 などの同人音楽イベントの新譜情報を自動的に収集・分析するツールです。
X（旧 Twitter）と YouTube の API を使用して新譜情報を収集し、Gemini を使用して分析を行います。

## 機能

- X（旧 Twitter）での新譜情報の収集
- YouTube での新譜情報の収集
- Gemini による新譜情報の分析
- 分析結果の Markdown 形式での出力

## 出力ファイル

### X 関連

- `results/x_results_YYYYMMDD_HHMMSS.json`: X で収集した投稿データ（JSON 形式）
- `results/analysis_results_YYYYMMDD_HHMMSS.md`: X の投稿を Gemini で分析した結果（Markdown 形式）
  - 分析結果
  - 参照元の投稿（ユーザー名と投稿 URL）

### YouTube 関連

- `results/youtube_results_YYYYMMDD_HHMMSS.json`: YouTube で収集した動画データ（JSON 形式）
- `results/youtube_results_YYYYMMDD_HHMMSS.md`: YouTube の動画情報（Markdown 形式）
  - 動画タイトル
  - 公開日
  - 説明文
  - 動画 URL

## セットアップ

1. pyenv のインストール（未インストールの場合）

```bash
# pyenvのインストール
curl https://pyenv.run | bash

# zshの設定ファイルに追記
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# シェルの再起動
exec $SHELL
```

2. Python 環境の構築

```bash
# 最新のPythonをインストール
pyenv install 3.12.0

# プロジェクト用の仮想環境を作成
pyenv virtualenv 3.12.0 m3-checker

# プロジェクトディレクトリで仮想環境を有効化
pyenv local m3-checker
```

3. 必要なパッケージのインストール

```bash
pip install -r requirements.txt
```

4. 環境変数の設定
   `.env`ファイルを作成し、以下の情報を設定してください：

```
# X API設定
X_API_KEY=your_api_key
X_API_SECRET=your_api_secret
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
X_BEARER_TOKEN=your_bearer_token

# YouTube API設定
YOUTUBE_API_KEY=your_youtube_api_key

# Gemini API設定
GEMINI_API_KEY=your_gemini_api_key
```

## 使用方法

1. スクリプトの実行:

```bash
python src/main.py
```

2. 出力ファイルの確認:

- `results`ディレクトリに生成されたファイルを確認してください
- 各ファイルには実行日時が含まれています

## 注意事項

- API の利用制限に注意してください
- 環境変数は必ず設定してください
- 出力ファイルは`results`ディレクトリに保存されます
