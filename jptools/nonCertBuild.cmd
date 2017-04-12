@set BUILDOPTIONS=publisher=%PUBLISHER% release=1 version=%VERSION% updateVersionType=%UPDATEVERSIONTYPE% %SCONSOPTIONS%
@scons source %BUILDOPTIONS%
@scons tests %BUILDOPTIONS%
@scons user_docs launcher %BUILDOPTIONS%
