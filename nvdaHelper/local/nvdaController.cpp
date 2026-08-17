/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2026 NV Access Limited, Leonard de Ruijter, Ethin Probst.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include <local/nvdaController.h>
#include <windows.h>

error_status_t(__stdcall *_nvdaController_speakText)(const wchar_t*) = nullptr;

error_status_t __stdcall nvdaController_speakText(const wchar_t* text) {
	if (_nvdaController_speakText == nullptr) {
		return ERROR_CALL_NOT_IMPLEMENTED;
	}
	return _nvdaController_speakText(text);
}

error_status_t(__stdcall *_nvdaController_speakSsml)(const wchar_t*, const SYMBOL_LEVEL, const SPEECH_PRIORITY, const boolean) = nullptr;

error_status_t __stdcall nvdaController_speakSsml(const wchar_t* ssml, const SYMBOL_LEVEL symbolLevel, const SPEECH_PRIORITY priority, const boolean asynchronous) {
	if (_nvdaController_speakSsml == nullptr) {
		return ERROR_CALL_NOT_IMPLEMENTED;
	}
	return _nvdaController_speakSsml(ssml, symbolLevel, priority, asynchronous);
}

error_status_t(__stdcall *_nvdaController_cancelSpeech)();

error_status_t __stdcall nvdaController_cancelSpeech() {
	if (_nvdaController_cancelSpeech == nullptr) {
		return ERROR_CALL_NOT_IMPLEMENTED;
	}
	return _nvdaController_cancelSpeech();
}

error_status_t(__stdcall *_nvdaController_brailleMessage)(const wchar_t*);

error_status_t __stdcall nvdaController_brailleMessage(const wchar_t* text) {
	if (_nvdaController_brailleMessage == nullptr) {
		return ERROR_CALL_NOT_IMPLEMENTED;
	}
	return _nvdaController_brailleMessage(text);
}

error_status_t(__stdcall *_nvdaController_setAppSleepMode)(const int mode) = nullptr;

error_status_t(__stdcall *_nvdaController_speakSpelling)(const wchar_t*) = nullptr;
error_status_t __stdcall nvdaController_speakSpelling(const wchar_t* text) {
	if (_nvdaController_speakSpelling == nullptr) {
		return ERROR_CALL_NOT_IMPLEMENTED;
	}
	return _nvdaController_speakSpelling(text);
}

error_status_t(__stdcall *_nvdaController_getPitch)() = nullptr;
error_status_t __stdcall nvdaController_getPitch() {
	if (_nvdaController_getPitch == nullptr) {
		return ERROR_CALL_NOT_IMPLEMENTED;
	}
	return _nvdaController_getPitch();
}

error_status_t(__stdcall *_nvdaController_setPitch)(const int) = nullptr;
error_status_t __stdcall nvdaController_setPitch(const int nPitch) {
	if (_nvdaController_setPitch == nullptr) {
		return ERROR_CALL_NOT_IMPLEMENTED;
	}
	return _nvdaController_setPitch(nPitch);
}

error_status_t(__stdcall *_nvdaController_getRate)() = nullptr;
error_status_t __stdcall nvdaController_getRate() {
	if (_nvdaController_getRate == nullptr) {
		return ERROR_CALL_NOT_IMPLEMENTED;
	}
	return _nvdaController_getRate();
}

error_status_t(__stdcall *_nvdaController_setRate)(const int) = nullptr;
error_status_t __stdcall nvdaController_setRate(const int nRate) {
	if (_nvdaController_setRate == nullptr) {
		return ERROR_CALL_NOT_IMPLEMENTED;
	}
	return _nvdaController_setRate(nRate);
}

error_status_t __stdcall nvdaController_setAppSleepMode(const int mode) {
	if (_nvdaController_setAppSleepMode == nullptr) {
		return ERROR_CALL_NOT_IMPLEMENTED;
	}
	return _nvdaController_setAppSleepMode(mode);
}

error_status_t __stdcall nvdaController_getProcessId(unsigned long* pid) {
	if (pid == nullptr) {
		return ERROR_INVALID_PARAMETER;
	}
	*pid = GetCurrentProcessId();
	return ERROR_SUCCESS;
}

error_status_t __stdcall nvdaController_testIfRunning() {
	return ERROR_SUCCESS;
}

error_status_t(__stdcall *_nvdaController_isSpeaking)(boolean*) = nullptr;

error_status_t __stdcall nvdaController_isSpeaking(boolean* isSpeaking) {
	if (isSpeaking == nullptr) return ERROR_INVALID_PARAMETER;
	if (_nvdaController_isSpeaking == nullptr) return ERROR_CALL_NOT_IMPLEMENTED;
	return _nvdaController_isSpeaking(isSpeaking);
}
