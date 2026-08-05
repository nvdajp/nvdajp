# システムテスト・CI カスタマイズ方針

**最終更新**: 2026-07-30
**対象ブランチ**: betajp（alphajp も原則準拠）

## 1. 基本原則

### 1.1 最小差分の原則

- upstream（nvaccess/beta）のファイルを変更する場合は、必要最小限の差分に留める
- JP 独自の追加は `# BEGIN JP PATCH` / `# END JP PATCH` で明示する（3 行以上の場合）
- 1〜2 行の変更は `# nvdajp` コメントでマークする
- JP 独自の新規ファイル（`jptools/` 配下など）にはマーカー不要

### 1.2 upstream 構造の尊重

- upstream のテスト分割・タグ構造・CI ワークフロー設計は、理由があってその形になっている
- むやみに構造を変更せず、JP 独自要件は「追加」で対応する
- upstream の設計意図が不明な場合は、コードコメントや PR 履歴から推測し、文書化する

### 1.3 テストの目的別分類

NVDA 日本語版は **OS ロケールに依存せず**、英語 Windows 上でも日本語 UI・日本語音声で動作する。
海外の日本語学習者や、英語 Windows を使う日本語話者もユーザーになりうる。
したがって「CI が英語 Windows だから」という理由だけでテストを除外すべきではない。

| 分類 | 説明 | CI 実行 | タグ |
|------|------|---------|------|
| **汎用テスト** | ロケール非依存、upstream と共通 | ✅ 実行 | upstream のタグを維持 |
| **JP 追加テスト** | NVDA 日本語版の機能を検証。OS ロケール非依存 | ✅ 実行（原則） | なし（CI で通す） |
| **JP 環境依存テスト** | 日本語 OS ロケール・日本語 IME が必須 | ❌ CI では除外 | `skip_in_ci` |
| **フレーキーテスト** | CI インフラ（音声デバイス不在等）で不安定 | ❌ CI では除外 | `skip_in_ci` + 理由コメント |

**分類の考え方**:

```
NVDA 日本語版をインストールすれば動くか？
  ├── YES（OS ロケール問わず）→ JP 追加テスト。CI で通すのが目標
  └── NO（日本語 OS ロケール必須）→ JP 環境依存テスト。skip_in_ci
```

**具体例**:

| テスト | 分類 | 根拠 |
|--------|------|------|
| WAIC aria-describedby | **JP 追加テスト** | JTalk が日本語を読めればパスする。OS ロケール不要 |
| chrome_link | **JP 追加テスト** | NVDA 日本語版の UI 文字列で判定。OS ロケール不要 |
| 記号発音（symbols） | **フレーキー** | 音声デバイス不在でタイムアウト。OS ロケールではない |
| 日本語 IME 入力 | **JP 環境依存** | 日本語キーボードレイアウト・IME が OS に必要 |
| 日本語点字（KGS） | **JP 追加テスト** | 点字ディスプレイ不要なら理論上 CI 可 |

## 2. ファイル別カスタマイズ方針

### 2.1 `.github/workflows/testAndPublish.yml`

**変更許可範囲**:
- `testSuite` マトリクスへの JP 独自テスト追加
- タイムアウト値の調整（JP 独自ターゲットのビルド時間を考慮）
- `EXCLUDE_SYSTEM_TEST_TAGS` 環境変数の追加
- JP 独自ジョブ（`jpSmokeTests`, `publishBetaRelease`）の追加
- キャッシュキーへの `SCONS_CACHE_SUFFIX` 追加

**変更禁止**:
- upstream ジョブの削除（無効化は `if: false` で行い、元の条件をコメントで残す）
- upstream のジョブ依存関係の変更（追加は可）

**テストスイート戦略**:
- upstream のテスト分割（`chrome_annotations`, `chrome_list` 等）をそのまま維持する
- JP 独自テストは新規タグ（`chrome_waic`）として追加し、独立したジョブで実行する
- 現在の betajp は upstream の 8 分割 + `chrome_waic` の 9 ジョブ構成

### 2.2 `ci/scripts/tests/systemTests.ps1`

**変更許可範囲**:
- `EXCLUDE_SYSTEM_TEST_TAGS` 環境変数の読み取りと `--exclude` への展開
- タイムアウト対策（`cmd /c` ラッパー等）

**`cmd /c` ラッパーの注意点**:
- `cmd /c` でバッチファイルをラップすると、PowerShell 変数展開が文字列内で壊れる
- `@includeTags` と `@excludeTags` が正しく展開されず、Robot Framework にタグが渡らない
- **解決済み**: `cmd /c` を削除し、upstream と同じ直接呼び出し方式に戻した
- 「Terminate batch job」問題が再発した場合は、`runsystemtests.bat` 側で `exit /b %ERRORLEVEL%` を明示する方式で対応する

**検証方法**:
- 変更後は必ず `--include chrome` でテストが 1 件以上実行されることを確認する
- CI ログに `Suite 'Robot' contains no tests matching tag` が出ていないことを確認する

