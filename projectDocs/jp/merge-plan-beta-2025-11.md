# nvaccess/beta から betajp へのマージ計画（Step 1）

この文書は、`projectDocs/jp/roadmap.md` の **Phase 1: 基盤整合と安定化（Step 1）** 方針に基づき、nvaccess/beta を betajp にマージするための段階的な実行計画です。

## この計画書の位置づけ

- **上位ロードマップ**: `projectDocs/jp/roadmap.md` の Phase 1 (Step 1) 全体が目標
- **この計画書**: Step 1 の中での「nvaccess/beta マージ作業」を細分化した作業段階（Phase 1-7）
- **用語の注意**: 
  - `roadmap.md` の「Phase 1」= Step 1 全体（大きなマイルストーン）
  - この計画書の「Phase 1-7」= Step 1 の中の細かい作業段階（作業フェーズ）

## 前提条件

- **目標**: Python 3.11 x86 を維持したまま、本家 beta の変更を取り込み、CI/ビルドは上流構成に整合（差分は最小）
- **除外**: Python 3.13 への移行、x64/arm64 切替、JAB 64bit、コードサイニング/配布の CI 実施
- **方針**: JP 固有は `ci/scripts/**` に寄せ、YAML には呼び出し1行＋`# BEGIN/END JP PATCH` マーカーのみ

## マージ戦略

### 原則

1. **上流優先**: 上流ファイルをベースに丸ごと更新 → JP 追加は最小化
2. **段階的解決**: 小さなPR単位で進め、各段階でテスト通過を確認
3. **差分最小化**: JP 固有変更は `# nvdajp begin/end` または `# BEGIN JP PATCH`/`# END JP PATCH` で明示
4. **検証必須**: 各段階でビルド・型チェック・単体テストを通過確認

### 作業順序

コンフリクトを優先度順に分類し、依存関係を考慮して段階的に解決します。

## 準備段階（Phase 0）

### 0.1 コンフリクトレポートの記録

**状態**: ✅ 完了（PR #570）

**成果物**:
- `projectDocs/jp/merge-conflicts-detailed-2025-11.md` - 詳細コンフリクト記録
- `projectDocs/jp/merge-issues-beta-2025-11.md` - 問題まとめ
- `projectDocs/jp/merge-issues-beta-2025-11.meta.md` - メタ情報
- `ci/scripts/tests/recordMergeConflicts.ps1` - コンフリクト記録スクリプト

**次のステップ**: 作業段階 1 から順次実行

## 作業段階 1: 基盤整備（依存関係の解決）

**注**: この「作業段階 1」は `roadmap.md` の Phase 1 (Step 1) の中の最初の作業フェーズです。

### 1.1 サブモジュールとロックファイル
**優先度**: 最高（他の作業の前提）

**タスク**:
- [ ] `miscDeps` サブモジュールのコンフリクト解決
  - 上流のコミットを採用
  - `git add miscDeps` で確定
- [ ] `.python-versions` の解決
  - 上流: `cpython-3.13.9-windows-x86_64-none`
  - JP: `cpython-3.11.9-windows-x86-none` を維持（Step 1 方針）
  - 解決: `cpython-3.11.9-windows-x86-none` のみ（3.13 は除外）
- [ ] `uv.lock` の再生成
  - コンフリクト解決後、ローカルで `uv lock --upgrade` を実行
  - Python 3.11 x86 環境で生成
  - 再生成前に `requires-python = "==3.11.*"` を確認

**検証**:
- `uv sync` が正常に完了
- `uv lock` がエラーなく実行

**PR**: `fix/merge-step1-foundation` (小規模)

---

## 作業段階 2: ビルドシステム（SCons・ヘルパー）

### 2.1 NVDAHelper パッケージ化
**優先度**: 高（多くのファイルが依存）

**タスク**:
- [ ] `source/NVDAHelper/__init__.py` のコンフリクト解決
  - 上流のパッケージ構成を採用
  - 旧 `source/NVDAHelper.py` からの import を `source/NVDAHelper/__init__.py` に移行
  - JP 固有の変更があれば `# nvdajp begin/end` で囲う
- [ ] 旧 `NVDAHelper.py` 参照の検索・置換
  - `grep -r "from NVDAHelper import"` で参照箇所を検索
  - `from NVDAHelper import` → `from NVDAHelper import` (パッケージとして読み込む)
  - `import NVDAHelper` → `from NVDAHelper import` に統一

**検証**:
- 型チェック: `ci/scripts/tests/typeCheck.ps1`
- ビルド: `scons source --all-cores`

**PR**: `fix/merge-step1-nvdahelper-package`

