xcopy /E /Y .\jtalk ..\include\jtalk
xcopy /E /Y ..\include\htsengineapi ..\include\python-jtalk\htsengineapi
xcopy /E /Y ..\include\libopenjtalk ..\include\python-jtalk\libopenjtalk
copy /Y ..\include\python-jtalk\jtalkCore.py ..\source\synthDrivers\jtalk\jtalkCore.py
copy /Y ..\include\python-jtalk\mecab.py ..\source\synthDrivers\jtalk\mecab.py
copy /Y ..\include\python-jtalk\text2mecab.py ..\source\synthDrivers\jtalk\text2mecab.py
copy /Y ..\include\python-jtalk\jtalkRunner.py .\jtalkRunner.py
