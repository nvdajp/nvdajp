# nvaccess beta マージ衝突レポート — メタ情報（再現性）

このファイルは `projectDocs/jp/merge-issues-beta-2025-11.md` の補足です。レポートの再現に必要な上流リビジョン、対象ブランチ、検出コマンド例をまとめます。

- 対象 upstream: `nvaccess/beta @ ac309fe35f1a10cb2b9ec15ffa8a7d5a665d0102`
- 取り込み先（base）: `betajp`
- 検出日時（例）: 2025-11-05 (JST)
- 参照ドキュメント: `projectDocs/jp/merge-issues-beta-2025-11.md`

## 衝突検出コマンド例（PowerShell）

```powershell
# すべてのコンフリクトマーカー行を一覧
rg -n "^(<<<<<<<|=======|>>>>>>>)" -S

# ファイルごとの最初の衝突位置（行番号つき）を要約
$pattern = '^(<<<<<<< |>>>>>>> ).*|^=======$'
$conflicts = rg --vimgrep -S -e $pattern | ForEach-Object { ($_ -split ":")[0..1] -join ":" }
$files = @{}
foreach($c in $conflicts){
  $parts = $c -split ":"; $f=$parts[0]; $l=[int]$parts[1]
  if(-not $files.ContainsKey($f)){ $files[$f]=$l } elseif($l -lt $files[$f]){ $files[$f]=$l }
}
$files.GetEnumerator() | Sort-Object Name | ForEach-Object { "$_" }

# 個別（workflow）の衝突だけ確認
rg --line-number -n -S -e '^(<<<<<<< |>>>>>>> ).*|^=======$' .github/workflows/testAndPublish.yml

# 上流SHAが埋まったマーカーの確認（>>>>>>> の右側にSHAが出る）
rg -n ">>>>>>> " -S
```

## 備考

- `ac309fe3…` はコンフリクトマーカーに現れた上流側のコミット SHA を採用しています。
- 実際の取り込み対象コミット/ブランチが変わる場合は、このファイルの upstream 記述を更新してください。
- 再現確認は `rg`（ripgrep）が必要です。未導入の場合は `grep` でも代替可能です（ただし正規表現の互換に注意）。