### 2.2 nvdaHelper/archBuild_sconscript
**優先度**: 高（ビルドに必須）

**タスク**:
- [ ] eSpeak ビルド条件の解決（267行目）
  - 上流: `if isNVDACoreArch:` (x86/x64/arm64 すべて)
  - JP: `if TARGET_ARCH == "x86":` (x86 のみ)
  - 解決: Step 1 では `if TARGET_ARCH == "x86":` を維持
    - ただし上流の構造に合わせて条件を整理
    - `# nvdajp begin: Step 1 - x86 only` コメントで明示
- [ ] liblouis と javaAccessBridge の条件も確認
  - 上流では `isNVDACoreArch` で条件分岐
  - JP では x86 のみビルド

**検証**:
- ビルド: `scons source --all-cores`
- 生成物確認: `source/liblouis.dll` が存在

**PR**: `fix/merge-step1-scons-arch` (2.1 と統合可能)

---

## 作業段階 3: CI/ワークフロー（最大のコンフリクト）

### 3.1 testAndPublish.yml の完全再構築
**優先度**: 高（22箇所のコンフリクト）

**戦略**: 上流ファイルを丸ごと取り込み、JP パッチを最小限に再適用

**タスク**:
- [ ] 上流ファイルをベースに取得
  ```powershell
  git show nvaccess/beta:.github/workflows/testAndPublish.yml > .github/workflows/testAndPublish.yml.upstream
  ```
- [ ] JP 固有の変更点をリストアップ
  - Python/Arch を 3.11/x86 固定
  - `ci/scripts/tests/beforeTests.ps1` の呼び出し
  - crowdin upload ジョブの無効化
  - SCons 実行前の `ilammy/msvc-dev-cmd@v1` で `arch: x86`
  - キャッシュキーに `run_id`/`pythonVersion`/`arch` を含める
- [ ] 上流ファイルをベースに、JP パッチを `# BEGIN JP PATCH`/`# END JP PATCH` で最小限に注入

**JP パッチ箇所**:
1. **トリガー** (6行目): ブランチ名を `betajp`/`releasejp` に変更
2. **Python セットアップ** (複数箇所): `python-version: '3.11.9'`, `architecture: 'x86'` に固定
3. **MSVC セットアップ** (複数箇所): `arch: x86` を追加
4. **beforeTests.ps1 呼び出し** (192行目付近): システムテスト前に実行
5. **crowdinUpload ジョブ** (447-456行目): `if: ${{ false }}` で無効化（既存パッチ継続）
6. **キャッシュキー**: `run_id`/`pythonVersion`/`arch` を含める

**検証**:
- YAML 構文チェック: `gh workflow view testAndPublish.yml`
- ローカルで主要ジョブをシミュレート（実際の実行は PR 後に）

**PR**: `fix/merge-step1-workflow-rebase` (大規模、慎重にレビュー)

---

## 作業段階 4: ソースコード（機能的なコンフリクト）

### 4.1 構文・軽微な変更
**優先度**: 中

**タスク**:
- [ ] `source/_remoteClient/secureDesktop.py` (483行目)
  - 上流: f-string の引数が変更
  - 解決: 上流の形式を採用（f-string の引数は上流に合わせる）
- [ ] `runlint.bat` (12行目)
  - 上流: ruff format の出力先処理が変更
  - 解決: 上流の形式を採用し、JP 固有の除外オプションは維持

**検証**:
- Lint: `uv run ruff format --check && uv run ruff check`
- ビルド: `scons source --all-cores`

**PR**: `fix/merge-step1-source-minor`

### 4.2 Braille 表示ロジック（JP 拡張の再適用）
**優先度**: 中（機能的な差分）

**タスク**:
- [ ] `source/braille.py` の2箇所のコンフリクト解決
  - **802行目**: `_nvdajp("vlnk")` vs `_("vlnk")`
    - 上流の `_("vlnk")` を採用
    - JP 固有の翻訳が必要なら `_nvdajp()` を維持（ただし上流の構造に合わせる）
  - **886行目**: ロール処理順序の変更
    - 上流の処理順序を採用
    - JP 固有の変更（rowHeaderText/columnHeaderText）は `# nvdajp begin/end` で囲って維持（835-842行目）
- [ ] `tests/unit/test_brailleTables.py` (23行目)
  - 上流: `subTest` 構造に変更
  - JP: `TABLES_DIR_JP` を参照する独自ロジック
  - 解決: 上流の `subTest` 構造を採用し、JP テーブルチェックは条件分岐で追加
    ```python
    with self.subTest(table=table.fileName):
        tables_dir = brailleTables.TABLES_DIR
        if table.displayName in ("Japanese 6 dot computer braille", ...):
            tables_dir = brailleTables.TABLES_DIR_JP
        self.assertTrue(...)
    ```

