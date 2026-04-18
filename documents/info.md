
# ■概要

- Python並みに書きやすく、Rust並みに安全・厳密
- インタプリタ + バイトコードVM（将来的にLLVM対応）
- `fn main()`があればそこから、なければ上から順に実行

---

## ■文法スタイル

- セミコロン必須
- インデント不要（C系）
- ブロックスコープ

---

## ■変数

```myaxel
let x;
let x = 10;
let mut x = 10;
let x: int = 10;
let mut sat x: int = 10;
```
- `let`で宣言、デフォルトはimmutable
- `mut`で可変
- `let x;`はNull
- overflowモード：`wrap`(default) / `panic` / `sat`（mutのみ）

---

## ■型システム

- 型推論あり、型明示可能
- `int / uint / float / str / bool / Null`
- ビット数推論あり、明示指定も可能（i64, u32, f16など）
- ジェネリクスあり

---

## ■ジェネリクス

```myaxel
fn first<T>(arr: [T]): T {
    return arr[0];
}
struct Box<T> { value: T }
trait Container<T> { }
fn pair<T, U>(a: T, b: U): (T, U) { }
```

---

## ■null

- 使われた瞬間に相手の型のデフォルト値に染まる
  - `int`→`0`、`str`→`""`、`bool`→`false`
- 後から代入したら普通にその型になる
- Option型も併用可能

---

## ■キャスト

```myaxel
x as int
x as f64
```

---

## ■演算子

```
+ - * / **
== != < > <= >=
= （代入）
:= （セイウチ）
. （メンバーアクセス）
&& ||
++ --
```

---

## ■演算子優先順位

```
=    1
:=   1
==   2
< >  3
+ -  4
* /  5
**   6
.    7
```

---

## ■演算ルール

- `int / int` → `int`
- float混ざる → `float`
- 型違いはエラー
- 明示的キャストあり
- 右から評価
- 短絡評価あり（`&&` `||`）

---

## ■文字列

```
"hello {name}"         // 変数埋め込み
"result: {1+1}"        // 式埋め込み
("{}", name)           // フォーマット風
```
- 文字列同士の`+`はOK

---

## ■配列

```
[1, 2, 3]
```
- 同一型のみ

---

## ■タプル

```myaxel
let x = (1, "hi");
let (a, b) = (1, "hi");  // デストラクチャリング
```

---

## ■辞書（予定）

```
{"key": value}
```
- keyは基本str

---

## ■デストラクチャリング

```myaxel
let (a, b) = (1, 2);        // タプル
let [a, b] = [1, 2];        // 配列
let {hp, name} = player;    // struct
```

---

## ■関数

```myaxel
fn add(a: int, b: int): int {
    return a + b;
}
fn add(a, b) {  // 推論
    return a + b;
}
```
- 関数は値
- ネスト可能
- クロージャあり
- デフォルト引数あり
- 可変長引数あり
- `self`は暗黙的（明示も可）

---

## ■ラムダ/無名関数

```myaxel
// JS風
let f = (x) => x + 1;
let f = (x) => { return x + 1; };

// Rust風
let f = |x| x + 1;
let f = |x| { return x + 1; };

// 引数に渡す
nums.map((x) => x * 2);
nums.map(|x| x * 2);
```

---

## ■OOP

```myaxel
struct Player {
    pub hp: int,
    priv name: str,
}
impl Player {
    pub fn greet() {
        println(self.name);
    }
}
class Player {
    pub hp: int,
    priv name: str,
    pub fn greet() {
        println(self.name);
    }
}
```
- `class`は`struct+impl`の糖衣構文
- アクセス修飾子：`pub` / `priv`（デフォルトは`priv`）
- 継承なし

---

## ■trait

```myaxel
trait Greet {
    fn hello();
    fn bye() {
        println("bye");
    }
}
impl Player: Greet, Drawable {
    fn hello() {
        println(self.name);
    }
}
```
- デフォルト実装あり
- 複数trait実装可能
- `self`は暗黙的

---

## ■enum

```myaxel
enum State {
    Idle,
    Run
}
```

---

## ■制御構文

```myaxel
if (cond) { }
elif (cond) { }
else { }

// if式
let x = if cond { a } else { b };
let x = if cond { a };  // elseなしはNull

while (cond) { }

// for
for i in 0..10 { }        // 0から9
for i in 0..=10 { }       // 0から10
for i in arr { }          // 配列ループ
for (i=0, i<10, i++) { }  // C風

break;
continue;
```

---

## ■セイウチ演算子

```myaxel
if (n := someFunc()) {
    println(n);
}
while (line := readLine()) {
    println(line);
}
```

---

## ■match（予定）

```myaxel
match x {
    1 => ...
}
```

---

## ■エラーハンドリング

- Result型
- panic あり
- エラーに修正案つき
- デフォルトはRust的な機械形式
- ビルド時に人間語モードに切り替え可能

---

## ■並列処理

- 言語レベルで安全に書ける（詳細未定）

---

## ■Mixin

- 言語標準でMixin搭載
- 既存コードを汚さず割り込める（SpongePowered Mixin的な）
- 詳細未定

---

## ■標準関数

```myaxel
print()
println()
input()
len()
```
- JSON / HTTP / 並列が標準ライブラリで使える

---

## ■import

```myaxel
import math;
use math.sqrt;
```
- 依存関係管理あり（競合・不足を事前に通知）

---

## ■スコープ

- ブロックスコープ
- 関数スコープ
- グローバル変数あり

---

## ■メモリ管理

- GCあり
- 手動解放も可能
- 解放済みアクセス → エラー（is_alive）

---

## ■参照・コピー

- デフォルトは参照渡し
- 明示コピーあり
- 複数参照OK

---

## ■静的解析

- 標準搭載（ツール不要）

---

## ■他言語相互運用

- トランスパイルorランタイムで別言語のコードをそのまま使える（詳細未定）

---

## ■テスト

- ユニットテスト自動生成

---

## ■コメント

```
// line comment
/* block comment */
```

---

## ■Lexer

```
Token(type, value, line, column)
COMMENT / LINE / KEYWORD / IDENT
NUMBER / STRING / OP / END
```

---

## ■Parser

- 再帰下降 + 優先順位制御 + エラー回復（Rust風）
```
parse_program
 → parse_statement
   → parse_let
   → parse_assign
   → parse_if
   → parse_expression
     → parse_term
       → parse_power
         → parse_primary
```

---

## ■AST

```
Program(statements)
Let(name, value, mutable, overflow, type_)
Assign(name, value)
If(condition, body, else_)
Binary(left, op, right)
Literal(value)
Variable(name)
Expr(value)
```