### 2.3 `tests/system/robotArgs.robot`

**原則**: 変更しない

- `--include fakeTagToEnforceUsageOfInclude` は upstream の設計（デフォルトで全テスト除外）
- `systemTests.ps1` が `--include` で上書きする前提
- このファイルを変更すると upstream とのマージが困難になる

### 2.4 `tests/system/robot/chromeTests.robot`

**変更許可範囲**:
- JP 独自テストケース（WAIC 等）の追加
- `[Tags]` への `skip_in_ci` 追加

**変更禁止**:
- upstream テストケースの削除
- upstream の `Force Tags` の削除（`NVDA` タグ等）
- upstream のサブグループタグ（`chrome_list`, `chrome_annotations` 等）の削除

**タグ付けルール**:
```robot
# JP 追加テスト（英語 CI と日本語ローカルの両方で実行）
# WAIC テストは should_contain で日本語コンテンツ文字列のみ検証し、
# ロール名（"button"/"ボタン"）には依存しない
test_waic_as_0029_01
    [Documentation] WAIC テストの説明
    [Tags]  chrome_waic
    test waic as 0029 01
```

### 2.5 `tests/system/robot/chromeTests.py`

**変更許可範囲**:
- JP 独自テスト関数の追加
- 環境差を吸収するリトライ・フォールバック処理の追加
- 複数候補を許容するアサーションの追加

**変更禁止**:
- upstream テスト関数の削除
- upstream の期待値を JP 環境向けに無条件で変更

**環境差吸収パターン**:
```python
# パターン1: 複数候補の許容
_asserts.strings_match_any(
    actualSpeech,
    ["Expected English", "期待される日本語"],
    message="Tab to button",
)

# パターン2: 初期フォーカス差の吸収
actualSpeech = _NvdaLib.getSpeechAfterKey("tab")
if "focus in app" in actualSpeech:
    actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("tab")
elif "push me" in actualSpeech and "has details" in actualSpeech:
    actualBraille = spy.get_last_braille()
else:
    _builtIn.fail(f"Unexpected state: {actualSpeech!r}")

# パターン3: リトライ（遅延解決対応）
actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey(READ_DETAILS_GESTURE)
for _ in range(2):
    if actualSpeech.strip() != "No additional details":
        break
    spy.wait_for_speech_to_finish()
    _builtIn.sleep("0.5 seconds")
    actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey(READ_DETAILS_GESTURE)
```

### 2.6 `tests/system/libraries/ChromeLib.py`

**変更許可範囲**:
- 多言語対応（英語 UI / 日本語 UI 両方のマーカー文字列を検出）

**変更禁止**:
- 既存メソッドのシグネチャ変更
- 既存の待機ロジックの無条件変更

## 3. タグ戦略

### 3.1 タグ一覧

| タグ | 意味 | 設定者 |
|------|------|--------|
| `skip_in_ci` | CI では実行しない | JP |
| `restarts_on_crash` | クラッシュ再起動テスト（CI 不安定） | upstream |
| `excluded_from_build` | ビルドから完全除外 | upstream |
| `robot:skip` | Robot Framework レベルでスキップ | upstream |

### 3.2 CI でのタグ適用

```yaml
# testAndPublish.yml
EXCLUDE_SYSTEM_TEST_TAGS: restarts_on_crash skip_in_ci
```

- `restarts_on_crash`: upstream も CI では除外（クラッシュ再起動は CI 環境で不安定）
- `skip_in_ci`: JP 独自タグ。**日本語 OS ロケールが必須**なテスト、または CI インフラ制約で通過できないテストに付与

### 3.3 タグ付け判断フロー

```
NVDA 日本語版をインストールすれば（OS ロケール問わず）動くか？
  ├── YES → CI で通すのが目標。skip_in_ci は付けない
  │         └── それでも CI で落ちるなら、それはバグ。修正する
  └── NO（日本語 OS ロケール・IME が必須）→ skip_in_ci を付与
```

**`skip_in_ci` を付けるべきケース**（網羅的）:

| ケース | 例 |
|--------|---|
| 日本語 OS ロケール必須 | 日本語 IME の入力・変換テスト |
| 日本語キーボードレイアウト必須 | かな入力モードのテスト |
| CI に物理デバイス不在 | 点字ディスプレイ実機テスト |
| CI インフラ制約（音声デバイス不在等） | 記号発音テストのタイムアウト |

**`skip_in_ci` を付けるべきでないケース**:

| ケース | 理由 |
|--------|------|
| 日本語音声出力の検証（JTalk） | JTalk は英語 Windows でも動作する |
| NVDA 日本語版 UI 文字列の検証 | UI 文字列は OS ロケール非依存 |
| 日本語点字テーブルの検証 | 点字テーブルは OS ロケール非依存 |
| WAIC aria-describedby テスト | JTalk が日本語を読めればパスする |

## 4. テストスイート構成

### 4.1 現在の betajp 構成

