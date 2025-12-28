@rem Delegate to jptools/vcsetup.cmd for x86 MSVC environment setup
@rem This script is kept for backward compatibility with existing callers.
@rem Path calculation: from miscDepsJp/include/python-jtalk to repo root jptools
call "%~dp0..\..\..\jptools\vcsetup.cmd" x86
