# 日本語点字テーブルの関係整理

## 概要

nvdajp には、日本語点字に関連する3つの異なるテーブル/エンジンが存在します。これらは混同されやすいため、ここで整理します。

## 1. `ja-jp-comp6.utb` - JP固有の疑似テーブル（情報処理点字）

### 特徴

- **ファイル**: `source/ja-jp-comp6.utb`
- **インストール先**: `dist/` のルート（`TABLES_DIR_JP`）
- **変換エンジン**: **liblouis を使用しない**。JP独自の `translator2` エンジンを使用
- **用途**: 日本語6点情報処理点字（第2種・6点コンピュータ点字）

### 動作原理

**注意**: 現在の実装では、`louisHelper.translate()` は liblouis を直接呼び出すだけです。`ja-jp-comp6.utb` の特別な処理は実装されていない可能性があります。

理論上の動作原理（`projectDocs/jp/braille-ja-jp-comp6.md` に記載）:

1. ユーザーが「日本語6点情報処理点字」を選択
2. `source/louisHelper.py` の `translate()` 関数で `ja-jp-comp6.utb` を検出
3. **liblouis を経由せず**、`miscDepsJp/source/synthDrivers/jtalk/translator2.py` の `translate()` を直接呼び出し
4. MeCab で形態素解析を行い、日本語点字ルールに従って変換

**実装状況の確認が必要**: `louisHelper.py` に `jpTranslate` の実装があるか、または別の場所で処理されているかを確認する必要があります。

### 詳細

- マスあけ、情報処理点字の記号付与など、日本語固有の処理を実装
- NABCC モード（`expandAtCursor`）に対応
- 詳細は `projectDocs/jp/braille-ja-jp-comp6.md` を参照

## 2. `ja-jp-rokutenkanji.tbl` - nvdajp 従来の六点漢字テーブル（非推奨・将来削除予定）

### 特徴

- **ソースファイル**: `source/ja-jp-rokutenkanji.tbl`
- **状態**: **非推奨**。上流版の`ja-rokutenkanji.utb`（liblouis 3.36.0以降）を使用すべき
- **登録名**: `ja-rokutenkanji.utb`（`source/brailleTables/__tables.py` で登録）
- **変換エンジン**: **liblouis を使用**
- **用途**: 六点漢字（漢字の点字表現）

### 歴史

- **追加日**: 2017年8月7日（コミット `8980c3542f`）
- **作成者**: Takuya Nishimoto
- **元データ**: Hasegawa system Japanese 6ten kanji characters table
  - 許可: Sadao Hasegawa
  - 著作権: Teruyoshi Fujinuma
  - 変換: Takuya Nishimoto

### 構造

```tbl
include ja-jp-comp6.utb

letter \x4e9c  6-1-12              	# 亜
letter \x5516  6-1-245             	# 唖
...
```

- `include ja-jp-comp6.utb` を含む
- しかし、**実際の変換は liblouis が行う**
- `ja-jp-comp6.utb` は疑似テーブルなので、liblouis は `ja-jp-comp6.utb` を読み込めない可能性がある

### 問題点

- `ja-jp-rokutenkanji.tbl` は `include ja-jp-comp6.utb` を含むが、`ja-jp-comp6.utb` は疑似テーブル（liblouis が処理できない）
- liblouis が `ja-jp-comp6.utb` を解決できない場合、`ja-jp-rokutenkanji.tbl` は動作しない可能性がある
- **上流版の`ja-rokutenkanji.utb`（liblouis 3.36.0以降）が利用可能になったため、このテーブルは不要**

### 現在の対応（一時的）

- **現在のブランチ（liblouis 3.34.0）**: `nvdaHelper/liblouis/sconscript`で`source/ja-jp-rokutenkanji.tbl`を`source/louis/tables/ja-rokutenkanji.utb`としてコピー（ユニットテストを通すため）
- **将来（liblouis 3.36.0以降）**: 上流版の`ja-rokutenkanji.utb`を使用し、`ja-jp-rokutenkanji.tbl`とSConsビルドでのコピー処理を削除すべき

## 3. 上流版の `ja-rokutenkanji.utb` - liblouis 公式の六点漢字テーブル（推奨）

### 特徴

- **ファイル**: `include/liblouis/tables/ja-rokutenkanji.utb`
- **登録**: `source/brailleTables/__tables.py` で `ja-rokutenkanji.utb` として登録されている
- **変換エンジン**: **liblouis を使用**
- **状態**: liblouis 3.36.0以降に含まれている（2025年7月26日のコミット `23d2cbb1` で追加）
- **メンテナンス**: liblouis公式でメンテナンスされている（Yoza Kensaku, Kiriake Masanori）
- **推奨**: **このテーブルを使用すべき**。nvdajp独自の`ja-jp-rokutenkanji.tbl`は非推奨

### 現状（2025年12月31日時点）

