/* mytest_ubuntu.c
 * by Takuya Nishimoto
 */

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
    handle = dlopen("libopenjtalk.so.0.0.0", RTLD_LAZY);
    if (!handle) {
        fputs (dlerror(), stderr);
	fputs ("\n", stderr);
        exit(1);
    }
    func_jtalk = dlsym(handle, "_libopenjtalk_main");
    if ((error = dlerror()) != NULL)  {
        fputs(error, stderr);
	fputs ("\n", stderr);
        exit(1);
    }
    ret = (*func_jtalk)(argc, argv);
    dlclose(handle);
    return ret;
}
