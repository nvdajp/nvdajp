# ベンダーサブモジュール運用（方針・TODO）

目的: Step 1 の範囲で「本家版に寄せた最小構成」を維持しつつ、JP 固有のベンダーツリー（python‑jtalk など）の取り扱いを明確化する。

## 基本方針（Step 1）

- SCons が必要に応じて自動的にベンダーをビルド（nmake 等）。開発者・CI ともに `scons` コマンドのみを意識すればよい。
- DLL が既に存在する場合は再ビルドをスキップ（ビルド時間の短縮）。
- オーバーレイは SCons で行う（`jtalkPrep` + `miscdepsjp`）。YAML はスクリプト呼び出しのみ（最小）。
- サブモジュールやベンダーツリーの更新は手動手順を明示し、PR では差分を最小化する。

## 実装済み（Step 1）

- SCons でのオンデマンドビルド（`jtalkPrep` 拡張）
  - DLL 不在時: 自動的に `nmake /f all.mak` を実行してビルド
  - TARGET_ARCH（x86/x64）に応じて `MACHINE=x64` を渡す
  - ビルド成功後、生成された DLL を payload に配置
  - DLL 存在時: 再ビルドをスキップし「build skipped」とログ出力
- 検証・ログ出力
  - `jtalkPrep` がアーキテクチャ・探索パス・ビルド有無をログ出力
  - エラー時は明確なメッセージ（MSVC 環境、サブモジュール取得の案内）

## TODO（将来）

- 純 Python 化の検討（Phase 2 以降）
  - nmake への依存を削減するため、ビルドロジックの純 Python 化を検討
  - Step 1 では nmake の使用を許容（内部実装の詳細として隠蔽）
- ベンダー更新フロー
  - サブモジュール更新時は、生成される DLL のハッシュ値を記録（検証用）
  - 別トピックブランチで実施し、差分がわかる形で PR 化

## 非目標（Step 1 ではやらない）

- YAML でのベンダービルドロジック（SCons に集約するため）
- YAML での複雑な同期・ミラー（robocopy / submodule 再展開等）

## 関連

- AGENTS.md（SCons/純 Python 優先、YAML は最小）
- projectDocs/jp/roadmap.md（Step 1 の目的・除外、CI の原則）

## python‑jtalk 運用（Step 1）

### 現在の動作（実装済み）

- **ビルド方法**: SCons が自動的にオンデマンドビルド
  - DLL 不在時: `jtalkPrep` が `nmake /f all.mak` を実行
  - DLL 存在時: 再ビルドスキップ（高速）
  - 開発者は `scons dist` だけを実行すればよい

- **レイアウト**（現状）
  - x86: `miscDepsJp/include/python-jtalk/libopenjtalk.dll`（直下）
  - x64: `miscDepsJp/include/python-jtalk/x64/libopenjtalk.dll`（将来対応）
  - MeCab 辞書: アーキ非依存のため共通

- **サブモジュール更新手順**
  - サブモジュール更新: `git submodule update --init --recursive`
  - 固定コミットへ: 該当ディレクトリで `git checkout <commit>`
  - DLL 削除（任意）: 既存 DLL を削除すれば次回ビルド時に自動再ビルド
  - 確認: `scons miscdepsjp` で自動ビルド＋overlay を確認
  - PR 提出: 小粒 PR でサブモジュール更新を記録

### 将来の TODO

- **x64 対応**
  - x64 DLL を `miscDepsJp/include/python-jtalk/x64/` に配置
  - `scons miscdepsjp TARGET_ARCH=x64` で自動ビルド可能
  - testAndPublish のマトリクスに x64 を段階追加（typeCheck→unit→system）

- **純 Python 化**（Phase 2 以降）
  - copy_jtalk_core_files.cmd を Python スクリプト化
  - nmake の置き換えを検討（現状は内部実装の詳細として許容）

## 固定したベンダーのリビジョン（参考）

- python‑jtalk: 40eb632705e1f16d64b96755cf923b5feb0e688f （PR #2 merge, Add optional x64 build support）
  - URL: https://github.com/nvdajp/python-jtalk/commit/40eb632705e1f16d64b96755cf923b5feb0e688f

## 付録: 開発者の操作とログ例

### 通常のビルド（開発者が意識するコマンド）

```bash
# これだけでビルド完結（ベンダービルド・overlay・dist 作成すべて自動）
scons dist

# または
scons source user_docs launcher
```

**内部で自動実行される**（開発者は意識不要）:

1. `jtalkPrep`: DLL チェック → 無ければ nmake でビルド → payload に配置
2. `miscdepsjp`: overlay で `source/` に配置
3. `source`, `dist` などのビルド

### ログ例（scons dist 実行時）

**DLL 存在時（再ビルドスキップ）**:

```text
jtalkPrep: using TARGET_ARCH=x86
jtalkPrep: looking for vendor DLL: miscDepsJp/include/python-jtalk/libopenjtalk.dll
jtalkPrep: using existing DLL (build skipped)
jtalkPrep: payload -> miscDepsJp/source/synthDrivers/jtalk/libopenjtalk.dll
```

**DLL 不在時（自動ビルド）**:

```text
jtalkPrep: using TARGET_ARCH=x86
jtalkPrep: looking for vendor DLL: miscDepsJp/include/python-jtalk/libopenjtalk.dll
jtalkPrep: DLL not found, attempting to build via nmake...
jtalkPrep: running: nmake /f all.mak in miscDepsJp/include/python-jtalk
[nmake の出力...]
jtalkPrep: build succeeded, DLL created at miscDepsJp/include/python-jtalk/libopenjtalk.dll
jtalkPrep: payload -> miscDepsJp/source/synthDrivers/jtalk/libopenjtalk.dll
```

### 手動で overlay だけ実行したい場合（通常は不要）

```bash
# overlay のみ実行（デバッグ用）
scons miscdepsjp

# x64 用（将来）
scons miscdepsjp TARGET_ARCH=x64
```
