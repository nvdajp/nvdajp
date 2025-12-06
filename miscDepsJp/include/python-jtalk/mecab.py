# coding: UTF-8
# mecab.py for python-jtalk

CODE = "utf-8"

import os
import re
import threading
from ctypes import *

try:
    from ._nvdajp_spellchar import convert as convertSpellChar
    from .roma2kana import getKanaFromRoma
    from .text2mecab import text2mecab
except (ImportError, ValueError):
    from _nvdajp_spellchar import convert as convertSpellChar  # type: ignore
    from roma2kana import getKanaFromRoma  # type: ignore
    from text2mecab import text2mecab  # type: ignore

c_double_p = POINTER(c_double)
c_double_p_p = POINTER(c_double_p)
c_short_p = POINTER(c_short)
c_char_p_p = POINTER(c_char_p)

##############################################

# http://mecab.sourceforge.net/libmecab.html
# c:/mecab/sdk/mecab.h
MECAB_NOR_NODE = 0
MECAB_UNK_NODE = 1
MECAB_BOS_NODE = 2
MECAB_EOS_NODE = 3


class mecab_token_t(Structure):
    pass


mecab_token_t_ptr = POINTER(mecab_token_t)


class mecab_path_t(Structure):
    pass


mecab_path_t_ptr = POINTER(mecab_path_t)


class mecab_node_t(Structure):
    pass


mecab_node_t_ptr = POINTER(mecab_node_t)
mecab_node_t_ptr_ptr = POINTER(mecab_node_t_ptr)
mecab_node_t._fields_ = [
    ("prev", mecab_node_t_ptr),
    ("next", mecab_node_t_ptr),
    ("enext", mecab_node_t_ptr),
    ("bnext", mecab_node_t_ptr),
    ("rpath", mecab_path_t_ptr),
    ("lpath", mecab_path_t_ptr),
    ("surface", c_char_p),
    ("feature", c_char_p),
    ("id", c_uint),
    ("length", c_ushort),
    ("rlength", c_ushort),
    ("rcAttr", c_ushort),
    ("lcAttr", c_ushort),
    ("posid", c_ushort),
    ("char_type", c_ubyte),
    ("stat", c_ubyte),
    ("isbest", c_ubyte),
    ("alpha", c_float),
    ("beta", c_float),
    ("prob", c_float),
    ("wcost", c_short),
    ("cost", c_long),
]

############################################

FELEN = 2000  # string len
FECOUNT = 1000
FEATURE = c_char * FELEN
FEATURE_ptr = POINTER(FEATURE)
FEATURE_ptr_array = FEATURE_ptr * FECOUNT
FEATURE_ptr_array_ptr = POINTER(FEATURE_ptr_array)

mecab = None
libmc = None
lock = threading.Lock()

mc_malloc = cdll.msvcrt.malloc
mc_malloc.restype = POINTER(c_ubyte)
mc_calloc = cdll.msvcrt.calloc
mc_calloc.restype = POINTER(c_ubyte)
mc_free = cdll.msvcrt.free


class NonblockingMecabFeatures(object):
    def __init__(self):
        self.size = 0
        self.feature = FEATURE_ptr_array()
        for i in range(0, FECOUNT):
            buf = mc_malloc(FELEN)
            self.feature[i] = cast(buf, FEATURE_ptr)

    def __del__(self):
        for i in range(0, FECOUNT):
            try:
                mc_free(self.feature[i])
            except:
                pass


class MecabFeatures(NonblockingMecabFeatures):
    def __init__(self):
        global lock
        lock.acquire()
        super(MecabFeatures, self).__init__()

    def __del__(self):
        global lock
        super(MecabFeatures, self).__del__()
        lock.release()


