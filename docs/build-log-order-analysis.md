# ビルドログ順序の考察

## 実際のログ順序（抜粋）

1. `Delete("source\_buildVersion.py")` / `Delete("source\__pycache__\_buildVersion...")`  
   → **NVDADistGenerator の最後のアクション**（dist ビルドの末尾）
2. `uninstaller\uninstGen.exe`
3. `signExecCertStore(["dist\uninstall.exe"], ...)` （uninstaller の PostAction）
4. `makensis ... /DNVDADistDir=...\dist ...` （launcher ビルド）
5. `signExecCertStore(["output\\nvda_....exe"], ...)` （launcher の PostAction）
6. `_cert_extras(...)` → jpCertExtras（dist 内 DLL の署名）

## 依存関係（sconstruct / scons_jp）

- `dist` は `uninstaller` に依存
- `jpCertExtras` は `dist` に依存（`env.Command(jp_cert_extras_stamp, dist_target, _cert_extras)`）
- `launcher` は `[nvdaLauncher.nsi, dist]` に依存し、さらに scons_jp で `jp_cert_extras_stamp` に依存

したがって**理論上の実行順**は:

`uninstaller` → `dist`（本体＋PostAction）→ `jpCertExtras` → `launcher`

## 問題点

1. **Delete が先に出力されている**  
   dist は uninstaller に依存しているので、本来は「uninstaller → dist」の順になるはず。  
   それにもかかわらず、ログ上は **dist の末尾（Delete）が uninstaller より前に**出ている。  
   → 並列ビルド（`-j` / `--all-cores`）で出力が入れ替わっているか、**PostAction の実行タイミングが本体とずれている**可能性がある。

2. **_sign_dist_exes_post_action の出力が一切ない**  
   dist 用に追加した PostAction（4 exe + nvda_synthDriverHost の署名）の print も signExec のログも出ていない。  
   → **dist の PostAction が、jpCertExtras や launcher より後に回っている、あるいは実行されていない**と解釈できる。

3. **SCons の PostAction の仕様**  
   PostAction は「ターゲットがビルドされたあと」に実行されるが、**依存関係の解決順や並列ジョブでは、他のターゲット（jpCertExtras など）が先に走り、dist の PostAction が後回しになる**ことがあり得る。  
   その場合、jpCertExtras 実行時点では dist 直下の 4 exe はまだ未署名のままになる。

## 結論と対策

- **PostAction だけに頼ると、dist 直下の 4 exe の署名が jpCertExtras より後になり、検証で失敗する可能性がある。**
- **対策**: dist の「4 exe 署名」を **PostAction ではなく、dist に依存する stamp 用 Command にし、jpCertExtras がその stamp に依存する**ようにする。  
  - 例: `dist` → `dist_exes_signed.stamp`（4 exe 署名＋touch）→ `jpCertExtras` が `dist_exes_signed.stamp` に依存  
  - これで「dist ビルド → 4 exe 署名 → jpCertExtras → launcher」の順が保証される。
