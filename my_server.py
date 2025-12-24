import datetime
import os

from mcp.server.fastmcp import FastMCP

# 1. MCPサーバーのインスタンスを作成
mcp = FastMCP("MyLocalHelper")


# 2. ツールを定義：現在時刻を取得する
@mcp.tool()
def get_current_time() -> str:
    """現在のサーバーの時刻を返します。"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 3. ツールを定義：ファイル一覧を取得する
@mcp.tool()
def list_files(directory: str = ".") -> str:
    """指定されたディレクトリ内のファイル一覧を取得します。

    Args:
        directory: 調査したいディレクトリのパス。デフォルトはカレントディレクトリ。
    """
    try:
        files = os.listdir(directory)
        return "\n".join(files) if files else "ファイルは見つかりませんでした。"
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"


if __name__ == "__main__":
    # 4. サーバーを起動（標準入出力を使用）
    mcp.run()