def Mecab_initialize(logwrite_=None, libmecab_dir=None, dic=None, user_dics=None):
    mecab_dll = os.path.join(libmecab_dir, "libmecab.dll")
    global libmc
    if libmc is None:
        libmc = cdll.LoadLibrary(mecab_dll)
        libmc.mecab_version.restype = c_char_p
        libmc.mecab_strerror.restype = c_char_p
        libmc.mecab_sparse_tonode.restype = mecab_node_t_ptr
        libmc.mecab_new.argtypes = [c_int, c_char_p_p]
    global mecab
    if mecab is None:
        if logwrite_:
            logwrite_("dic: %s" % dic)
        try:
            f = open(os.path.join(dic, "DIC_VERSION"))
            s = f.read().strip()
            f.close()
            logwrite_("mecab:" + libmc.mecab_version() + " " + s)
            # check utf-8 dictionary
            if not CODE in s:
                raise RuntimeError("utf-8 dictionary for mecab required.")
        except:
            pass
        mecabrc = os.path.join(libmecab_dir, "mecabrc")
        argc, args = 5, (c_char_p * 5)(
            b"mecab", b"-d", dic.encode("utf-8"), b"-r", mecabrc.encode("utf-8")
        )
        if user_dics:
            # ignore item which contains comma
            ud = ",".join([s for s in user_dics if not "," in s])
            if logwrite_:
                logwrite_("user_dics: %s" % ud)
            argc, args = 7, (c_char_p * 7)(
                b"mecab",
                b"-d",
                dic.encode("utf-8"),
                b"-r",
                mecabrc.encode("utf-8"),
                b"-u",
                ud.encode("utf-8"),
            )
        mecab = libmc.mecab_new(argc, args)
        if logwrite_:
            if not mecab:
                logwrite_("mecab_new failed.")
            s = libmc.mecab_strerror(mecab).strip()
            if s:
                logwrite_(s)


def Mecab_analysis(src, features, logwrite_=None):
    if not src:
        if logwrite_:
            logwrite_("src empty")
        features.size = 0
        return
    head = libmc.mecab_sparse_tonode(mecab, src)
    if head is None:
        if logwrite_:
            logwrite_("mecab_sparse_tonode result empty")
        features.size = 0
        return
    features.size = 0

    # make array of features
    node = head
    i = 0
    while node:
        s = node[0].stat
        if s != MECAB_BOS_NODE and s != MECAB_EOS_NODE:
            c = node[0].length
            s = string_at(node[0].surface, c) + b"," + string_at(node[0].feature)
            if logwrite_:
                logwrite_(s.decode(CODE, "ignore"))
            buf = create_string_buffer(s)
            dst_ptr = features.feature[i]
            src_ptr = byref(buf)
            memmove(dst_ptr, src_ptr, len(s) + 1)
            i += 1
        node = node[0].next
        features.size = i
        if i >= FECOUNT:
            if logwrite_:
                logwrite_("too many nodes")
            return
    return


# for debug
def Mecab_print(mf, logwrite_=None, CODE_=CODE, output_header=True):
    if logwrite_ is None:
        return
    feature = mf.feature
    size = mf.size
    if feature is None or size is None:
        if output_header:
            logwrite_("Mecab_print size: 0")
        return
    s2 = ""
    if output_header:
        s2 += "Mecab_print size: %d\n" % size
    for i in range(0, size):
        s = string_at(feature[i])
        if s:
            if CODE_ is None:
                s2 += "%d %s\n" % (i, s)
            else:
                s2 += "%d %s\n" % (i, s.decode(CODE_, "ignore"))
        else:
            s2 += "[None]\n"
    logwrite_(s2)


def Mecab_getFeature(mf, pos, CODE_=CODE):
    s = string_at(mf.feature[pos])
    return s.decode(CODE_, "ignore")


def Mecab_setFeature(mf, pos, s, CODE_=CODE):
    s = s.encode(CODE_, "ignore")
    buf = create_string_buffer(s)
    dst_ptr = mf.feature[pos]
    src_ptr = byref(buf)
    memmove(dst_ptr, src_ptr, len(s) + 1)


