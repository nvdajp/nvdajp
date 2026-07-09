# Injected by build/common_build.ps1 after git clone.
# Pin SCons to Visual Studio 2022 (MSVC 14.3) when VS 2026+ is also installed.
# vcsetup.cmd already prefers VS 2022; SCons otherwise auto-selects the newest MSVC (14.5).
#
# Setting MSVC_VERSION at module scope is not enough: NVDA's SConstruct calls
# Environment(variables=vars, ...) without MSVC_VERSION, so we wrap Environment.

from __future__ import annotations

import SCons.Script

_MSVC_VERSION = "14.3"
_orig_environment = SCons.Script.Environment


def Environment(*args, **kwargs):
	kwargs.setdefault("MSVC_VERSION", _MSVC_VERSION)
	return _orig_environment(*args, **kwargs)


SCons.Script.Environment = Environment