**検証**:
- 単体テスト: `rununittests.bat`
- ビルド: `scons source --all-cores`

**PR**: `fix/merge-step1-braille` (機能テストを追加)

### 4.3 GUI・インストーラ（JP 固有の表示）
**優先度**: 中

**タスク**:
- [ ] `source/gui/__init__.py` (113行目)
  - ICON_PATH: `nvdajp3.ico` を維持（JP 固有）
  - DONATE_URL: `https://www.nvda.jp/donate.html` を維持（JP 固有）
  - 上流の `buildVersion` への変更は採用
  - 解決: 上流の構造を採用し、JP 固有の値は `# nvdajp begin/end` で囲う
- [ ] `source/installer.py` (276行目)
  - DisplayIcon: `nvdajp3.ico` を維持（JP 固有）
  - 上流の `buildVersion` への変更は採用
  - 解決: 同様に上流構造を採用し、JP 固有値を明示

**検証**:
- ビルド: `scons source --all-cores`
- インストーラビルド: `scons dist launcher` (ローカルのみ)

**PR**: `fix/merge-step1-gui-installer`

### 4.4 合成音声ドライバ
**優先度**: 中

**タスク**:
- [ ] `source/synthDriverHandler.py` (486行目)
  - 上流: `["oneCore", "espeak", "silence"]`
  - JP: `["nvdajp_jtalk", "espeak", "silence"]` を先頭に
  - 解決: JP の優先順位を維持（jtalk を先頭）
    - ただし上流の構造（Windows 10 で oneCore を先頭）は条件分岐で維持
    ```python
    defaultSynthPriorityList = ["nvdajp_jtalk", "espeak", "silence"]
    if winVersion.getWinVer() >= winVersion.WIN10:
        # Insert oneCore for Windows 10+, but keep jtalk first
        defaultSynthPriorityList.insert(1, "oneCore")
    ```

**検証**:
- ビルド: `scons source --all-cores`
- 単体テスト: `rununittests.bat`

**PR**: `fix/merge-step1-synth` (4.3 と統合可能)

---

## 作業段階 5: テスト（テストコードの整合）

### 5.1 SystemTest 設定
**優先度**: 低（テストのみ）

**タスク**:
- [ ] `tests/system/libraries/SystemTestSpy/configManager.py` (131行目)
  - 上流: シンプルな `remove_directory` 呼び出し
  - JP: リトライロジックと `taskkill` 呼び出し
  - 解決: JP のリトライロジックを維持（CI での安定性向上）
    - ただし上流の構造に合わせて整理
    - `# nvdajp begin: retry logic for CI stability` で明示

**検証**:
- システムテスト: `ci/scripts/tests/systemTests.ps1` (ローカルで実行)

**PR**: `fix/merge-step1-tests` (作業段階 4 と統合可能)

---

## 作業段階 6: 翻訳ファイル（大規模、手動作業）

### 6.1 nvda.po のマージ
**優先度**: 中（38箇所のコンフリクト）

**タスク**:
- [ ] 上流 pot ファイルを取得
  ```powershell
  git show nvaccess/beta:source/locale/ja/LC_MESSAGES/nvda.po > nvda.po.upstream
  ```
- [ ] msgmerge で上流 pot に追随
  ```powershell
  msgmerge -U source/locale/ja/LC_MESSAGES/nvda.po nvda.pot
  ```
- [ ] コンフリクト箇所を手動で解決
  - 上流の翻訳を優先
  - JP 固有の追加翻訳（IME 関連など）は維持
  - メタ情報（POT-Creation-Date など）は上流に合わせる
- [ ] 翻訳チェック
  ```powershell
  ci/scripts/tests/translationCheck.ps1
  ```

**検証**:
- 翻訳チェック: `ci/scripts/tests/translationCheck.ps1`
- ビルド: `scons source --all-cores`

**PR**: `fix/merge-step1-translation` (大規模、レビュー要)

---

## 作業段階 7: 最終統合と検証

### 7.1 全体マージの実行
**優先度**: 最高

**タスク**:
- [ ] すべての PR を betajp にマージ
- [ ] 上流 beta との最終マージを実行
  ```powershell
  git checkout betajp
  git pull origin betajp
  git merge nvaccess/beta
  ```
- [ ] 残存コンフリクトの確認
  - 予期しないコンフリクトがないか確認
  - 各作業段階で解決したはずのファイルに再コンフリクトがないか確認

