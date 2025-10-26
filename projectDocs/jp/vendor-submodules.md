# ベンダーサブモジュール運用（方針・TODO）

目的: Step 1 の範囲で「本家版に寄せた最小構成」を維持しつつ、JP 固有のベンダーツリー（python‑jtalk など）の取り扱いを明確化する。

## 基本方針（Step 1）

- CI ではベンダーのネイティブ再ビルド（nmake 等）を行わない。testAndPublish と同様に「事前配置された DLL/ソース」を前提とする。
- オーバーレイは SCons で行う（`jtalkPrep` + `miscdepsjp`）。YAML はスクリプト呼び出しのみ（最小）。
- サブモジュールやベンダーツリーの更新は手動手順を明示し、PR では差分を最小化する。

## TODO（実務）

- vendor 構成の確認とドキュメント化
  - 既定: `miscDepsJp/include/python-jtalk` 配下に必要ファイル（`libopenjtalk.dll` を含む）が存在すること。
  - `jptools/copy_jtalk_core_files.cmd` の役割と前提（宛先ディレクトリ、xcopy の無対話化）を README 化。
- 純 Python 化の検討（任意）
  - `copy_jtalk_core_files.cmd` の置き換え（mkdir + コピー）を純 Python スクリプトに分離し、SCons から呼び出せるようにする。
  - これにより YAML からも SCons からも同一経路で実行可能にする。
- 検証の追加（SCons 側）
  - `jtalkPrep` 前後で、最低限の存在チェック（`python-jtalk/libopenjtalk.dll` など）をログに出す軽量検証を追加。
- 更新フロー（手動）
  - ベンダー更新は別トピックブランチで実施し、差分がわかる形で PR 化。
  - nmake 等のネイティブ再ビルドが必要な場合は、別リポ/別ワークフローで行い、本リポでは成果物消費のみに留める。

## 非目標（Step 1 ではやらない）

- CI でのベンダー再ビルド（HTS/libopenjtalk の nmake）
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
  - ベンダーの nmake などの再ビルドは行わない
  - アーティファクト系は「オーバーレイ検証＋収集」に限定（既存 DLL が無ければスキップ・成功扱い）

- x64 への段階
  - 段階1: x86 運用を揃える（SCons の自動選択と検証）
  - 段階2: x64 DLL を同一レイアウトで提供→SCons で TARGET_ARCH=x64 を選択可能に
  - 段階3: testAndPublish のマトリクスに x64 を段階的に追加（typeCheck→unit→system）
