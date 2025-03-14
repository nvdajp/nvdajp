# miscDepsJpのサブモジュール管理改善戦略

## 現状の問題点

現在のmiscDepsJpのサブモジュール構造には以下の問題があります：

1. **複雑なサブモジュール構造**:
   - miscDepsJpはnvdajpのサブモジュール
   - miscDepsJp内にさらにサブモジュール（libopenjtalk、htsengineapi、python-jtalk、libkuraji）が存在
   - サブモジュールのネスト構造が管理を複雑にしている

## 改善の目標

1. サブモジュール構造をシンプルにする

## 段階的な改善戦略

### フェーズ2: サブモジュール構造の改善（リスク: 中）

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

9. **検証**:
   ```bash
   # ビルドテスト
   jptools\devbuild2024.cmd
   
   # NVDA本体の実行テスト
   runnvda.bat
   ```
