# NVDA 譌･譛ｬ隱樒沿 髢狗匱閠・Γ繝｢

繧ｷ繝･繧｢繝ｫ繧ｿ/NVDA譌･譛ｬ隱槭メ繝ｼ繝 隘ｿ譛ｬ蜊謎ｹ・
## 繝薙Ν繝臥腸蠅・ｺ門ｙ縺ｨ繧ｽ繝ｼ繧ｹ繧ｳ繝ｼ繝牙叙蠕・
[蜈ｬ蠑上・諠・ｱ](https://github.com/nvdajp/nvdajp/blob/betajp/projectDocs/dev/createDevEnvironment.md)

莉･荳九・ NVDA 2024.4.1jp (2024蟷ｴ11譛・4譌･譎らせ縺ｧ縺ｮ betajp 繝悶Λ繝ｳ繝・ 縺ｮ迥ｶ豕・
### (1) Windows 10/11 64繝薙ャ繝・
遒ｺ螳溘↓繝薙Ν繝峨〒縺阪ｋ菴懈･ｭ迺ｰ蠅・・ Windows 10 縺ｾ縺溘・ 11 64繝薙ャ繝・
### (2) Visual Studio Community

莉･荳九°繧峨ム繧ｦ繝ｳ繝ｭ繝ｼ繝峨＠縺ｦ繧､繝ｳ繧ｹ繝医・繝ｩ繝ｼ繧貞ｮ溯｡・
https://www.visualstudio.com/ja/downloads/

* Visual Studio 2022 v17.12.1 縺ｧ繝薙Ν繝峨〒縺阪ｋ縺薙→繧堤｢ｺ隱阪＠縺・
#### (2.1) 驕ｸ謚槭☆繧九後Ρ繝ｼ繧ｯ繝ｭ繝ｼ繝峨阪・鬆・岼

* C++縺ｫ繧医ｋ繝・せ繧ｯ繝医ャ繝鈴幕逋ｺ

#### (2.2) 縲梧ｦりｦ√阪靴++縺ｫ繧医ｋ繝・せ繧ｯ繝医ャ繝鈴幕逋ｺ縲阪後が繝励す繝ｧ繝ｳ縲阪〒驕ｸ謚槭☆繧矩・岼

* Windows 逕ｨ C++ Clang 繝・・繝ｫ

#### (2.3) 縲悟句挨縺ｮ繧ｳ繝ｳ繝昴・繝阪Φ繝医阪後さ繝ｼ繝峨ヤ繝ｼ繝ｫ縲阪〒驕ｸ謚槭☆繧矩・岼

蛟句挨縺ｮ繧ｳ繝ｳ繝昴・繝阪Φ繝・
* Windows 11 SDK (10.0.22621.0)
* MSVC v143 - VS 2022 C++ ARM64/ARM64EC 繝薙Ν繝峨ヤ繝ｼ繝ｫ(譛譁ｰ)
* MSVC v143 - VS 2022 C++ x64/x86 繝薙Ν繝峨ヤ繝ｼ繝ｫ(譛譁ｰ)
* 譛譁ｰ縺ｮ v143 繝薙Ν繝峨ヤ繝ｼ繝ｫ逕ｨ C++ ATL (x86 縺翫ｈ縺ｳ x64)
* 譛譁ｰ縺ｮ v143 繝薙Ν繝峨ヤ繝ｼ繝ｫ逕ｨ C++ ATL (ARM64/ARM64EC)

繧ｳ繝ｼ繝峨ヤ繝ｼ繝ｫ

* Git for Windows = 蠕瑚ｿｰ

#### (2.4) 繧､繝ｳ繧ｹ繝医・繝ｫ縺ｮ螳溯｡・
謨ｰGB縺ｮ繝輔ぃ繧､繝ｫ縺ｮ繝繧ｦ繝ｳ繝ｭ繝ｼ繝峨→繧､繝ｳ繧ｹ繝医・繝ｫ縺瑚｡後ｏ繧後ｋ縲・
#### (2.5) Git 縺ｮ遒ｺ隱・
Visual Studio 縺ｨ荳邱偵↓繧､繝ｳ繧ｹ繝医・繝ｫ縺励↑縺・ｴ蜷医・荳玖ｨ倥°繧峨ム繧ｦ繝ｳ繝ｭ繝ｼ繝峨＠縺ｦ繧､繝ｳ繧ｹ繝医・繝ｩ繝ｼ繧貞ｮ溯｡後☆繧九・
https://git-for-windows.github.io/

Git 縺ｮ險ｭ螳・
* Adjusting your PATH environment : Use Git and optional Unix tools from the Windows Command Prompt

* Configuring the line ending conversions : Chechout Windows-style, commit Unix-style line ending

險ｭ螳壹＠逶ｴ縺吝ｴ蜷医・

```text
> git config --global core.autocrlf true
```

迺ｰ蠅・､画焚 PATH 繧定・蛻・〒險ｭ螳壹＠縺ｪ縺翫☆蝣ｴ蜷医・縲∽ｻ･荳九′逋ｻ骭ｲ縺輔ｌ縺ｦ縺・ｋ縺薙→縲・
```text
C:\Program Files\Git\cmd
C:\Program Files\Git\usr\bin
```

蛯呵・ｼ・繝ｪ繝｢繝ｼ繝医Μ繝昴ず繝医Μ縺ｸ縺ｮ繧｢繝・・繝ｭ繝ｼ繝・(git push) 縺吶ｋ縺溘ａ縺ｫ縺ｯ
push 蜈茨ｼ・itHub縺ｪ縺ｩ・峨・繧｢繧ｫ繧ｦ繝ｳ繝医・繧ｻ繝・ヨ繧｢繝・・繧・・髢矩嵯縺ｮ險ｭ螳壹∵ｨｩ髯舌・蜿門ｾ励′蠢・ｦ√・
#### (2.6) 陬懆ｶｳ

createDevEnvironment.md 縺ｮ蜀・ｮｹ縺縺後√％縺ｮ謇矩・嶌縺ｧ縺ｯ菴ｿ縺｣縺ｦ縺・↑縺・・
* VS繧､繝ｳ繧ｹ繝医・繝ｩ繝ｼ縺ｮ繧､繝ｳ繝昴・繝域ｩ溯・縺ｧ .vsconfig 繧定ｪｭ縺ｿ霎ｼ繧縺薙→縺後〒縺阪ｋ
* Visual Studio Code 繧剃ｽｿ逕ｨ縺吶ｋ蝣ｴ蜷医・縲¨VDA逕ｨ莠句燕險ｭ螳壽ｸ医∩繝ｯ繝ｼ繧ｯ繧ｹ繝壹・繧ｹ讒区・繧貞茜逕ｨ縺ｧ縺阪ｋ縲ゅΜ繝昴ず繝医Μ縺ｮ繝ｫ繝ｼ繝医〒莉･荳九・繧ｳ繝槭Φ繝峨ｒ螳溯｡後☆繧九％縺ｨ縺ｧ縲√Ρ繝ｼ繧ｯ繧ｹ繝壹・繧ｹ讒区・繧偵メ繧ｧ繝・け繧｢繧ｦ繝医〒縺阪ｋ縲・
```text
> git clone https://github.com/nvaccess/vscode-nvda.git .vscode
```

### (4) 7-Zip (7z)

7-Zip 繧ｵ繧､繝医°繧・64bit Windows x64 (7z****-x64.exe) 繧偵ム繧ｦ繝ｳ繝ｭ繝ｼ繝峨☆繧九・
http://www.7-zip.org/download.html

繧､繝ｳ繧ｹ繝医・繝ｩ繝ｼ繧貞ｮ溯｡後＠縺ｦ繝・ヵ繧ｩ繝ｫ繝医〒繧､繝ｳ繧ｹ繝医・繝ｫ縺吶ｋ縲・
迺ｰ蠅・､画焚 PATH 縺ｫ莉･荳九ｒ逋ｻ骭ｲ縺吶ｋ縲・
```text
C:\Program Files\7-Zip
```

### (5) Python 3.11 (Windows 32bit)

繝繧ｦ繝ｳ繝ｭ繝ｼ繝峨＠縺ｦ螳溯｡後＠縲√う繝ｳ繧ｹ繝医・繝ｫ縺吶ｋ縲・繧ｪ繝励す繝ｧ繝ｳ縺ｯ繝・ヵ繧ｩ繝ｫ繝医〒繧医＞縲・
https://www.python.org/downloads/release/python-3119/

Windows x86 executable installer (python-3.11.9.exe)

### (6) 遒ｺ隱阪☆繧九％縺ｨ

PowerShell 縺ｾ縺溘・繧ｳ繝槭Φ繝峨・繝ｭ繝ｳ繝励ヨ縺ｧ Python 3.11 (32bit) 縺瑚ｵｷ蜍輔☆繧九・
```text
> py -3.11-32 -V
Python 3.11.9
```

PowerShell 縺ｧ git, patch, 7z 縺後◎繧後◇繧悟ｮ溯｡後〒縺阪ｋ縲・
```text
> gcm git | % Source
C:\Program Files\Git\cmd\git.exe

> gcm patch | % Source
C:\Program Files\Git\usr\bin\patch.exe

> gcm 7z | % Source
C:\Program Files\7-Zip\7z.exe
```

縺ｾ縺溘・繧ｳ繝槭Φ繝峨・繝ｭ繝ｳ繝励ヨ縺ｧ git, patch, 7z 縺後◎繧後◇繧悟ｮ溯｡後〒縺阪ｋ縲・
```text
> where git
C:\Program Files\Git\cmd\git.exe

> where patch
C:\Program Files\Git\usr\bin\patch.exe

> where 7z
C:\Program Files\7-Zip\7z.exe
```

### (7) NVDA譌･譛ｬ隱樒沿縺ｮ繧ｽ繝ｼ繧ｹ繧ｳ繝ｼ繝牙叙蠕励→繝薙Ν繝・
莉･荳九〒譛ｬ菴薙♀繧医・ Git 縺ｮ繧ｵ繝悶Δ繧ｸ繝･繝ｼ繝ｫ縺悟叙蠕励＆繧後ｋ縲・
譌･譛ｬ隱樒沿縺ｮ繧ｽ繝ｼ繧ｹ繧ｳ繝ｼ繝・betajp 繝悶Λ繝ｳ繝√ｒ betajp-dev 繝輔か繝ｫ繝縺ｫ蜿門ｾ・
```text
> git clone --recurse-submodules --shallow-submodules -b betajp https://github.com/nvdajp/nvdajp.git betajp-dev
```

繧ｽ繝ｼ繧ｹ繧ｳ繝ｼ繝峨°繧牙ｮ溯｡後☆繧九◆繧√・貅門ｙ菴懈･ｭ

```text
> cd betajp-dev
> jptools\devbuild2024.cmd
```

繝ｦ繝九ャ繝医ユ繧ｹ繝医・蜃ｺ蜉帙′ `OK (skipped=5)` 縺ｧ縺ゅｌ縺ｰ萓晏ｭ倥Δ繧ｸ繝･繝ｼ繝ｫ縺ｯ貅門ｙ縺ｧ縺阪※縺・ｋ縲・
NVDA 譛ｬ菴薙ｒ螳溯｡後☆繧九↓縺ｯ

```text
> runnvda.bat
```

### (8) NVDA譌･譛ｬ隱樒沿縺ｮ繝ｪ繝ｪ繝ｼ繧ｹ繝薙Ν繝・
迴ｾ蝨ｨ縺ｯ `signtool sign /a` 繧剃ｽｿ縺医ｋ縺薙→縺悟燕謠舌・
```text
> cd betajp-dev
> set VERSION=2024.3jp
> venvUtils\venvCmd jptools\certBuild2023.cmd version_build=99999
> rununittests.bat
```

### (9) NVDA譛ｬ螳ｶ迚医・繧ｽ繝ｼ繧ｹ繧ｳ繝ｼ繝牙叙蠕励→繝薙Ν繝・
```text
> git clone --recurse-submodules --shallow-submodules https://github.com/nvaccess/nvda.git
```

```text
> cd nvda
> .\scons
```

## 繝槭う繝ｫ繧ｹ繝医・繝ｳ閾ｪ蜍募牡繧雁ｽ薙※讖溯・

NVDA譌･譛ｬ隱樒沿縺ｧ縺ｯ縲；itHub Actions繧剃ｽｿ逕ｨ縺励※Issue繧Пull Request縺ｫ繝槭う繝ｫ繧ｹ繝医・繝ｳ繧定・蜍慕噪縺ｫ蜑ｲ繧雁ｽ薙※繧区ｩ溯・繧貞ｰ主・縺励※縺・∪縺吶・
### 蜍穂ｽ懈ｦりｦ・
`.github/workflows/assign-milestone-on-close.yml` 繝ｯ繝ｼ繧ｯ繝輔Ο繝ｼ縺ｫ繧医ｊ縲∽ｻ･荳九・譚｡莉ｶ繧呈ｺ縺溘☆蝣ｴ蜷医↓閾ｪ蜍慕噪縺ｫ繝槭う繝ｫ繧ｹ繝医・繝ｳ縺悟牡繧雁ｽ薙※繧峨ｌ縺ｾ縺呻ｼ・
1. Issue縺ｾ縺溘・Pull Request縺後け繝ｭ繝ｼ繧ｺ縺輔ｌ縺滓凾
2. 繝槭う繝ｫ繧ｹ繝医・繝ｳ縺梧悴險ｭ螳壹〒縺ゅｋ
3. 莉･荳九・縺・★繧後°縺ｮ譚｡莉ｶ繧呈ｺ縺溘☆・・   - Issue縺後慶ompleted縲阪→縺励※繧ｯ繝ｭ繝ｼ繧ｺ縺輔ｌ縺・   - Pull Request縺後・繝ｼ繧ｸ縺輔ｌ縺・
### 險ｭ螳壽婿豕・
繝ｪ繝昴ず繝医Μ螟画焚 `MILESTONE_ID` 縺ｫ縲∬・蜍募牡繧雁ｽ薙※縺励◆縺・・繧､繝ｫ繧ｹ繝医・繝ｳ縺ｮID繧定ｨｭ螳壹＠縺ｾ縺呻ｼ・
```bash
gh variable set MILESTONE_ID --body "71" --repo nvdajp/nvdajp
```

迴ｾ蝨ｨ縺ｯ `2025.2jp` (ID: 71) 縺瑚ｨｭ螳壹＆繧後※縺・∪縺吶・
### 驕狗畑謇矩・
1. 譁ｰ縺励＞繝ｪ繝ｪ繝ｼ繧ｹ縺ｮ貅門ｙ譎ゅ↓縲；itHub縺ｧ譁ｰ縺励＞繝槭う繝ｫ繧ｹ繝医・繝ｳ・井ｾ具ｼ啻2025.3jp`・峨ｒ菴懈・
2. 繝槭う繝ｫ繧ｹ繝医・繝ｳ縺ｮID繧堤｢ｺ隱搾ｼ・RL縺ｮ譛ｫ蟆ｾ縺ｮ謨ｰ蟄暦ｼ・3. `MILESTONE_ID` 螟画焚繧呈眠縺励＞繝槭う繝ｫ繧ｹ繝医・繝ｳ縺ｮID縺ｫ譖ｴ譁ｰ

縺薙・讖溯・縺ｫ繧医ｊ縲√Μ繝ｪ繝ｼ繧ｹ繝弱・繝井ｽ懈・譎ゅ↓隧ｲ蠖薙・繧､繝ｫ繧ｹ繝医・繝ｳ縺ｧ繝輔ぅ繝ｫ繧ｿ縺励※螟画峩轤ｹ繧堤ｰ｡蜊倥↓謚頑升縺ｧ縺阪∪縺吶・
## git 驕狗畑譁ｹ驥昴→繝医Λ繝悶Ν繧ｷ繝･繝ｼ繝・ぅ繝ｳ繧ｰ

### 繝悶Λ繝ｳ繝・°逕ｨ

* 譛ｬ螳ｶ nvda 縺ｮ繝・ヵ繧ｩ繝ｫ繝医ヶ繝ｩ繝ｳ繝√・ master 縺ｧ縺ゅｋ縲・* nvdajp 縺ｮ繝・ヵ繧ｩ繝ｫ繝医ヶ繝ｩ繝ｳ繝√・ betajp 縺ｧ縺ゅｋ縲・* nvdajp 縺ｮ alphajp 繝悶Λ繝ｳ繝√↓縺ｯ譛ｬ螳ｶ master 縺九ｉ縺ｮ git pull 繧貞ｮ壽悄逧・↓陦後≧縲・* nvdajp 縺ｮ betajp 繝悶Λ繝ｳ繝√・ alphajp 縺九ｉ縺ｮ pull request 縺ｫ繧医▲縺ｦ谺｡縺ｮ繝ｪ繝ｪ繝ｼ繧ｹ縺ｫ蜷代￠縺滓峩譁ｰ繧定｡後≧縲・
### 繝輔ぃ繧､繝ｫ謾ｹ陦後さ繝ｼ繝峨→ editorconfig

* Windows 縺ｧ git clone 縺励◆蝣ｴ蜷医∵隼陦後さ繝ｼ繝峨′ CRLF 縺ｫ縺ｪ繧翫“it 縺ｫ commit 縺吶ｋ縺ｨ LF 縺ｫ縺ｪ繧九・* 譛ｬ螳ｶ縺ｮ .editorconfig 縺ｯ end_of_line = lf 縺ｫ縺ｪ縺｣縺ｦ縺翫ｊ縲仝indows 縺ｮ Visual Studio Code 縺ｧ editorconfig 繧呈怏蜉ｹ縺ｫ縺吶ｋ縺ｨ縲∵眠隕丈ｽ懈・縺励◆繝輔ぃ繧､繝ｫ縺ｯ菫晏ｭ倥☆繧九→縺阪↓謾ｹ陦後さ繝ｼ繝峨′ LF 縺ｫ縺ｪ繧九・* 縺薙・謖吝虚縺ｯ Windows 縺ｧ菴懈･ｭ縺吶ｋ蝣ｴ蜷医↓縺ｯ荳堺ｾｿ縺ｪ縺ｮ縺ｧ縲・editorconfig 縺ｮ end_of_line = crlf 縺ｫ螟画峩縺励※縺・ｋ縲・* macOS 繧・Linux 縺ｧ菴懈･ｭ縺吶ｋ蝣ｴ蜷医・縲・editorconfig 縺ｮ end_of_line = lf 縺ｫ謌ｻ縺吶→繧医＞縲・
### 繝輔ぃ繧､繝ｫ縺ｮ荳崎ｶｳ繧・ヰ繝ｼ繧ｸ繝ｧ繝ｳ縺ｮ荳堺ｸ閾ｴ

繧ｵ繝悶Δ繧ｸ繝･繝ｼ繝ｫ縺ｮ蜷梧悄繧・峩譁ｰ縺ｮ螟ｱ謨励・
荳玖ｨ倥ｒ螳溯｡鯉ｼ・
```text
> git submodule sync
> git submodule update --init --recursive
```

蛯呵・ｼ・譛ｬ螳ｶ縺九ｉ git fetch, git merge FETCH_HEAD 縺励◆縺ゅ→縺ｧ

```text
modified:   include/espeak (new commits)
```

縺ｮ繧医≧縺ｫ縺ｪ縺｣縺溘→縺阪↓縺薙・謫堺ｽ懊ｒ縺吶ｋ縺ｨ隗｣豎ｺ縺吶ｋ縺薙→縺悟､壹＞縲・
荳榊ｿ・ｦ√↑ modified 繧定ｪ､縺｣縺ｦ繝槭・繧ｸ縺励※ git push 縺吶ｋ縺ｨ縲・繧ｵ繝悶Δ繧ｸ繝･繝ｼ繝ｫ縺ｮ繝舌・繧ｸ繝ｧ繝ｳ縺梧悽螳ｶ縺ｨ縺壹ｌ縺溽憾諷九・縺ｾ縺ｾ GitHub 縺ｫ蜈ｬ髢九＆繧後※縺励∪縺・・
### git submodule update 縺ｮ繧ｨ繝ｩ繝ｼ蟇ｾ蠢・
```text
> git submodule update --init

fatal: reference is not a tree: 1e1e7587cfbc263b351644e52fdaf2684103d6c8
Unable to checkout '1e1e7587cfbc263b351644e52fdaf2684103d6c8' in submodule path 'include/liblouis'
```

include/liblouis 繧ｵ繝悶Δ繧ｸ繝･繝ｼ繝ｫ縺ｮ checkout 縺ｫ螟ｱ謨励＠縺ｦ縺・ｋ縲・
liblouis 縺ｫ cd 縺励※ git fetch -t 縺励※縺九ｉ繧・ｊ逶ｴ縺励※縺ｿ繧具ｼ・
```text
> cd include\liblouis
> git fetch -t

remote: Counting objects: 412, done.
remote: Compressing objects: 100% (144/144), done.
Remote: Total 412 (delta 268), reused 412 (delta 268)eceiving objects:  91% (37
Receiving objects: 100% (412/412), 86.54 KiB | 0 bytes/s, done.
・育払・・
> cd ..\..
> git submodule update --init --recursive
```

### comInterfaces 縺ｮ蜀咲函謌・
繝薙Ν繝・devbuild2024)繧堤ｹｰ繧願ｿ斐☆縺ｨ comInterfaces 縺悟｣翫ｌ縺ｦ荳驛ｨ縺ｮ繝ｦ繝九ャ繝医ユ繧ｹ繝医′螟ｱ謨励＠縺溘ｊ runnvda 縺ｧ縺阪↑縺上↑縺｣縺溘ｊ縺吶ｋ縲・comInterfaces 繝輔ぃ繧､繝ｫ縺ｯ git 縺ｧ邂｡逅・＆繧後※縺・↑縺・◆繧√∽ｸ玖ｨ倥・繧医≧縺ｫ縺励※蜀咲函謌舌☆繧九・
```text
> venvUtils\venvCmd.bat scons source\comInterfaces -c
> venvUtils\venvCmd.bat scons source\comInterfaces
```

## 繧ｷ繧ｹ繝・Β繝・せ繝・
### 譁ｹ驥・
* 譛ｬ繝峨く繝･繝｡繝ｳ繝医・謇矩・〒譌･譛ｬ隱・Windows 迺ｰ蠅・ｼ医Ο繝ｼ繧ｫ繝ｫ迺ｰ蠅・ｼ峨〒繧ｷ繧ｹ繝・Β繝・せ繝医′騾壹ｋ縺薙→
* 蜷梧凾縺ｫ AppVeyor 縺ｧ繧ｷ繧ｹ繝・Β繝・せ繝医′騾壹ｋ縺薙→

### 譛ｬ螳ｶ迚医・隱ｲ鬘・
* Chrome 襍ｷ蜍輔が繝励す繝ｧ繝ｳ縺ｧ UI 險隱槭ｒ闍ｱ隱槭↓縺励※縺・ｋ縺後∬ｵｷ蜍墓ｸ医∩縺ｮ Chrome 繧､繝ｳ繧ｹ繧ｿ繝ｳ繧ｹ縺後≠繧九→縲∬ｵｷ蜍輔が繝励す繝ｧ繝ｳ縺ｫ縺九°繧上ｉ縺壹，hrome 縺ｮ UI 險隱槭′譌｢蟄倥う繝ｳ繧ｹ繧ｿ繝ｳ繧ｹ縺ｮ險隱槭↓縺ｪ繧九ゅい繝峨Ξ繧ｹ讀懃ｴ｢繝舌・縺ｮ隱ｭ縺ｿ荳翫￡縺ｫ萓晏ｭ倥＠縺溷・逅・′縺ゅｋ縺溘ａ縲，hrome 縺ｮ UI 險隱槭′譌･譛ｬ隱槭〒縺ゅｋ縺薙→縺後ユ繧ｹ繝医↓騾壹ｉ縺ｪ縺・次蝗縺ｫ縺ｪ繧九・* Chrome 繝励Ο繝輔ぃ繧､繝ｫ驕ｸ謚樒判髱｢縺悟・縺ｦ縺励∪縺・→縲√ユ繧ｹ繝医↓騾ｲ繧√↑縺・・* NVDA 譌･譛ｬ隱樒沿縺ｮ譁・ｭ苓ｪｬ譏弱Δ繝ｼ繝峨・莉墓ｧ伜､画峩縺ｫ繧医ｊ縲∝ｷｦ蜿ｳ遏｢蜊ｰ繧ｭ繝ｼ繧呈款縺励◆縺ｨ縺阪・隱ｭ縺ｿ荳翫￡縺檎焚縺ｪ繧句ｴ蜷医′縺ゅｋ縲・
### 蟇ｾ蠢・
* appveyor-jp.yml : 螳滄圀縺ｫ菴ｿ逕ｨ縺励※縺・ｋ AppVeyor 險ｭ螳壹ヵ繧｡繧､繝ｫ縲よ悽螳ｶ迚医・ appveyor.yml 縺ｯ縺昴・縺ｾ縺ｾ谿九＠縺ｦ縺・ｋ縲・* _chromeArgs.py : 繝ｭ繝ｼ繧ｫ繝ｫ迺ｰ蠅・→ AppVeyor 繧貞・騾壹・繧ｳ繝ｼ繝峨〒蜍輔°縺吶◆繧・Chrome 縺ｮ UI 險隱槭ｒ ja-JP 縺ｫ螟画峩縺励※縺・ｋ縲ゅ∪縺溘√ご繧ｹ繝医Δ繝ｼ繝峨〒襍ｷ蜍輔☆繧九◆繧√↓蠢・ｦ√↑繧ｪ繝励す繝ｧ繝ｳ繧定ｿｽ蜉縺励※縺・ｋ縲・* ChromeLib.py : 繧｢繝峨Ξ繧ｹ讀懃ｴ｢繝舌・縺ｮ隱ｭ縺ｿ荳翫￡縺ｨ縺励※譛溷ｾ・☆繧九ユ繧ｭ繧ｹ繝医ｒ "Address and search bar" 縺九ｉ "繧｢繝峨Ξ繧ｹ讀懃ｴ｢繝舌・" 縺ｫ螟画峩縺励※縺・ｋ縲・* jpRobotUtil.py : press_numpad2_4_times 繧貞ｮ溯｣・＠縺ｦ縺翫ｊ縲∵枚蟄苓ｪｬ譏弱・隱ｭ縺ｿ荳翫￡繧呈悽螳ｶ迚医↓縺昴ｍ縺医ｋ縺溘ａ縺ｫ繝・せ繝医さ繝ｼ繝峨↓霑ｽ蜉縺励※縺・ｋ縲・* NVDA 縺昴・繧ゅ・縺ｮ險隱橸ｼ・VDA 縺ｫ逕ｱ譚･縺吶ｋ繝・く繧ｹ繝茨ｼ峨・闍ｱ隱槭・縺ｾ縺ｾ繝・せ繝医ｒ縺励※縺・ｋ縲ゅユ繧ｹ繝医・縺輔ｉ縺ｪ繧区律譛ｬ隱槫喧縺ｯ莉雁ｾ後・隱ｲ鬘後〒縺ゅｋ縲・* chromeTests : 荳驛ｨ縺ｮ繝・せ繝医↓縺､縺・※ speech 縺ｮ縺ｿ繧呈怏蜉ｹ蛹悶＠ braille 繧堤┌蜉ｹ蛹悶＠縺ｦ縺・ｋ縲・* symbolPronunciationTests : 譛ｬ螳ｶ迚医〒縺ｯ辟｡蜉ｹ蛹悶＆繧後※縺・ｋ縺後≠縺医※譛牙柑蛹悶＠縲∵律譛ｬ隱樒沿縺ｧ蜍輔°縺呎隼螟峨ｒ縺励※縺・ｋ縲ゆｻ雁ｾ後∵律譛ｬ隱樒沿縺ｫ蝗ｺ譛峨・莉墓ｧ倥・繝・せ繝医ｒ謨ｴ蛯吶☆繧九・
### 繧ｷ繧ｹ繝・Β繝・せ繝医・螳溯｡・
繧ｷ繧ｹ繝・Β繝・せ繝医ｒ螳溯｡後☆繧九↓縺ｯ

```text
> runsystemtests.bat --include symbols --test "moveByCharacter"
```

NVDA譌･譛ｬ隱樒沿縺ｮ繝薙Ν繝峨〒陦後▲縺ｦ縺・ｋ繧ｷ繧ｹ繝・Β繝・せ繝・
```text
> runsystemtests.bat --include NVDA --exclude restarts_on_crash
> runsystemtests.bat --variable whichNVDA:installed --variable installDir:"output\nvda_%VERSION%.exe" --include installer
> runsystemtests.bat --include chrome
```

* restarts_on_crash 繧ｿ繧ｰ繧定ｿｽ蜉縺励※縺・ｋ縲ゅ％繧後ｉ縺ｯ AppVeyor 縺ｧ縺ｯ騾壹ｋ縺後√Ο繝ｼ繧ｫ繝ｫ迺ｰ蠅・〒縺ｯ騾壹ｉ縺ｪ縺・◆繧√・勁螟悶☆繧・* installer 縺ｯ繝薙Ν繝峨＠縺・NVDA 縺ｮ exe 繝輔ぃ繧､繝ｫ繧呈欠螳壹☆繧・* AppVeyor 繝薙Ν繝峨↓譎る俣縺後°縺九ｋ縺溘ａ appveyor-jp.yml 縺ｧ縺ｯ chrome 繝・せ繝医ｒ NVDA 繧ｿ繧ｰ縺九ｉ髯､螟悶＠縺ｦ縺・ｋ
* 繧ｷ繧ｹ繝・Β繝・せ繝井ｸｭ縺ｫNVDA縺ｮ襍ｷ蜍輔→邨ゆｺ・〒髻ｳ繧貞・蜉帙☆繧・
繧ｷ繧ｹ繝・Β繝・せ繝医′螟ｱ謨励☆繧句ｴ蜷・
* 繝槭Ν繝√ョ繧｣繧ｹ繝励Ξ繧､迺ｰ蠅・* 螳溯｡御ｸｭ縺ｫ逕ｻ髱｢謫堺ｽ・* 莠句燕縺ｫ Chrome 繧定ｵｷ蜍輔＠縺ｦ縺・ｋ

## 蜊倅ｽ薙ユ繧ｹ繝医→譁・ｭ苓ｪｬ譏弱・繝√ぉ繝・け

髢狗匱荳ｭ縺ｫ螳牙・縺ｫ螳溯｡後〒縺阪ｋ繝・せ繝医ｄ遒ｺ隱堺ｽ懈･ｭ縺ｨ縺励※縲∽ｻ･荳九・繧ゅ・縺後≠繧翫∪縺吶・
### 譌･譛ｬ隱櫁ｾ樊嶌縺ｮ繝・せ繝・
```text
> cd jptools
> py jpDicTest.py
```

縺薙・繧ｹ繧ｯ繝ｪ繝励ヨ縺ｯ譌･譛ｬ隱櫁ｾ樊嶌・・vdajp_dic.py・峨・讖溯・繧偵ユ繧ｹ繝医＠縺ｾ縺吶よ枚蟄励・隱ｬ譏弱ｄ螻樊ｧ縺ｮ蜿門ｾ励∵枚蟄礼ｨｮ縺ｮ蛻､螳壹↑縺ｩ繧偵メ繧ｧ繝・け縺励∪縺吶・
### 譁・ｭ苓ｪｬ譏弱→險伜捷縺ｮ繝√ぉ繝・け

jpchar繝・ぅ繝ｬ繧ｯ繝医Μ縺ｫ縺ｯ縲∵枚蟄苓ｪｬ譏弱→險伜捷縺ｮ荳雋ｫ諤ｧ繧偵メ繧ｧ繝・け縺吶ｋ繧ｹ繧ｯ繝ｪ繝励ヨ縺後≠繧翫∪縺吶りｩｳ邏ｰ縺ｯ `jpchar/readme.txt` 繧貞盾辣ｧ縺励※縺上□縺輔＞縲・
荳ｻ縺ｪ繧ｹ繧ｯ繝ｪ繝励ヨ・・- checkCharDesc.py - 譁・ｭ苓ｪｬ譏弱・荳雋ｫ諤ｧ繝√ぉ繝・け
- checkSymbols.py - 險伜捷縺ｮ荳雋ｫ諤ｧ繝√ぉ繝・け
- compareSymbolsDic.py - 險伜捷霎樊嶌縺ｮ豈碑ｼ・
### 萓晏ｭ倬未菫ゅ・繝・せ繝医→蝙九メ繧ｧ繝・け

```text
> jptools\testMiscDepsJp.cmd
```

縺薙・繧ｹ繧ｯ繝ｪ繝励ヨ縺ｯ萓晏ｭ倬未菫ゅ・繝・せ繝医→蝙九メ繧ｧ繝・け繧定｡後＞縺ｾ縺吶１ython莉ｮ諠ｳ迺ｰ蠅・ｒ菴懈・縺励［ypy縺ｫ繧医ｋ蝙九メ繧ｧ繝・け繧貞ｮ溯｡後＠縺ｾ縺吶ゆｸｻ縺ｫ莉･荳九・蜃ｦ逅・ｒ陦後＞縺ｾ縺呻ｼ・
1. Python 3.11 (32bit)縺ｮ莉ｮ諠ｳ迺ｰ蠅・ｒ菴懈・
2. 髢狗匱逕ｨ縺ｮ萓晏ｭ倥ヱ繝・こ繝ｼ繧ｸ繧偵う繝ｳ繧ｹ繝医・繝ｫ
3. jtalk繧ｳ繧｢繝輔ぃ繧､繝ｫ縺ｮ繧ｳ繝斐・
4. mypy縺ｫ繧医ｋ蝙九メ繧ｧ繝・け
5. jtalk縺ｮ繝薙Ν繝峨→繝・せ繝・6. HTML繝峨く繝･繝｡繝ｳ繝医・逕滓・

## 莉雁ｾ後・隱ｲ鬘・
### 繝薙Ν繝峨せ繧ｯ繝ｪ繝励ヨ縺ｮ蜃ｦ逅・ｧ矩縺ｨ螳溯｡後ヵ繝ｭ繝ｼ

`jptools/certBuild2023.cmd`繧剃ｸｭ蠢・→縺励◆繝薙Ν繝峨せ繧ｯ繝ｪ繝励ヨ縺ｯ隍・焚縺ｮ繧ｹ繧ｯ繝ｪ繝励ヨ縺檎嶌莠偵↓蜻ｼ縺ｳ蜃ｺ縺怜粋縺・､・尅縺ｪ讒矩縺ｫ縺ｪ縺｣縺ｦ縺・∪縺吶ゆｻ･荳九↓縺昴・蜃ｦ逅・・豬√ｌ繧定ｩｳ邏ｰ縺ｫ隱ｬ譏弱＠縺ｾ縺呻ｼ・
1. **certBuild2023.cmd縺ｮ荳ｻ縺ｪ蜃ｦ逅・ヵ繝ｭ繝ｼ**
   - 迺ｰ蠅・､画焚縺ｮ險ｭ螳夲ｼ・CONSOPTIONS, TIMESERVER・・   - Visual C++迺ｰ蠅・・險ｭ螳夲ｼ・csetup.cmd・・   - nmake縺ｨpatch繧ｳ繝槭Φ繝峨・遒ｺ隱・   - jtalk繧ｳ繧｢繝輔ぃ繧､繝ｫ縺ｮ繧ｳ繝斐・蜃ｦ逅・     ```
     cd miscDepsJp\jptools
     call copy_jtalk_core_files.cmd
     ```
   - jtalk縺ｮ繝薙Ν繝峨→繝・せ繝・     ```
     call build-and-test.cmd
     ```
   - 萓晏ｭ倥Λ繧､繝悶Λ繝ｪ縺ｮ繧ｻ繝・ヨ繧｢繝・・
     ```
     call jptools\setupMiscDepsJp.cmd
     ```
   - 蜷・ｨｮDLL繝輔ぃ繧､繝ｫ縺ｸ縺ｮ髮ｻ蟄千ｽｲ蜷・     ```
     %SIGNTOOL% sign /a /fd SHA256 /tr %TIMESERVER% /td SHA256 [繝輔ぃ繧､繝ｫ蜷江
     ```
   - scons縺ｫ繧医ｋNVDA縺ｮ繝薙Ν繝・     ```
     call scons.bat source user_docs launcher release=1 publisher=%PUBLISHER% %SCONSARGS%
     ```
   - jtalk縺ｨkgs繧｢繝峨が繝ｳ縺ｮ繝代ャ繧ｱ繝ｼ繧ｸ繝ｳ繧ｰ
   - 繧ｳ繝ｳ繝医Ο繝ｼ繝ｩ繝ｼ繧ｯ繝ｩ繧､繧｢繝ｳ繝医・繝薙Ν繝・   - 繝・せ繝医・螳溯｡・   - 鄂ｲ蜷阪・讀懆ｨｼ

2. **build-and-test.cmd縺ｮ蜃ｦ逅・*
   - jtalk繧ｳ繧｢繝輔ぃ繧､繝ｫ縺ｮ繧ｳ繝斐・・・opy_jtalk_core_files.cmd・・   - Visual C++迺ｰ蠅・・險ｭ螳・   - jtalk縺ｮ繝薙Ν繝牙・逅・     ```
     call all-clean.cmd
     call all-build.cmd
     call all-install.cmd
     ```
   - python-jtalk縺ｮ繧ｯ繝ｪ繝ｼ繝ｳ蜃ｦ逅・   - 繝・せ繝医・螳溯｡・
3. **setupMiscDepsJp.cmd縺ｮ蜃ｦ逅・*
   - jtalk縺ｮ繝薙Ν繝牙・逅・     ```
     call all-clean.cmd
     call all-build.cmd
     call all-install.cmd
     call all-clean.cmd
     ```
   - 荳譎ゅヵ繧｡繧､繝ｫ縺ｮ蜑企勁
   - source繝・ぅ繝ｬ繧ｯ繝医Μ縺ｮ繧｢繝ｼ繧ｫ繧､繝悶→螻暮幕
     ```
     7z a ..\nvdajp-miscdep.7z source
     cd ..
     7z x -y nvdajp-miscdep.7z
     del /Q nvdajp-miscdep.7z
     ```
   - 蜷・ｨｮ繧ｯ繝ｪ繝ｼ繝ｳ繧｢繝・・蜃ｦ逅・
4. **繧ｹ繧ｯ繝ｪ繝励ヨ髢薙・蜻ｼ縺ｳ蜃ｺ縺鈴未菫ゅ→驥崎､・ヵ繧｡繧､繝ｫ**
   - certBuild2023.cmd 竊・copy_jtalk_core_files.cmd
   - certBuild2023.cmd 竊・build-and-test.cmd 竊・copy_jtalk_core_files.cmd
   - certBuild2023.cmd 竊・setupMiscDepsJp.cmd
   - devbuild.cmd 竊・copy_jtalk_core_files.cmd
   - devbuild.cmd 竊・setupMiscDepsJp.cmd
   
   繝薙Ν繝峨せ繧ｯ繝ｪ繝励ヨ縺ｫ縺ｯ蜷悟錐縺ｮ繝輔ぃ繧､繝ｫ縺瑚､・焚縺ｮ蝣ｴ謇縺ｫ蟄伜惠縺励※縺翫ｊ縲√◎繧後◇繧檎焚縺ｪ繧句・逅・ｒ陦後▲縺ｦ縺・∪縺呻ｼ・   
   1. **build-and-test.cmd**
      - `miscDepsJp/jptools/build-and-test.cmd`・壻ｸｻ縺ｫjtalk縺ｮ繝薙Ν繝峨→繝・せ繝医ｒ陦後≧
        ```
        call copy_jtalk_core_files.cmd
        call ..\include\python-jtalk\vcsetup.cmd
        cd /d %~dp0
        cd ..\include\jtalk
        call all-clean.cmd
        call all-build.cmd
        call all-install.cmd
        cd ..\python-jtalk
        call clean.cmd
        cd ..\..\jptools
        call test.cmd
        ```
      - `miscDepsJp/jptools/jtalk/build-and-test.cmd`・壹ｈ繧企剞螳夂噪縺ｪ蜃ｦ逅・ｒ陦後≧
        ```
        call all-build.cmd
        call all-install.cmd
        cd ..\..\jptools
        call test-mecab.cmd
        cd ..\include\jtalk
        ```
   
   2. **all-build.cmd / all-clean.cmd / all-install.cmd**
      - `miscDepsJp/jptools/jtalk/`繝・ぅ繝ｬ繧ｯ繝医Μ縺ｫ蟄伜惠
      - `miscDepsJp/include/jtalk/`繝・ぅ繝ｬ繧ｯ繝医Μ縺ｫ縺ｯ蟄伜惠縺励↑縺・′縲∽ｸ願ｨ倥°繧峨さ繝斐・縺輔ｌ縲√せ繧ｯ繝ｪ繝励ヨ蜀・〒蜻ｼ縺ｳ蜃ｺ縺輔ｌ縺ｦ縺・ｋ
   
   3. **vcsetup.cmd**
      - `jptools/vcsetup.cmd`・医Γ繧､繝ｳ繝ｪ繝昴ず繝医Μ・・      - `miscDepsJp/include/python-jtalk/vcsetup.cmd`・医し繝悶Δ繧ｸ繝･繝ｼ繝ｫ・・   
   4. **clean.cmd**
      - `miscDepsJp/jptools/clean.cmd`・医Γ繧､繝ｳ繝ｪ繝昴ず繝医Μ・・      - `miscDepsJp/include/python-jtalk/clean.cmd`・医し繝悶Δ繧ｸ繝･繝ｼ繝ｫ・・   
   縺薙ｌ繧峨・蜷悟錐繧ｹ繧ｯ繝ｪ繝励ヨ縺ｯ縲√◎繧後◇繧檎焚縺ｪ繧句・逅・ｒ陦後≧縺溘ａ縺ｫ菴懈・縺輔ｌ縺溘ｂ縺ｮ縺ｧ縺吶′縲∝他縺ｳ蜃ｺ縺鈴未菫ゅ′隍・尅縺ｫ縺ｪ縺｣縺ｦ縺・∪縺吶・
5. **蜃ｦ逅・・迚ｹ蠕ｴ**
   - 蜷後§繝輔ぃ繧､繝ｫ縺ｮ繧ｳ繝斐・縺瑚､・焚蝗槫ｮ溯｡後＆繧後ｋ蝣ｴ蜷医′縺ゅｋ
   - jtalk縺ｮ繝薙Ν繝牙・逅・ｼ・lean竊鍛uild竊段nstall・峨′隍・焚蝗槫ｮ溯｡後＆繧後ｋ
   - 繧ｯ繝ｪ繝ｼ繝ｳ繧｢繝・・蜃ｦ逅・′隍・焚縺ｮ繧ｹ繧ｯ繝ｪ繝励ヨ縺ｫ蛻・淵縺励※縺・ｋ
   - 繧ｨ繝ｩ繝ｼ繝√ぉ繝・け縺ｯ荳驛ｨ縺ｮ蜃ｦ逅・〒縺ｮ縺ｿ螳溯｣・＆繧後※縺・ｋ
   - 繧｢繝ｼ繧ｫ繧､繝悶→螻暮幕繧剃ｽｿ縺｣縺溘ヵ繧｡繧､繝ｫ繧ｳ繝斐・蜃ｦ逅・′縺ゅｋ

縺薙ｌ繧峨・隍・尅縺ｪ蜃ｦ逅・ｧ矩縺ｯ縲・聞蟷ｴ縺ｮ髢狗匱驕守ｨ九〒谿ｵ髫守噪縺ｫ霑ｽ蜉繝ｻ菫ｮ豁｣縺輔ｌ縺ｦ縺阪◆繧ゅ・縺ｧ縲∵隼蝟・′蠢・ｦ√〒縺吶・
### 繝薙Ν繝峨せ繧ｯ繝ｪ繝励ヨ隍・尅蛹悶・豁ｴ蜿ｲ逧・ｵ檎ｷｯ

#### 繧ｵ繝悶Δ繧ｸ繝･繝ｼ繝ｫ蜈･繧悟ｭ先ｧ矩縺ｮ蝠城｡後→隗｣豸・
NVDA譌･譛ｬ隱樒沿縺ｧ縺ｯ縲∽ｻ･蜑阪・ `miscDepsJp` 繧偵し繝悶Δ繧ｸ繝･繝ｼ繝ｫ縺ｨ縺励※邂｡逅・＠縲√◎縺ｮ荳ｭ縺ｧ縺輔ｉ縺ｫ隍・焚縺ｮ繧ｵ繝悶Δ繧ｸ繝･繝ｼ繝ｫ・・ython-jtalk, htsengineapi, libopenjtalk, libkuraji・峨ｒ菴ｿ逕ｨ縺吶ｋ蜈･繧悟ｭ先ｧ矩繧呈治逕ｨ縺励※縺・∪縺励◆縲ゅ％繧後↓繧医ｊ縲∽ｾ晏ｭ倬未菫ゅ・縺ゅｋ繧ｳ繝ｳ繝昴・繝阪Φ繝茨ｼ・talk髢｢騾｣縺ｮ繝ｩ繧､繝悶Λ繝ｪ縺ｪ縺ｩ・峨′閾ｪ辟ｶ縺ｪ蠖｢縺ｧ驟咲ｽｮ縺輔ｌ縺ｦ縺・∪縺励◆縲・
縺励°縺励√し繝悶Δ繧ｸ繝･繝ｼ繝ｫ縺ｮ蜈･繧悟ｭ先ｧ矩縺ｫ縺ｯ縺・￥縺､縺九・蝠城｡後′縺ゅｊ縺ｾ縺励◆・・- 隍・尅縺ｪ萓晏ｭ倬未菫ゅ・邂｡逅・- 繧ｵ繝悶Δ繧ｸ繝･繝ｼ繝ｫ譖ｴ譁ｰ譎ゅ・蝠城｡・- 髢狗匱迺ｰ蠅・・繧ｻ繝・ヨ繧｢繝・・縺ｮ蝗ｰ髮｣縺・- Git謫堺ｽ懊・隍・尅諤ｧ・育音縺ｫ `git submodule update --init --recursive`・・
**2025蟷ｴ3譛医↓PR #492縺ｫ繧医ｊ蜈･繧悟ｭ先ｧ矩繧定ｧ｣豸・*・・- `miscDepsJp` 繧ｵ繝悶Δ繧ｸ繝･繝ｼ繝ｫ繧貞炎髯､縺励√◎縺ｮ蜀・ｮｹ繧堤峩謗･繝｡繧､繝ｳ繝ｪ繝昴ず繝医Μ縺ｫ邨ｱ蜷・- 蛟句挨縺ｮ繧ｵ繝悶Δ繧ｸ繝･繝ｼ繝ｫ・・ython-jtalk遲会ｼ峨・邯ｭ謖√＠縲～miscDepsJp/include/` 驟堺ｸ九↓驟咲ｽｮ
- 縺薙・螟画峩縺ｫ繧医ｊ邏・60荳・｡後・繝輔ぃ繧､繝ｫ縺後Γ繧､繝ｳ繝ｪ繝昴ず繝医Μ縺ｫ霑ｽ蜉縺輔ｌ縺・
**迴ｾ蝨ｨ縺ｮ繧ｵ繝悶Δ繧ｸ繝･繝ｼ繝ｫ讒区・**・・```
miscDepsJp/include/
笏懌楳笏 python-jtalk/     # 繧ｵ繝悶Δ繧ｸ繝･繝ｼ繝ｫ (nvdajp/python-jtalk)
笏懌楳笏 htsengineapi/     # 繧ｵ繝悶Δ繧ｸ繝･繝ｼ繝ｫ (nishimotz/htsengineapi)
笏懌楳笏 libopenjtalk/     # 繧ｵ繝悶Δ繧ｸ繝･繝ｼ繝ｫ (nishimotz/libopenjtalk)
笏披楳笏 libkuraji/        # 繧ｵ繝悶Δ繧ｸ繝･繝ｼ繝ｫ (nishimotz/libkuraji)
```

#### 繝・ぅ繝ｬ繧ｯ繝医Μ讒区・邯ｭ謖√・縺溘ａ縺ｮ繧ｳ繝斐・蜃ｦ逅・
繧ｵ繝悶Δ繧ｸ繝･繝ｼ繝ｫ縺ｮ蜈･繧悟ｭ先ｧ矩繧定ｧ｣豸医☆繧矩圀縲∽ｻ･荳九・蛻ｶ邏・′縺ゅｊ縺ｾ縺励◆・・- 譌｢蟄倥・繝・ぅ繝ｬ繧ｯ繝医Μ讒区・繧貞､ｧ蟷・↓螟画峩縺励◆縺上↑縺・- 繝薙Ν繝峨せ繧ｯ繝ｪ繝励ヨ縺ｸ縺ｮ蠖ｱ髻ｿ繧呈怙蟆城剞縺ｫ謚代∴縺溘＞
- 譌｢蟄倥・髢狗匱閠・・菴懈･ｭ迺ｰ蠅・∈縺ｮ蠖ｱ髻ｿ繧帝∩縺代◆縺・
縺薙・邨先棡縲・*繧ｳ繝斐・蜃ｦ逅・↓繧医▲縺ｦ譌｢蟄倥・繝・ぅ繝ｬ繧ｯ繝医Μ讒区・繧呈ｨ｡蛟｣縺吶ｋ**譁ｹ豕輔′謗｡逕ｨ縺輔ｌ縺ｾ縺励◆・・
1. **copy_jtalk_core_files.cmd**縺ｮ蟆主・
   - 繧ｵ繝悶Δ繧ｸ繝･繝ｼ繝ｫ縺九ｉ蠢・ｦ√↑繝輔ぃ繧､繝ｫ繧帝←蛻・↑蝣ｴ謇縺ｫ繧ｳ繝斐・
   - `miscDepsJp/include/htsengineapi` 竊・`miscDepsJp/include/python-jtalk/htsengineapi`
   - `miscDepsJp/include/python-jtalk/*.py` 竊・`source/synthDrivers/jtalk/`

2. **驥崎､・ｮ溯｡後・逋ｺ逕・*
   - 逡ｰ縺ｪ繧九ン繝ｫ繝峨ヵ繧ｧ繝ｼ繧ｺ縺ｧ蜷後§繧ｳ繝斐・蜃ｦ逅・ｒ螳溯｡・   - 螳牙・諤ｧ繧帝㍾隕悶＠縺ｦ繧ｳ繝斐・蜃ｦ逅・ｒ隍・焚邂・園縺ｫ驟咲ｽｮ

#### 謚陦鍋噪雋蛯ｵ縺ｨ縺励※縺ｮ迴ｾ迥ｶ

縺薙・豁ｴ蜿ｲ逧・ｵ檎ｷｯ縺ｫ繧医ｊ縲∫樟蝨ｨ縺ｮ繝薙Ν繝峨す繧ｹ繝・Β縺ｯ莉･荳九・迚ｹ蠕ｴ繧呈戟縺｣縺ｦ縺・∪縺呻ｼ・
**蛻ｩ轤ｹ**・・- 譌｢蟄倥・髢狗匱迺ｰ蠅・∈縺ｮ蠖ｱ髻ｿ繧呈怙蟆丞喧
- 谿ｵ髫守噪縺ｪ遘ｻ陦後′蜿ｯ閭ｽ
- 繝薙Ν繝峨・螳牙ｮ壽ｧ遒ｺ菫・
**隱ｲ鬘・*・・- 繝薙Ν繝画凾髢薙・蠅怜刈・磯㍾隍・・逅・ｼ・- 繝｡繝ｳ繝・リ繝ｳ繧ｹ縺ｮ隍・尅諤ｧ
- 譁ｰ隕城幕逋ｺ閠・∈縺ｮ逅・ｧ｣雋諡・
#### 莉雁ｾ後・謾ｹ蝟・婿蜷・
逅・Φ逧・↓縺ｯ莉･荳九・鬆・ｺ上〒謾ｹ蝟・ｒ騾ｲ繧√ｋ縺薙→縺梧悍縺ｾ縺励＞縺ｧ縺呻ｼ・
1. **遏ｭ譛溽噪謾ｹ蝟・*・育樟蝨ｨ螳滓命荳ｭ・・   - 驥崎､・・逅・・譛驕ｩ蛹・   - 繧ｨ繝ｩ繝ｼ繝上Φ繝峨Μ繝ｳ繧ｰ縺ｮ謾ｹ蝟・   - PR #510 縺ｧ縺ｮ `copy_jtalk_core_files.cmd` 譛驕ｩ蛹・
2. **荳ｭ譛溽噪謾ｹ蝟・*
   - 繝・ぅ繝ｬ繧ｯ繝医Μ讒区・縺ｮ谿ｵ髫守噪謨ｴ逅・   - 繝薙Ν繝峨せ繧ｯ繝ｪ繝励ヨ縺ｮ讒矩蛹・   - 蜷悟錐繧ｹ繧ｯ繝ｪ繝励ヨ繝輔ぃ繧､繝ｫ縺ｮ邨ｱ蜷・
3. **髟ｷ譛溽噪謾ｹ蝟・*
   - 譬ｹ譛ｬ逧・↑繝・ぅ繝ｬ繧ｯ繝医Μ讒区・縺ｮ隕狗峩縺・   - 萓晏ｭ倬未菫らｮ｡逅・・迴ｾ莉｣蛹・
#### 蜿り・Μ繝ｳ繧ｯ

- **PR #492**: [Refactor: Improve submodule management strategy for miscDepsJp](https://github.com/nvdajp/nvdajp/pull/492) - 繧ｵ繝悶Δ繧ｸ繝･繝ｼ繝ｫ蜈･繧悟ｭ先ｧ矩縺ｮ隗｣豸・- **PR #510**: [繝薙Ν繝峨せ繧ｯ繝ｪ繝励ヨ縺ｮ驥崎､・・逅・ｒ譛驕ｩ蛹望(https://github.com/nvdajp/nvdajp/pull/510) - 繧ｳ繝斐・蜃ｦ逅・・譛驕ｩ蛹・
### CI/CD 縺ｮ modernization

2025蟷ｴ8譛医↓譛ｬ螳ｶ縺ｮ CI/CD 謾ｹ蝟・ｒ蜿悶ｊ霎ｼ縺ｿ荳ｭ・・- GitHub Actions 繝ｯ繝ｼ繧ｯ繝輔Ο繝ｼ縺ｮ譛驕ｩ蛹・- 繝・せ繝医ず繝ｧ繝悶・蛻・屬・・ypeCheck, licenseCheck遲会ｼ・- SCons MSVC Cache 縺ｫ繧医ｋ鬮倬溷喧
- windows-2025 繝ｩ繝ｳ繝翫・縺ｸ縺ｮ遘ｻ陦・
谿ｵ髫守噪縺ｪ謾ｹ蝟・い繝励Ο繝ｼ繝・ｼ・1. 隨ｬ1谿ｵ髫趣ｼ壽悽螳ｶ CI/CD 讒矩縺ｮ蜿悶ｊ霎ｼ縺ｿ・・025蟷ｴ8譛亥ｮ滓命・・2. 隨ｬ2谿ｵ髫趣ｼ啀ython 3.13 蟇ｾ蠢・3. 隨ｬ3谿ｵ髫趣ｼ噎64 繝薙Ν繝牙ｯｾ蠢懊・讀懆ｨ・
### Python 繝舌・繧ｸ繝ｧ繝ｳ縺ｮ蟇ｾ蠢懃憾豕・
#### 迴ｾ蝨ｨ縺ｮ迥ｶ豕・ｼ・025蟷ｴ8譛茨ｼ・- Python 3.11.9 (32bit) 繧剃ｽｿ逕ｨ
- 譛ｬ螳ｶ NVDA 縺ｯ Python 3.11.9 縺ｨ 3.13.6 縺ｮ繝槭ヨ繝ｪ繝・け繧ｹ繝・せ繝医ｒ螳滓命

#### 莉雁ｾ後・蟇ｾ蠢・- Python 3.13 縺ｸ縺ｮ蟇ｾ蠢懊・谿ｵ髫守噪縺ｫ螳滓命莠亥ｮ・- 縺ｾ縺壽悽螳ｶ beta 縺ｮ繝槭・繧ｸ縺ｨ CI/CD 縺ｮ螳牙ｮ壼喧繧貞━蜈・- 縺昴・蠕後￣ython 3.13 蟇ｾ蠢懊ｒ蛻･ PR 縺ｧ螳滓命

#### Python 3.13 蟇ｾ蠢懈凾縺ｮ豕ｨ諢冗せ
- 萓晏ｭ倥ヱ繝・こ繝ｼ繧ｸ縺ｮ莠呈鋤諤ｧ遒ｺ隱阪′蠢・ｦ・- 譌･譛ｬ隱樒沿蝗ｺ譛峨・繝｢繧ｸ繝･繝ｼ繝ｫ・・talk遲会ｼ峨・蜍穂ｽ懃｢ｺ隱阪′蠢・ｦ・- 繝槭ヨ繝ｪ繝・け繧ｹ繝・せ繝医・蟆主・繧呈､懆ｨ・


