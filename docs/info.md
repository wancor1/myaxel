
# ■概要

- Python並みに書きやすく、Rust並みに安全・厳密
- インタプリタ + バイトコードVM（将来的にLLVM対応）
- `fn main()`があればそこから、なければ上から順に実行
- DB・フロントエンド・ゲーム・数値計算など何でもこの言語一つでできる

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
- `int / uint / float / str / bool / Null / range`
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

## ■newtype

```
newtype UserId = int;
newtype Email = str;

let id: UserId = 1;
let x: int = id;  // エラー！互換性なし
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
x as int   // Rust風
int(x)     // 関数風
```

---

## ■範囲型

```myaxel
let r: range = 0..10;   // 0から9
let r: range = 0..=10;  // 0から10

for i in r { }          // ループに使う
r.contains(5);          // 含まれるか確認
```

---

## ■演算子

```
+ - * / **
== != < > <= >=
=  （代入）
:= （セイウチ）
.  （メンバーアクセス）
&& ||
++ --
|> （パイプ）
?. （オプショナルチェーン）
... （スプレッド）
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
|>   8
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
let arr2 = [...arr1, 4, 5];  // スプレッド
```
- 同一型のみ

---

## ■タプル

```myaxel
let x = (1, "hi");
let (a, b) = (1, "hi");
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
add(a=1, b=2);  // 名前付き引数
```
- 関数は値
- ネスト可能
- クロージャあり
- デフォルト引数あり
- 可変長引数あり
- `self`は暗黙的（明示も可）

---

## ■pure関数

```
pure fn add(a, b) {
    return a + b;   // OK
    println("hi");  // エラー！副作用あり
}
```

---

## ■ラムダ/無名関数

```myaxel
let f = (x) => x + 1;
let f = (x) => { return x + 1; };
let f = |x| x + 1;
let f = |x| { return x + 1; };
nums.map((x) => x * 2);
nums.map(|x| x * 2);
```

---

## ■パイプ演算子

```
x |> f |> g;
[1,2,3] |> map((x) => x*2) |> filter((x) => x>2);
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

let x = if cond { a } else { b };
let x = if cond { a };

while (cond) { }

for i in 0..10 { }
for i in arr { }
for (i=0, i<10, i++) { }

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

## ■オプショナルチェーン

```
obj?.field?.method();  // nullなら全体がnull
```

---

## ■match（予定）

```myaxel
match x {
    1 => ...
    1..=10 => ...      // 範囲
    int => ...         // 型
    n if n > 0 => ...  // 条件付き
}
```

---

## ■アノテーション

```
@trace
let mut x = 0;
x++;  // 「x: 0→1 (line:2)」みたいに自動追跡
```

---

## ■エラーハンドリング

- panic + unwrap_orで対応（Result型なし）
- エラーに修正案つき
- デフォルトはRust的な機械形式
- ビルド時に人間語モードに切り替え可能

---

## ■unwrap_or

```myaxel
// イテレータ
x = arr.iter().next().unwrap_or(0);

// 関数の戻り値がpanic/wrapなら
x = someFunc().unwrap_or(0);
```
- 関数やイテレータの戻り値に使う
- panic/wrapが起きそうなら代替値を返す

---

## ■イテレータ

```
arr.iter()
   .next()
   .unwrap_or(0);
```
- `map` / `filter` / `collect`等は後で追加予定

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

```
print()
println()
input()
len()
etc
```

JSON / HTTP / 並列が標準ライブラリで使える

---

## ■標準ライブラリ

■標準ライブラリ
基本：
- `std.io` / `std.fs` / `std.math` / `std.string` / `std.collections`

ネットワーク/Web：
- `std.http` / `std.json` / `std.websocket` / `std.html`

DB：
- `std.db` / `std.db.sql` / `std.db.nosql`

フロントエンド：
- `std.ui` / `std.dom` / `std.css`

ゲーム：
- `std.game` / `std.render` / `std.physics` / `std.audio`

数値/科学計算：
- `std.stats` / `std.matrix` / `std.complex` / `std.bignum`

並列/非同期：
- `std.async` / `std.thread` / `std.channel`

---

## ■import

```myaxel
import math;
use math.sqrt;
import math use math.sqrt; // pythonのfrom xxx import xxxと同じ
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
- overflowが起きそうな箇所を事前に警告
- nullがどこで染まるか追跡可能

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

## ■エラーレベル

```
Lv1 - 構文エラー（パース不能）
Lv2 - 実行時エラー（未定義変数、型不一致、ゼロ除算など）
Lv3 - 警告（未使用変数、到達不能コード、未初期化変数など）
Lv4 - 情報（動的型付け通知、deprecatedな書き方）
Lv5 - 通知（null染まりなど意図した動作の通知）
```
- デフォルト表示はLv3以上
- `myaxel-lint`：改善提案・コードスタイル・パフォーマンス警告（別枠）
