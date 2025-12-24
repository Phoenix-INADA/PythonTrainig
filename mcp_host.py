import asyncio
import os

import google.generativeai as genai
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# .envの内容を読み込む
load_dotenv()
my_key = os.getenv("GEMINI_API_KEY")
# 1. Geminiの設定
genai.configure(api_key=my_key)


async def run_gemini_mcp_loop():
    # MCPサーバー（先ほど作成した my_server.py）の起動設定
    server_params = StdioServerParameters(
        command="python", args=["my_server.py"], env=os.environ.copy()
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # MCPサーバー初期化
            await session.initialize()

            # --- 準備: MCPツールを Gemini 形式に変換 ---
            mcp_tools = await session.list_tools()

            # 本来はここで MCP の Tool 定義を Gemini の tools 形式に変換しますが、
            # 簡易化のため、Gemini に「利用可能なツール」として自然言語で教える構成にします。
            # (※より高度な実装では Function Calling API を使用します)

            chat = genai.GenerativeModel("gemini-3-flash-preview").start_chat(
                history=[]
            )

            print("--- Gemini MCP Agent 起動中 (exit で終了) ---")

            while True:
                user_input = input("\n質問を入力してください: ")
                if user_input.lower() == "exit":
                    break

                # 1. Gemini にユーザーの意図を解釈させる
                prompt = f"""
                あなたは以下の MCP ツールにアクセスできます:
                {mcp_tools}

                ユーザーの質問に対して、ツールが必要な場合は、以下の形式だけで回答してください。
                CALL:ツール名(引数名=値)

                ツールが不要な場合は、そのまま回答してください。

                質問: {user_input}
                """

                response = chat.send_message(prompt)
                res_text = response.text.strip()

                # 2. ツール実行の判定
                if res_text.startswith("CALL:"):
                    # 簡易的なパース (例: CALL:get_current_time())
                    # ※本番環境では正規表現や Function Calling API 推奨
                    tool_call_raw = res_text.replace("CALL:", "")
                    tool_name = tool_call_raw.split("(")[0]

                    print(f"[システム] ツール実行中: {tool_name}...")

                    # 3. MCP サーバー経由で実際のツールを呼び出す
                    # 引数がある場合は arguments={} に指定
                    tool_result = await session.call_tool(tool_name, arguments={})

                    # 4. 実行結果を Gemini に戻して最終回答を得る
                    final_prompt = f"ツールの実行結果は以下の通りです: {tool_result.content}\nこれをもとにユーザーへ回答してください。"
                    final_response = chat.send_message(final_prompt)

                    print(f"\nGemini: {final_response.text}")
                else:
                    print(f"\nGemini: {res_text}")


if __name__ == "__main__":
    asyncio.run(run_gemini_mcp_loop())
