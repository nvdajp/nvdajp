# miscDepsJpのサブモジュール管理改善戦略

## 現状の問題点

現在のmiscDepsJpのサブモジュール構造には以下の問題があります：

1. **複雑なサブモジュール構造**:
   - miscDepsJpはnvdajpのサブモジュール
   - miscDepsJp内にさらにサブモジュール（libopenjtalk、htsengineapi、python-jtalk、libkuraji）が存在
   - サブモジュールのネスト構造が管理を複雑にしている

2. **重複したファイル**:
   - ビルドプロセスでサブモジュール間でファイルがコピーされる
   - 例：htsengineapiからpython-jtalk/htsengineapiへ、libopenjtalkからpython-jtalk/libopenjtalkへ
   - 同じファイルが複数の場所に存在し、一貫性の維持が難しい

3. **複雑なビルドプロセス**:
   - ファイルのコピー、パッチ適用、ビルド、再コピーなど多段階のプロセス
   - エラーが発生しやすく、デバッグが困難

## 改善の目標

1. サブモジュール構造をシンプルにする
2. ファイルの重複を減らす
3. ビルドプロセスを簡素化する
4. 既存の機能を維持する（ビルド結果が変わらない）
5. 移行プロセスを安全に行う

## 段階的な改善戦略

### フェーズ1: 現状の詳細分析と準備（リスク: 低）

1. **現状の詳細な調査**:
   - 各サブモジュールの依存関係を図式化
   - ビルドプロセスの各ステップを文書化
   - 重複ファイルのリストアップ

2. **テスト環境の準備**:
   - 現状のビルド結果を保存（比較用のベースライン）
   - ビルド結果の検証方法を確立

3. **バックアップの作成**:
   - 現状のリポジトリ構造の完全なバックアップ
   - 復元手順の文書化

### フェーズ2: サブモジュール構造の改善（リスク: 中）

1. **新しいブランチの作成**:
   ```bash
   git checkout -b improve-miscdepsjp-submodules
   ```

2. **miscDepsJpサブモジュールのコミットハッシュの記録**:
   ```bash
   cd miscDepsJp
   git rev-parse HEAD > ../miscDepsJp-commit.txt
   cd ..
   ```

3. **各サブモジュールのコミットハッシュの記録**:
   ```bash
   cd miscDepsJp/include/libopenjtalk
   git rev-parse HEAD > ../../../libopenjtalk-commit.txt
   cd ../../..
   
   cd miscDepsJp/include/htsengineapi
   git rev-parse HEAD > ../../../htsengineapi-commit.txt
   cd ../../..
   
   cd miscDepsJp/include/python-jtalk
   git rev-parse HEAD > ../../../python-jtalk-commit.txt
   cd ../../..
   
   cd miscDepsJp/include/libkuraji
   git rev-parse HEAD > ../../../libkuraji-commit.txt
   cd ../../..
   ```

4. **miscDepsJpサブモジュールの分離**:
   ```bash
   # サブモジュールを削除（ファイルは残す）
   git submodule deinit -f miscDepsJp
   git rm --cached miscDepsJp
   rm -rf .git/modules/miscDepsJp
   
   # miscDepsJpディレクトリをgitに追加
   git add miscDepsJp
   git commit -m "Convert miscDepsJp from submodule to regular directory"
   ```

5. **各サブモジュールの再設定**:
   ```bash
   # .gitmodulesファイルを編集
   # miscDepsJpエントリを削除し、各サブモジュールを直接参照するように変更
   ```

   .gitmodulesファイルの例:
   ```
   [submodule "miscDepsJp/include/libopenjtalk"]
       path = miscDepsJp/include/libopenjtalk
       url = https://github.com/nishimotz/libopenjtalk.git
   [submodule "miscDepsJp/include/htsengineapi"]
       path = miscDepsJp/include/htsengineapi
       url = https://github.com/nishimotz/htsengineapi.git
   [submodule "miscDepsJp/include/python-jtalk"]
       path = miscDepsJp/include/python-jtalk
       url = https://github.com/nvdajp/python-jtalk.git
   [submodule "miscDepsJp/include/libkuraji"]
       path = miscDepsJp/include/libkuraji
       url = https://github.com/nishimotz/libkuraji.git
   ```