def getMoraCount(s):
    # 1/3 => 3
    # */* => 0
    m = s.split("/")
    if len(m) == 2:
        m2 = m[1]
        if m2 != "*":
            return int(m2)
    return 0


RE_FULLSHAPE_ALPHA = re.compile("^[Ａ-Ｚａ-ｚ]+$")


def _shouldWorkAroundLatinWordPostfix(ar3, ar2, ar):
    return (
        (not (ar3 and ar3[0] == "\u3000" and ar2 and ar2[0] == "’"))
        and ar2
        and ar[0] in ("ｓ", "ｄ", "ｅｄ", "ｒ", "ｔｉｎｇ", "ｔ")
    )


def _makeFeatureFromLatinWordAndPostfix(org, ar, symbol=""):
    _hyoki = ar[0]
    _yomi = ar[8] if len(ar) > 8 else convertSpellChar(_hyoki).replace(" ", "")
    _pron = ar[9] if len(ar) > 9 else convertSpellChar(_hyoki).replace(" ", "")
    hin1 = ar[1]
    hin2 = ar[2]
    hin3 = ar[3]
    postfix = ""
    if org == "ｓ":
        postfix = "ズ"
        if _hyoki.endswith("ｐ") or _hyoki.endswith("ｋｅ") or _hyoki.endswith("ｒｋ"):
            postfix = "ス"
        elif _hyoki.endswith("ｔｈａｔ"):
            # that's ザットゥズ -> ザッツ
            postfix = "ツ"
            _yomi = _yomi[:-2]
            _pron = _pron[:-2]
        elif _hyoki.endswith("ｗｏｒｄ"):
            # https://github.com/nvdajp/nvdajpmiscdep/issues/53
            # words ワードズ -> ワーズ
            postfix = "ズ"
            _yomi = _yomi[:-1]
            _pron = _pron[:-1]
    elif org == "ｔ":
        postfix = "ト"
    elif org in ("ｄ", "ｅｄ"):
        if _hyoki.endswith("ｔｅ") and _yomi.endswith("ト"):
            # update アップデート -> updated アップデーティド
            postfix = "ティド"
            _yomi = _yomi[:-1]
            _pron = _pron[:-1]
        else:
            postfix = "ド"
    elif org == "ｒ":
        postfix = "ア"
        if _hyoki.endswith("ｓｅ"):
            postfix = "ザー"
            _yomi = _yomi[:-1]
            _pron = _pron[:-1]
    elif _hyoki.endswith("ｔ") and _yomi.endswith("ト") and org == "ｔｉｎｇ":
        postfix = "ティング"
        _yomi = _yomi[:-1]
        _pron = _pron[:-1]
    hyoki = _hyoki + symbol + org
    yomi = _yomi + postfix
    pron = _pron + postfix
    mora = getMoraCount(ar[10]) + 1 if len(ar) > 10 else len(pron)
    feature = "{h},{h1},{h2},{h3},*,*,*,{h},{y},{p},0/{m},C0".format(
        h=hyoki, h1=hin1, h2=hin2, h3=hin3, y=yomi, p=pron, m=mora
    )
    return feature


def _makeBraillePatternReading(s):
    n = ord(s) - 0x2800
    if n == 0:
        return "マスアケ"
    ar = []
    if n & 0x01:
        ar.append("イチ")
    if n & 0x02:
        ar.append("ニー")
    if n & 0x04:
        ar.append("サン")
    if n & 0x08:
        ar.append("ヨン")
    if n & 0x10:
        ar.append("ゴー")
    if n & 0x20:
        ar.append("ロク")
    if n & 0x40:
        ar.append("ナナ")
    if n & 0x80:
        ar.append("ハチ")
    return "".join(ar) + "ノテン"


