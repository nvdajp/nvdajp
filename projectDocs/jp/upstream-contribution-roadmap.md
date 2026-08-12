# 本家 NVDA への貢献ロードマップ（upstream contribution roadmap）

## 目的

betajp（および alphajp）で実装・検証した、言語に依存しない**汎用バグ修正**を
本家 `nvaccess/nvda` へ順次 PR 提案するための管理ドキュメント。

NVDA の開発サイクルでは **機能フリーズ** 前後にバグ修正のマージ窓が限られる。
本家への提案は「小さく、独立していて、単体テスト付きで、JP 固有設定に依存しない」
ものを優先する。JP 固有設定（`nvdajp*` / `jp*` / `[language]`）へ依存する変更は、
本家へは出さず JP 固有として維持する。

このドキュメントは `projectDocs/jp/roadmap.md`（実行中タスクの正本）のサブセットであり、
「上流へ還元すべきタスク」を追跡する。個別の実装・検証メモは各 issue ドキュメントを正本とする。

## 還元方針（原則）

1. **言語・地域に依存しない**修正のみを本家へ提案する。
2. 本家 PR では `# BEGIN/END JP PATCH` マーカーと `# nvdajp` コメントを外し、
   上流のコードスタイル・コーディング標準（`projectDocs/dev/codingStandards.md`）に合わせる。
3. **単体テストを添える**（本家のテスト標準 `tests/unit/` に合わせる）。
4. 各 PR は1テーマに限定し、依存関係を切って独立してマージ可能にする。
5. 提案前に本家の既存 issue/PR を検索し、重複を避ける。
6. 本家への issue 番号は nvdajp のものとは別に、nvaccess 側で新規に立て直す。

## 候補一覧

| # | 対象ファイル | 内容 | 状態 | 優先度 | 上流への適性 |
|---|--------------|------|------|--------|--------------|
| 494 | `source/characterProcessing.py` | 完全ロケールのシンボル欠落時、ベース言語へフォールバック | ✅ betajp マージ済（`86f8ca3cc2`） | 🥇 最優先 | 🟢 高い（汎用・テスト付き・JP設定非依存） |
| 113 | `source/...`（Scintilla 系） | CRLF を1文字の改行として読む | ✅ betajp マージ済（`637d8735fe`） | 🥈 高い | 🟢 高い（Notepad++ 等で再現・汎用） |
| 575 | `nvdaHelper/remote/winword.cpp` | Word 二重取り消し線を単一より先に判定（オブジェクトモデル経路） | ✅ betajp マージ済（`5d9a57677f`） | 🥈 高い | 🟢 高い（言語非依存・C++ 6行） |
| 710 | `source/NVDAObjects/UIA/__init__.py` | UIA 経路で二重取り消し線を区別して報告 | ✅ betajp マージ済（`c36d44401f`） | 🥈 高い | 🟢 高い（**575 と対で提案**） |
| 94 | `source/NVDAObjects/IAccessible/chromium.py` | Chromium でマウス追跡（`beTransparentToMouse`） | 🟡 `betajp-fix-94`（実験段階） | 🥉 中 | 🟡 要検証（ツリー未構築時は不変） |

## 詳細

### 494 — シンボルのベース言語フォールバック

* **コミット**: `86f8ca3cc2`（PR #716）
* **変更**: `source/characterProcessing.py` の2箇所
  * `LocaleDataMap.__init__`（`SymbolDefinitionSource` 系）で `fetchLocaleData(locale, fallback=True)` に変更
  * `getSymbols()` でも `fallback=True` に変更
* **背景**: 完全ロケール（例 `ja_JP`）に専用シンボルデータがない場合、`FileNotFoundError` が発生。
  文字説明（character descriptions）は既にベース言語へフォールバックするため、動作を揃える。
* **テスト**: `tests/unit/test_characterProcessing.py` にフォールバック動作の単体テスト追加。
* **上流提案メモ**:
  * `fallback` 引数の既定値は本家仕様に合わせて調整する（現在 `fallback=True` を明示）。
  * JP PATCH マーカーを外し、本家のコード規約に合わせる。

### 113 — CRLF を単一の改行として読む

