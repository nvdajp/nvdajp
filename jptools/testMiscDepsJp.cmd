@rem (usage)
@rem > jptools\testMiscDepsJp.cmd
cd miscDepsJp
py -3.11-32 -m venv .venv
call .venv\scripts\activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
cd jptools
uv run python -c "import sys; sys.path.insert(0, '.'); from scons_jp import _copy_jtalk_core_files; from pathlib import Path; exit(_copy_jtalk_core_files(Path('..').resolve()))"
if not "%ERRORLEVEL%"=="0" goto onerror
mypy @"../mypy_jptools.txt" > ..\__mypy.txt
cd ..
cd source\synthDrivers
mypy @"../../mypy_source_synthDrivers.txt" >> ..\..\__mypy.txt
cd ..\..
cd jptools
call build-and-test.cmd
call make_html.cmd
cd ..
cd ..
deactivate