def Mecab_correctFeatures(mf, CODE_=CODE):
    for pos in range(0, mf.size):
        ar = Mecab_getFeature(mf, pos, CODE_=CODE_).split(",")
        if pos >= 1:
            ar2 = Mecab_getFeature(mf, pos - 1, CODE_=CODE_).split(",")
        else:
            ar2 = None
        if pos >= 2:
            ar3 = Mecab_getFeature(mf, pos - 2, CODE_=CODE_).split(",")
        else:
            ar3 = None
        if (
            ar3
            and ar2
            and RE_FULLSHAPE_ALPHA.match(ar3[0])
            and RE_FULLSHAPE_ALPHA.match(ar2[0])
            and RE_FULLSHAPE_ALPHA.match(ar[0])
        ):
            # nvdajp/nvdajpmiscdep#28
            # before:
            # 0 ｓ,記号,アルファベット,*,*,*,*,ｓ,エス,エス,1/2,*
            # 1 ａｔｏｋ,名詞,一般,*,*,*,*,ａｔｏｋ,エイトック,エイトック,0/5,C0
            # 2 ｏ,記号,アルファベット,*,*,*,*,ｏ,オー,オー,1/2,*
            # after:
            # 0 ,,,*,*,*,*
            # 1 ,,,*,*,*,*
            # 2 ｓａｔｏｋｏ,名詞,固有名詞,*,*,*,*,ｓａｔｏｋｏ,サトコ,サトコ,0/3,C0
            hyoki = ar3[0] + ar2[0] + ar[0]
            hin1 = "名詞"
            hin2 = "固有名詞"
            yomi = getKanaFromRoma(hyoki)
            if yomi:
                pron = yomi
                mora = len(yomi)
                feature = "{h},{h1},{h2},*,*,*,*,{h},{y},{p},0/{m},C0".format(
                    h=hyoki, h1=hin1, h2=hin2, y=yomi, p=pron, m=mora
                )
                Mecab_setFeature(mf, pos - 2, ",,,*,*,*,*", CODE_=CODE_)
                Mecab_setFeature(mf, pos - 1, ",,,*,*,*,*", CODE_=CODE_)
                Mecab_setFeature(mf, pos, feature, CODE_=CODE_)
        elif (ar[2] == "数" and ar[7] == "*") or (
            ar[1] == "名詞" and ar[2] == "サ変接続" and ar[7] == "*"
        ):
            # PATTERN 1
            # before:
            # 1 五絡脈病証,名詞,数,*,*,*,*,*
            #
            # after:
            # 1 五絡脈病証,名詞,普通名詞,*,*,*,*,五絡脈病証,ゴミャクラクビョウショウ,
            # ゴミャクラクビョーショー,1/9,C0
            #
            # PATTERN 2
            # before:
            # 0 ∫⣿♪　,名詞,サ変接続,*,*,*,*,*
            #
            # after:
            # 0 ∫⣿♪　,名詞,サ変接続,*,*,*,*,∫♪　,セキブンキゴーイチニーサンヨンゴーロクナナ
            # ハチノテンオンプ,セキブンキゴーイチニーサンヨンゴーロクナナハチノテンオンプ,1/29,C0
            #
            hyoki = ar[0]
            yomi = ""
            pron = ""
            mora = 0
            nbmf = NonblockingMecabFeatures()
            for c in hyoki:
                Mecab_analysis(text2mecab(c, CODE_=CODE_), nbmf)
                for pos2 in range(0, nbmf.size):
                    ar2 = Mecab_getFeature(nbmf, pos2, CODE_=CODE_).split(",")
                    if len(ar2) > 10:
                        yomi += ar2[8]
                        pron += ar2[9]
                        mora += getMoraCount(ar2[10])
            nbmf = None
            feature = "{h},名詞,普通名詞,*,*,*,*,{h},{y},{p},0/{m},C0".format(
                h=hyoki, y=yomi, p=pron, m=mora
            )
            Mecab_setFeature(mf, pos, feature, CODE_=CODE_)
        elif ar2 and ar[0] == "ー" and ar[1] == "名詞" and ar[2] == "一般":
            # PATTERN 3
            # before:
            # 0 ま,接頭詞,名詞接続,*,*,*,*,ま,マ,マ,1/1,P2
            # 1 ー,名詞,一般,*,*,*,*,*
            #
            # after:
            # 0 ま,接頭詞,名詞接続,*,*,*,*,まー,マー,マー,1/2,P2
            # 1 ー,名詞,一般,*,*,*,*,*
            #
            if len(ar2) > 10:
                hyoki = ar2[0] + "ー"
                hin1 = ar2[1]
                hin2 = ar2[2]
                yomi = ar2[8] + "ー"
                pron = ar2[9] + "ー"
                mora = getMoraCount(ar2[10]) + 1
                feature = "{h},{h1},{h2},*,*,*,*,{h},{y},{p},0/{m},C0".format(
                    h=hyoki, h1=hin1, h2=hin2, y=yomi, p=pron, m=mora
                )
                Mecab_setFeature(mf, pos - 1, feature, CODE_=CODE_)
            elif ar3 and len(ar3) > 10 and ar3[1] != "記号":
                hyoki = ar3[0] + ar2[0] + "ー"
                hin1 = ar3[1]
                hin2 = ar3[2]
                yomi = ar3[8] + ar2[0] + "ー"
                pron = ar3[9] + ar2[0] + "ー"
                mora = getMoraCount(ar3[10]) + len(ar2[0]) + 1
                feature = "{h},{h1},{h2},*,*,*,*,{h},{y},{p},0/{m},C0".format(
                    h=hyoki, h1=hin1, h2=hin2, y=yomi, p=pron, m=mora
                )
                Mecab_setFeature(mf, pos - 2, feature, CODE_=CODE_)
        elif _shouldWorkAroundLatinWordPostfix(ar3, ar2, ar):
            # https://github.com/nvdajp/nvdajpmiscdep/issues/42
            # print ((unicode(ar3[0]) if ar3 else '*') + '/' + (unicode(ar2[0]) if ar2 else '*') + '/' + (unicode(ar[0]) if ar else '*')).encode('utf-8')
            # pattern 5
            if ar3 and ar2[0] in ("'", "’"):
                # PATTERN 5 "author's"
                # before:
                # 0 ａｕｔｈｏｒ,名詞,一般,*,*,*,*,ａｕｔｈｏｒ,オーサー,オーサー,1/4,C0
                # 1 ’,記号,括弧閉,*,*,*,*,’,’,’,*/*,*
                # 2 ｓ,記号,アルファベット,*,*,*,*,ｓ,エス,エス,1/2,*
                #
                # after:
                # 0 ,,,*,*,*,*
                # 1 ,,,*,*,*,*
                # 2 ａｕｔｈｏｒｓ,名詞,一般,*,*,*,*,ｓ,オーサーズ,オーサーズ,1/5,C0
                Mecab_setFeature(mf, pos - 2, ",,,*,*,*,*", CODE_=CODE_)
                Mecab_setFeature(mf, pos - 1, ",,,*,*,*,*", CODE_=CODE_)
                f = _makeFeatureFromLatinWordAndPostfix(ar[0], ar3, symbol="'")
                Mecab_setFeature(mf, pos, f, CODE_=CODE_)
            elif len(ar2) > 10 and RE_FULLSHAPE_ALPHA.match(ar2[0]) and len(ar2[0]) > 1:
                # PATTERN 4
                # before:
                # 0 ｔａｋｅ,名詞,一般,*,*,*,*,ｔａｋｅ,テイク,テイク,1/3,C0
                # 1 ｓ,記号,アルファベット,*,*,*,*,ｓ,エス,エス,1/2,*
                #
                # after:
                # 0 ,,,*,*,*,*
                # 1 ｔａｋｅｓ,名詞,一般,*,*,*,*,ｔａｋｅ,テイクス,テイクス,1/4,C0
                Mecab_setFeature(mf, pos - 1, ",,,*,*,*,*", CODE_=CODE_)
                f = _makeFeatureFromLatinWordAndPostfix(ar[0], ar2)
                Mecab_setFeature(mf, pos, f, CODE_=CODE_)
        elif (
            ar2 and RE_FULLSHAPE_ALPHA.match(ar[0]) and RE_FULLSHAPE_ALPHA.match(ar2[0])
        ):
            # and not (len(ar2) > 10 and ar2[10] and ar2[10][0] == '0' and len(ar) > 10 and ar[10] and ar[10][0] == '0'):
            # 0 ｓｈｉ,名詞,一般,*,*,*,*,ｓｈｉ,シ,シ,1/1,C0
            # 1 ｍａｎｅ,名詞,一般,*,*,*,*,ｍａｎｅ,メイン,メイン,1/3,C0
            #
            # 0 ｋｉｔ,名詞,一般,*,*,*,*,ｋｉｔ,キットゥ,キットゥ,1/4,C0
            # 1 ａ,記号,アルファベット,*,*,*,*,ａ,エイ,エイ,1/2,*
            #
            # https://github.com/nvdajp/nvdajpmiscdep/issues/58
            # 英単語を0型アクセントで登録しているので、0型同士の場合は元の読みを使用する
            #
            hyoki = ar2[0] + ar[0]
            hin1 = "名詞"
            hin2 = "固有名詞"
            yomi = getKanaFromRoma(hyoki)
            if yomi:
                pron = yomi
                mora = len(yomi)
                feature = "{h},{h1},{h2},*,*,*,*,{h},{y},{p},0/{m},C0".format(
                    h=hyoki, h1=hin1, h2=hin2, y=yomi, p=pron, m=mora
                )
                Mecab_setFeature(mf, pos - 1, ",,,*,*,*,*", CODE_=CODE_)
                Mecab_setFeature(mf, pos, feature, CODE_=CODE_)
        elif RE_FULLSHAPE_ALPHA.match(ar[0]) and ar[7] == "*":
            roma = ar[0]
            kana = getKanaFromRoma(roma)
            if kana:
                c = len(kana)
                Mecab_setFeature(
                    mf,
                    pos,
                    "%s,名詞,固有名詞,*,*,*,*,%s,%s,%s,0/%d,C0" % (roma, roma, kana, kana, c),
                    CODE_=CODE_,
                )
        elif len(ar[0]) == 1 and 0x2800 <= ord(ar[0]) <= 0x28FF:
            ar[8] = ar[9] = _makeBraillePatternReading(ar[0])
            Mecab_setFeature(mf, pos, ",".join(ar), CODE_=CODE_)


