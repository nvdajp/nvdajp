# `ja-rokutenkanji.utb` テーブル解決エラー修正方針

## 問題の概要

ユニットテスト実行時に以下のエラーが発生しています：

```
LookupError: Could not resolve table 'ja-rokutenkanji.utb', looked in paths: ['F:\\nvda\\gh\\betajp-260102\\source\\louis\\tables']
```

## 根本原因の特定

### サブモジュール liblouis の状態

**重要な発見**: サブモジュール liblouis が上流（nvaccess/nvda beta）から正しく取り込まれていません。

1. **現在のブランチのliblouis**:
   - コミット: `5a0d978798b2dd2bc497128568634ab37049abfa`
   - バージョン: `v3.34.0-1-g5a0d9787`
   - `tables/ja-rokutenkanji.utb`の存在: **存在しない**（False）

2. **上流（nvaccess/nvda beta）のliblouis**:
   - コミット: `b798a79ebc9ffe7f5fc56c09e87c75c17d3583e8`
   - バージョン: `v3.36.0`
   - `tables/ja-rokutenkanji.utb`の存在: **存在する**（True）

3. **liblouisでの`ja-rokutenkanji.utb`追加**:
   - コミット: `23d2cbb1adcbb03c6bd362d9b548253dffa6cafe`（2025年7月26日）
   - コミットメッセージ: "Add new table for Japanese Rokuten Kanji braille"
   - このコミットは上流のliblouis（b798a79e）には含まれているが、現在のブランチ（5a0d9787）には含まれていない

### 現状の整理

1. **登録情報**:
   - `source/brailleTables/__tables.py`で`ja-rokutenkanji.utb`が登録されている
   - 登録名: `ja-rokutenkanji.utb`
   - 表示名: "Japanese (Rokuten Kanji) Braille"
   - ソース: `TableSource.BUILTIN`（デフォルト）

2. **ファイルの存在**:
   - **上流のliblouis**: `include/liblouis/tables/ja-rokutenkanji.utb`が存在する
   - **現在のブランチのliblouis**: `include/liblouis/tables/ja-rokutenkanji.utb`が存在しない
   - **nvdajp独自のファイル**: `source/ja-jp-rokutenkanji.tbl`が存在する（これは別物）
   - **期待される場所**: `source/louis/tables/ja-rokutenkanji.utb`（または`ja-jp-rokutenkanji.tbl`）
   - **現在の状態**: `source/louis/tables/`には存在しない

3. **インストール設定**:
   - `source/setup.py`では`dist/louis/tables/`に`ja-jp-rokutenkanji.tbl`をインストールする設定になっている
   - しかし、開発環境（`source/louis/tables/`）にはコピーされていない

4. **テーブル解決の仕組み**:
   - `louisHelper._resolveTableInner()`は`brailleTables.TABLES_DIR`（`source/louis/tables/`）を検索する
   - 登録されたテーブルの`source`が`TableSource.BUILTIN`の場合、`TABLES_DIR`を検索する
   - ファイルが見つからない場合、`LookupError`が発生する

## 既存ドキュメントの参照

`projectDocs/jp/braille-tables-relationship.md`によると：

- `ja-jp-rokutenkanji.tbl`は`ja-rokutenkanji.utb`として登録されている
- インストール先: `dist/louis/tables/`（`TABLES_DIR`）
- 変換エンジン: liblouisを使用
- 問題点: `include ja-jp-comp6.utb`を含むが、`ja-jp-comp6.utb`は疑似テーブル（liblouisが処理できない可能性）

## 修正方針

### 方針1: SConsビルドで`source/louis/tables/`にコピー（採用済み）

**概要**: `nvdaHelper/liblouis/sconscript`で`source/ja-jp-rokutenkanji.tbl`を`source/louis/tables/ja-rokutenkanji.utb`としてコピーする

**理由**:
- サブモジュールを手動で更新しても、nvaccess/betaのマージで自動的に更新されない
- nvaccess/betaのコミット`58dd14767`をマージすることで、liblouisサブモジュールも自動的に更新されるべき
- しかし、現在のブランチでは`58dd14767`をマージしてもliblouisが3.34.0のままの可能性がある
- そのため、nvdajp独自の`ja-jp-rokutenkanji.tbl`を`source/louis/tables/ja-rokutenkanji.utb`としてコピーする方針を採用

**メリット**:
- 開発環境とインストール環境で一貫性が保たれる
- 既存のビルドシステム（SCons）を活用できる
- 他のテーブルファイルと同じ場所に配置される
- nvaccess/betaのマージに依存しない
- ユニットテストが正常に動作する

