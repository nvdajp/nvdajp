# Diff for: `miscDepsJp\jptools\jtusrdic\plumbum\commands\daemons.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\miscDepsJp\jptools\jtusrdic\plumbum\commands\daemons.py`  
**Current**: `F:\nvda\gh\alphajp\miscDepsJp\jptools\jtusrdic\plumbum\commands\daemons.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\jtusrdic\\plumbum\\commands\\daemons.py" "b/F:\\nvda\\gh\\alphajp\\miscDepsJp\\jptools\\jtusrdic\\plumbum\\commands\\daemons.py"
index 4294a4bc79..f6d683cbfd 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\jtusrdic\\plumbum\\commands\\daemons.py"
+++ "b/F:\\nvda\\gh\\alphajp\\miscDepsJp\\jptools\\jtusrdic\\plumbum\\commands\\daemons.py"
@@ -27,7 +27,7 @@ def posix_daemonize(command, cwd):
             proc = command.popen(cwd = cwd, close_fds = True, stdin = stdin.fileno(), 
                 stdout = stdout.fileno(), stderr = stderr.fileno())
             os.write(wfd, str(proc.pid).encode("utf8"))
-        except:
+        except Exception:
             rc = 1
             tbtext = "".join(traceback.format_exception(*sys.exc_info()))[-MAX_SIZE:]
             os.write(wfd, tbtext.encode("utf8"))

```