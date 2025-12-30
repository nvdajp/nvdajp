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

## 2. `ja-jp-rokutenkanji.tbl` - nvdajp 従来の六点漢字テーブル

### 特徴

- **ファイル**: `source/ja-jp-rokutenkanji.tbl`
- **インストール先**: `dist/louis/tables/`（`TABLES_DIR`）
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

## 3. 上流版の `ja-rokutenkanji.utb` - liblouis 公式の六点漢字テーブル

### 特徴

- **ファイル**: `include/liblouis/tables/ja-rokutenkanji.utb`（**現在存在しない**）
- **登録**: `source/brailleTables/__tables.py` で `ja-rokutenkanji.utb` として登録されている
- **変換エンジン**: **liblouis を使用**
- **状態**: 上流版の liblouis には**まだ含まれていない**（x64移行時点）

### 現状

- `source/brailleTables/__tables.py` では `ja-rokutenkanji.utb` が登録されている
- しかし、`include/liblouis/tables/` には `ja-rokutenkanji.utb` が存在しない
- これは、上流版の NVDA が将来の liblouis バージョンに含まれる予定のテーブルを先取りして登録している可能性がある

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
│ ja-jp-rokutenkanji.tbl (nvdajp 従来)                        │
│ - 登録名: ja-rokutenkanji.utb                               │
│ - 変換エンジン: liblouis                                     │
│ - インストール先: dist/louis/tables/ (TABLES_DIR)          │
│ - 問題: include ja-jp-comp6.utb を含むが、                  │
│   疑似テーブルなので liblouis が解決できない可能性          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ ja-rokutenkanji.utb (上流版・将来)                         │
│ - 変換エンジン: liblouis                                     │
│ - インストール先: dist/louis/tables/ (TABLES_DIR)          │
│ - 状態: 現在存在しない（将来の liblouis に含まれる予定？）  │
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

### 短期的な対応

1. **`ja-jp-rokutenkanji.tbl` の修正**
   - `include ja-jp-comp6.utb` を削除し、必要な定義を直接含める
   - または、`ja-jp-comp6.utb` の内容を liblouis が処理できる形式に変換

2. **名前の変更**
   - `ja-jp-rokutenkanji.tbl` を `ja-jp-rokutenkanji.utb` として登録（現在は `ja-rokutenkanji.utb`）
   - 上流版の `ja-rokutenkanji.utb` との衝突を回避

### 長期的な対応

1. **上流版との統合方針の決定**
   - 上流版の `ja-rokutenkanji.utb` が追加された場合、nvdajp の `ja-jp-rokutenkanji.tbl` をどうするか
   - 統合するか、別名で維持するか

2. **ドキュメントの更新**
   - 各テーブルの関係と用途を明確化
   - ユーザー向けの説明を追加

## 参考資料

- `projectDocs/jp/braille-ja-jp-comp6.md` - `ja-jp-comp6.utb` の詳細
- `source/ja-jp-rokutenkanji.tbl` - nvdajp 従来の六点漢字テーブル
- `source/brailleTables/__tables.py` - テーブル登録
- `source/louisHelper.py` - エンジン切り替えロジック