- **上流（nvaccess/nvda beta）のliblouis 3.36.0**: `include/liblouis/tables/ja-rokutenkanji.utb`が存在する
- **現在のブランチ（betajp-260102）のliblouis 3.34.0**: `include/liblouis/tables/ja-rokutenkanji.utb`が存在しない
- **一時的な対応**: `source/ja-jp-rokutenkanji.tbl`を`source/louis/tables/ja-rokutenkanji.utb`としてコピーする実装を追加（`nvdaHelper/liblouis/sconscript`）
- **将来の対応**: nvaccess/betaのマージでliblouisが3.36.0に更新された場合、上流版の`ja-rokutenkanji.utb`を使用し、`ja-jp-rokutenkanji.tbl`とSConsビルドでのコピー処理を削除すべき

### 利点

- liblouis公式でメンテナンスされているため、継続的に更新される
- `include ja-jp-comp6.utb`を含まないため、liblouisが正常に処理できる
- nvdajp独自のメンテナンスが不要

## 関係図

```
┌─────────────────────────────────────────────────────────────┐
│ ja-jp-comp6.utb (疑似テーブル)                              │
│ - 変換エンジン: translator2 (JP独自)                        │
│ - liblouis を使用しない                                      │
│ - インストール先: dist/ (TABLES_DIR_JP)                     │
└─────────────────────────────────────────────────────────────┘
                          ↑
                          │ include
                          │
┌─────────────────────────────────────────────────────────────┐
│ ja-jp-rokutenkanji.tbl (nvdajp 従来・非推奨)                │
│ - 登録名: ja-rokutenkanji.utb                               │
│ - 変換エンジン: liblouis                                     │
│ - 状態: 非推奨（上流版を使用すべき）                         │
│ - 問題: include ja-jp-comp6.utb を含むが、                  │
│   疑似テーブルなので liblouis が解決できない可能性          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ ja-rokutenkanji.utb (上流版・liblouis 3.36.0以降・推奨)    │
│ - 変換エンジン: liblouis                                     │
│ - インストール先: dist/louis/tables/ (TABLES_DIR)          │
│ - 状態: liblouis 3.36.0以降に含まれている                    │
│ - メンテナンス: liblouis公式で継続的に更新される             │
│ - 注意: 現在のブランチ（liblouis 3.34.0）には含まれていない │
│   一時的にja-jp-rokutenkanji.tblをコピーして使用            │
└─────────────────────────────────────────────────────────────┘
```

## 問題点と課題

### 1. 名前の衝突

- `ja-jp-rokutenkanji.tbl` は `ja-rokutenkanji.utb` として登録されている
- 上流版の `ja-rokutenkanji.utb` が将来追加された場合、名前が衝突する

### 2. `ja-jp-rokutenkanji.tbl` の依存関係

- `ja-jp-rokutenkanji.tbl` は `include ja-jp-comp6.utb` を含む
- しかし、`ja-jp-comp6.utb` は疑似テーブル（liblouis が処理できない）
- liblouis が `ja-jp-comp6.utb` を解決できない場合、`ja-jp-rokutenkanji.tbl` は動作しない

### 3. 上流版との統合

- 上流版の `ja-rokutenkanji.utb` が追加された場合、nvdajp の `ja-jp-rokutenkanji.tbl` との関係をどうするか

## 推奨される対応

### 短期的な対応（現在のブランチ）

1. **一時的な対応**
   - `nvdaHelper/liblouis/sconscript`で`source/ja-jp-rokutenkanji.tbl`を`source/louis/tables/ja-rokutenkanji.utb`としてコピー
   - これにより、liblouis 3.34.0の環境でもユニットテストが正常に動作する

### 長期的な対応（liblouis 3.36.0以降）

1. **上流版のテーブルを使用**
   - nvaccess/betaのマージでliblouisが3.36.0に更新された場合、上流版の`ja-rokutenkanji.utb`を使用
   - `source/ja-jp-rokutenkanji.tbl`を削除
   - `nvdaHelper/liblouis/sconscript`でのコピー処理を削除

2. **理由**
   - 上流版のテーブルはliblouis公式でメンテナンスされている
   - `include ja-jp-comp6.utb`の問題がない
   - nvdajp独自のメンテナンスが不要

## 参考資料

- `projectDocs/jp/braille-ja-jp-comp6.md` - `ja-jp-comp6.utb` の詳細
- `projectDocs/jp/ja-rokutenkanji-table-fix-plan.md` - `ja-rokutenkanji.utb` テーブル解決エラー修正方針
- `source/ja-jp-rokutenkanji.tbl` - nvdajp 従来の六点漢字テーブル
- `source/brailleTables/__tables.py` - テーブル登録
- `source/louisHelper.py` - エンジン切り替えロジック
- `nvdaHelper/liblouis/sconscript` - ビルドスクリプト（`ja-jp-rokutenkanji.tbl`を`source/louis/tables/ja-rokutenkanji.utb`としてコピー）
