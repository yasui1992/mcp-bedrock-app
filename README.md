# mcp-bedrock-app

このプロジェクトは個人の学習と練習を目的としています。

## Environment

- アーキテクチャ: x86_64
- OS: Ubuntu 24.04.2 LTS  
  （`Ubuntu 24.04.2 LTS`で動作確認しています。ほとんどのLinuxディストリビューションでも動作すると思います）
- Required tools:
  - make
  - Docker

## Preparation

### 環境変数の設定
AWSとBedrockの環境変数を`.env`に設定します。

- Bedrock Converse APIの実行権限を持つIAMロールのcredentials
- BedrockのモデルID

以下のコマンドは例です。

```sh
cat <<EOF > .env
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_DEFAULT_REGION=...
BEDROCK_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
EOF
```

### `mcp_servers.json`の設定
`README.md`と同じディレクトリに`mcp_servers.json`ファイルを用意してください。このファイルはMCPサーバの設定に使用されます。
`.gitignore`によりGit管理から除外されているので、必要に応じてカスタマイズ可能です。  

例として、以下の内容で`mcp_servers.json`を作成します。

```.json
{
    "mcpServers": {
        "aws-documentation": {
            "command": "uvx",
            "args": [
                "awslabs.aws-documentation-mcp-server@latest"
            ],
            "env": {
                "FASTMCP_LOG_LEVEL": "ERROR"
            }
        }
    }
}
```

## Usage
アプリケーションを起動するには、下記のコマンドを実行します。

```sh
make up
```

デバッグモードで起動するには、下記のコマンドを実行します。

```sh
make up-debug
```

開発環境で起動するには、下記のコマンドを実行します。

```sh
make up-dev
```

開発環境かつデバッグモードで起動するには、下記のコマンドを実行します。

```sh
make up-dev-debug
```