```yaml
testSuite:
  - installer
  - startupShutdown
  - chrome_annotations
  - chrome_list
  - chrome_table
  - chrome_language
  - chrome_roleDescription
  - chrome_misc_aria
  - chrome_misc
  - chrome_link
  - chrome_waic  # nvdajp: WAIC aria-describedby tests
```

- upstream の 8 分割をそのまま維持
- `chrome_waic` を JP 独自ジョブとして追加
- `symbols` と `vscode` は除外（CI インフラ制約）

## 5. 日本語環境テストの扱い

### 5.1 WAIC テスト

- **目的**: 日本語の aria-describedby 読み上げを検証
- **分類**: **JP 追加テスト**（JTalk が日本語を読めればパス。OS ロケール不要）
- **CI での扱い**: `chrome_waic` タグで独立ジョブとして実行。`skip_in_ci` は付けない
- **両環境対応**: `should_contain` で日本語コンテンツ文字列のみ検証。ロール名（"button"/"ボタン"）には依存しない
- **ローカル実行**: `runsystemtests.bat --include chrome_waic`
- **参照**: `projectDocs/jp/waic-tests.md`

### 5.2 chrome_link テスト

- **目的**: NVDA+K によるリンク先 URL の報告
- **分類**: **汎用テスト**（upstream と共通。OS ロケール非依存）
- **CI での扱い**: upstream と同じ `chrome_link` タグで実行。`skip_in_ci` は付けない
- **参照**: `projectDocs/jp/chrome-system-test-japanese-environment.md`

### 5.3 記号発音テスト（symbols）

- **目的**: 記号・文字説明の読み上げを検証
- **分類**: **フレーキー**（CI の音声デバイス不在で `Speech did not finish before timeout`）
- **CI での扱い**: 現在除外中
- **対応方針**: タイムアウト延長で解決するか調査。解決しない場合は `skip_in_ci` 維持（CI インフラ制約のため）

### 5.4 真に `skip_in_ci` が必要なテスト

以下の条件に **1 つでも該当**する場合のみ `skip_in_ci` を付与する:

1. 日本語 OS ロケールが必須（IME 入力・変換テスト等）
2. 日本語キーボードレイアウトが必須（かな入力モード等）
3. CI に物理デバイスが不在（点字ディスプレイ実機等）
4. CI インフラ制約でどうしても通過できない（音声デバイス不在等）

**WAIC テストも chrome_link テストも、上記のいずれにも該当しない。**
したがって、これらの `skip_in_ci` は**暫定措置**であり、根本原因を修正して CI で通すのが目標である。

## 6. 既知の問題と対応状況

### 6.1 `cmd /c` ラッパーによるタグ引数破壊 ✅ 解決済み

- **問題**: PR #713 の `cmd /c` ラッパーが `@includeTags` / `@excludeTags` の展開を阻害
- **影響**: Chrome テストが 0 件実行（`fakeTagToEnforceUsageOfInclude` のみ有効）
- **対応**: `cmd /c` を削除し、upstream と同じ直接呼び出し方式に戻した

### 6.2 テストスイート統合による upstream との乖離 ✅ 解決済み

- **問題**: upstream の 8 分割を `chrome` 1 つに統合していた
- **対応**: upstream の 8 分割を復元。JP 独自テストは `chrome_waic` として追加

### 6.3 `Force Tags` からの `NVDA` タグ削除 ✅ 解決済み

- **問題**: `chromeTests.robot` の `Force Tags` から `NVDA` が削除されていた
- **対応**: upstream の `Force Tags` を復元

### 6.4 WAIC テストの `skip_in_ci` ✅ 解決済み

- **問題**: WAIC テストに `skip_in_ci` が付与され、CI で実行されなかった
- **対応**: `should_contain` によるロケール非依存の検証に変更。`chrome_waic` タグで独立ジョブ化

## 7. 変更時のチェックリスト

システムテスト・CI 関連ファイルを変更する場合、以下を確認する:

- [ ] `# BEGIN JP PATCH` / `# END JP PATCH` が正しく記述されている
- [ ] upstream の構造（タグ・テスト分割）を破壊していない
- [ ] `--include chrome` でテストが 1 件以上実行されることを確認した
- [ ] `EXCLUDE_SYSTEM_TEST_TAGS` が正しく設定されている
- [ ] 新規追加テストに適切なタグ（`skip_in_ci` 等）が付与されている
- [ ] 本ドキュメントの関連セクションを更新した
- [ ] `projectDocs/jp/chrome-system-test-japanese-environment.md` の更新チェックリストを確認した

## 8. 参照文書

- `projectDocs/jp/chrome-system-test-japanese-environment.md` — Chrome テストの日本語環境差分
- `projectDocs/jp/waic-tests.md` — WAIC テストの詳細
- `projectDocs/jp/system-tests-ci-restoration-plan.md` — CI 復帰計画
- `projectDocs/jp/ci-system-tests-improvement-plan.md` — CI 改善計画
- `AGENTS.md` — JP 自動化ガイドライン
- `.github/instructions/review.instructions.md` — コードレビュー指示
