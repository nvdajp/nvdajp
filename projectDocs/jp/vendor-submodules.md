# ベンダーサブモジュール運用（方針・TODO）

目的: Step 1 の範囲で「本家版に寄せた最小構成」を維持しつつ、JP 固有のベンダーツリー（python‑jtalk など）の取り扱いを明確化する。

## 基本方針（Step 1）

- SCons が必要に応じて自動的にベンダーをビルド（nmake 等）。開発者・CI ともに `scons` コマンドのみを意識すればよい。
- DLL が既に存在する場合は再ビルドをスキップ（ビルド時間の短縮）。
- オーバーレイは SCons で行う（`jtalkPrep` + `miscdepsjp`）。YAML はスクリプト呼び出しのみ（最小）。
- サブモジュールやベンダーツリーの更新は手動手順を明示し、PR では差分を最小化する。

## TODO（実務）

- SCons でのオンデマンドビルド実装
  - `jtalkPrep` を拡張し、DLL が存在しない場合は自動的に nmake を実行してビルド
  - TARGET_ARCH（x86/x64）に応じて適切なビルドパラメータを渡す
  - ビルド成功後、生成された DLL を payload に配置
- 検証の追加（SCons 側）
  - `jtalkPrep` でアーキテクチャ・探索パス・ビルド有無をログ出力
  - DLL 存在時は再ビルドをスキップし、その旨をログに記録
- 純 Python 化の検討（中長期）
  - nmake への依存を将来的に削減するため、ビルドロジックの純 Python 化を検討
  - ただし Step 1 では nmake の使用を許容する
- 更新フロー（手動）
  - ベンダー更新は別トピックブランチで実施し、差分がわかる形で PR 化
  - サブモジュール更新時は、生成される DLL のハッシュ値を記録（検証用）

## 非目標（Step 1 ではやらない）

- YAML でのベンダービルドロジック（SCons に集約するため）
- YAML での複雑な同期・ミラー（robocopy / submodule 再展開等）

## 関連

- AGENTS.md（SCons/純 Python 優先、YAML は最小）
- projectDocs/jp/roadmap.md（Step 1 の目的・除外、CI の原則）

## python‑jtalk TODO（運用を明確化）

- レイアウト（推奨・準備）
  - miscDepsJp/include/python-jtalk/ 配下にアーキ別 DLL を用意（将来移行用）
    - 例: x86/libopenjtalk.dll、x64/libopenjtalk.dll
    - 現状の単一路径（直下の libopenjtalk.dll）は当面維持。SCons 側で TARGET_ARCH に応じて自動選択できるようにする。
  - MeCab 辞書はアーキ非依存のため共通（現行の配置を維持）。

- 成果物要件（各アーキ）
  - 必須: libopenjtalk.dll
  - 任意: libmecab.dll（使用している場合のみ）
  - ライセンス: COPYING-HTS_engine_API.txt、COPYING-libopenjtalk.txt を同梱

- バージョニング／供給方法
  - python‑jtalk 側で GitHub リリース（x86/x64 両 DLL とハッシュ）を発行
  - 本リポはサブモジュール（固定コミット）で追従し、DLL はリリースから取得して配置（再ビルドはしない）

- 更新手順（手動）
  - サブモジュール更新（git submodule update --remote 等）→ 追従コミットへ固定
  - DLL を python-jtalk/（x86|x64）/libopenjtalk.dll に配置（当面は直下の DLL も残す）
  - scons miscdepsjp でオーバーレイ確認→小粒 PR 提出（DLL 由来を明記）

- 検証（自動）
  - SCons に軽量チェックを追加（例）:
    - TARGET_ARCH の DLL 探索→存在しない場合は明確なエラー
    - overlay へコピーした DLL のパスをログ出力

- コピー処理の純 Python 化（中期）
  - copy_jtalk_core_files.cmd の mkdir/xcopy 相当を jptools/vendor_sync.py に集約
  - 非対話・再入可能・差分最小を満たすこと

- CI 方針（Step 1）
  - SCons が必要に応じて自動的にベンダーをビルド（DLL 不在時のみ）
  - YAML 側ではビルドロジックを持たず、`scons dist` などの標準コマンドのみを実行

- x64 への段階
  - 段階1: x86 運用を揃える（SCons の自動選択と検証）
  - 段階2: x64 DLL を同一レイアウトで提供→SCons で TARGET_ARCH=x64 を選択可能に
  - 段階3: testAndPublish のマトリクスに x64 を段階的に追加（typeCheck→unit→system）

## 固定したベンダーのリビジョン（参考）

- python‑jtalk: 40eb632705e1f16d64b96755cf923b5feb0e688f （PR #2 merge, Add optional x64 build support）
  - URL: https://github.com/nvdajp/python-jtalk/commit/40eb632705e1f16d64b96755cf923b5feb0e688f

## 付録: SCons オーバーレイの例と使い方

- 目的: CI/開発双方で「SCons がベンダービルドを自動処理」することを可視化。
- ログ例（想定）:
  - DLL 存在時（再ビルドスキップ）:
    - jtalkPrep: using TARGET_ARCH=x86
    - jtalkPrep: found vendor DLL: miscDepsJp/include/python-jtalk/libopenjtalk.dll
    - jtalkPrep: payload -> miscDepsJp/source/synthDrivers/jtalk/libopenjtalk.dll
  - DLL 不在時（自動ビルド）:
    - jtalkPrep: using TARGET_ARCH=x86
    - jtalkPrep: DLL not found, attempting to build via nmake...
    - jtalkPrep: running: nmake /f all.mak in miscDepsJp/include/python-jtalk
    - jtalkPrep: build succeeded, DLL created at miscDepsJp/include/python-jtalk/libopenjtalk.dll
    - jtalkPrep: payload -> miscDepsJp/source/synthDrivers/jtalk/libopenjtalk.dll
- 使い方（例）:
  - x86 既定: `scons miscdepsjp`
  - 明示 x86: `scons miscdepsjp TARGET_ARCH=x86`
  - 将来の x64 ビルド: `scons miscdepsjp TARGET_ARCH=x64`
    - x64 DLL が無い場合は自動的に `nmake /f all.mak MACHINE=x64` を実行
