# コード署名を考慮したビルド依存関係

この文書は、署名の有無で分岐する NVDA 日本語版ビルドの依存関係を示す正本である。

## 最短コマンド

### 署名あり

```powershell
.\scons.bat launcher
```

前提として Azure Key Vault 署名が有効であること（`AZURE_KV_SIGNING=1` が既定）。ローカル証明書（`certFile` / `CERT_SHA1` / `CERT_NAME`）は廃止。`--all-cores` は使わない（JP ターゲットで並列ビルドが失敗することがある）。

### 署名なし（明示的スキップ）

```powershell
$env:SKIP_SIGNING = "1"
.\scons.bat launcher
```

## フローの使い分け

### 必須フロー（共通）

```text
jtalkPrep -> jtalkSync -> source -> user_docs -> dist -> launcher
```

- `dist` までは署名有無にかかわらず共通である。
- `launcher` は必ず `dist` を入力に取る。

### 署名ありフロー

```text
jtalkPrep -> jtalkSync -> source -> user_docs -> dist -> jpCertExtras -> launcher
```

- `jpCertExtras` が `dist` 完了後に実行される。
- `dist/synthDrivers/jtalk/libopenjtalk.dll` と `libmecab.dll` を署名する。
- その後に `launcher` が作成され、署名済み DLL を含む。

### 署名なしフロー

- `SKIP_SIGNING` が有効な場合、`jpCertExtras` は実行されない。
- `launcher` は `dist` のみを入力として作成される。
- 出力物（DLL/EXE）は未署名のままである。

## 依存関係の要点

- `jpCertExtras` は `dist` ターゲット（または `dist` ディレクトリノード）に依存する。
- これにより、`dist` 完了後にだけ `jpCertExtras` が実行される。
- 署名設定が有効な場合のみ、`launcher` は `jpCertExtras` に依存する。

## 署名設定

### 有効化される設定

- Azure Key Vault HSM: `AZURE_KV_SIGNING=1`（既定。`az login` または `AZURE_KV_ACCESS_TOKEN` で認証）

旧方式のローカル証明書ストア署名（`CERT_SHA1` / `CERT_NAME`）は Sectigo 失効（2026-08-06）に伴い廃止済み。

### 明示的無効化

- `SKIP_SIGNING` が設定されると、上記すべての署名設定を無効化する。

## トラブルシューティング

### `jpCertExtras` が走らない

- 署名設定が未指定、または `SKIP_SIGNING` が有効である。

### 証明書ストア署名が意図せず有効になる

- `CERT_SHA1` / `CERT_NAME` の環境変数が残っている可能性がある（旧方式の残骸）。
- 未署名ビルドにしたい場合は `SKIP_SIGNING=1` を明示する。

### `dist/` が無い、または DLL が見つからない

- `scons.bat source user_docs dist` を先に完了させる。
- 必要に応じて `scons.bat jtalkSync dist` を再実行する。

## GitHub Actions によるクラウド署名リリース（2026.2jp 移行）

2026.2jp から `releasejp` ブランチでも `alphajp` / `betajp` と同様に、GitHub Actions の `workflow_dispatch` で Azure Key Vault 署名付きリリースビルドを行えるようになった。

### 発火条件と署名の有無

| ブランチ | push / pull_request | workflow_dispatch |
|---|---|---|
| alphajp | 署名なし | 署名あり（Azure KV） |
| betajp | 署名なし | 署名あり（Azure KV） |
| releasejp | 署名なし | 署名あり（Azure KV）※本 PR で追加 |

- ブランチへの `push` / `pull_request` は常に署名なしビルドである。
- タグの `push` は CI を発火しない（`on.push` は `branches` のみで `tags` を対象にしていない）。
- 署名が必要なリリース / プレリリースは必ず `workflow_dispatch` で発火する。

### リリースワークフローの使い分け

#### alphajp（自動タグ生成）

```text
workflow_dispatch on alphajp
  → publishAlphaRelease
  → タグ: alphajp-{YYMMDD}{hour}
  → 常にプレリリース
```

