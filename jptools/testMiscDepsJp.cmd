@rem (usage)
@rem > jptools\testMiscDepsJp.cmd
cd miscDepsJp
py -3.11-32 -m venv .venv
call .venv\scripts\activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
cd jptools
call copy_jtalk_core_files.cmd
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
