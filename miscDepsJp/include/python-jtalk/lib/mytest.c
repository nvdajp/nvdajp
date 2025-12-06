/* mytest.c
 * by Takuya Nishimoto
 */

#define WINDOWS

#ifndef WINDOWS
#include <stdlib.h>
#include <stdio.h>
#include <dlfcn.h>
#include <string.h>
 
int main(int argc, char **argv)
{
    void *handle;
    int (*func_jtalk)(int ac, char **av);
    char *error;
    int ret;
    handle = dlopen("libopenjtalk.dll", RTLD_LAZY);
    if (!handle) {
        fputs (dlerror(), stderr);
        exit(1);
    }
    func_jtalk = dlsym(handle, "libopen_jtalk_main");
    if ((error = dlerror()) != NULL)  {
        fputs(error, stderr);
        exit(1);
    }
    ret = (*func_jtalk)(argc, argv);
    dlclose(handle);
    return ret;
}

#else
#include <windows.h>
#include <stdio.h>
#include "njd.h"
#include "jpcommon.h"
#include "HTS_engine.h"
int main(int argc, char **argv)
{
    HMODULE hModule;
    int (*func_jtalk)(char *buff, char *owfile);
    int ret = 1;

    hModule = LoadLibrary( "libopenjtalk.dll" );
    if (hModule != NULL) {
	func_jtalk = (void *)GetProcAddress( hModule, "libopen_jtalk_main" );
	if (func_jtalk != NULL) {
	    char *buff = "こんにちは"; // UTF-8
	    char *owfile = "out1.wav";
	    ret = (*func_jtalk)(buff, owfile);
	}
	FreeLibrary(hModule);
    }
    
    printf("HTS_Global %d\n", sizeof(HTS_Global));
    printf("HTS_ModelSet %d\n", sizeof(HTS_ModelSet));
    printf("HTS_Label %d\n", sizeof(HTS_Label));
    printf("HTS_SStreamSet %d\n", sizeof(HTS_SStreamSet));
    printf("HTS_PStreamSet %d\n", sizeof(HTS_PStreamSet));
    printf("HTS_GStreamSet %d\n", sizeof(HTS_GStreamSet));
    printf("NJD %d\n", sizeof(NJD));
    printf("JPCommon %d\n", sizeof(JPCommon));
    return ret;
}

#endif
