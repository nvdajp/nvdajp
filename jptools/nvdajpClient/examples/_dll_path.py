# coding: utf-8
"""Controller Client DLL のパスを解決する共通モジュール。

examples/ から実行する場合:
  - パッケージ構成: 親ディレクトリの x86/x64/nvdaControllerClient.dll を参照
  - リポジトリ構成: extras/controllerClient/x86|x64/nvdaControllerClient.dll を参照
"""

from __future__ import annotations

import os
import sys


def get_nvda_controller_client_dll_path() -> str:
	"""Python のアーキテクチャに応じて nvdaControllerClient.dll のパスを返す。"""
	arch = "x64" if sys.maxsize > 2**32 else "x86"
	dll_name = "nvdaControllerClient.dll"

	# 1) パッケージ構成: examples/ の親 (nvdajpClient) 直下の x86|x64/
	script_dir = os.path.dirname(os.path.abspath(__file__))
	parent = os.path.dirname(script_dir)
	dll = os.path.join(parent, arch, dll_name)
	if os.path.isfile(dll):
		return dll

	# 2) リポジトリ構成: jptools/nvdajpClient/examples -> リポジトリルート
	repo_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
	dll = os.path.join(repo_root, "extras", "controllerClient", arch, dll_name)
	if os.path.isfile(dll):
		return dll

	# フォールバック（見つからなければ呼び出し側でエラー）
	return os.path.join(parent, arch, dll_name)