#### betajp（自動タグ生成）

```text
workflow_dispatch on betajp
  → publishBetaRelease
  → タグ: betajp-{YYYY.Mjp-beta-YYMMDD}{hour}
  → 常にプレリリース
  → S3 へ beta-meta.json をアップロード
```

#### releasejp（人がタグを指定）

```text
workflow_dispatch on releasejp + releaseTag 入力
  → publishRelease
  → タグ: 入力で指定（例: release-2026.2jp-rc1 / release-2026.2jp）
  → rc / beta を含むタグ名 → プレリリース
  → 含まないタグ名 → 正式リリース
```

- `releaseTag` 入力は必須。`release-` で始まり `jp` を含む形式を要求する。
- 成果物は `nvda_2026.2jp.exe`、`nvdajp-jtalk-*.nvda-addon`、`kgsbraille-*.nvda-addon`、`nvda_*_controllerClientJp.zip`。

### リリース手順例（2026.2jp RC1）

1. `releasejp` ブランチを最新にする
2. GitHub Actions → CI/CD Japanese Version → `Run workflow`
3. ブランチ: `releasejp`、入力 `releaseTag: release-2026.2jp-rc1` で発火
4. 全テストが通過すれば `nvda_2026.2jp.exe` が署名付きで作成され、GitHub Releases にプレリリースとして公開される

RC で不備が見つかった場合は修正コミットを `releasejp` ブランチに追加し、次の `releaseTag`（例: `release-2026.2jp-rc2`）で再度発火する。OK ならば `releaseTag: release-2026.2jp` で `workflow_dispatch` を発火して正式リリースを作成する。タグは手動で打たないこと。`publishRelease` ジョブが `gh release create` により `releasejp` ブランチの HEAD に `release-2026.2jp` タグを自動生成するため、手動でタグを打つとビルド対象リビジョンとタグのリビジョンがずれる恐れがある。

### 更新通知

- RC / プレリリースでは `version=2026.2jp`、`updateVersionType=nvdajp` として署名ビルドが作成される。
- 実行後、NVDA の更新チェックは `2026.2jp` を自身のバージョンとして通知する。

### リリース公開後の作業（ランブック）

正式リリースの公開完了後、以下の運用作業を実施する。

#### 1. リリースと連動したディスカッションの作成（前提踏襲）

正式リリースの公開後、GitHub Releases と連動したディスカッション（カテゴリ「お知らせ」）を作成・紐づける。
GitHub Releases API（`PATCH`）で `discussion_category_name` を指定することで、過去リリース（2026.1jp、2026.1.1jp 等）と同様に自動生成および相互リンクが行われる。

```bash
# タグ名から release ID を取得してディスカッションを生成・紐づけ
gh api -X PATCH "repos/nvdajp/nvdajp/releases/$(gh api repos/nvdajp/nvdajp/releases/tags/<tag_name> --jq .id)" \
  -f discussion_category_name="お知らせ"

# 確認（discussion_url が設定されていること）
gh api "repos/nvdajp/nvdajp/releases/tags/<tag_name>" --jq '{name: .name, tag_name: .tag_name, discussion_url: .discussion_url}'
```

#### 2. 次期マイルストーンへの自動割り当て切り替え

新バージョンの正式リリース完了後、PRマージ時のマイルストーン自動付与先（`.github/workflows/assign-milestone-on-close.yml`）を次期マイルストーンに切り替える。

```powershell
# 次期マイルストーンの数値 ID を確認（例: 2026.3jp の ID が 81 の場合）
gh variable set MILESTONE_ID --body "81" --repo nvdajp/nvdajp

# 設定確認
gh variable list --repo nvdajp/nvdajp
```

## 関連

- `jptools/scons_jp.py`
- `sconstruct`
- `jptools/certBuild2023.cmd`
- `projectDocs/jp/README.md`
- 詳細アーカイブ: `projectDocs/jp/archive/code-signing-dependencies-details.md`