* **コミット**: `637d8735fe`（ブランチ `betajp-fix-113`）
* **背景**: Scintilla 系（Notepad++ 等）では CRLF が1キャレット位置。文字単位移動で `"\r\n"` が
  2文字のユニットとなり、単一文字スペルパスが発火せず「blank」と読まれていた。
  LF のみ／CR のみの文書では正しく読めた。
* **対応**: 文字・単語ユニットのテキストがちょうど `"\r\n"` の場合、単一の `"\n"` として扱い、
  LF 文書と同じ改行シンボル読み上げにする。単体テストで Scintilla 挙動を模擬。
* **上流提案メモ**: 影響が広いため、本家側のブラウズモード／エディット文字読みに
  回帰を出さないか確認が必要。

### 575 — Word 二重取り消し線（オブジェクトモデル経路）

* **コミット**: `5d9a57677f`（ブランチ `betajp-fix-575`）
* **変更**: `nvdaHelper/remote/winword.cpp` の `generateXMLAttribsForFormatting`
  * 判定順序を `DOUBLESTRIKETHROUGH` → `STRIKETHROUGH` に逆転
* **背景**: Word で二重取り消し線を設定すると `Strikethrough` プロパティも `True` を返すため、
  二重取り消し線の判定が到達しなかった。
* **上流提案メモ**: 6行の小さな C++ 変更。`strikethrough="double"` の書式は既に上流で
  受け入れられている（`#15205` 等）ため、順序修正のみの提案にできる。

### 710 — Word 二重取り消し線（UIA 経路）

* **コミット**: `c36d44401f`（ブランチ `feature/uia-double-strikethrough-710`）
* **変更**: `source/NVDAObjects/UIA/__init__.py` の `_getFormatFieldFontAttributes`
  * `UIA_StrikethroughStyleAttributeId` が `TextDecorationLineStyleEnum` を返すため、
    値 3（`TextDecorationLineStyle_Double`）→ `strikethrough="double"`、1（Single）→ `True`、他 → bool
* **背景**: Word 2016 build 15000 以上 + Windows 11 では UIA 経路になる。
  UIA 属性は数値で二重取り消し線を区別できるため、音声・点字で単一と区別して報告。
* **上流提案メモ**: **575（オブジェクトモデル）と対で1 PR** にまとめるのが望ましい。
  JP PATCH マーカーを外し、`TextDecorationLineStyle_Double` 定数参照へ置き換え。

### 94 — Chromium マウス追跡（実験段階）

* **ブランチ**: `betajp-fix-94`
* **変更**: `source/NVDAObjects/IAccessible/chromium.py` に Firefox と同等の
  `TextLeaf(beTransparentToMouse=True)` を追加
* **背景**: Chromium 系ではテキスト葉ノードがマウスを吸収し「無音」「1文字だけ読む」等になる。
  jcsteh 自身が nvaccess#8076 で Mozilla と同じ手法を提案済み。
* **既知の制限**: アクセシビリティツリー未構築時（hit test がドキュメントルートのみ）は改善しない。
  実機での再現性確認が未完のため実験段階。
* **参照**: `projectDocs/jp/issue-94-chromium-mouse-tracking.md`

## 提案手順（各 PR）

1. betajp から feature ブランチを切り、該当コミットを `cherry-pick`（または再実装）。
2. `# BEGIN/END JP PATCH` / `# nvdajp` マーカーを除去。
3. 上流の単体テスト標準に合わせてテストを調整。
4. 本家 `nvaccess/nvda` へ PR を作成（ベース: `master`、機能フリーズ前を狙う）。
5. 本家レビュー指摘を取り込み、マージを確認。
6. マージ後、本ドキュメントの状態列を更新。

## 上流提案の対象外（JP 固有として維持）

* **117**（NFKC 展開文字の点字位置マッピング）— `jpBrailleUtils`/translator 依存
* **224**（キリル文字点字）、**456**（ギリシャ文字点字）— translator1 依存
* **695**（カタカナピッチ既定値）、**706**（バックスラッシュ記号）— 日本語設定依存
* JTalk / Haruka 音声ドライバ、IME 系（`nvdajpEnableKeyEvents` 等）、点字テーブル — JP 固有

## メンテナンス

* 本家 PR がマージされたら、状態列を「✅ 上流マージ済」に更新する。
* 新たに汎用バグ修正が betajp に入ったら、この表へ追記する。
* 本家の機能フリーズ期は、この表の優先度順に提案を詰める。