def Mecab_utf8_to_cp932(mf):
    for pos in range(0, mf.size):
        s = Mecab_getFeature(mf, pos, CODE_="utf-8")
        Mecab_setFeature(mf, pos, s, CODE_="cp932")


def Mecab_duplicateFeatures(mf, startPos=0, stopPos=None, CODE_="utf-8"):
    if not stopPos:
        stopPos = mf.size
    nbmf = NonblockingMecabFeatures()
    newPos = 0
    for pos in range(startPos, stopPos):
        s = Mecab_getFeature(mf, pos, CODE_)
        Mecab_setFeature(nbmf, newPos, s, CODE_)
        newPos += 1
    nbmf.size = newPos
    return nbmf


def Mecab_splitFeatures(mf, CODE_="utf-8"):
    ar = []
    startPos = 0
    for pos in range(mf.size):
        a = Mecab_getFeature(mf, pos, CODE_).split(",")
        if a[0].isspace() or a[1] == "記号" and a[2] in ("空白", "句点", "読点"):
            f = Mecab_duplicateFeatures(mf, startPos, pos + 1, CODE_)
            ar.append(f)
            startPos = pos + 1
    if startPos < mf.size:
        f = Mecab_duplicateFeatures(mf, startPos, mf.size, CODE_)
        ar.append(f)
    return ar