**検証**:
- 型チェック: `ci/scripts/tests/typeCheck.ps1`
- Lint: `uv run ruff format --check && uv run ruff check`
- ビルド: `scons source --all-cores`
- 単体テスト: `rununittests.bat`
- CI: GitHub Actions で全ジョブがグリーン

**PR**: `merge/beta-2025-11-final` (または直接 betajp にマージ)

---

## リスクと対策

### リスク 1: コンフリクトの再発
**対策**: 各作業段階で解決したファイルを追跡し、最終マージ時に再確認

### リスク 2: ビルド失敗
**対策**: 各作業段階でビルドを検証し、失敗した場合はその作業段階で修正

### リスク 3: テスト失敗
**対策**: 単体テストは各作業段階で実行し、システムテストは最終作業段階で実行

### リスク 4: 翻訳ファイルの大規模変更
**対策**: 作業段階 6 は独立して進め、他の作業段階の影響を受けないようにする

---

## 参照

- 詳細コンフリクト記録: `projectDocs/jp/merge-conflicts-detailed-2025-11.md`
- 問題点まとめ: `projectDocs/jp/merge-issues-beta-2025-11.md`
- ロードマップ: `projectDocs/jp/roadmap.md`
- エージェント向け: `AGENTS.md`

---

## 改変の目的・経緯に関する質問リスト

このセクションは、計画書作成時に nvdajp 側の改変の目的や経緯が不明確だった箇所をまとめたものです。回答を追加して計画書を完成させてください。

### 1. `_nvdajp()` 関数の目的と経緯
**箇所**: `source/braille.py` の `_nvdajp("vlnk")` vs `_("vlnk")` (802行目付近)

**質問**:
- `_nvdajp()` 関数は何のために存在しますか？標準の `_()` 関数では不十分な理由は？
- この関数はどのような処理をしますか？（独自の翻訳ロジック、フォールバックなど）
- いつ導入されましたか？関連する Issue や PR はありますか？

**回答**: *(to be written)*

---

### 2. `rowHeaderText` と `columnHeaderText` の追加
**箇所**: `source/braille.py` 835-842行目（issue #109）

**質問**:
- issue #109 の内容を教えてください
- なぜこの追加が必要でしたか？日本語点字表示の特殊要件ですか？
- 上流でも同様の機能追加が予定されていますか？

**回答**: *(to be written)*

---

### 3. `TABLES_DIR_JP` の必要性
**箇所**: `tests/unit/test_brailleTables.py` (23行目付近)

**質問**:
- 日本語点字テーブルを別ディレクトリに分ける理由は？
- どのようなテーブルが `TABLES_DIR_JP` にありますか？
- 将来的に上流に統合する予定はありますか？

**回答**: *(to be written)*

---

### 4. jtalk の優先順位
**箇所**: `source/synthDriverHandler.py` の `defaultSynthPriorityList` (486行目付近)

**質問**:
- jtalk を先頭にする理由は？（日本語ユーザー向けのデフォルト設定など）
- 上流の oneCore 優先方針との整合性は問題ありませんか？
- Windows 10 以降でも jtalk を先頭にする必要はありますか？

**回答**: *(to be written)*

---

### 5. アイコンパスとドネーションURLの変更
**箇所**: `source/gui/__init__.py` (113行目付近) と `source/installer.py` (276行目付近)

**質問**:
- `nvdajp3.ico` はどのようなアイコンですか？（日本語版のロゴなど）
- なぜ標準の `nvda.ico` では不十分ですか？
- ドネーションURLは日本語版専用のページですか？統合予定はありますか？

**回答**: *(to be written)*

---

### 6. SystemTest のリトライロジック
**箇所**: `tests/system/libraries/SystemTestSpy/configManager.py` (131行目付近)

**質問**:
- リトライロジックと `taskkill` 呼び出しが必要だった理由は？
- CI環境で発生していた問題は何ですか？（ファイルロック、プロセス終了など）
- 上流でも同様の問題が発生しますか？

**回答**: *(to be written)*

---

### 7. `nvdaHelper/archBuild_sconscript` の x86 限定条件
**箇所**: eSpeak ビルド条件 (267行目付近)

**質問**:
- なぜ x86 限定にしていますか？（Step 1 の制約以外に技術的理由はありますか）
- 上流の `isNVDACoreArch` への移行は roadmap.md の Phase 2 以降で検討しますか？

**回答**: *(to be written)*

---

### 8. その他、計画書に記載すべき改変の目的・経緯

**質問**:
- 他に重要な改変があれば、その目的と経緯を教えてください

**回答**: *(to be written)*