6. **サブモジュールの初期化と特定コミットのチェックアウト**:
   ```bash
   git submodule init
   
   # 各サブモジュールを特定のコミットでチェックアウト
   git submodule update --init miscDepsJp/include/libopenjtalk
   cd miscDepsJp/include/libopenjtalk
   git checkout $(cat ../../../libopenjtalk-commit.txt)
   cd ../../..
   
   git submodule update --init miscDepsJp/include/htsengineapi
   cd miscDepsJp/include/htsengineapi
   git checkout $(cat ../../../htsengineapi-commit.txt)
   cd ../../..
   
   git submodule update --init miscDepsJp/include/python-jtalk
   cd miscDepsJp/include/python-jtalk
   git checkout $(cat ../../../python-jtalk-commit.txt)
   cd ../../..
   
   git submodule update --init miscDepsJp/include/libkuraji
   cd miscDepsJp/include/libkuraji
   git checkout $(cat ../../../libkuraji-commit.txt)
   cd ../../..
   ```

7. **不要なファイルの削除**:
   ```bash
   # miscDepsJpが独立したリポジトリでなくなったため、不要なファイルを削除
   rm miscDepsJp/.gitmodules
   rm miscDepsJp/appveyor.yml
   # .gitignoreは残しておく
   ```

8. **変更のコミット**:
   ```bash
   git add .gitmodules
   git add miscDepsJp
   git commit -m "Refactor: Convert nested submodules to direct submodules"
   ```

9. **検証**:
   ```bash
   # ビルドテスト
   jptools\devbuild2024.cmd
   
   # NVDA本体の実行テスト
   runnvda.bat
   ```

### フェーズ3: ビルドプロセスの改善（リスク: 高）

**注意**: このフェーズはフェーズ2が完全に成功した後に実施します。

1. **新しいブランチの作成**:
   ```bash
   git checkout -b improve-miscdepsjp-build-process
   ```

2. **ビルドスクリプトの分析**:
   - 現在のビルドプロセスの依存関係を図式化
   - 改善可能な箇所を特定

3. **ビルドスクリプトの段階的な改善**:
   - ファイルコピーを最小限に抑える
   - パッチ適用プロセスを簡素化
   - 直接サブモジュールを参照するように修正

4. **検証**:
   ```bash
   # ビルドテスト
   jptools\devbuild2024.cmd
   
   # NVDA本体の実行テスト
   runnvda.bat
   
   # ビルド結果の比較（フェーズ1で保存したベースラインと比較）
   ```

### フェーズ4: ドキュメント整備と展開（リスク: 低）

1. **ドキュメントの更新**:
   - 新しいサブモジュール構造の説明
   - 新しいビルドプロセスの説明
   - トラブルシューティングガイド

2. **開発者向けガイドの作成**:
   - 新しい構造での開発方法
   - サブモジュールの更新方法
   - ビルドプロセスのカスタマイズ方法

3. **プルリクエストの作成と展開**:
   - コードレビュー
   - CI/CDでのテスト
   - 段階的なマージ（フェーズ2とフェーズ3を別々に）

## 安全対策

1. **各ステップでのバックアップ**:
   - 重要な変更前にはリポジトリの状態をバックアップ
   - 復元ポイントの作成

2. **検証プロセス**:
   - 各フェーズ後に複数の環境でビルドテスト
   - ビルド結果の比較による一貫性確認
   - NVDA本体の機能テスト

3. **段階的なロールバック計画**:
   - 各フェーズでの問題発生時の対応手順
   - 完全復元手順

4. **並行開発の考慮**:
   - 移行中の他の開発作業との競合回避
   - 移行完了後の開発者向けガイダンス

## 移行後の利点

1. **シンプルなサブモジュール構造**:
   - 直接的なサブモジュール参照
   - ネストされたサブモジュールの排除

2. **メンテナンスの容易さ**:
   - サブモジュールの更新が簡単に
   - 依存関係の明確化

3. **ビルドプロセスの改善**:
   - 冗長なファイルコピーの削減
   - エラーの少ないビルドプロセス

4. **将来の拡張性**:
   - 新しいコンポーネントの追加が容易に
   - 依存関係の管理が明確に

## 結論

この段階的な戦略により、miscDepsJpのサブモジュール管理を安全に改善することができます。各フェーズは独立しており、問題が発生した場合は前のフェーズに戻ることができます。また、各ステップで検証を行うことで、機能の一貫性を確保します。

特にフェーズ2（サブモジュール構造の改善）は、比較的リスクが低く、大きな効果が期待できるため、最初に実施することをお勧めします。フェーズ3（ビルドプロセスの改善）は、より複雑でリスクが高いため、フェーズ2が完全に成功した後に実施します。
