# --- デコレータ ---
from rich import print as rprint


def logger(func):
    def wrapper(*args, **kwargs):
        rprint(f"[bold blue]>>> Start: {func.__name__}[/bold blue]")
        result = func(*args, **kwargs)
        rprint(f"[bold green]<<< End: {func.__name__}[/bold green]")
        return result

    return wrapper


# --- クラス（特殊メソッド・イテレータ） ---
class NumberStack:
    """特殊メソッドとイテレータを含むクラス"""

    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, position):
        return self.data[position]

    def __iter__(self):
        """イテレータを返す"""
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.data):
            result = self.data[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration


# --- 関数（ジェネレータ・引数・例外処理・with文・ラムダ） ---
@logger
def process_data(initial_val, *args, multiplier=1, **kwargs):
    """
    全ての引数定義 (*args, **kwargs) を含む関数。
    with文によるファイル操作と例外処理を含む。
    """
    try:
        # 1. ジェネレータの作成 (内包表記を利用)
        gen = (x * multiplier for x in args)

        # 2. ラムダ式 (無名関数) の利用
        # kwargsから計算式を受け取る想定（デフォルトは加算）
        calc = kwargs.get("calc", lambda x, y: x + y)

        result = initial_val
        for val in gen:
            result = calc(result, val)

        # 3. with 文によるファイル書き込み
        with open("output.txt", "w", encoding="utf-8") as f:
            f.write(f"Calculation Result: {result}")

        return result

    except ZeroDivisionError as e:
        print(f"Error: ゼロ除算が発生しました - {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
    finally:
        print("Processing finished.")


# --- メイン処理 ---
if __name__ == "__main__":
    # クラスのインスタンス化
    stack = NumberStack([10, 20, 30])

    # イテレータと特殊メソッド (__len__) の利用
    print(f"Stack size: {len(stack)}")

    # 関数の呼び出し
    # *argsにstackを、multiplierに2を、ラムダ式をkwargsに渡す
    final_score = process_data(100, *stack, multiplier=2, calc=lambda a, b: a + b)

    print(f"Final Score: {final_score}")