**実装内容**:
1. `nvdaHelper/liblouis/sconscript`にJP PATCHを追加
2. `source/ja-jp-rokutenkanji.tbl`を`source/louis/tables/ja-rokutenkanji.utb`としてコピー
   - または、`source/louis/tables/ja-jp-rokutenkanji.tbl`としてコピー（登録名との対応は`louisHelper`が処理）

**注意点**:
- ファイル名の対応: 登録名は`ja-rokutenkanji.utb`だが、実際のファイルは`ja-jp-rokutenkanji.tbl`
- `louisHelper._resolveTableInner()`は登録されたテーブルの`fileName`を使用して検索するため、`fileName`と実際のファイル名が一致する必要がある
- または、`brailleTables.getTable()`で取得した`BrailleTable`の`absolutePath`を使用する（現在の実装では`fileName`のみを使用）

**実装例**:
```python
# nvdaHelper/liblouis/sconscript に追加
# BEGIN JP PATCH (Japanese braille table: ja-jp-rokutenkanji.tbl)
japaneseTable = env.InstallAs(
    outDir.Dir("tables").File("ja-rokutenkanji.utb"),
    sourceDir.File("ja-jp-rokutenkanji.tbl")
)
env.Depends(louisPython, japaneseTable)
# END JP PATCH
```

### 方針2: 登録名を`ja-jp-rokutenkanji.tbl`に変更

**概要**: `source/brailleTables/__tables.py`で登録名を`ja-jp-rokutenkanji.tbl`に変更し、`source/ja-jp-rokutenkanji.tbl`を直接参照する

**メリット**:
- ファイル名と登録名が一致する
- 既存のファイルをそのまま使用できる

**デメリット**:
- 上流版の`ja-rokutenkanji.utb`との名前衝突を回避できない（将来的な問題）
- `source/`のルートにテーブルファイルが存在することになる（他のテーブルは`source/louis/tables/`にある）

**実装内容**:
1. `source/brailleTables/__tables.py`で登録名を`ja-jp-rokutenkanji.tbl`に変更
2. `louisHelper._resolveTableInner()`で`source/`のルートも検索対象に追加（または、`TABLES_DIR_JP`を使用）

### 方針3: `TABLES_DIR_JP`を使用（非推奨）

**概要**: `ja-rokutenkanji.utb`の`source`を`TableSource.BUILTIN_JP`に変更し、`TABLES_DIR_JP`（`source/`のルート）を検索対象にする

**デメリット**:
- `TABLES_DIR_JP`は`ja-jp-comp6.utb`専用のディレクトリとして設計されている
- `ja-jp-rokutenkanji.tbl`はliblouisが使用するテーブルなので、`TABLES_DIR`に配置する方が適切

## 実装完了（方針1を採用）

### 実装内容

`nvdaHelper/liblouis/sconscript`に以下を追加（2025年12月31日実装）：

```python
# BEGIN JP PATCH (Japanese braille table: ja-jp-rokutenkanji.tbl)
# Copy ja-jp-rokutenkanji.tbl to source/louis/tables/ja-rokutenkanji.utb
# Note: The table is registered as ja-rokutenkanji.utb in brailleTables/__tables.py
japaneseTable = env.InstallAs(
	outDir.Dir("tables").File("ja-rokutenkanji.utb"),
	sourceDir.File("ja-jp-rokutenkanji.tbl")
)
env.Depends(louisPython, japaneseTable)
# END JP PATCH
```

### 検証結果

1. ✅ `scons source`を実行して`source/louis/tables/ja-rokutenkanji.utb`が作成されることを確認
2. ✅ `rununittests.bat`を実行してエラーが解消されることを確認（951 tests, OK）

### ステップ3: 依存関係の確認

`ja-jp-rokutenkanji.tbl`は`include ja-jp-comp6.utb`を含むが、`ja-jp-comp6.utb`は疑似テーブル（liblouisが処理できない）という問題がある。ただし、これは実行時の問題であり、ユニットテストのテーブル解決エラーとは別の問題。

## 関連ファイル

- `source/ja-jp-rokutenkanji.tbl` - 実際のテーブルファイル
- `source/brailleTables/__tables.py` - テーブル登録
- `source/louisHelper.py` - テーブル解決ロジック
- `nvdaHelper/liblouis/sconscript` - ビルドスクリプト
- `source/setup.py` - インストール設定
- `projectDocs/jp/braille-tables-relationship.md` - 既存ドキュメント

## 参考

- `projectDocs/jp/braille-tables-relationship.md` - 日本語点字テーブルの関係整理
- `source/louisHelper.py:36-68` - テーブル解決の実装
- `source/brailleTables/__init__.py:22-54` - テーブルディレクトリの定義
