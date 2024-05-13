# NVDAJP Release Notes NVDA_VERSION

[TOC]

## Overview

* last update: 2022-12-03
* updated by: NVDA Japanese Team / Takuya Nishimoto (Shuaruta Inc.)

Release by [NVDA Japanese Team (nvdajp)](http://www.nvda.jp/en/), based on NVDA from NV Access.

This document describes difference between original release of NVDA and the NVDAJP.
NVDAJP releases are based on NV Access's rc branch.
Please read this document and NVDA User Guide as well.

NVDA Japanese is provided "as is", without warranty.

### Web site

* [NVDA Japanese www.nvda.jp/en](https://www.nvda.jp/en/)

### Contributors

[Contributors for NVDA Japanese](https://osdn.net/projects/nvdajp/wiki/contributors_ja)

## Install

NVDAJP requires 120MB storage space.

Launcher package of stable version is available at http://i.nvda.jp

Application icon is changed to the goldfish.

## Launching NVDA

Windows shortcut for starting NVDA is CTRL+ALT+N, if installed.

It may conflicts to other screen reader which is popular in Japan.

This shortcut can be modified using the property (ALT+Enter) of NVDAJP icon of Windows desktop.

## Object Navigation

### Character description mode

Character description mode can be changed for caret moves by left arrow or right arrow key and character review commands.

Pressing "Report current character in review" (numpad2 or NVDA+period) four-times can enable or disable the description mode.

| Name |Desktop key |Laptop key |Touch |Description|
|---|---|---|---|---|
|Move to previous character in review |numpad1 |NVDA+left arrow |flick left (text mode) |Moves the review cursor to the previous character on the current line in the text. If description mode is enabled, the character is described.|
|Report current character in review |numpad2 |NVDA+period |none |Announces the current character on the line of text where the review cursor is positioned. If description mode is enabled, the character is described. Pressing twice reports the character with its attributes and description. Pressing three times reports the numeric value of the character in decimal and hexadecimal. Pressing four-times toggles the description mode.|
|Move to next character in review |numpad3 |NVDA+right arrow |flick right (text mode) |Move the review cursor to the next character on the current line of text. If description mode is enabled, the character is described.|

## Configuration

### General settings

### Language settings

Language settings dialog contains settings for Japanese keyboard, character description, and input composition.

#### Use NonConvert as NVDA key

If checked, NonConvert key can be used as NVDA modifier key. Default is on.
The Welcome dialog also has this option.

#### Use Convert as NVDA key

If checked, Convert key can be used as NVDA modifier key. Default is off.
The Welcome dialog also has this option.

#### Use Escape as NVDA key

If checked, Escape key can be used as NVDA modifier key. Default is off.
The Welcome dialog also has this option.

#### Beep if IME mode is changed

If checked, the press of Half-shape/Full-shape key is announced only with beep.
Default is off.

#### Phonetic reading for Kana

If checked, Hiragana and Katakana characters are reported using phonetic reading when "Report current character in review" is pressed twice.
Default is off.

#### Phonetic reading for Latin

If checked, Latin characters are reported using phonetic reading when "Report current character in review" is pressed twice.
Default is off.

#### Katakana pitch change percentage

The amount that the pitch of the voice will change when speaking a Katakana letter for character review.
Default is -20.

For candidates of Japanese input methods, pitch change is not available.

#### Half-shape pitch change percentage

The amount that the pitch of the voice will change when speaking a half-shape letter for character review.
Default is 20.

For candidates of Japanese input methods, pitch change is not available.

#### Announce candidate number

The default of 'Announce candidate number' is disabled.
If checked, items in candidate window of Japanese input methods such as Micosoft IME are annonced with numbers.
If 'IME support of nvdajp' is disabled, this option has no effect.

#### Use IME support of nvdajp

The default of 'Use IME support of nvdajp' is enabled.

If this option is enabled, pressing escape key to clear the input method session will announce as 'clear', rather than announcing the cancelled text itself.

To disable, turn off the option.

#### Work around ANSI editbox

NVDA Japanese have made a work around edit control for ANSI applications. Because of this, some applications cannot handle line ending positions correctly.
If this option is turned off, edit controls are treated as same as the original version of NVDA.
If you use Winbiff e-mail software, please turn this option off.

#### Announce new line in editable text

This option allows announcement of new line when Enter key is pressed in editable text.
If Enter key is used for ending input composition session, it is not announced.
When 'Speak typed character' is disabled in Keyboard settings, it is not announced as well.
This is experimental feature, so it may not work correctly in some applications.

#### Open document file by MSHTA

In Japanese version, 'Open document file by MSHTA' option is enabled by default.

If it is enabled, some documents in NVDA help menu are opened as an application, rather than using the system's default Web browser.

If it is disabled, the system's default Web browser, such as Internet Explorer or Mozilla Firefox, is used for the documents.

A technology called HTA (mshta.exe) is used for opening the help document as an application.
If you use the environment where HTA is not allowed, disable the option.

#### Speak math in English

'Speak math in English' option is checked by default.

If the option is not checked, NVDA may say "No navigation files for this speech style in this language" during interactive navigation of MathML content in Japanese.

The issue is discussed at [NVDAJP ticket 29872](https://osdn.net/ticket/browse.php?group_id=4221&tid=35208) and [#5126](http://community.nvda-project.org/ticket/5126).

### Voice settings

#### Capital pitch change percentage

The default value of Capital pitch change percentage is 0.
This is because NVDAJP uses pitch for indicating types of phonetic characters of Japanese language.

#### Say "cap" before capitals

'Say "cap" before capitals' is enabled by default.
This is because NVDAJP uses pitch for indicating types of phonetic characters of Japanese language.

#### Use spelling functionality if supported

NVDAJP uses internal dictionary for spelling reading rather than using functionarity of speech synthesizers.

This option should be turned off with some Japanese TTS, because of issues with the functionality.

### Braille settings

#### Japanese braille table

"Japanese 6 dot computer braille" output table is added and changed to the default. It is 'pseudo' table and it does not use LibLouis.

Cursor position mapping is implemented for Japanese output table.

'Expand to computer braille for the word at the cursor' is supported with Japanese braille translator. It expands all alphabet, number and symbol characters, which can be translated to NABCC, regardless of cursor position.

Experimental braille input tables of "Japanese 6 dot computer braille" and "Japanese 6 dot kanji braille" are available. Their usages are similar to English grade 2 input table. However, they cover very limited charactors so far.

### Keyboard settings

Caps Lock key of Japanese keyboard array cannot be used as NVDA modifier key.

'Speak typed words' should be turned off if Japanese input method editor is used.

Candidates of Japanese input method editor is announced, even if 'Speak typed characters' is disabled.

### Input composition settings

'Automatically report all available candidates' should be turned off for the use of Japanese input method editors, such as Microsoft IME or ATOK.

## Synthesizer

### Jtalk

JTalk driver is the default synthesizer of NVDAJP, which supports Japanese language.

* JTalk (Japanese TTS) has M001, Lite, Mei and Tohoku-f01 voices. M001 and Lite are male voices. Mei and Tohoku-f01 are female voice.
* M001 and Mei are at sampling rate of 48kHz. Lite is at sampling rate of 16kHz.
* Speed, Volume, Pitch, Inflection can be changed.
* Rate boost option is available.
* 'Automatic Language switching' is supported. If the content has language attributes, it is used for selecting voices. Voices of eSpeak NG are used other than Japanese voice. Speech rate or other settings are not applied to voices other than Japanese.
* 'Automatic Dialect switching' is not supported.
* It works with audio ducking mode of 'Duck when outputting speech and sounds.'

### eSpeak NG

eSpeak NG of NVDAJP supports reading of Japanese characters and Chinese characters. It uses Japanese text processing of Jtalk internally.

eSpeak NG of NVDA cannot handle Japanese language.

## Braille display

### KGS Braille Memo series

The driver for braille display "KGS BrailleMemo series" from [KGS Corporation](http://www.kgs-jpn.co.jp/) is added. BMS40 and BM46 are used for development and tests. BM32 is tested by the community.

Both automatic and manual port setting can be used. It also works with Bluetooth.

The BM Utility is used if it is installed to the computer. This driver is tested with BM Utility Version 6.4.0.

For USB connection, virtual serial driver must also be installed.
The device should be configured to use 9600BPS connection speed for virtual serial driver.

This driver allows you to choose connection port from the available serial ports and the detected BM series devices via USB or Bluetooth connection.

If NVDA's braille display driver is set to "automatic", NVDA may repeat the automatic detection of the braille display of KGS Corporation.
This is especially likely in situations where you've plugged in a braille display of KGS Corporation, but it's not currently plugged in, especially with the Bluetooth connections.
To work around this issue, set NVDA to "No Braille" or disable Bluetooth in the Windows settings.

KGS Braille Memo driver supports following commands:

Basic operations (1):

| Name |Key |BM46|
|---|---|---|
|up |up |up|
|down |down |down|
|left |left |left|
|right |right |right|
|Shift + up |select+up |f2+up|
|Shift + down |select+down |f2+down|
|Shift + left |select+left |f2+left|
|Shift + right |select+right |f2+right|
|review previous line |bw |f3+up|
|review next line |fw |f3+down|
|review previous word |ls |f3+left|
|review next word |rs |f3+right|
|move to cell |tether |tether|
|display previous |f1 |f1|
|display forward |f4 |f4|
|Enter |enter |left thumb|
|Space |space |right thumb|
|Control |ctrl |left little finger 1|
|Alt |alt |left little finger 2|
|Shift |select |right little finger 1|
|Windows |read |right little finger 2|

Basic operations (2):

| Name |Key |BM46(left hand mode) |BM46(right hand mode)|
|---|---|---|---|
|NVDA menu |ins |f1+up |f4+up|
|Backspace |bs |f1+left |f4+left|
|Delete |del |f1+right |f4+right|
|Enter |ok |f4+up |f1+up|
|Enter |set |f4+down |f1+down|
|Tab |inf |f4+left |f1+left|
|Esc |esc |f4+right |f1+right|
|Alt+Tab |alt+inf |f4+left little finger 2+left |f1+left little finger 2+left|
|Shift+Tab |select+inf |f4+right little finger 1+left |f1+right little finger 1+left|

Latin characters:

| Name |Key|
|---|---|
|a |1|
|b |12|
|c |14|
|d |145|
|e |15|
|f |124|
|g |1245|
|h |125|
|i |24|
|j |245|
|k |13|
|l |123|
|m |134|
|n |1345|
|o |135|
|p |1234|
|q |12345|
|r |1235|
|s |234|
|t |2345|
|u |136|
|v |1236|
|w |2456|
|x |1346|
|y |13456|
|z |1356|

Latin characters with control key:

| Name |Key |BM46|
|---|---|---|
|Control+a |ctrl+1 |left little finger 1+1|
|Control+b |ctrl+12 |left little finger 1+12|
|Control+c |ctrl+14 |left little finger 1+14|
|Control+d |ctrl+145 |left little finger 1+145|
|Control+e |ctrl+15 |left little finger 1+15|
|Control+f |ctrl+124 |left little finger 1+124|
|Control+g |ctrl+1245 |left little finger 1+1245|
|Control+h |ctrl+125 |left little finger 1+125|
|Control+i |ctrl+24 |left little finger 1+24|
|Control+j |ctrl+245 |left little finger 1+245|
|Control+k |ctrl+13 |left little finger 1+13|
|Control+l |ctrl+123 |left little finger 1+123|
|Control+m |ctrl+134 |left little finger 1+134|
|Control+n |ctrl+1345 |left little finger 1+1345|
|Control+o |ctrl+135 |left little finger 1+135|
|Control+p |ctrl+1234 |left little finger 1+1234|
|Control+q |ctrl+12345 |left little finger 1+12345|
|Control+r |ctrl+1235 |left little finger 1+1235|
|Control+s |ctrl+234 |left little finger 1+234|
|Control+t |ctrl+2345 |left little finger 1+2345|
|Control+u |ctrl+136 |left little finger 1+136|
|Control+v |ctrl+1236 |left little finger 1+1236|
|Control+w |ctrl+2456 |left little finger 1+2456|
|Control+x |ctrl+1346 |left little finger 1+1346|
|Control+y |ctrl+13456 |left little finger 1+13456|
|Control+z |ctrl+1356 |left little finger 1+1356|

Latin characters with Alt key:

| Name |Key |BM46|
|---|---|---|
|Alt+a |alt+1 |left little finger 2+1|
|Alt+b |alt+12 |left little finger 2+12|
|Alt+c |alt+14 |left little finger 2+41|
|Alt+d |alt+145 |left little finger 2+145|
|Alt+e |alt+15 |left little finger 2+15|
|Alt+f |alt+124 |left little finger 2+124|
|Alt+g |alt+1245 |left little finger 2+1245|
|Alt+h |alt+125 |left little finger 2+125|
|Alt+i |alt+24 |left little finger 2+24|
|Alt+j |alt+245 |left little finger 2+245|
|Alt+k |alt+13 |left little finger 2+13|
|Alt+l |alt+123 |left little finger 2+123|
|Alt+m |alt+134 |left little finger 2+134|
|Alt+n |alt+1345 |left little finger 2+1345|
|Alt+o |alt+135 |left little finger 2+135|
|Alt+p |alt+1234 |left little finger 2+1234|
|Alt+q |alt+12345 |left little finger 2+12345|
|Alt+r |alt+1235 |left little finger 2+1235|
|Alt+s |alt+234 |left little finger 2+234|
|Alt+t |alt+2345 |left little finger 2+2345|
|Alt+u |alt+136 |left little finger 2+136|
|Alt+v |alt+1236 |left little finger 2+1236|
|Alt+w |alt+2456 |left little finger 2+2456|
|Alt+x |alt+1346 |left little finger 2+1346|
|Alt+y |alt+13456 |left little finger 2+13456|
|Alt+z |alt+1356 |left little finger 2+1356|

Symbols:

| Name |Key|
|---|---|
|. (period) |256|
|: (colon) |25|
|; (semicolon) |23|
|, (comma) |2|
|- (minus) |36|
|? (question) |236|
|! (exclamation) |235|
|' (apostrophe) |3|

### KGS BrailleNote 46C/46D

The driver for braille display "KGS BrailleNote 46C/46D" from [KGS Corporation](http://www.kgs-jpn.co.jp/) is added.

The BM Utility can be used if it is installed to the computer.

BrailleNote BN46X can be used with "KGS BrailleMemo series" driver if BM Utility is installed.
BrailleNote BN46X can be used with "KGS BrailleNote 46C/46D" driver if BM Utility is not installed.

For USB connection, virtual serial driver must also be installed.
The device should be configured to use 9600BPS connection speed for virtual serial driver.

BrailleNote 46C/46D driver supports following commands:

| Name |Key|
|---|---|
|NVDA menu |f1|
|move to cell |tether|
|scroll back |sl|
|scroll forward |sr|
|review previous line |f2+bk|
|review next line |f2+lf|
|review previous word |f2+sl|
|review next word |f2+sr|
|up arrow |bk|
|down arrow |lf|
|left arrow |f3|
|right arrow |f4|

### BrailleMemo experimental

BrailleMemo experimental driver is added for evaluating Grade 2 Braille input tables.

* Compatible with the devices as same as "KGS BrailleMemo series" driver.
* Left hand thumb key is assigned to dot 7 (delete previous cell or character).
* Right hand thumb key is assigned to dot 8 (Braille translation and Enter key).
* Left hand thumb key and Right hand thumb key (dot 7+ dot 8) is for Braille translation.
* dot 4 + dot 8 is for space key.
* Latin characters cannot be typed without using Braille input table. It is deprecated for this driver.
* Not tested very well with devices other than KGS BM46.

## NVDA Menu

### Braille Viewer

"Braille Viewer" is added in Tools menu. Available for Japanese language.

It translates spoken words to Japanese braille pattens, so it is not exactly same as the output to braille devices.

For Windows XP or Vista, DejaVu Sans font must be installed to display braille patterns. If you install LibreOffice, DejaVu Sans font will be installed as well.

## Applications

### Microsoft Word support

Paragraph indent of Microsoft Word is now supported by NVDA. ([#4165](http://community.nvda-project.org/ticket/4165))

## Configurations

### Character dictionary

NVDAJP can modify character descriptions and spelling readings by users. A dictionary file can be created in the user config directory.

User config directory (Windows XP):

    C:\Documents and Settings\(User Name)\Application Data\nvda

(Windows Vista, 7, 8.1, 10):

    C:\Users\(User Name)\AppData\Roaming\nvda

The dictionary file name should be characters-ja.dic. ('ja' is the locale identifier.)

The file should be plain text with UTF-8 encoding. The lines should be tab-separated values.

    field 1: character
    field 2: Unicode hexadicimal character code
    field 3: spelling reading quoted with [ and ]
    field 4 (or later): field 2 or later items of charactersDescriptions.dic

If the line starts with '#', it is ignored. If the line starts with '\#', the character is '#' itself.

Details (in Japanese) [NVDAJP ticket 29872](https://osdn.net/ticket/browse.php?group_id=4221&tid=29872)

## Miscellaneous

### Source code and build server

We use git hosting services as follows:

* GitHub: https://github.com/nvdajp

We use AppVeyor as public build server:

* [AppVeyor (public build server)](https://ci.appveyor.com/project/TakuyaNishimoto/nvdajp)

### Issues

* [OSDN Tickets](https://osdn.net/projects/nvdajp/ticket/)
* [GitHub Issues (nvdajp)](https://github.com/nvdajp/nvdajp/issues)

### Controller Client API

* [Controller Client enhancement by NVDAJP](https://osdn.net/projects/nvdajp/wiki/ControllerClient)
* [NvdaDemoApp (bitbucket.org)](https://bitbucket.org/nishimotz/nvdademoapp)

