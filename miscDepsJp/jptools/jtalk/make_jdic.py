# coding: utf-8
# make_jdic.py
# Copyright (C) 2010-2013 Takuya Nishimoto (NVDA Japanese Team)

import os
import shutil
import subprocess
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from os import path
from pathlib import Path

import custom_dic_maker
import eng_dic_maker
import tankan_dic_maker
from filter_jdic import filter_jdic


def open_file(name, mode, encoding):
    return open(name, mode, encoding=encoding)


def _log_mode() -> str:
    mode = os.environ.get("JP_MECAB_LOG_MODE", "file").lower()
    if mode not in {"file", "console"}:
        mode = "file"
    return mode


@contextmanager
def _log_redirect(repo_root: Path, mode: str):
    if mode == "console":
        yield None, None
        return
    log_dir = repo_root / "output" / "_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "make_jdic.log"
    with log_path.open("w", encoding="utf-8", errors="ignore") as fp, redirect_stdout(fp), redirect_stderr(fp):
        yield log_path, fp


def mkdir_p(path):
    os.makedirs(path, exist_ok=True)


def convert_file(src_file, src_enc, dest_file, dest_enc, apply_filter=False):
    print("converting %s to %s" % (src_file, dest_file))
    with open_file(src_file, "r", src_enc) as sf:
        with open_file(dest_file, "w", dest_enc) as df:
            while 1:
                s = sf.readline()
                if not s:
                    break
                if apply_filter:
                    s = s.rstrip()
                    s = filter_jdic(s)
                    if s:
                        s += "\n"  # do not use os.linesep here
                df.write(s)


def _main():
    # MECAB_DICT_INDEX と OUTDIR は libopenjtalk/mecab-naist-jdic/_temp が基準
    jtdir = path.dirname(path.abspath(__file__))
    engdic = path.normpath(path.join(jtdir, "bep-eng.dic"))
    cs_file = path.normpath(path.join(jtdir, "characters-ja.dic"))

    thisdir = path.normpath(path.join(jtdir, "libopenjtalk", "mecab-naist-jdic"))
    # Build output directly under source/ to avoid extra copy in jtalkSync.
    repo_root = Path(path.normpath(path.join(jtdir, "..", "..", "..")))
    outdir = path.normpath(path.join(repo_root, "source", "synthDrivers", "jtalk", "dic"))
    tempdir = path.normpath(path.join(thisdir, "_temp"))
    mecab_dict_index = path.normpath(path.join(thisdir, "..", "mecab", "src", "mecab-dict-index.exe"))
    code = "utf-8"  # cp932

    mode = _log_mode()
    with _log_redirect(repo_root, mode) as (log_path, log_fp):
        mkdir_p(outdir)
        mkdir_p(tempdir)

        eng_dic_maker.make_dic(engdic, code, thisdir)
        tankan_dic_maker.make_dic(code, cs_file, thisdir)
        custom_dic_maker.make_dic(code, thisdir)

        files = [
            "dicrc",
            "nvdajp-eng-dic.csv",
            "nvdajp-tankan-dic.csv",
            "nvdajp-custom-dic.csv",
        ]

        euc_files = [
            "char.def",
            "feature.def",
            "left-id.def",
            "matrix.def",
            "pos-id.def",
            "rewrite.def",
            "right-id.def",
            "unk.def",
        ]

        jdic_file = "naist-jdic.csv"

        for f in files:
            print("copy %s to %s" % (path.join(thisdir, f), tempdir))
            shutil.copy(path.join(thisdir, f), tempdir)

        for f in euc_files:
            convert_file(path.join(thisdir, f), "euc-jp", path.join(tempdir, f), code)

        convert_file(
            path.join(thisdir, jdic_file),
            "euc-jp",
            path.join(tempdir, jdic_file),
            code,
            apply_filter=True,
        )

        print(tempdir, [mecab_dict_index, "-d", ".", "-o", outdir, "-f", code, "-c", code])
        # In console mode (log_fp is None), don't set stdout/stderr to preserve default console output
        # In file mode (log_fp is set), redirect both stdout and stderr to the log file
        run_kwargs = {
            "cwd": tempdir,
            "text": True,
        }
        if log_fp:
            run_kwargs["stdout"] = log_fp
            run_kwargs["stderr"] = subprocess.STDOUT
        result = subprocess.run(
            [mecab_dict_index, "-d", ".", "-o", outdir, "-f", code, "-c", code],
            **run_kwargs,
        )
        if result.returncode != 0:
            raise SystemExit(result.returncode)

        print("copy %s to %s" % (path.join(thisdir, "dicrc"), outdir))
        shutil.copy(path.join(thisdir, "dicrc"), outdir)
        dic_version_file = path.join(outdir, "DIC_VERSION")
        print("dic version file: " + dic_version_file)
        version = f"nvdajp-jtalk-dic ({code}) {datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
        print(version)
        with open_file(dic_version_file, "w", "utf-8") as f:
            f.write(version + os.linesep)

    if mode == "file" and log_path:
        print(f"make_jdic: output suppressed; see {log_path}")


if __name__ == "__main__":
    _main()
