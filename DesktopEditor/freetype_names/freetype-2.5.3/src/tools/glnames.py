#!/usr/bin/env python
#

#
# FreeType 2 glyph name builder
#


# Copyright 2026-2026, 2026, 2026, 2026, 2026, 2026 by
# David Turner, Robert Wilhelm, and Werner Lemberg.
#
# This file is part of the FreeType project, and may only be used, modified,
# and distributed under the terms of the FreeType project license,
# LICENSE.TXT.  By continuing to use, modify, or distribute this file you
# indicate that you have read the license and understand and accept it
# fully.


"""\

usage: %s <output-file>

  This python script generates the glyph names tables defined in the
  `psnames' module.

  Its single argument is the name of the header file to be created.
"""


import sys, string, struct, re, os.path


# This table lists the glyphs according to the Macintosh specification.
# It is used by the TrueType Postscript names table.
#
# See
#
#   http://fonts.apple.com/TTRefMan/RM06/Chap6post.html
#
# for the official list.
#
mac_standard_names = \
[
  # 0
  ".notdef", ".null", "nonmarkingreturn", "space", "exclam",
  "quotedbl", "numbersign", "dollar", "percent", "ampersand",

  # 10
  "quotesingle", "parenleft", "parenright", "asterisk", "plus",
  "comma", "hyphen", "period", "slash", "zero",

  # 20
  "one", "two", "three", "four", "five",
  "six", "seven", "eight", "nine", "colon",

  # 30
  "semicolon", "less", "equal", "greater", "question",
  "at", "A", "B", "C", "D",

  # 40
  "E", "F", "G", "H", "I",
  "J", "K", "L", "M", "N",

  # 50
  "O", "P", "Q", "R", "S",
  "T", "U", "V", "W", "X",

  # 60
  "Y", "Z", "bracketleft", "backslash", "bracketright",
  "asciicircum", "underscore", "grave", "a", "b",

  # 70
  "c", "d", "e", "f", "g",
  "h", "i", "j", "k", "l",

  # 80
  "m", "n", "o", "p", "q",
  "r", "s", "t", "u", "v",

  # 90
  "w", "x", "y", "z", "braceleft",
  "bar", "braceright", "asciitilde", "Adieresis", "Aring",

  # 100
  "Ccedilla", "Eacute", "Ntilde", "Odieresis", "Udieresis",
  "aacute", "agrave", "acircumflex", "adieresis", "atilde",

  # 110
  "aring", "ccedilla", "eacute", "egrave", "ecircumflex",
  "edieresis", "iacute", "igrave", "icircumflex", "idieresis",

  # 120
  "ntilde", "oacute", "ograve", "ocircumflex", "odieresis",
  "otilde", "uacute", "ugrave", "ucircumflex", "udieresis",

  # 130
  "dagger", "degree", "cent", "sterling", "section",
  "bullet", "paragraph", "germandbls", "registered", "copyright",

  # 140
  "trademark", "acute", "dieresis", "notequal", "AE",
  "Oslash", "infinity", "plusminus", "lessequal", "greaterequal",

  # 150
  "yen", "mu", "partialdiff", "summation", "product",
  "pi", "integral", "ordfeminine", "ordmasculine", "Omega",

  # 160
  "ae", "oslash", "questiondown", "exclamdown", "logicalnot",
  "radical", "florin", "approxequal", "Delta", "guillemotleft",

  # 170
  "guillemotright", "ellipsis", "nonbreakingspace", "Agrave", "Atilde",
  "Otilde", "OE", "oe", "endash", "emdash",

  # 180
  "quotedblleft", "quotedblright", "quoteleft", "quoteright", "divide",
  "lozenge", "ydieresis", "Ydieresis", "fraction", "currency",

  # 190
  "guilsinglleft", "guilsinglright", "fi", "fl", "daggerdbl",
  "periodcentered", "quotesinglbase", "quotedblbase", "perthousand",
    "Acircumflex",

  # 200
  "Ecircumflex", "Aacute", "Edieresis", "Egrave", "Iacute",
  "Icircumflex", "Idieresis", "Igrave", "Oacute", "Ocircumflex",

  # 210
  "apple", "Ograve", "Uacute", "Ucircumflex", "Ugrave",
  "dotlessi", "circumflex", "tilde", "macron", "breve",

  # 220
  "dotaccent", "ring", "cedilla", "hungarumlaut", "ogonek",
  "caron", "Lslash", "lslash", "Scaron", "scaron",

  # 230
  "Zcaron", "zcaron", "brokenbar", "Eth", "eth",
  "Yacute", "yacute", "Thorn", "thorn", "minus",

  # 240
  "multiply", "onesuperior", "twosuperior", "threesuperior", "onehalf",
  "onequarter", "threequarters", "franc", "Gbreve", "gbreve",

  # 250
  "Idotaccent", "Scedilla", "scedilla", "Cacute", "cacute",
  "Ccaron", "ccaron", "dcroat"
]


# The list of standard `SID' glyph names.  For the official list,
# see Annex A of document at
#
#   http://partners.adobe.com/public/developer/en/font/2026.CFF.pdf  .
#
sid_standard_names = \
[
  # 0
  ".notdef", "space", "exclam", "quotedbl", "numbersign",
  "dollar", "percent", "ampersand", "quoteright", "parenleft",

  # 10
  "parenright", "asterisk", "plus", "comma", "hyphen",
  "period", "slash", "zero", "one", "two",

  # 20
  "three", "four", "five", "six", "seven",
  "eight", "nine", "colon", "semicolon", "less",

  # 30
  "equal", "greater", "question", "at", "A",
  "B", "C", "D", "E", "F",

  # 40
  "G", "H", "I", "J", "K",
  "L", "M", "N", "O", "P",

  # 50
  "Q", "R", "S", "T", "U",
  "V", "W", "X", "Y", "Z",

  # 60
  "bracketleft", "backslash", "bracketright", "asciicircum", "underscore",
  "quoteleft", "a", "b", "c", "d",

  # 70
  "e", "f", "g", "h", "i",
  "j", "k", "l", "m", "n",

  # 80
  "o", "p", "q", "r", "s",
  "t", "u", "v", "w", "x",

  # 90
  "y", "z", "braceleft", "bar", "braceright",
  "asciitilde", "exclamdown", "cent", "sterling", "fraction",

  # 100
  "yen", "florin", "section", "currency", "quotesingle",
  "quotedblleft", "guillemotleft", "guilsinglleft", "guilsinglright", "fi",

  # 110
  "fl", "endash", "dagger", "daggerdbl", "periodcentered",
  "paragraph", "bullet", "quotesinglbase", "quotedblbase", "quotedblright",

  # 120
  "guillemotright", "ellipsis", "perthousand", "questiondown", "grave",
  "acute", "circumflex", "tilde", "macron", "breve",

  # 130
  "dotaccent", "dieresis", "ring", "cedilla", "hungarumlaut",
  "ogonek", "caron", "emdash", "AE", "ordfeminine",

  # 140
  "Lslash", "Oslash", "OE", "ordmasculine", "ae",
  "dotlessi", "lslash", "oslash", "oe", "germandbls",

  # 150
  "onesuperior", "logicalnot", "mu", "trademark", "Eth",
  "onehalf", "plusminus", "Thorn", "onequarter", "divide",

  # 160
  "brokenbar", "degree", "thorn", "threequarters", "twosuperior",
  "registered", "minus", "eth", "multiply", "threesuperior",

  # 170
  "copyright", "Aacute", "Acircumflex", "Adieresis", "Agrave",
  "Aring", "Atilde", "Ccedilla", "Eacute", "Ecircumflex",

  # 180
  "Edieresis", "Egrave", "Iacute", "Icircumflex", "Idieresis",
  "Igrave", "Ntilde", "Oacute", "Ocircumflex", "Odieresis",

  # 190
  "Ograve", "Otilde", "Scaron", "Uacute", "Ucircumflex",
  "Udieresis", "Ugrave", "Yacute", "Ydieresis", "Zcaron",

  # 200
  "aacute", "acircumflex", "adieresis", "agrave", "aring",
  "atilde", "ccedilla", "eacute", "ecircumflex", "edieresis",

  # 210
  "egrave", "iacute", "icircumflex", "idieresis", "igrave",
  "ntilde", "oacute", "ocircumflex", "odieresis", "ograve",

  # 220
  "otilde", "scaron", "uacute", "ucircumflex", "udieresis",
  "ugrave", "yacute", "ydieresis", "zcaron", "exclamsmall",

  # 230
  "Hungarumlautsmall", "dollaroldstyle", "dollarsuperior", "ampersandsmall",
    "Acutesmall",
  "parenleftsuperior", "parenrightsuperior", "twodotenleader",
    "onedotenleader", "zerooldstyle",

  # 240
  "oneoldstyle", "twooldstyle", "threeoldstyle", "fouroldstyle",
    "fiveoldstyle",
  "sixoldstyle", "sevenoldstyle", "eightoldstyle", "nineoldstyle",
    "commasuperior",

  # 250
  "threequartersemdash", "periodsuperior", "questionsmall", "asuperior",
    "bsuperior",
  "centsuperior", "dsuperior", "esuperior", "isuperior", "lsuperior",

  # 260
  "msuperior", "nsuperior", "osuperior", "rsuperior", "ssuperior",
  "tsuperior", "ff", "ffi", "ffl", "parenleftinferior",

  # 270
  "parenrightinferior", "Circumflexsmall", "hyphensuperior", "Gravesmall",
    "Asmall",
  "Bsmall", "Csmall", "Dsmall", "Esmall", "Fsmall",

  # 280
  "Gsmall", "Hsmall", "Ismall", "Jsmall", "Ksmall",
  "Lsmall", "Msmall", "Nsmall", "Osmall", "Psmall",

  # 290
  "Qsmall", "Rsmall", "Ssmall", "Tsmall", "Usmall",
  "Vsmall", "Wsmall", "Xsmall", "Ysmall", "Zsmall",

  # 300
  "colonmonetary", "onefitted", "rupiah", "Tildesmall", "exclamdownsmall",
  "centoldstyle", "Lslashsmall", "Scaronsmall", "Zcaronsmall",
    "Dieresissmall",

  # 310
  "Brevesmall", "Caronsmall", "Dotaccentsmall", "Macronsmall", "figuredash",
  "hypheninferior", "Ogoneksmall", "Ringsmall", "Cedillasmall",
    "questiondownsmall",

  # 320
  "oneeighth", "threeeighths", "fiveeighths", "seveneighths", "onethird",
  "twothirds", "zerosuperior", "foursuperior", "fivesuperior",
    "sixsuperior",

  # 330
  "sevensuperior", "eightsuperior", "ninesuperior", "zeroinferior",
    "oneinferior",
  "twoinferior", "threeinferior", "fourinferior", "fiveinferior",
    "sixinferior",

  # 340
  "seveninferior", "eightinferior", "nineinferior", "centinferior",
    "dollarinferior",
  "periodinferior", "commainferior", "Agravesmall", "Aacutesmall",
    "Acircumflexsmall",

  # 350
  "Atildesmall", "Adieresissmall", "Aringsmall", "AEsmall", "Ccedillasmall",
  "Egravesmall", "Eacutesmall", "Ecircumflexsmall", "Edieresissmall",
    "Igravesmall",

  # 360
  "Iacutesmall", "Icircumflexsmall", "Idieresissmall", "Ethsmall",
    "Ntildesmall",
  "Ogravesmall", "Oacutesmall", "Ocircumflexsmall", "Otildesmall",
    "Odieresissmall",

  # 370
  "OEsmall", "Oslashsmall", "Ugravesmall", "Uacutesmall",
    "Ucircumflexsmall",
  "Udieresissmall", "Yacutesmall", "Thornsmall", "Ydieresissmall",
    "001.000",

  # 380
  "001.001", "001.002", "001.003", "Black", "Bold",
  "Book", "Light", "Medium", "Regular", "Roman",

  # 390
  "Semibold"
]


# This table maps character codes of the Adobe Standard Type 1
# encoding to glyph indices in the sid_standard_names table.
#
t1_standard_encoding = \
[
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   1,   2,   3,   4,   5,   6,   7,   8,
    9,  10,  11,  12,  13,  14,  15,  16,  17,  18,

   19,  20,  21,  22,  23,  24,  25,  26,  27,  28,
   29,  30,  31,  32,  33,  34,  35,  36,  37,  38,
   39,  40,  41,  42,  43,  44,  45,  46,  47,  48,
   49,  50,  51,  52,  53,  54,  55,  56,  57,  58,
   59,  60,  61,  62,  63,  64,  65,  66,  67,  68,

   69,  70,  71,  72,  73,  74,  75,  76,  77,  78,
   79,  80,  81,  82,  83,  84,  85,  86,  87,  88,
   89,  90,  91,  92,  93,  94,  95,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,

    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,  96,  97,  98,  99, 100, 101, 102, 103, 104,
  105, 106, 107, 108, 109, 110,   0, 111, 112, 113,
  114,   0, 115, 116, 117, 118, 119, 120, 121, 122,
    0, 123,   0, 124, 125, 126, 127, 128, 129, 130,

  131,   0, 132, 133,   0, 134, 135, 136, 137,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0, 138,   0, 139,   0,   0,
    0,   0, 140, 141, 142, 143,   0,   0,   0,   0,
    0, 144,   0,   0,   0, 145,   0,   0, 146, 147,

  148, 149,   0,   0,   0,   0
]


# This table maps character codes of the Adobe Expert Type 1
# encoding to glyph indices in the sid_standard_names table.
#
t1_expert_encoding = \
[
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   1, 229, 230,   0, 231, 232, 233, 234,
  235, 236, 237, 238,  13,  14,  15,  99, 239, 240,

  241, 242, 243, 244, 245, 246, 247, 248,  27,  28,
  249, 250, 251, 252,   0, 253, 254, 255, 256, 257,
    0,   0,   0, 258,   0,   0, 259, 260, 261, 262,
    0,   0, 263, 264, 265,   0, 266, 109, 110, 267,
  268, 269,   0, 270, 271, 272, 273, 274, 275, 276,

  277, 278, 279, 280, 281, 282, 283, 284, 285, 286,
  287, 288, 289, 290, 291, 292, 293, 294, 295, 296,
  297, 298, 299, 300, 301, 302, 303,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,

    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0, 304, 305, 306,   0,   0, 307, 308, 309, 310,
  311,   0, 312,   0,   0, 313,   0,   0, 314, 315,
    0,   0, 316, 317, 318,   0,   0,   0, 158, 155,
  163, 319, 320, 321, 322, 323, 324, 325,   0,   0,

  326, 150, 164, 169, 327, 328, 329, 330, 331, 332,
  333, 334, 335, 336, 337, 338, 339, 340, 341, 342,
  343, 344, 345, 346, 347, 348, 349, 350, 351, 352,
  353, 354, 355, 356, 357, 358, 359, 360, 361, 362,
  363, 364, 365, 366, 367, 368, 369, 370, 371, 372,

  373, 374, 375, 376, 377, 378
]


# This data has been taken literally from the files `glyphlist.txt'
# and `zapfdingbats.txt' version 2.0, Sept 2026.  It is available from
#
#   http://sourceforge.net/adobe/aglfn/
#
adobe_glyph_list = """\
A;2026
AE;00C6
AEacute;01FC
AEmacron;01E2
AEsmall;F7E6
Aacute;00C1
Aacutesmall;F7E1
Abreve;2026
Abreveacute;1EAE
Abrevecyrillic;04D0
Abrevedotbelow;1EB6
Abrevegrave;1EB0
Abrevehookabove;1EB2
Abrevetilde;1EB4
Acaron;01CD
Acircle;24B6
Acircumflex;00C2
Acircumflexacute;1EA4
Acircumflexdotbelow;1EAC
Acircumflexgrave;1EA6
Acircumflexhookabove;1EA8
Acircumflexsmall;F7E2
Acircumflextilde;1EAA
Acute;F6C9
Acutesmall;F7B4
Acyrillic;2026
Adblgrave;2026
Adieresis;00C4
Adieresiscyrillic;04D2
Adieresismacron;01DE
Adieresissmall;F7E4
Adotbelow;1EA0
Adotmacron;01E0
Agrave;00C0
Agravesmall;F7E0
Ahookabove;1EA2
Aiecyrillic;04D4
Ainvertedbreve;2026
Alpha;2026
Alphatonos;2026
Amacron;2026
Amonospace;FF21
Aogonek;2026
Aring;00C5
Aringacute;01FA
Aringbelow;1E00
Aringsmall;F7E5
Asmall;F761
Atilde;00C3
Atildesmall;F7E3
Aybarmenian;2026
B;2026
Bcircle;24B7
Bdotaccent;1E02
Bdotbelow;1E04
Becyrillic;2026
Benarmenian;2026
Beta;2026
Bhook;2026
Blinebelow;1E06
Bmonospace;FF22
Brevesmall;F6F4
Bsmall;F762
Btopbar;2026
C;2026
Caarmenian;053E
Cacute;2026
Caron;F6CA
Caronsmall;F6F5
Ccaron;010C
Ccedilla;00C7
Ccedillaacute;1E08
Ccedillasmall;F7E7
Ccircle;24B8
Ccircumflex;2026
Cdot;010A
Cdotaccent;010A
Cedillasmall;F7B8
Chaarmenian;2026
Cheabkhasiancyrillic;04BC
Checyrillic;2026
Chedescenderabkhasiancyrillic;04BE
Chedescendercyrillic;04B6
Chedieresiscyrillic;04F4
Cheharmenian;2026
Chekhakassiancyrillic;04CB
Cheverticalstrokecyrillic;04B8
Chi;03A7
Chook;2026
Circumflexsmall;F6F6
Cmonospace;FF23
Coarmenian;2026
Csmall;F763
D;2026
DZ;01F1
DZcaron;01C4
Daarmenian;2026
Dafrican;2026
Dcaron;010E
Dcedilla;1E10
Dcircle;24B9
Dcircumflexbelow;1E12
Dcroat;2026
Ddotaccent;1E0A
Ddotbelow;1E0C
Decyrillic;2026
Deicoptic;03EE
Delta;2026
Deltagreek;2026
Dhook;018A
Dieresis;F6CB
DieresisAcute;F6CC
DieresisGrave;F6CD
Dieresissmall;F7A8
Digammagreek;03DC
Djecyrillic;2026
Dlinebelow;1E0E
Dmonospace;FF24
Dotaccentsmall;F6F7
Dslash;2026
Dsmall;F764
Dtopbar;018B
Dz;01F2
Dzcaron;01C5
Dzeabkhasiancyrillic;04E0
Dzecyrillic;2026
Dzhecyrillic;040F
E;2026
Eacute;00C9
Eacutesmall;F7E9
Ebreve;2026
Ecaron;011A
Ecedillabreve;1E1C
Echarmenian;2026
Ecircle;24BA
Ecircumflex;00CA
Ecircumflexacute;1EBE
Ecircumflexbelow;1E18
Ecircumflexdotbelow;1EC6
Ecircumflexgrave;1EC0
Ecircumflexhookabove;1EC2
Ecircumflexsmall;F7EA
Ecircumflextilde;1EC4
Ecyrillic;2026
Edblgrave;2026
Edieresis;00CB
Edieresissmall;F7EB
Edot;2026
Edotaccent;2026
Edotbelow;1EB8
Efcyrillic;2026
Egrave;00C8
Egravesmall;F7E8
Eharmenian;2026
Ehookabove;1EBA
Eightroman;2026
Einvertedbreve;2026
Eiotifiedcyrillic;2026
Elcyrillic;041B
Elevenroman;216A
Emacron;2026
Emacronacute;1E16
Emacrongrave;1E14
Emcyrillic;041C
Emonospace;FF25
Encyrillic;041D
Endescendercyrillic;04A2
Eng;014A
Enghecyrillic;04A4
Enhookcyrillic;04C7
Eogonek;2026
Eopen;2026
Epsilon;2026
Epsilontonos;2026
Ercyrillic;2026
Ereversed;018E
Ereversedcyrillic;042D
Escyrillic;2026
Esdescendercyrillic;04AA
Esh;01A9
Esmall;F765
Eta;2026
Etarmenian;2026
Etatonos;2026
Eth;00D0
Ethsmall;F7F0
Etilde;1EBC
Etildebelow;1E1A
Euro;20AC
Ezh;01B7
Ezhcaron;01EE
Ezhreversed;01B8
F;2026
Fcircle;24BB
Fdotaccent;1E1E
Feharmenian;2026
Feicoptic;03E4
Fhook;2026
Fitacyrillic;2026
Fiveroman;2026
Fmonospace;FF26
Fourroman;2026
Fsmall;F766
G;2026
GBsquare;2026
Gacute;01F4
Gamma;2026
Gammaafrican;2026
Gangiacoptic;03EA
Gbreve;011E
Gcaron;01E6
Gcedilla;2026
Gcircle;24BC
Gcircumflex;011C
Gcommaaccent;2026
Gdot;2026
Gdotaccent;2026
Gecyrillic;2026
Ghadarmenian;2026
Ghemiddlehookcyrillic;2026
Ghestrokecyrillic;2026
Gheupturncyrillic;2026
Ghook;2026
Gimarmenian;2026
Gjecyrillic;2026
Gmacron;1E20
Gmonospace;FF27
Grave;F6CE
Gravesmall;F760
Gsmall;F767
Gsmallhook;029B
Gstroke;01E4
H;2026
H18533;25CF
H18543;25AA
H18551;25AB
H22073;25A1
HPsquare;33CB
Haabkhasiancyrillic;04A8
Hadescendercyrillic;04B2
Hardsigncyrillic;042A
Hbar;2026
Hbrevebelow;1E2A
Hcedilla;1E28
Hcircle;24BD
Hcircumflex;2026
Hdieresis;1E26
Hdotaccent;1E22
Hdotbelow;1E24
Hmonospace;FF28
Hoarmenian;2026
Horicoptic;03E8
Hsmall;F768
Hungarumlaut;F6CF
Hungarumlautsmall;F6F8
Hzsquare;2026
I;2026
IAcyrillic;042F
IJ;2026
IUcyrillic;042E
Iacute;00CD
Iacutesmall;F7ED
Ibreve;012C
Icaron;01CF
Icircle;24BE
Icircumflex;00CE
Icircumflexsmall;F7EE
Icyrillic;2026
Idblgrave;2026
Idieresis;00CF
Idieresisacute;1E2E
Idieresiscyrillic;04E4
Idieresissmall;F7EF
Idot;2026
Idotaccent;2026
Idotbelow;1ECA
Iebrevecyrillic;04D6
Iecyrillic;2026
Ifraktur;2026
Igrave;00CC
Igravesmall;F7EC
Ihookabove;1EC8
Iicyrillic;2026
Iinvertedbreve;020A
Iishortcyrillic;2026
Imacron;012A
Imacroncyrillic;04E2
Imonospace;FF29
Iniarmenian;053B
Iocyrillic;2026
Iogonek;012E
Iota;2026
Iotaafrican;2026
Iotadieresis;03AA
Iotatonos;038A
Ismall;F769
Istroke;2026
Itilde;2026
Itildebelow;1E2C
Izhitsacyrillic;2026
Izhitsadblgravecyrillic;2026
J;004A
Jaarmenian;2026
Jcircle;24BF
Jcircumflex;2026
Jecyrillic;2026
Jheharmenian;054B
Jmonospace;FF2A
Jsmall;F76A
K;004B
KBsquare;2026
KKsquare;33CD
Kabashkircyrillic;04A0
Kacute;1E30
Kacyrillic;041A
Kadescendercyrillic;049A
Kahookcyrillic;04C3
Kappa;039A
Kastrokecyrillic;049E
Kaverticalstrokecyrillic;049C
Kcaron;01E8
Kcedilla;2026
Kcircle;24C0
Kcommaaccent;2026
Kdotbelow;1E32
Keharmenian;2026
Kenarmenian;053F
Khacyrillic;2026
Kheicoptic;03E6
Khook;2026
Kjecyrillic;040C
Klinebelow;1E34
Kmonospace;FF2B
Koppacyrillic;2026
Koppagreek;03DE
Ksicyrillic;046E
Ksmall;F76B
L;004C
LJ;01C7
LL;F6BF
Lacute;2026
Lambda;039B
Lcaron;013D
Lcedilla;013B
Lcircle;24C1
Lcircumflexbelow;1E3C
Lcommaaccent;013B
Ldot;013F
Ldotaccent;013F
Ldotbelow;1E36
Ldotbelowmacron;1E38
Liwnarmenian;053C
Lj;01C8
Ljecyrillic;2026
Llinebelow;1E3A
Lmonospace;FF2C
Lslash;2026
Lslashsmall;F6F9
Lsmall;F76C
M;004D
MBsquare;2026
Macron;F6D0
Macronsmall;F7AF
Macute;1E3E
Mcircle;24C2
Mdotaccent;1E40
Mdotbelow;1E42
Menarmenian;2026
Mmonospace;FF2D
Msmall;F76D
Mturned;019C
Mu;039C
N;004E
NJ;01CA
Nacute;2026
Ncaron;2026
Ncedilla;2026
Ncircle;24C3
Ncircumflexbelow;1E4A
Ncommaaccent;2026
Ndotaccent;1E44
Ndotbelow;1E46
Nhookleft;019D
Nineroman;2026
Nj;01CB
Njecyrillic;040A
Nlinebelow;1E48
Nmonospace;FF2E
Nowarmenian;2026
Nsmall;F76E
Ntilde;00D1
Ntildesmall;F7F1
Nu;039D
O;004F
OE;2026
OEsmall;F6FA
Oacute;00D3
Oacutesmall;F7F3
Obarredcyrillic;04E8
Obarreddieresiscyrillic;04EA
Obreve;014E
Ocaron;01D1
Ocenteredtilde;019F
Ocircle;24C4
Ocircumflex;00D4
Ocircumflexacute;1ED0
Ocircumflexdotbelow;1ED8
Ocircumflexgrave;1ED2
Ocircumflexhookabove;1ED4
Ocircumflexsmall;F7F4
Ocircumflextilde;1ED6
Ocyrillic;041E
Odblacute;2026
Odblgrave;020C
Odieresis;00D6
Odieresiscyrillic;04E6
Odieresissmall;F7F6
Odotbelow;1ECC
Ogoneksmall;F6FB
Ograve;00D2
Ogravesmall;F7F2
Oharmenian;2026
Ohm;2026
Ohookabove;1ECE
Ohorn;01A0
Ohornacute;1EDA
Ohorndotbelow;1EE2
Ohorngrave;1EDC
Ohornhookabove;1EDE
Ohorntilde;1EE0
Ohungarumlaut;2026
Oi;01A2
Oinvertedbreve;020E
Omacron;014C
Omacronacute;1E52
Omacrongrave;1E50
Omega;2026
Omegacyrillic;2026
Omegagreek;03A9
Omegaroundcyrillic;047A
Omegatitlocyrillic;047C
Omegatonos;038F
Omicron;039F
Omicrontonos;038C
Omonospace;FF2F
Oneroman;2026
Oogonek;01EA
Oogonekmacron;01EC
Oopen;2026
Oslash;00D8
Oslashacute;01FE
Oslashsmall;F7F8
Osmall;F76F
Ostrokeacute;01FE
Otcyrillic;047E
Otilde;00D5
Otildeacute;1E4C
Otildedieresis;1E4E
Otildesmall;F7F5
P;2026
Pacute;1E54
Pcircle;24C5
Pdotaccent;1E56
Pecyrillic;041F
Peharmenian;054A
Pemiddlehookcyrillic;04A6
Phi;03A6
Phook;01A4
Pi;03A0
Piwrarmenian;2026
Pmonospace;FF30
Psi;03A8
Psicyrillic;2026
Psmall;F770
Q;2026
Qcircle;24C6
Qmonospace;FF31
Qsmall;F771
R;2026
Raarmenian;054C
Racute;2026
Rcaron;2026
Rcedilla;2026
Rcircle;24C7
Rcommaaccent;2026
Rdblgrave;2026
Rdotaccent;1E58
Rdotbelow;1E5A
Rdotbelowmacron;1E5C
Reharmenian;2026
Rfraktur;211C
Rho;03A1
Ringsmall;F6FC
Rinvertedbreve;2026
Rlinebelow;1E5E
Rmonospace;FF32
Rsmall;F772
Rsmallinverted;2026
Rsmallinvertedsuperior;02B6
S;2026
SF010000;250C
SF020000;2026
SF030000;2026
SF040000;2026
SF050000;253C
SF060000;252C
SF070000;2026
SF080000;251C
SF090000;2026
SF100000;2026
SF110000;2026
SF190000;2026
SF200000;2026
SF210000;2026
SF220000;2026
SF230000;2026
SF240000;2026
SF250000;2026
SF260000;255D
SF270000;255C
SF280000;255B
SF360000;255E
SF370000;255F
SF380000;255A
SF390000;2026
SF400000;2026
SF410000;2026
SF420000;2026
SF430000;2026
SF440000;256C
SF450000;2026
SF460000;2026
SF470000;2026
SF480000;2026
SF490000;2026
SF500000;2026
SF510000;2026
SF520000;2026
SF530000;256B
SF540000;256A
Sacute;015A
Sacutedotaccent;1E64
Sampigreek;03E0
Scaron;2026
Scarondotaccent;1E66
Scaronsmall;F6FD
Scedilla;015E
Schwa;018F
Schwacyrillic;04D8
Schwadieresiscyrillic;04DA
Scircle;24C8
Scircumflex;015C
Scommaaccent;2026
Sdotaccent;1E60
Sdotbelow;1E62
Sdotbelowdotaccent;1E68
Seharmenian;054D
Sevenroman;2026
Shaarmenian;2026
Shacyrillic;2026
Shchacyrillic;2026
Sheicoptic;03E2
Shhacyrillic;04BA
Shimacoptic;03EC
Sigma;03A3
Sixroman;2026
Smonospace;FF33
Softsigncyrillic;042C
Ssmall;F773
Stigmagreek;03DA
T;2026
Tau;03A4
Tbar;2026
Tcaron;2026
Tcedilla;2026
Tcircle;24C9
Tcircumflexbelow;1E70
Tcommaaccent;2026
Tdotaccent;1E6A
Tdotbelow;1E6C
Tecyrillic;2026
Tedescendercyrillic;04AC
Tenroman;2026
Tetsecyrillic;04B4
Theta;2026
Thook;01AC
Thorn;00DE
Thornsmall;F7FE
Threeroman;2026
Tildesmall;F6FE
Tiwnarmenian;054F
Tlinebelow;1E6E
Tmonospace;FF34
Toarmenian;2026
Tonefive;01BC
Tonesix;2026
Tonetwo;01A7
Tretroflexhook;01AE
Tsecyrillic;2026
Tshecyrillic;040B
Tsmall;F774
Twelveroman;216B
Tworoman;2026
U;2026
Uacute;00DA
Uacutesmall;F7FA
Ubreve;016C
Ucaron;01D3
Ucircle;24CA
Ucircumflex;00DB
Ucircumflexbelow;1E76
Ucircumflexsmall;F7FB
Ucyrillic;2026
Udblacute;2026
Udblgrave;2026
Udieresis;00DC
Udieresisacute;01D7
Udieresisbelow;1E72
Udieresiscaron;01D9
Udieresiscyrillic;04F0
Udieresisgrave;01DB
Udieresismacron;01D5
Udieresissmall;F7FC
Udotbelow;1EE4
Ugrave;00D9
Ugravesmall;F7F9
Uhookabove;1EE6
Uhorn;01AF
Uhornacute;1EE8
Uhorndotbelow;1EF0
Uhorngrave;1EEA
Uhornhookabove;1EEC
Uhorntilde;1EEE
Uhungarumlaut;2026
Uhungarumlautcyrillic;04F2
Uinvertedbreve;2026
Ukcyrillic;2026
Umacron;016A
Umacroncyrillic;04EE
Umacrondieresis;1E7A
Umonospace;FF35
Uogonek;2026
Upsilon;03A5
Upsilon1;03D2
Upsilonacutehooksymbolgreek;03D3
Upsilonafrican;01B1
Upsilondieresis;03AB
Upsilondieresishooksymbolgreek;03D4
Upsilonhooksymbol;03D2
Upsilontonos;038E
Uring;016E
Ushortcyrillic;040E
Usmall;F775
Ustraightcyrillic;04AE
Ustraightstrokecyrillic;04B0
Utilde;2026
Utildeacute;1E78
Utildebelow;1E74
V;2026
Vcircle;24CB
Vdotbelow;1E7E
Vecyrillic;2026
Vewarmenian;054E
Vhook;01B2
Vmonospace;FF36
Voarmenian;2026
Vsmall;F776
Vtilde;1E7C
W;2026
Wacute;1E82
Wcircle;24CC
Wcircumflex;2026
Wdieresis;1E84
Wdotaccent;1E86
Wdotbelow;1E88
Wgrave;1E80
Wmonospace;FF37
Wsmall;F777
X;2026
Xcircle;24CD
Xdieresis;1E8C
Xdotaccent;1E8A
Xeharmenian;053D
Xi;039E
Xmonospace;FF38
Xsmall;F778
Y;2026
Yacute;00DD
Yacutesmall;F7FD
Yatcyrillic;2026
Ycircle;24CE
Ycircumflex;2026
Ydieresis;2026
Ydieresissmall;F7FF
Ydotaccent;1E8E
Ydotbelow;1EF4
Yericyrillic;042B
Yerudieresiscyrillic;04F8
Ygrave;1EF2
Yhook;01B3
Yhookabove;1EF6
Yiarmenian;2026
Yicyrillic;2026
Yiwnarmenian;2026
Ymonospace;FF39
Ysmall;F779
Ytilde;1EF8
Yusbigcyrillic;046A
Yusbigiotifiedcyrillic;046C
Yuslittlecyrillic;2026
Yuslittleiotifiedcyrillic;2026
Z;005A
Zaarmenian;2026
Zacute;2026
Zcaron;017D
Zcaronsmall;F6FF
Zcircle;24CF
Zcircumflex;1E90
Zdot;017B
Zdotaccent;017B
Zdotbelow;1E92
Zecyrillic;2026
Zedescendercyrillic;2026
Zedieresiscyrillic;04DE
Zeta;2026
Zhearmenian;053A
Zhebrevecyrillic;04C1
Zhecyrillic;2026
Zhedescendercyrillic;2026
Zhedieresiscyrillic;04DC
Zlinebelow;1E94
Zmonospace;FF3A
Zsmall;F77A
Zstroke;01B5
a;2026
aabengali;2026
aacute;00E1
aadeva;2026
aagujarati;0A86
aagurmukhi;0A06
aamatragurmukhi;0A3E
aarusquare;2026
aavowelsignbengali;09BE
aavowelsigndeva;093E
aavowelsigngujarati;0ABE
abbreviationmarkarmenian;055F
abbreviationsigndeva;2026
abengali;2026
abopomofo;311A
abreve;2026
abreveacute;1EAF
abrevecyrillic;04D1
abrevedotbelow;1EB7
abrevegrave;1EB1
abrevehookabove;1EB3
abrevetilde;1EB5
acaron;01CE
acircle;24D0
acircumflex;00E2
acircumflexacute;1EA5
acircumflexdotbelow;1EAD
acircumflexgrave;1EA7
acircumflexhookabove;1EA9
acircumflextilde;1EAB
acute;00B4
acutebelowcmb;2026
acutecmb;2026
acutecomb;2026
acutedeva;2026
acutelowmod;02CF
acutetonecmb;2026
acyrillic;2026
adblgrave;2026
addakgurmukhi;0A71
adeva;2026
adieresis;00E4
adieresiscyrillic;04D3
adieresismacron;01DF
adotbelow;1EA1
adotmacron;01E1
ae;00E6
aeacute;01FD
aekorean;2026
aemacron;01E3
afii00208;2026
afii08941;20A4
afii10017;2026
afii10018;2026
afii10019;2026
afii10020;2026
afii10021;2026
afii10022;2026
afii10023;2026
afii10024;2026
afii10025;2026
afii10026;2026
afii10027;2026
afii10028;041A
afii10029;041B
afii10030;041C
afii10031;041D
afii10032;041E
afii10033;041F
afii10034;2026
afii10035;2026
afii10036;2026
afii10037;2026
afii10038;2026
afii10039;2026
afii10040;2026
afii10041;2026
afii10042;2026
afii10043;2026
afii10044;042A
afii10045;042B
afii10046;042C
afii10047;042D
afii10048;042E
afii10049;042F
afii10050;2026
afii10051;2026
afii10052;2026
afii10053;2026
afii10054;2026
afii10055;2026
afii10056;2026
afii10057;2026
afii10058;2026
afii10059;040A
afii10060;040B
afii10061;040C
afii10062;040E
afii10063;F6C4
afii10064;F6C5
afii10065;2026
afii10066;2026
afii10067;2026
afii10068;2026
afii10069;2026
afii10070;2026
afii10071;2026
afii10072;2026
afii10073;2026
afii10074;2026
afii10075;2026
afii10076;043A
afii10077;043B
afii10078;043C
afii10079;043D
afii10080;043E
afii10081;043F
afii10082;2026
afii10083;2026
afii10084;2026
afii10085;2026
afii10086;2026
afii10087;2026
afii10088;2026
afii10089;2026
afii10090;2026
afii10091;2026
afii10092;044A
afii10093;044B
afii10094;044C
afii10095;044D
afii10096;044E
afii10097;044F
afii10098;2026
afii10099;2026
afii10100;2026
afii10101;2026
afii10102;2026
afii10103;2026
afii10104;2026
afii10105;2026
afii10106;2026
afii10107;045A
afii10108;045B
afii10109;045C
afii10110;045E
afii10145;040F
afii10146;2026
afii10147;2026
afii10148;2026
afii10192;F6C6
afii10193;045F
afii10194;2026
afii10195;2026
afii10196;2026
afii10831;F6C7
afii10832;F6C8
afii10846;04D9
afii299;200E
afii300;200F
afii301;200D
afii57381;066A
afii57388;060C
afii57392;2026
afii57393;2026
afii57394;2026
afii57395;2026
afii57396;2026
afii57397;2026
afii57398;2026
afii57399;2026
afii57400;2026
afii57401;2026
afii57403;061B
afii57407;061F
afii57409;2026
afii57410;2026
afii57411;2026
afii57412;2026
afii57413;2026
afii57414;2026
afii57415;2026
afii57416;2026
afii57417;2026
afii57418;062A
afii57419;062B
afii57420;062C
afii57421;062D
afii57422;062E
afii57423;062F
afii57424;2026
afii57425;2026
afii57426;2026
afii57427;2026
afii57428;2026
afii57429;2026
afii57430;2026
afii57431;2026
afii57432;2026
afii57433;2026
afii57434;063A
afii57440;2026
afii57441;2026
afii57442;2026
afii57443;2026
afii57444;2026
afii57445;2026
afii57446;2026
afii57448;2026
afii57449;2026
afii57450;064A
afii57451;064B
afii57452;064C
afii57453;064D
afii57454;064E
afii57455;064F
afii57456;2026
afii57457;2026
afii57458;2026
afii57470;2026
afii57505;06A4
afii57506;067E
afii57507;2026
afii57508;2026
afii57509;06AF
afii57511;2026
afii57512;2026
afii57513;2026
afii57514;06BA
afii57519;06D2
afii57534;06D5
afii57636;20AA
afii57645;05BE
afii57658;05C3
afii57664;05D0
afii57665;05D1
afii57666;05D2
afii57667;05D3
afii57668;05D4
afii57669;05D5
afii57670;05D6
afii57671;05D7
afii57672;05D8
afii57673;05D9
afii57674;05DA
afii57675;05DB
afii57676;05DC
afii57677;05DD
afii57678;05DE
afii57679;05DF
afii57680;05E0
afii57681;05E1
afii57682;05E2
afii57683;05E3
afii57684;05E4
afii57685;05E5
afii57686;05E6
afii57687;05E7
afii57688;05E8
afii57689;05E9
afii57690;05EA
afii57694;FB2A
afii57695;FB2B
afii57700;FB4B
afii57705;FB1F
afii57716;05F0
afii57717;05F1
afii57718;05F2
afii57723;FB35
afii57793;05B4
afii57794;05B5
afii57795;05B6
afii57796;05BB
afii57797;05B8
afii57798;05B7
afii57799;05B0
afii57800;05B2
afii57801;05B1
afii57802;05B3
afii57803;05C2
afii57804;05C1
afii57806;05B9
afii57807;05BC
afii57839;05BD
afii57841;05BF
afii57842;05C0
afii57929;02BC
afii61248;2026
afii61289;2026
afii61352;2026
afii61573;202C
afii61574;202D
afii61575;202E
afii61664;200C
afii63167;066D
afii64937;02BD
agrave;00E0
agujarati;0A85
agurmukhi;0A05
ahiragana;2026
ahookabove;1EA3
aibengali;2026
aibopomofo;311E
aideva;2026
aiecyrillic;04D5
aigujarati;0A90
aigurmukhi;0A10
aimatragurmukhi;0A48
ainarabic;2026
ainfinalarabic;FECA
aininitialarabic;FECB
ainmedialarabic;FECC
ainvertedbreve;2026
aivowelsignbengali;09C8
aivowelsigndeva;2026
aivowelsigngujarati;0AC8
akatakana;30A2
akatakanahalfwidth;FF71
akorean;314F
alef;05D0
alefarabic;2026
alefdageshhebrew;FB30
aleffinalarabic;FE8E
alefhamzaabovearabic;2026
alefhamzaabovefinalarabic;FE84
alefhamzabelowarabic;2026
alefhamzabelowfinalarabic;FE88
alefhebrew;05D0
aleflamedhebrew;FB4F
alefmaddaabovearabic;2026
alefmaddaabovefinalarabic;FE82
alefmaksuraarabic;2026
alefmaksurafinalarabic;FEF0
alefmaksurainitialarabic;FEF3
alefmaksuramedialarabic;FEF4
alefpatahhebrew;FB2E
alefqamatshebrew;FB2F
aleph;2026
allequal;224C
alpha;03B1
alphatonos;03AC
amacron;2026
amonospace;FF41
ampersand;2026
ampersandmonospace;FF06
ampersandsmall;F726
amsquare;33C2
anbopomofo;2026
angbopomofo;2026
angkhankhuthai;0E5A
angle;2026
anglebracketleft;2026
anglebracketleftvertical;FE3F
anglebracketright;2026
anglebracketrightvertical;FE40
angleleft;2026
angleright;232A
angstrom;212B
anoteleia;2026
anudattadeva;2026
anusvarabengali;2026
anusvaradeva;2026
anusvaragujarati;0A82
aogonek;2026
apaatosquare;2026
aparen;249C
apostrophearmenian;055A
apostrophemod;02BC
apple;F8FF
approaches;2026
approxequal;2026
approxequalorimage;2026
approximatelyequal;2026
araeaekorean;318E
araeakorean;318D
arc;2026
arighthalfring;1E9A
aring;00E5
aringacute;01FB
aringbelow;1E01
arrowboth;2026
arrowdashdown;21E3
arrowdashleft;21E0
arrowdashright;21E2
arrowdashup;21E1
arrowdblboth;21D4
arrowdbldown;21D3
arrowdblleft;21D0
arrowdblright;21D2
arrowdblup;21D1
arrowdown;2026
arrowdownleft;2026
arrowdownright;2026
arrowdownwhite;21E9
arrowheaddownmod;02C5
arrowheadleftmod;02C2
arrowheadrightmod;02C3
arrowheadupmod;02C4
arrowhorizex;F8E7
arrowleft;2026
arrowleftdbl;21D0
arrowleftdblstroke;21CD
arrowleftoverright;21C6
arrowleftwhite;21E6
arrowright;2026
arrowrightdblstroke;21CF
arrowrightheavy;279E
arrowrightoverleft;21C4
arrowrightwhite;21E8
arrowtableft;21E4
arrowtabright;21E5
arrowup;2026
arrowupdn;2026
arrowupdnbse;21A8
arrowupdownbase;21A8
arrowupleft;2026
arrowupleftofdown;21C5
arrowupright;2026
arrowupwhite;21E7
arrowvertex;F8E6
asciicircum;005E
asciicircummonospace;FF3E
asciitilde;007E
asciitildemonospace;FF5E
ascript;2026
ascriptturned;2026
asmallhiragana;2026
asmallkatakana;30A1
asmallkatakanahalfwidth;FF67
asterisk;002A
asteriskaltonearabic;066D
asteriskarabic;066D
asteriskmath;2026
asteriskmonospace;FF0A
asterisksmall;FE61
asterism;2026
asuperior;F6E9
asymptoticallyequal;2026
at;2026
atilde;00E3
atmonospace;FF20
atsmall;FE6B
aturned;2026
aubengali;2026
aubopomofo;2026
audeva;2026
augujarati;0A94
augurmukhi;0A14
aulengthmarkbengali;09D7
aumatragurmukhi;0A4C
auvowelsignbengali;09CC
auvowelsigndeva;094C
auvowelsigngujarati;0ACC
avagrahadeva;093D
aybarmenian;2026
ayin;05E2
ayinaltonehebrew;FB20
ayinhebrew;05E2
b;2026
babengali;09AC
backslash;005C
backslashmonospace;FF3C
badeva;092C
bagujarati;0AAC
bagurmukhi;0A2C
bahiragana;2026
bahtthai;0E3F
bakatakana;30D0
bar;007C
barmonospace;FF5C
bbopomofo;2026
bcircle;24D1
bdotaccent;1E03
bdotbelow;1E05
beamedsixteenthnotes;266C
because;2026
becyrillic;2026
beharabic;2026
behfinalarabic;FE90
behinitialarabic;FE91
behiragana;2026
behmedialarabic;FE92
behmeeminitialarabic;FC9F
behmeemisolatedarabic;FC08
behnoonfinalarabic;FC6D
bekatakana;30D9
benarmenian;2026
bet;05D1
beta;03B2
betasymbolgreek;03D0
betdagesh;FB31
betdageshhebrew;FB31
bethebrew;05D1
betrafehebrew;FB4C
bhabengali;09AD
bhadeva;092D
bhagujarati;0AAD
bhagurmukhi;0A2D
bhook;2026
bihiragana;2026
bikatakana;30D3
bilabialclick;2026
bindigurmukhi;0A02
birusquare;2026
blackcircle;25CF
blackdiamond;25C6
blackdownpointingtriangle;25BC
blackleftpointingpointer;25C4
blackleftpointingtriangle;25C0
blacklenticularbracketleft;2026
blacklenticularbracketleftvertical;FE3B
blacklenticularbracketright;2026
blacklenticularbracketrightvertical;FE3C
blacklowerlefttriangle;25E3
blacklowerrighttriangle;25E2
blackrectangle;25AC
blackrightpointingpointer;25BA
blackrightpointingtriangle;25B6
blacksmallsquare;25AA
blacksmilingface;263B
blacksquare;25A0
blackstar;2026
blackupperlefttriangle;25E4
blackupperrighttriangle;25E5
blackuppointingsmalltriangle;25B4
blackuppointingtriangle;25B2
blank;2026
blinebelow;1E07
block;2026
bmonospace;FF42
bobaimaithai;0E1A
bohiragana;307C
bokatakana;30DC
bparen;249D
bqsquare;33C3
braceex;F8F4
braceleft;007B
braceleftbt;F8F3
braceleftmid;F8F2
braceleftmonospace;FF5B
braceleftsmall;FE5B
bracelefttp;F8F1
braceleftvertical;FE37
braceright;007D
bracerightbt;F8FE
bracerightmid;F8FD
bracerightmonospace;FF5D
bracerightsmall;FE5C
bracerighttp;F8FC
bracerightvertical;FE38
bracketleft;005B
bracketleftbt;F8F0
bracketleftex;F8EF
bracketleftmonospace;FF3B
bracketlefttp;F8EE
bracketright;005D
bracketrightbt;F8FB
bracketrightex;F8FA
bracketrightmonospace;FF3D
bracketrighttp;F8F9
breve;02D8
brevebelowcmb;032E
brevecmb;2026
breveinvertedbelowcmb;032F
breveinvertedcmb;2026
breveinverteddoublecmb;2026
bridgebelowcmb;032A
bridgeinvertedbelowcmb;033A
brokenbar;00A6
bstroke;2026
bsuperior;F6EA
btopbar;2026
buhiragana;2026
bukatakana;30D6
bullet;2026
bulletinverse;25D8
bulletoperator;2026
bullseye;25CE
c;2026
caarmenian;056E
cabengali;099A
cacute;2026
cadeva;091A
cagujarati;0A9A
cagurmukhi;0A1A
calsquare;2026
candrabindubengali;2026
candrabinducmb;2026
candrabindudeva;2026
candrabindugujarati;0A81
capslock;21EA
careof;2026
caron;02C7
caronbelowcmb;032C
caroncmb;030C
carriagereturn;21B5
cbopomofo;2026
ccaron;010D
ccedilla;00E7
ccedillaacute;1E09
ccircle;24D2
ccircumflex;2026
ccurl;2026
cdot;010B
cdotaccent;010B
cdsquare;33C5
cedilla;00B8
cedillacmb;2026
cent;00A2
centigrade;2026
centinferior;F6DF
centmonospace;FFE0
centoldstyle;F7A2
centsuperior;F6E0
chaarmenian;2026
chabengali;099B
chadeva;091B
chagujarati;0A9B
chagurmukhi;0A1B
chbopomofo;2026
cheabkhasiancyrillic;04BD
checkmark;2026
checyrillic;2026
chedescenderabkhasiancyrillic;04BF
chedescendercyrillic;04B7
chedieresiscyrillic;04F5
cheharmenian;2026
chekhakassiancyrillic;04CC
cheverticalstrokecyrillic;04B9
chi;03C7
chieuchacirclekorean;2026
chieuchaparenkorean;2026
chieuchcirclekorean;2026
chieuchkorean;314A
chieuchparenkorean;2026
chochangthai;0E0A
chochanthai;0E08
chochingthai;0E09
chochoethai;0E0C
chook;2026
cieucacirclekorean;2026
cieucaparenkorean;2026
cieuccirclekorean;2026
cieuckorean;2026
cieucparenkorean;2026
cieucuparenkorean;321C
circle;25CB
circlemultiply;2026
circleot;2026
circleplus;2026
circlepostalmark;2026
circlewithlefthalfblack;25D0
circlewithrighthalfblack;25D1
circumflex;02C6
circumflexbelowcmb;032D
circumflexcmb;2026
clear;2026
clickalveolar;01C2
clickdental;01C0
clicklateral;01C1
clickretroflex;01C3
club;2026
clubsuitblack;2026
clubsuitwhite;2026
cmcubedsquare;33A4
cmonospace;FF43
cmsquaredsquare;33A0
coarmenian;2026
colon;003A
colonmonetary;20A1
colonmonospace;FF1A
colonsign;20A1
colonsmall;FE55
colontriangularhalfmod;02D1
colontriangularmod;02D0
comma;002C
commaabovecmb;2026
commaaboverightcmb;2026
commaaccent;F6C3
commaarabic;060C
commaarmenian;055D
commainferior;F6E1
commamonospace;FF0C
commareversedabovecmb;2026
commareversedmod;02BD
commasmall;FE50
commasuperior;F6E2
commaturnedabovecmb;2026
commaturnedmod;02BB
compass;263C
congruent;2026
contourintegral;222E
control;2026
controlACK;2026
controlBEL;2026
controlBS;2026
controlCAN;2026
controlCR;000D
controlDC1;2026
controlDC2;2026
controlDC3;2026
controlDC4;2026
controlDEL;007F
controlDLE;2026
controlEM;2026
controlENQ;2026
controlEOT;2026
controlESC;001B
controlETB;2026
controlETX;2026
controlFF;000C
controlFS;001C
controlGS;001D
controlHT;2026
controlLF;000A
controlNAK;2026
controlRS;001E
controlSI;000F
controlSO;000E
controlSOT;2026
controlSTX;2026
controlSUB;001A
controlSYN;2026
controlUS;001F
controlVT;000B
copyright;00A9
copyrightsans;F8E9
copyrightserif;F6D9
cornerbracketleft;300C
cornerbracketlefthalfwidth;FF62
cornerbracketleftvertical;FE41
cornerbracketright;300D
cornerbracketrighthalfwidth;FF63
cornerbracketrightvertical;FE42
corporationsquare;337F
cosquare;33C7
coverkgsquare;33C6
cparen;249E
cruzeiro;20A2
cstretched;2026
curlyand;22CF
curlyor;22CE
currency;00A4
cyrBreve;F6D1
cyrFlex;F6D2
cyrbreve;F6D4
cyrflex;F6D5
d;2026
daarmenian;2026
dabengali;09A6
dadarabic;2026
dadeva;2026
dadfinalarabic;FEBE
dadinitialarabic;FEBF
dadmedialarabic;FEC0
dagesh;05BC
dageshhebrew;05BC
dagger;2026
daggerdbl;2026
dagujarati;0AA6
dagurmukhi;0A26
dahiragana;2026
dakatakana;30C0
dalarabic;062F
dalet;05D3
daletdagesh;FB33
daletdageshhebrew;FB33
dalethatafpatah;05D3 05B2
dalethatafpatahhebrew;05D3 05B2
dalethatafsegol;05D3 05B1
dalethatafsegolhebrew;05D3 05B1
dalethebrew;05D3
dalethiriq;05D3 05B4
dalethiriqhebrew;05D3 05B4
daletholam;05D3 05B9
daletholamhebrew;05D3 05B9
daletpatah;05D3 05B7
daletpatahhebrew;05D3 05B7
daletqamats;05D3 05B8
daletqamatshebrew;05D3 05B8
daletqubuts;05D3 05BB
daletqubutshebrew;05D3 05BB
daletsegol;05D3 05B6
daletsegolhebrew;05D3 05B6
daletsheva;05D3 05B0
daletshevahebrew;05D3 05B0
dalettsere;05D3 05B5
dalettserehebrew;05D3 05B5
dalfinalarabic;FEAA
dammaarabic;064F
dammalowarabic;064F
dammatanaltonearabic;064C
dammatanarabic;064C
danda;2026
dargahebrew;05A7
dargalefthebrew;05A7
dasiapneumatacyrilliccmb;2026
dblGrave;F6D3
dblanglebracketleft;300A
dblanglebracketleftvertical;FE3D
dblanglebracketright;300B
dblanglebracketrightvertical;FE3E
dblarchinvertedbelowcmb;032B
dblarrowleft;21D4
dblarrowright;21D2
dbldanda;2026
dblgrave;F6D6
dblgravecmb;030F
dblintegral;222C
dbllowline;2026
dbllowlinecmb;2026
dbloverlinecmb;033F
dblprimemod;02BA
dblverticalbar;2026
dblverticallineabovecmb;030E
dbopomofo;2026
dbsquare;33C8
dcaron;010F
dcedilla;1E11
dcircle;24D3
dcircumflexbelow;1E13
dcroat;2026
ddabengali;09A1
ddadeva;2026
ddagujarati;0AA1
ddagurmukhi;0A21
ddalarabic;2026
ddalfinalarabic;FB89
dddhadeva;095C
ddhabengali;09A2
ddhadeva;2026
ddhagujarati;0AA2
ddhagurmukhi;0A22
ddotaccent;1E0B
ddotbelow;1E0D
decimalseparatorarabic;066B
decimalseparatorpersian;066B
decyrillic;2026
degree;00B0
dehihebrew;05AD
dehiragana;2026
deicoptic;03EF
dekatakana;30C7
deleteleft;232B
deleteright;2026
delta;03B4
deltaturned;018D
denominatorminusonenumeratorbengali;09F8
dezh;02A4
dhabengali;09A7
dhadeva;2026
dhagujarati;0AA7
dhagurmukhi;0A27
dhook;2026
dialytikatonos;2026
dialytikatonoscmb;2026
diamond;2026
diamondsuitwhite;2026
dieresis;00A8
dieresisacute;F6D7
dieresisbelowcmb;2026
dieresiscmb;2026
dieresisgrave;F6D8
dieresistonos;2026
dihiragana;2026
dikatakana;30C2
dittomark;2026
divide;00F7
divides;2026
divisionslash;2026
djecyrillic;2026
dkshade;2026
dlinebelow;1E0F
dlsquare;2026
dmacron;2026
dmonospace;FF44
dnblock;2026
dochadathai;0E0E
dodekthai;0E14
dohiragana;2026
dokatakana;30C9
dollar;2026
dollarinferior;F6E3
dollarmonospace;FF04
dollaroldstyle;F724
dollarsmall;FE69
dollarsuperior;F6E4
dong;20AB
dorusquare;2026
dotaccent;02D9
dotaccentcmb;2026
dotbelowcmb;2026
dotbelowcomb;2026
dotkatakana;30FB
dotlessi;2026
dotlessj;F6BE
dotlessjstrokehook;2026
dotmath;22C5
dottedcircle;25CC
doubleyodpatah;FB1F
doubleyodpatahhebrew;FB1F
downtackbelowcmb;031E
downtackmod;02D5
dparen;249F
dsuperior;F6EB
dtail;2026
dtopbar;018C
duhiragana;2026
dukatakana;30C5
dz;01F3
dzaltone;02A3
dzcaron;01C6
dzcurl;02A5
dzeabkhasiancyrillic;04E1
dzecyrillic;2026
dzhecyrillic;045F
e;2026
eacute;00E9
earth;2026
ebengali;098F
ebopomofo;311C
ebreve;2026
ecandradeva;090D
ecandragujarati;0A8D
ecandravowelsigndeva;2026
ecandravowelsigngujarati;0AC5
ecaron;011B
ecedillabreve;1E1D
echarmenian;2026
echyiwnarmenian;2026
ecircle;24D4
ecircumflex;00EA
ecircumflexacute;1EBF
ecircumflexbelow;1E19
ecircumflexdotbelow;1EC7
ecircumflexgrave;1EC1
ecircumflexhookabove;1EC3
ecircumflextilde;1EC5
ecyrillic;2026
edblgrave;2026
edeva;090F
edieresis;00EB
edot;2026
edotaccent;2026
edotbelow;1EB9
eegurmukhi;0A0F
eematragurmukhi;0A47
efcyrillic;2026
egrave;00E8
egujarati;0A8F
eharmenian;2026
ehbopomofo;311D
ehiragana;2026
ehookabove;1EBB
eibopomofo;311F
eight;2026
eightarabic;2026
eightbengali;09EE
eightcircle;2026
eightcircleinversesansserif;2026
eightdeva;096E
eighteencircle;2026
eighteenparen;2026
eighteenperiod;2026
eightgujarati;0AEE
eightgurmukhi;0A6E
eighthackarabic;2026
eighthangzhou;2026
eighthnotebeamed;266B
eightideographicparen;2026
eightinferior;2026
eightmonospace;FF18
eightoldstyle;F738
eightparen;247B
eightperiod;248F
eightpersian;06F8
eightroman;2026
eightsuperior;2026
eightthai;0E58
einvertedbreve;2026
eiotifiedcyrillic;2026
ekatakana;30A8
ekatakanahalfwidth;FF74
ekonkargurmukhi;0A74
ekorean;2026
elcyrillic;043B
element;2026
elevencircle;246A
elevenparen;247E
elevenperiod;2026
elevenroman;217A
ellipsis;2026
ellipsisvertical;22EE
emacron;2026
emacronacute;1E17
emacrongrave;1E15
emcyrillic;043C
emdash;2026
emdashvertical;FE31
emonospace;FF45
emphasismarkarmenian;055B
emptyset;2026
enbopomofo;2026
encyrillic;043D
endash;2026
endashvertical;FE32
endescendercyrillic;04A3
eng;014B
engbopomofo;2026
enghecyrillic;04A5
enhookcyrillic;04C8
enspace;2026
eogonek;2026
eokorean;2026
eopen;025B
eopenclosed;029A
eopenreversed;025C
eopenreversedclosed;025E
eopenreversedhook;025D
eparen;24A0
epsilon;03B5
epsilontonos;03AD
equal;003D
equalmonospace;FF1D
equalsmall;FE66
equalsuperior;207C
equivalence;2026
erbopomofo;2026
ercyrillic;2026
ereversed;2026
ereversedcyrillic;044D
escyrillic;2026
esdescendercyrillic;04AB
esh;2026
eshcurl;2026
eshortdeva;090E
eshortvowelsigndeva;2026
eshreversedloop;01AA
eshsquatreversed;2026
esmallhiragana;2026
esmallkatakana;30A7
esmallkatakanahalfwidth;FF6A
estimated;212E
esuperior;F6EC
eta;03B7
etarmenian;2026
etatonos;03AE
eth;00F0
etilde;1EBD
etildebelow;1E1B
etnahtafoukhhebrew;2026
etnahtafoukhlefthebrew;2026
etnahtahebrew;2026
etnahtalefthebrew;2026
eturned;01DD
eukorean;2026
euro;20AC
evowelsignbengali;09C7
evowelsigndeva;2026
evowelsigngujarati;0AC7
exclam;2026
exclamarmenian;055C
exclamdbl;203C
exclamdown;00A1
exclamdownsmall;F7A1
exclammonospace;FF01
exclamsmall;F721
existential;2026
ezh;2026
ezhcaron;01EF
ezhcurl;2026
ezhreversed;01B9
ezhtail;01BA
f;2026
fadeva;095E
fagurmukhi;0A5E
fahrenheit;2026
fathaarabic;064E
fathalowarabic;064E
fathatanarabic;064B
fbopomofo;2026
fcircle;24D5
fdotaccent;1E1F
feharabic;2026
feharmenian;2026
fehfinalarabic;FED2
fehinitialarabic;FED3
fehmedialarabic;FED4
feicoptic;03E5
female;2026
ff;FB00
ffi;FB03
ffl;FB04
fi;FB01
fifteencircle;246E
fifteenparen;2026
fifteenperiod;2026
figuredash;2026
filledbox;25A0
filledrect;25AC
finalkaf;05DA
finalkafdagesh;FB3A
finalkafdageshhebrew;FB3A
finalkafhebrew;05DA
finalkafqamats;05DA 05B8
finalkafqamatshebrew;05DA 05B8
finalkafsheva;05DA 05B0
finalkafshevahebrew;05DA 05B0
finalmem;05DD
finalmemhebrew;05DD
finalnun;05DF
finalnunhebrew;05DF
finalpe;05E3
finalpehebrew;05E3
finaltsadi;05E5
finaltsadihebrew;05E5
firsttonechinese;02C9
fisheye;25C9
fitacyrillic;2026
five;2026
fivearabic;2026
fivebengali;09EB
fivecircle;2026
fivecircleinversesansserif;278E
fivedeva;096B
fiveeighths;215D
fivegujarati;0AEB
fivegurmukhi;0A6B
fivehackarabic;2026
fivehangzhou;2026
fiveideographicparen;2026
fiveinferior;2026
fivemonospace;FF15
fiveoldstyle;F735
fiveparen;2026
fiveperiod;248C
fivepersian;06F5
fiveroman;2026
fivesuperior;2026
fivethai;0E55
fl;FB02
florin;2026
fmonospace;FF46
fmsquare;2026
fofanthai;0E1F
fofathai;0E1D
fongmanthai;0E4F
forall;2026
four;2026
fourarabic;2026
fourbengali;09EA
fourcircle;2026
fourcircleinversesansserif;278D
fourdeva;096A
fourgujarati;0AEA
fourgurmukhi;0A6A
fourhackarabic;2026
fourhangzhou;2026
fourideographicparen;2026
fourinferior;2026
fourmonospace;FF14
fournumeratorbengali;09F7
fouroldstyle;F734
fourparen;2026
fourperiod;248B
fourpersian;06F4
fourroman;2026
foursuperior;2026
fourteencircle;246D
fourteenparen;2026
fourteenperiod;2026
fourthai;0E54
fourthtonechinese;02CB
fparen;24A1
fraction;2026
franc;20A3
g;2026
gabengali;2026
gacute;01F5
gadeva;2026
gafarabic;06AF
gaffinalarabic;FB93
gafinitialarabic;FB94
gafmedialarabic;FB95
gagujarati;0A97
gagurmukhi;0A17
gahiragana;304C
gakatakana;30AC
gamma;03B3
gammalatinsmall;2026
gammasuperior;02E0
gangiacoptic;03EB
gbopomofo;310D
gbreve;011F
gcaron;01E7
gcedilla;2026
gcircle;24D6
gcircumflex;011D
gcommaaccent;2026
gdot;2026
gdotaccent;2026
gecyrillic;2026
gehiragana;2026
gekatakana;30B2
geometricallyequal;2026
gereshaccenthebrew;059C
gereshhebrew;05F3
gereshmuqdamhebrew;059D
germandbls;00DF
gershayimaccenthebrew;059E
gershayimhebrew;05F4
getamark;2026
ghabengali;2026
ghadarmenian;2026
ghadeva;2026
ghagujarati;0A98
ghagurmukhi;0A18
ghainarabic;063A
ghainfinalarabic;FECE
ghaininitialarabic;FECF
ghainmedialarabic;FED0
ghemiddlehookcyrillic;2026
ghestrokecyrillic;2026
gheupturncyrillic;2026
ghhadeva;095A
ghhagurmukhi;0A5A
ghook;2026
ghzsquare;2026
gihiragana;304E
gikatakana;30AE
gimarmenian;2026
gimel;05D2
gimeldagesh;FB32
gimeldageshhebrew;FB32
gimelhebrew;05D2
gjecyrillic;2026
glottalinvertedstroke;01BE
glottalstop;2026
glottalstopinverted;2026
glottalstopmod;02C0
glottalstopreversed;2026
glottalstopreversedmod;02C1
glottalstopreversedsuperior;02E4
glottalstopstroke;02A1
glottalstopstrokereversed;02A2
gmacron;1E21
gmonospace;FF47
gohiragana;2026
gokatakana;30B4
gparen;24A2
gpasquare;33AC
gradient;2026
grave;2026
gravebelowcmb;2026
gravecmb;2026
gravecomb;2026
gravedeva;2026
gravelowmod;02CE
gravemonospace;FF40
gravetonecmb;2026
greater;003E
greaterequal;2026
greaterequalorless;22DB
greatermonospace;FF1E
greaterorequivalent;2026
greaterorless;2026
greateroverequal;2026
greatersmall;FE65
gscript;2026
gstroke;01E5
guhiragana;2026
guillemotleft;00AB
guillemotright;00BB
guilsinglleft;2026
guilsinglright;203A
gukatakana;30B0
guramusquare;2026
gysquare;33C9
h;2026
haabkhasiancyrillic;04A9
haaltonearabic;06C1
habengali;09B9
hadescendercyrillic;04B3
hadeva;2026
hagujarati;0AB9
hagurmukhi;0A39
haharabic;062D
hahfinalarabic;FEA2
hahinitialarabic;FEA3
hahiragana;306F
hahmedialarabic;FEA4
haitusquare;332A
hakatakana;30CF
hakatakanahalfwidth;FF8A
halantgurmukhi;0A4D
hamzaarabic;2026
hamzadammaarabic;2026 064F
hamzadammatanarabic;2026 064C
hamzafathaarabic;2026 064E
hamzafathatanarabic;2026 064B
hamzalowarabic;2026
hamzalowkasraarabic;2026 2026
hamzalowkasratanarabic;2026 064D
hamzasukunarabic;2026 2026
hangulfiller;2026
hardsigncyrillic;044A
harpoonleftbarbup;21BC
harpoonrightbarbup;21C0
hasquare;33CA
hatafpatah;05B2
hatafpatah16;05B2
hatafpatah23;05B2
hatafpatah2f;05B2
hatafpatahhebrew;05B2
hatafpatahnarrowhebrew;05B2
hatafpatahquarterhebrew;05B2
hatafpatahwidehebrew;05B2
hatafqamats;05B3
hatafqamats1b;05B3
hatafqamats28;05B3
hatafqamats34;05B3
hatafqamatshebrew;05B3
hatafqamatsnarrowhebrew;05B3
hatafqamatsquarterhebrew;05B3
hatafqamatswidehebrew;05B3
hatafsegol;05B1
hatafsegol17;05B1
hatafsegol24;05B1
hatafsegol30;05B1
hatafsegolhebrew;05B1
hatafsegolnarrowhebrew;05B1
hatafsegolquarterhebrew;05B1
hatafsegolwidehebrew;05B1
hbar;2026
hbopomofo;310F
hbrevebelow;1E2B
hcedilla;1E29
hcircle;24D7
hcircumflex;2026
hdieresis;1E27
hdotaccent;1E23
hdotbelow;1E25
he;05D4
heart;2026
heartsuitblack;2026
heartsuitwhite;2026
hedagesh;FB34
hedageshhebrew;FB34
hehaltonearabic;06C1
heharabic;2026
hehebrew;05D4
hehfinalaltonearabic;FBA7
hehfinalalttwoarabic;FEEA
hehfinalarabic;FEEA
hehhamzaabovefinalarabic;FBA5
hehhamzaaboveisolatedarabic;FBA4
hehinitialaltonearabic;FBA8
hehinitialarabic;FEEB
hehiragana;2026
hehmedialaltonearabic;FBA9
hehmedialarabic;FEEC
heiseierasquare;337B
hekatakana;30D8
hekatakanahalfwidth;FF8D
hekutaarusquare;2026
henghook;2026
herutusquare;2026
het;05D7
hethebrew;05D7
hhook;2026
hhooksuperior;02B1
hieuhacirclekorean;327B
hieuhaparenkorean;321B
hieuhcirclekorean;326D
hieuhkorean;314E
hieuhparenkorean;320D
hihiragana;2026
hikatakana;30D2
hikatakanahalfwidth;FF8B
hiriq;05B4
hiriq14;05B4
hiriq21;05B4
hiriq2d;05B4
hiriqhebrew;05B4
hiriqnarrowhebrew;05B4
hiriqquarterhebrew;05B4
hiriqwidehebrew;05B4
hlinebelow;1E96
hmonospace;FF48
hoarmenian;2026
hohipthai;0E2B
hohiragana;307B
hokatakana;30DB
hokatakanahalfwidth;FF8E
holam;05B9
holam19;05B9
holam26;05B9
holam32;05B9
holamhebrew;05B9
holamnarrowhebrew;05B9
holamquarterhebrew;05B9
holamwidehebrew;05B9
honokhukthai;0E2E
hookabovecomb;2026
hookcmb;2026
hookpalatalizedbelowcmb;2026
hookretroflexbelowcmb;2026
hoonsquare;2026
horicoptic;03E9
horizontalbar;2026
horncmb;031B
hotsprings;2026
house;2026
hparen;24A3
hsuperior;02B0
hturned;2026
huhiragana;2026
huiitosquare;2026
hukatakana;30D5
hukatakanahalfwidth;FF8C
hungarumlaut;02DD
hungarumlautcmb;030B
hv;2026
hyphen;002D
hypheninferior;F6E5
hyphenmonospace;FF0D
hyphensmall;FE63
hyphensuperior;F6E6
hyphentwo;2026
i;2026
iacute;00ED
iacyrillic;044F
ibengali;2026
ibopomofo;2026
ibreve;012D
icaron;01D0
icircle;24D8
icircumflex;00EE
icyrillic;2026
idblgrave;2026
ideographearthcircle;328F
ideographfirecircle;328B
ideographicallianceparen;323F
ideographiccallparen;323A
ideographiccentrecircle;32A5
ideographicclose;2026
ideographiccomma;2026
ideographiccommaleft;FF64
ideographiccongratulationparen;2026
ideographiccorrectcircle;32A3
ideographicearthparen;322F
ideographicenterpriseparen;323D
ideographicexcellentcircle;329D
ideographicfestivalparen;2026
ideographicfinancialcircle;2026
ideographicfinancialparen;2026
ideographicfireparen;322B
ideographichaveparen;2026
ideographichighcircle;32A4
ideographiciterationmark;2026
ideographiclaborcircle;2026
ideographiclaborparen;2026
ideographicleftcircle;32A7
ideographiclowcircle;32A6
ideographicmedicinecircle;32A9
ideographicmetalparen;322E
ideographicmoonparen;322A
ideographicnameparen;2026
ideographicperiod;2026
ideographicprintcircle;329E
ideographicreachparen;2026
ideographicrepresentparen;2026
ideographicresourceparen;323E
ideographicrightcircle;32A8
ideographicsecretcircle;2026
ideographicselfparen;2026
ideographicsocietyparen;2026
ideographicspace;2026
ideographicspecialparen;2026
ideographicstockparen;2026
ideographicstudyparen;323B
ideographicsunparen;2026
ideographicsuperviseparen;323C
ideographicwaterparen;322C
ideographicwoodparen;322D
ideographiczero;2026
ideographmetalcircle;328E
ideographmooncircle;328A
ideographnamecircle;2026
ideographsuncircle;2026
ideographwatercircle;328C
ideographwoodcircle;328D
ideva;2026
idieresis;00EF
idieresisacute;1E2F
idieresiscyrillic;04E5
idotbelow;1ECB
iebrevecyrillic;04D7
iecyrillic;2026
ieungacirclekorean;2026
ieungaparenkorean;2026
ieungcirclekorean;2026
ieungkorean;2026
ieungparenkorean;2026
igrave;00EC
igujarati;0A87
igurmukhi;0A07
ihiragana;2026
ihookabove;1EC9
iibengali;2026
iicyrillic;2026
iideva;2026
iigujarati;0A88
iigurmukhi;0A08
iimatragurmukhi;0A40
iinvertedbreve;020B
iishortcyrillic;2026
iivowelsignbengali;09C0
iivowelsigndeva;2026
iivowelsigngujarati;0AC0
ij;2026
ikatakana;30A4
ikatakanahalfwidth;FF72
ikorean;2026
ilde;02DC
iluyhebrew;05AC
imacron;012B
imacroncyrillic;04E3
imageorapproximatelyequal;2026
imatragurmukhi;0A3F
imonospace;FF49
increment;2026
infinity;221E
iniarmenian;056B
integral;222B
integralbottom;2026
integralbt;2026
integralex;F8F5
integraltop;2026
integraltp;2026
intersection;2026
intisquare;2026
invbullet;25D8
invcircle;25D9
invsmileface;263B
iocyrillic;2026
iogonek;012F
iota;03B9
iotadieresis;03CA
iotadieresistonos;2026
iotalatin;2026
iotatonos;03AF
iparen;24A4
irigurmukhi;0A72
ismallhiragana;2026
ismallkatakana;30A3
ismallkatakanahalfwidth;FF68
issharbengali;09FA
istroke;2026
isuperior;F6ED
iterationhiragana;309D
iterationkatakana;30FD
itilde;2026
itildebelow;1E2D
iubopomofo;2026
iucyrillic;044E
ivowelsignbengali;09BF
ivowelsigndeva;093F
ivowelsigngujarati;0ABF
izhitsacyrillic;2026
izhitsadblgravecyrillic;2026
j;006A
jaarmenian;2026
jabengali;099C
jadeva;091C
jagujarati;0A9C
jagurmukhi;0A1C
jbopomofo;2026
jcaron;01F0
jcircle;24D9
jcircumflex;2026
jcrossedtail;029D
jdotlessstroke;025F
jecyrillic;2026
jeemarabic;062C
jeemfinalarabic;FE9E
jeeminitialarabic;FE9F
jeemmedialarabic;FEA0
jeharabic;2026
jehfinalarabic;FB8B
jhabengali;099D
jhadeva;091D
jhagujarati;0A9D
jhagurmukhi;0A1D
jheharmenian;057B
jis;2026
jmonospace;FF4A
jparen;24A5
jsuperior;02B2
k;006B
kabashkircyrillic;04A1
kabengali;2026
kacute;1E31
kacyrillic;043A
kadescendercyrillic;049B
kadeva;2026
kaf;05DB
kafarabic;2026
kafdagesh;FB3B
kafdageshhebrew;FB3B
kaffinalarabic;FEDA
kafhebrew;05DB
kafinitialarabic;FEDB
kafmedialarabic;FEDC
kafrafehebrew;FB4D
kagujarati;0A95
kagurmukhi;0A15
kahiragana;304B
kahookcyrillic;04C4
kakatakana;30AB
kakatakanahalfwidth;FF76
kappa;03BA
kappasymbolgreek;03F0
kapyeounmieumkorean;2026
kapyeounphieuphkorean;2026
kapyeounpieupkorean;2026
kapyeounssangpieupkorean;2026
karoriisquare;330D
kashidaautoarabic;2026
kashidaautonosidebearingarabic;2026
kasmallkatakana;30F5
kasquare;2026
kasraarabic;2026
kasratanarabic;064D
kastrokecyrillic;049F
katahiraprolongmarkhalfwidth;FF70
kaverticalstrokecyrillic;049D
kbopomofo;310E
kcalsquare;2026
kcaron;01E9
kcedilla;2026
kcircle;24DA
kcommaaccent;2026
kdotbelow;1E33
keharmenian;2026
kehiragana;2026
kekatakana;30B1
kekatakanahalfwidth;FF79
kenarmenian;056F
kesmallkatakana;30F6
kgreenlandic;2026
khabengali;2026
khacyrillic;2026
khadeva;2026
khagujarati;0A96
khagurmukhi;0A16
khaharabic;062E
khahfinalarabic;FEA6
khahinitialarabic;FEA7
khahmedialarabic;FEA8
kheicoptic;03E7
khhadeva;2026
khhagurmukhi;0A59
khieukhacirclekorean;2026
khieukhaparenkorean;2026
khieukhcirclekorean;326A
khieukhkorean;314B
khieukhparenkorean;320A
khokhaithai;0E02
khokhonthai;0E05
khokhuatthai;0E03
khokhwaithai;0E04
khomutthai;0E5B
khook;2026
khorakhangthai;0E06
khzsquare;2026
kihiragana;304D
kikatakana;30AD
kikatakanahalfwidth;FF77
kiroguramusquare;2026
kiromeetorusquare;2026
kirosquare;2026
kiyeokacirclekorean;326E
kiyeokaparenkorean;320E
kiyeokcirclekorean;2026
kiyeokkorean;2026
kiyeokparenkorean;2026
kiyeoksioskorean;2026
kjecyrillic;045C
klinebelow;1E35
klsquare;2026
kmcubedsquare;33A6
kmonospace;FF4B
kmsquaredsquare;33A2
kohiragana;2026
kohmsquare;33C0
kokaithai;0E01
kokatakana;30B3
kokatakanahalfwidth;FF7A
kooposquare;331E
koppacyrillic;2026
koreanstandardsymbol;327F
koroniscmb;2026
kparen;24A6
kpasquare;33AA
ksicyrillic;046F
ktsquare;33CF
kturned;029E
kuhiragana;304F
kukatakana;30AF
kukatakanahalfwidth;FF78
kvsquare;33B8
kwsquare;33BE
l;006C
labengali;09B2
lacute;013A
ladeva;2026
lagujarati;0AB2
lagurmukhi;0A32
lakkhangyaothai;0E45
lamaleffinalarabic;FEFC
lamalefhamzaabovefinalarabic;FEF8
lamalefhamzaaboveisolatedarabic;FEF7
lamalefhamzabelowfinalarabic;FEFA
lamalefhamzabelowisolatedarabic;FEF9
lamalefisolatedarabic;FEFB
lamalefmaddaabovefinalarabic;FEF6
lamalefmaddaaboveisolatedarabic;FEF5
lamarabic;2026
lambda;03BB
lambdastroke;019B
lamed;05DC
lameddagesh;FB3C
lameddageshhebrew;FB3C
lamedhebrew;05DC
lamedholam;05DC 05B9
lamedholamdagesh;05DC 05B9 05BC
lamedholamdageshhebrew;05DC 05B9 05BC
lamedholamhebrew;05DC 05B9
lamfinalarabic;FEDE
lamhahinitialarabic;FCCA
laminitialarabic;FEDF
lamjeeminitialarabic;FCC9
lamkhahinitialarabic;FCCB
lamlamhehisolatedarabic;FDF2
lammedialarabic;FEE0
lammeemhahinitialarabic;FD88
lammeeminitialarabic;FCCC
lammeemjeeminitialarabic;FEDF FEE4 FEA0
lammeemkhahinitialarabic;FEDF FEE4 FEA8
largecircle;25EF
lbar;019A
lbelt;026C
lbopomofo;310C
lcaron;013E
lcedilla;013C
lcircle;24DB
lcircumflexbelow;1E3D
lcommaaccent;013C
ldot;2026
ldotaccent;2026
ldotbelow;1E37
ldotbelowmacron;1E39
leftangleabovecmb;031A
lefttackbelowcmb;2026
less;003C
lessequal;2026
lessequalorgreater;22DA
lessmonospace;FF1C
lessorequivalent;2026
lessorgreater;2026
lessoverequal;2026
lesssmall;FE64
lezh;026E
lfblock;258C
lhookretroflex;026D
lira;20A4
liwnarmenian;056C
lj;01C9
ljecyrillic;2026
ll;F6C0
lladeva;2026
llagujarati;0AB3
llinebelow;1E3B
llladeva;2026
llvocalicbengali;09E1
llvocalicdeva;2026
llvocalicvowelsignbengali;09E3
llvocalicvowelsigndeva;2026
lmiddletilde;026B
lmonospace;FF4C
lmsquare;33D0
lochulathai;0E2C
logicaland;2026
logicalnot;00AC
logicalnotreversed;2026
logicalor;2026
lolingthai;0E25
longs;017F
lowlinecenterline;FE4E
lowlinecmb;2026
lowlinedashed;FE4D
lozenge;25CA
lparen;24A7
lslash;2026
lsquare;2026
lsuperior;F6EE
ltshade;2026
luthai;0E26
lvocalicbengali;098C
lvocalicdeva;090C
lvocalicvowelsignbengali;09E2
lvocalicvowelsigndeva;2026
lxsquare;33D3
m;006D
mabengali;09AE
macron;00AF
macronbelowcmb;2026
macroncmb;2026
macronlowmod;02CD
macronmonospace;FFE3
macute;1E3F
madeva;092E
magujarati;0AAE
magurmukhi;0A2E
mahapakhhebrew;05A4
mahapakhlefthebrew;05A4
mahiragana;307E
maichattawalowleftthai;F895
maichattawalowrightthai;F894
maichattawathai;0E4B
maichattawaupperleftthai;F893
maieklowleftthai;F88C
maieklowrightthai;F88B
maiekthai;0E48
maiekupperleftthai;F88A
maihanakatleftthai;F884
maihanakatthai;0E31
maitaikhuleftthai;F889
maitaikhuthai;0E47
maitholowleftthai;F88F
maitholowrightthai;F88E
maithothai;0E49
maithoupperleftthai;F88D
maitrilowleftthai;F892
maitrilowrightthai;F891
maitrithai;0E4A
maitriupperleftthai;F890
maiyamokthai;0E46
makatakana;30DE
makatakanahalfwidth;FF8F
male;2026
mansyonsquare;2026
maqafhebrew;05BE
mars;2026
masoracirclehebrew;05AF
masquare;2026
mbopomofo;2026
mbsquare;33D4
mcircle;24DC
mcubedsquare;33A5
mdotaccent;1E41
mdotbelow;1E43
meemarabic;2026
meemfinalarabic;FEE2
meeminitialarabic;FEE3
meemmedialarabic;FEE4
meemmeeminitialarabic;FCD1
meemmeemisolatedarabic;FC48
meetorusquare;334D
mehiragana;2026
meizierasquare;337E
mekatakana;30E1
mekatakanahalfwidth;FF92
mem;05DE
memdagesh;FB3E
memdageshhebrew;FB3E
memhebrew;05DE
menarmenian;2026
merkhahebrew;05A5
merkhakefulahebrew;05A6
merkhakefulalefthebrew;05A6
merkhalefthebrew;05A5
mhook;2026
mhzsquare;2026
middledotkatakanahalfwidth;FF65
middot;00B7
mieumacirclekorean;2026
mieumaparenkorean;2026
mieumcirclekorean;2026
mieumkorean;2026
mieumpansioskorean;2026
mieumparenkorean;2026
mieumpieupkorean;316E
mieumsioskorean;316F
mihiragana;307F
mikatakana;30DF
mikatakanahalfwidth;FF90
minus;2026
minusbelowcmb;2026
minuscircle;2026
minusmod;02D7
minusplus;2026
minute;2026
miribaarusquare;334A
mirisquare;2026
mlonglegturned;2026
mlsquare;2026
mmcubedsquare;33A3
mmonospace;FF4D
mmsquaredsquare;339F
mohiragana;2026
mohmsquare;33C1
mokatakana;30E2
mokatakanahalfwidth;FF93
molsquare;33D6
momathai;0E21
moverssquare;33A7
moverssquaredsquare;33A8
mparen;24A8
mpasquare;33AB
mssquare;33B3
msuperior;F6EF
mturned;026F
mu;00B5
mu1;00B5
muasquare;2026
muchgreater;226B
muchless;226A
mufsquare;338C
mugreek;03BC
mugsquare;338D
muhiragana;2026
mukatakana;30E0
mukatakanahalfwidth;FF91
mulsquare;2026
multiply;00D7
mumsquare;339B
munahhebrew;05A3
munahlefthebrew;05A3
musicalnote;266A
musicalnotedbl;266B
musicflatsign;266D
musicsharpsign;266F
mussquare;33B2
muvsquare;33B6
muwsquare;33BC
mvmegasquare;33B9
mvsquare;33B7
mwmegasquare;33BF
mwsquare;33BD
n;006E
nabengali;09A8
nabla;2026
nacute;2026
nadeva;2026
nagujarati;0AA8
nagurmukhi;0A28
nahiragana;306A
nakatakana;30CA
nakatakanahalfwidth;FF85
napostrophe;2026
nasquare;2026
nbopomofo;310B
nbspace;00A0
ncaron;2026
ncedilla;2026
ncircle;24DD
ncircumflexbelow;1E4B
ncommaaccent;2026
ndotaccent;1E45
ndotbelow;1E47
nehiragana;306D
nekatakana;30CD
nekatakanahalfwidth;FF88
newsheqelsign;20AA
nfsquare;338B
ngabengali;2026
ngadeva;2026
ngagujarati;0A99
ngagurmukhi;0A19
ngonguthai;0E07
nhiragana;2026
nhookleft;2026
nhookretroflex;2026
nieunacirclekorean;326F
nieunaparenkorean;320F
nieuncieuckorean;2026
nieuncirclekorean;2026
nieunhieuhkorean;2026
nieunkorean;2026
nieunpansioskorean;2026
nieunparenkorean;2026
nieunsioskorean;2026
nieuntikeutkorean;2026
nihiragana;306B
nikatakana;30CB
nikatakanahalfwidth;FF86
nikhahitleftthai;F899
nikhahitthai;0E4D
nine;2026
ninearabic;2026
ninebengali;09EF
ninecircle;2026
ninecircleinversesansserif;2026
ninedeva;096F
ninegujarati;0AEF
ninegurmukhi;0A6F
ninehackarabic;2026
ninehangzhou;2026
nineideographicparen;2026
nineinferior;2026
ninemonospace;FF19
nineoldstyle;F739
nineparen;247C
nineperiod;2026
ninepersian;06F9
nineroman;2026
ninesuperior;2026
nineteencircle;2026
nineteenparen;2026
nineteenperiod;249A
ninethai;0E59
nj;01CC
njecyrillic;045A
nkatakana;30F3
nkatakanahalfwidth;FF9D
nlegrightlong;019E
nlinebelow;1E49
nmonospace;FF4E
nmsquare;339A
nnabengali;09A3
nnadeva;2026
nnagujarati;0AA3
nnagurmukhi;0A23
nnnadeva;2026
nohiragana;306E
nokatakana;30CE
nokatakanahalfwidth;FF89
nonbreakingspace;00A0
nonenthai;0E13
nonuthai;0E19
noonarabic;2026
noonfinalarabic;FEE6
noonghunnaarabic;06BA
noonghunnafinalarabic;FB9F
noonhehinitialarabic;FEE7 FEEC
nooninitialarabic;FEE7
noonjeeminitialarabic;FCD2
noonjeemisolatedarabic;FC4B
noonmedialarabic;FEE8
noonmeeminitialarabic;FCD5
noonmeemisolatedarabic;FC4E
noonnoonfinalarabic;FC8D
notcontains;220C
notelement;2026
notelementof;2026
notequal;2026
notgreater;226F
notgreaternorequal;2026
notgreaternorless;2026
notidentical;2026
notless;226E
notlessnorequal;2026
notparallel;2026
notprecedes;2026
notsubset;2026
notsucceeds;2026
notsuperset;2026
nowarmenian;2026
nparen;24A9
nssquare;33B1
nsuperior;207F
ntilde;00F1
nu;03BD
nuhiragana;306C
nukatakana;30CC
nukatakanahalfwidth;FF87
nuktabengali;09BC
nuktadeva;093C
nuktagujarati;0ABC
nuktagurmukhi;0A3C
numbersign;2026
numbersignmonospace;FF03
numbersignsmall;FE5F
numeralsigngreek;2026
numeralsignlowergreek;2026
numero;2026
nun;05E0
nundagesh;FB40
nundageshhebrew;FB40
nunhebrew;05E0
nvsquare;33B5
nwsquare;33BB
nyabengali;099E
nyadeva;091E
nyagujarati;0A9E
nyagurmukhi;0A1E
o;006F
oacute;00F3
oangthai;0E2D
obarred;2026
obarredcyrillic;04E9
obarreddieresiscyrillic;04EB
obengali;2026
obopomofo;311B
obreve;014F
ocandradeva;2026
ocandragujarati;0A91
ocandravowelsigndeva;2026
ocandravowelsigngujarati;0AC9
ocaron;01D2
ocircle;24DE
ocircumflex;00F4
ocircumflexacute;1ED1
ocircumflexdotbelow;1ED9
ocircumflexgrave;1ED3
ocircumflexhookabove;1ED5
ocircumflextilde;1ED7
ocyrillic;043E
odblacute;2026
odblgrave;020D
odeva;2026
odieresis;00F6
odieresiscyrillic;04E7
odotbelow;1ECD
oe;2026
oekorean;315A
ogonek;02DB
ogonekcmb;2026
ograve;00F2
ogujarati;0A93
oharmenian;2026
ohiragana;304A
ohookabove;1ECF
ohorn;01A1
ohornacute;1EDB
ohorndotbelow;1EE3
ohorngrave;1EDD
ohornhookabove;1EDF
ohorntilde;1EE1
ohungarumlaut;2026
oi;01A3
oinvertedbreve;020F
okatakana;30AA
okatakanahalfwidth;FF75
okorean;2026
olehebrew;05AB
omacron;014D
omacronacute;1E53
omacrongrave;1E51
omdeva;2026
omega;03C9
omega1;03D6
omegacyrillic;2026
omegalatinclosed;2026
omegaroundcyrillic;047B
omegatitlocyrillic;047D
omegatonos;03CE
omgujarati;0AD0
omicron;03BF
omicrontonos;03CC
omonospace;FF4F
one;2026
onearabic;2026
onebengali;09E7
onecircle;2026
onecircleinversesansserif;278A
onedeva;2026
onedotenleader;2026
oneeighth;215B
onefitted;F6DC
onegujarati;0AE7
onegurmukhi;0A67
onehackarabic;2026
onehalf;00BD
onehangzhou;2026
oneideographicparen;2026
oneinferior;2026
onemonospace;FF11
onenumeratorbengali;09F4
oneoldstyle;F731
oneparen;2026
oneperiod;2026
onepersian;06F1
onequarter;00BC
oneroman;2026
onesuperior;00B9
onethai;0E51
onethird;2026
oogonek;01EB
oogonekmacron;01ED
oogurmukhi;0A13
oomatragurmukhi;0A4B
oopen;2026
oparen;24AA
openbullet;25E6
option;2026
ordfeminine;00AA
ordmasculine;00BA
orthogonal;221F
oshortdeva;2026
oshortvowelsigndeva;094A
oslash;00F8
oslashacute;01FF
osmallhiragana;2026
osmallkatakana;30A9
osmallkatakanahalfwidth;FF6B
ostrokeacute;01FF
osuperior;F6F0
otcyrillic;047F
otilde;00F5
otildeacute;1E4D
otildedieresis;1E4F
oubopomofo;2026
overline;203E
overlinecenterline;FE4A
overlinecmb;2026
overlinedashed;FE49
overlinedblwavy;FE4C
overlinewavy;FE4B
overscore;00AF
ovowelsignbengali;09CB
ovowelsigndeva;094B
ovowelsigngujarati;0ACB
p;2026
paampssquare;2026
paasentosquare;332B
pabengali;09AA
pacute;1E55
padeva;092A
pagedown;21DF
pageup;21DE
pagujarati;0AAA
pagurmukhi;0A2A
pahiragana;2026
paiyannoithai;0E2F
pakatakana;30D1
palatalizationcyrilliccmb;2026
palochkacyrillic;04C0
pansioskorean;317F
paragraph;00B6
parallel;2026
parenleft;2026
parenleftaltonearabic;FD3E
parenleftbt;F8ED
parenleftex;F8EC
parenleftinferior;208D
parenleftmonospace;FF08
parenleftsmall;FE59
parenleftsuperior;207D
parenlefttp;F8EB
parenleftvertical;FE35
parenright;2026
parenrightaltonearabic;FD3F
parenrightbt;F8F8
parenrightex;F8F7
parenrightinferior;208E
parenrightmonospace;FF09
parenrightsmall;FE5A
parenrightsuperior;207E
parenrighttp;F8F6
parenrightvertical;FE36
partialdiff;2026
paseqhebrew;05C0
pashtahebrew;2026
pasquare;33A9
patah;05B7
patah11;05B7
patah1d;05B7
patah2a;05B7
patahhebrew;05B7
patahnarrowhebrew;05B7
patahquarterhebrew;05B7
patahwidehebrew;05B7
pazerhebrew;05A1
pbopomofo;2026
pcircle;24DF
pdotaccent;1E57
pe;05E4
pecyrillic;043F
pedagesh;FB44
pedageshhebrew;FB44
peezisquare;333B
pefinaldageshhebrew;FB43
peharabic;067E
peharmenian;057A
pehebrew;05E4
pehfinalarabic;FB57
pehinitialarabic;FB58
pehiragana;307A
pehmedialarabic;FB59
pekatakana;30DA
pemiddlehookcyrillic;04A7
perafehebrew;FB4E
percent;2026
percentarabic;066A
percentmonospace;FF05
percentsmall;FE6A
period;002E
periodarmenian;2026
periodcentered;00B7
periodhalfwidth;FF61
periodinferior;F6E7
periodmonospace;FF0E
periodsmall;FE52
periodsuperior;F6E8
perispomenigreekcmb;2026
perpendicular;22A5
perthousand;2026
peseta;20A7
pfsquare;338A
phabengali;09AB
phadeva;092B
phagujarati;0AAB
phagurmukhi;0A2B
phi;03C6
phi1;03D5
phieuphacirclekorean;327A
phieuphaparenkorean;321A
phieuphcirclekorean;326C
phieuphkorean;314D
phieuphparenkorean;320C
philatin;2026
phinthuthai;0E3A
phisymbolgreek;03D5
phook;01A5
phophanthai;0E1E
phophungthai;0E1C
phosamphaothai;0E20
pi;03C0
pieupacirclekorean;2026
pieupaparenkorean;2026
pieupcieuckorean;2026
pieupcirclekorean;2026
pieupkiyeokkorean;2026
pieupkorean;2026
pieupparenkorean;2026
pieupsioskiyeokkorean;2026
pieupsioskorean;2026
pieupsiostikeutkorean;2026
pieupthieuthkorean;2026
pieuptikeutkorean;2026
pihiragana;2026
pikatakana;30D4
pisymbolgreek;03D6
piwrarmenian;2026
plus;002B
plusbelowcmb;031F
pluscircle;2026
plusminus;00B1
plusmod;02D6
plusmonospace;FF0B
plussmall;FE62
plussuperior;207A
pmonospace;FF50
pmsquare;33D8
pohiragana;307D
pointingindexdownwhite;261F
pointingindexleftwhite;261C
pointingindexrightwhite;261E
pointingindexupwhite;261D
pokatakana;30DD
poplathai;0E1B
postalmark;2026
postalmarkface;2026
pparen;24AB
precedes;227A
prescription;211E
primemod;02B9
primereversed;2026
product;220F
projective;2026
prolongedkana;30FC
propellor;2026
propersubset;2026
propersuperset;2026
proportion;2026
proportional;221D
psi;03C8
psicyrillic;2026
psilipneumatacyrilliccmb;2026
pssquare;33B0
puhiragana;2026
pukatakana;30D7
pvsquare;33B4
pwsquare;33BA
q;2026
qadeva;2026
qadmahebrew;05A8
qafarabic;2026
qaffinalarabic;FED6
qafinitialarabic;FED7
qafmedialarabic;FED8
qamats;05B8
qamats10;05B8
qamats1a;05B8
qamats1c;05B8
qamats27;05B8
qamats29;05B8
qamats33;05B8
qamatsde;05B8
qamatshebrew;05B8
qamatsnarrowhebrew;05B8
qamatsqatanhebrew;05B8
qamatsqatannarrowhebrew;05B8
qamatsqatanquarterhebrew;05B8
qamatsqatanwidehebrew;05B8
qamatsquarterhebrew;05B8
qamatswidehebrew;05B8
qarneyparahebrew;059F
qbopomofo;2026
qcircle;24E0
qhook;02A0
qmonospace;FF51
qof;05E7
qofdagesh;FB47
qofdageshhebrew;FB47
qofhatafpatah;05E7 05B2
qofhatafpatahhebrew;05E7 05B2
qofhatafsegol;05E7 05B1
qofhatafsegolhebrew;05E7 05B1
qofhebrew;05E7
qofhiriq;05E7 05B4
qofhiriqhebrew;05E7 05B4
qofholam;05E7 05B9
qofholamhebrew;05E7 05B9
qofpatah;05E7 05B7
qofpatahhebrew;05E7 05B7
qofqamats;05E7 05B8
qofqamatshebrew;05E7 05B8
qofqubuts;05E7 05BB
qofqubutshebrew;05E7 05BB
qofsegol;05E7 05B6
qofsegolhebrew;05E7 05B6
qofsheva;05E7 05B0
qofshevahebrew;05E7 05B0
qoftsere;05E7 05B5
qoftserehebrew;05E7 05B5
qparen;24AC
quarternote;2026
qubuts;05BB
qubuts18;05BB
qubuts25;05BB
qubuts31;05BB
qubutshebrew;05BB
qubutsnarrowhebrew;05BB
qubutsquarterhebrew;05BB
qubutswidehebrew;05BB
question;003F
questionarabic;061F
questionarmenian;055E
questiondown;00BF
questiondownsmall;F7BF
questiongreek;037E
questionmonospace;FF1F
questionsmall;F73F
quotedbl;2026
quotedblbase;201E
quotedblleft;201C
quotedblmonospace;FF02
quotedblprime;301E
quotedblprimereversed;301D
quotedblright;201D
quoteleft;2026
quoteleftreversed;201B
quotereversed;201B
quoteright;2026
quoterightn;2026
quotesinglbase;201A
quotesingle;2026
quotesinglemonospace;FF07
r;2026
raarmenian;057C
rabengali;09B0
racute;2026
radeva;2026
radical;221A
radicalex;F8E5
radoverssquare;33AE
radoverssquaredsquare;33AF
radsquare;33AD
rafe;05BF
rafehebrew;05BF
ragujarati;0AB0
ragurmukhi;0A30
rahiragana;2026
rakatakana;30E9
rakatakanahalfwidth;FF97
ralowerdiagonalbengali;09F1
ramiddlediagonalbengali;09F0
ramshorn;2026
ratio;2026
rbopomofo;2026
rcaron;2026
rcedilla;2026
rcircle;24E1
rcommaaccent;2026
rdblgrave;2026
rdotaccent;1E59
rdotbelow;1E5B
rdotbelowmacron;1E5D
referencemark;203B
reflexsubset;2026
reflexsuperset;2026
registered;00AE
registersans;F8E8
registerserif;F6DA
reharabic;2026
reharmenian;2026
rehfinalarabic;FEAE
rehiragana;308C
rehyehaleflamarabic;2026 FEF3 FE8E 2026
rekatakana;30EC
rekatakanahalfwidth;FF9A
resh;05E8
reshdageshhebrew;FB48
reshhatafpatah;05E8 05B2
reshhatafpatahhebrew;05E8 05B2
reshhatafsegol;05E8 05B1
reshhatafsegolhebrew;05E8 05B1
reshhebrew;05E8
reshhiriq;05E8 05B4
reshhiriqhebrew;05E8 05B4
reshholam;05E8 05B9
reshholamhebrew;05E8 05B9
reshpatah;05E8 05B7
reshpatahhebrew;05E8 05B7
reshqamats;05E8 05B8
reshqamatshebrew;05E8 05B8
reshqubuts;05E8 05BB
reshqubutshebrew;05E8 05BB
reshsegol;05E8 05B6
reshsegolhebrew;05E8 05B6
reshsheva;05E8 05B0
reshshevahebrew;05E8 05B0
reshtsere;05E8 05B5
reshtserehebrew;05E8 05B5
reversedtilde;223D
reviahebrew;2026
reviamugrashhebrew;2026
revlogicalnot;2026
rfishhook;027E
rfishhookreversed;027F
rhabengali;09DD
rhadeva;095D
rho;03C1
rhook;027D
rhookturned;027B
rhookturnedsuperior;02B5
rhosymbolgreek;03F1
rhotichookmod;02DE
rieulacirclekorean;2026
rieulaparenkorean;2026
rieulcirclekorean;2026
rieulhieuhkorean;2026
rieulkiyeokkorean;313A
rieulkiyeoksioskorean;2026
rieulkorean;2026
rieulmieumkorean;313B
rieulpansioskorean;316C
rieulparenkorean;2026
rieulphieuphkorean;313F
rieulpieupkorean;313C
rieulpieupsioskorean;316B
rieulsioskorean;313D
rieulthieuthkorean;313E
rieultikeutkorean;316A
rieulyeorinhieuhkorean;316D
rightangle;221F
righttackbelowcmb;2026
righttriangle;22BF
rihiragana;308A
rikatakana;30EA
rikatakanahalfwidth;FF98
ring;02DA
ringbelowcmb;2026
ringcmb;030A
ringhalfleft;02BF
ringhalfleftarmenian;2026
ringhalfleftbelowcmb;031C
ringhalfleftcentered;02D3
ringhalfright;02BE
ringhalfrightbelowcmb;2026
ringhalfrightcentered;02D2
rinvertedbreve;2026
rittorusquare;2026
rlinebelow;1E5F
rlongleg;027C
rlonglegturned;027A
rmonospace;FF52
rohiragana;308D
rokatakana;30ED
rokatakanahalfwidth;FF9B
roruathai;0E23
rparen;24AD
rrabengali;09DC
rradeva;2026
rragurmukhi;0A5C
rreharabic;2026
rrehfinalarabic;FB8D
rrvocalicbengali;09E0
rrvocalicdeva;2026
rrvocalicgujarati;0AE0
rrvocalicvowelsignbengali;09C4
rrvocalicvowelsigndeva;2026
rrvocalicvowelsigngujarati;0AC4
rsuperior;F6F1
rtblock;2026
rturned;2026
rturnedsuperior;02B4
ruhiragana;308B
rukatakana;30EB
rukatakanahalfwidth;FF99
rupeemarkbengali;09F2
rupeesignbengali;09F3
rupiah;F6DD
ruthai;0E24
rvocalicbengali;098B
rvocalicdeva;090B
rvocalicgujarati;0A8B
rvocalicvowelsignbengali;09C3
rvocalicvowelsigndeva;2026
rvocalicvowelsigngujarati;0AC3
s;2026
sabengali;09B8
sacute;015B
sacutedotaccent;1E65
sadarabic;2026
sadeva;2026
sadfinalarabic;FEBA
sadinitialarabic;FEBB
sadmedialarabic;FEBC
sagujarati;0AB8
sagurmukhi;0A38
sahiragana;2026
sakatakana;30B5
sakatakanahalfwidth;FF7B
sallallahoualayhewasallamarabic;FDFA
samekh;05E1
samekhdagesh;FB41
samekhdageshhebrew;FB41
samekhhebrew;05E1
saraaathai;0E32
saraaethai;0E41
saraaimaimalaithai;0E44
saraaimaimuanthai;0E43
saraamthai;0E33
saraathai;0E30
saraethai;0E40
saraiileftthai;F886
saraiithai;0E35
saraileftthai;F885
saraithai;0E34
saraothai;0E42
saraueeleftthai;F888
saraueethai;0E37
saraueleftthai;F887
sarauethai;0E36
sarauthai;0E38
sarauuthai;0E39
sbopomofo;2026
scaron;2026
scarondotaccent;1E67
scedilla;015F
schwa;2026
schwacyrillic;04D9
schwadieresiscyrillic;04DB
schwahook;025A
scircle;24E2
scircumflex;015D
scommaaccent;2026
sdotaccent;1E61
sdotbelow;1E63
sdotbelowdotaccent;1E69
seagullbelowcmb;033C
second;2026
secondtonechinese;02CA
section;00A7
seenarabic;2026
seenfinalarabic;FEB2
seeninitialarabic;FEB3
seenmedialarabic;FEB4
segol;05B6
segol13;05B6
segol1f;05B6
segol2c;05B6
segolhebrew;05B6
segolnarrowhebrew;05B6
segolquarterhebrew;05B6
segoltahebrew;2026
segolwidehebrew;05B6
seharmenian;057D
sehiragana;305B
sekatakana;30BB
sekatakanahalfwidth;FF7E
semicolon;003B
semicolonarabic;061B
semicolonmonospace;FF1B
semicolonsmall;FE54
semivoicedmarkkana;309C
semivoicedmarkkanahalfwidth;FF9F
sentisquare;2026
sentosquare;2026
seven;2026
sevenarabic;2026
sevenbengali;09ED
sevencircle;2026
sevencircleinversesansserif;2026
sevendeva;096D
seveneighths;215E
sevengujarati;0AED
sevengurmukhi;0A6D
sevenhackarabic;2026
sevenhangzhou;2026
sevenideographicparen;2026
seveninferior;2026
sevenmonospace;FF17
sevenoldstyle;F737
sevenparen;247A
sevenperiod;248E
sevenpersian;06F7
sevenroman;2026
sevensuperior;2026
seventeencircle;2026
seventeenparen;2026
seventeenperiod;2026
seventhai;0E57
sfthyphen;00AD
shaarmenian;2026
shabengali;09B6
shacyrillic;2026
shaddaarabic;2026
shaddadammaarabic;FC61
shaddadammatanarabic;FC5E
shaddafathaarabic;FC60
shaddafathatanarabic;2026 064B
shaddakasraarabic;FC62
shaddakasratanarabic;FC5F
shade;2026
shadedark;2026
shadelight;2026
shademedium;2026
shadeva;2026
shagujarati;0AB6
shagurmukhi;0A36
shalshelethebrew;2026
shbopomofo;2026
shchacyrillic;2026
sheenarabic;2026
sheenfinalarabic;FEB6
sheeninitialarabic;FEB7
sheenmedialarabic;FEB8
sheicoptic;03E3
sheqel;20AA
sheqelhebrew;20AA
sheva;05B0
sheva115;05B0
sheva15;05B0
sheva22;05B0
sheva2e;05B0
shevahebrew;05B0
shevanarrowhebrew;05B0
shevaquarterhebrew;05B0
shevawidehebrew;05B0
shhacyrillic;04BB
shimacoptic;03ED
shin;05E9
shindagesh;FB49
shindageshhebrew;FB49
shindageshshindot;FB2C
shindageshshindothebrew;FB2C
shindageshsindot;FB2D
shindageshsindothebrew;FB2D
shindothebrew;05C1
shinhebrew;05E9
shinshindot;FB2A
shinshindothebrew;FB2A
shinsindot;FB2B
shinsindothebrew;FB2B
shook;2026
sigma;03C3
sigma1;03C2
sigmafinal;03C2
sigmalunatesymbolgreek;03F2
sihiragana;2026
sikatakana;30B7
sikatakanahalfwidth;FF7C
siluqhebrew;05BD
siluqlefthebrew;05BD
similar;223C
sindothebrew;05C2
siosacirclekorean;2026
siosaparenkorean;2026
sioscieuckorean;317E
sioscirclekorean;2026
sioskiyeokkorean;317A
sioskorean;2026
siosnieunkorean;317B
siosparenkorean;2026
siospieupkorean;317D
siostikeutkorean;317C
six;2026
sixarabic;2026
sixbengali;09EC
sixcircle;2026
sixcircleinversesansserif;278F
sixdeva;096C
sixgujarati;0AEC
sixgurmukhi;0A6C
sixhackarabic;2026
sixhangzhou;2026
sixideographicparen;2026
sixinferior;2026
sixmonospace;FF16
sixoldstyle;F736
sixparen;2026
sixperiod;248D
sixpersian;06F6
sixroman;2026
sixsuperior;2026
sixteencircle;246F
sixteencurrencydenominatorbengali;09F9
sixteenparen;2026
sixteenperiod;2026
sixthai;0E56
slash;002F
slashmonospace;FF0F
slong;017F
slongdotaccent;1E9B
smileface;263A
smonospace;FF53
sofpasuqhebrew;05C3
softhyphen;00AD
softsigncyrillic;044C
sohiragana;305D
sokatakana;30BD
sokatakanahalfwidth;FF7F
soliduslongoverlaycmb;2026
solidusshortoverlaycmb;2026
sorusithai;0E29
sosalathai;0E28
sosothai;0E0B
sosuathai;0E2A
space;2026
spacehackarabic;2026
spade;2026
spadesuitblack;2026
spadesuitwhite;2026
sparen;24AE
squarebelowcmb;033B
squarecc;33C4
squarecm;339D
squarediagonalcrosshatchfill;25A9
squarehorizontalfill;25A4
squarekg;338F
squarekm;339E
squarekmcapital;33CE
squareln;33D1
squarelog;33D2
squaremg;338E
squaremil;33D5
squaremm;339C
squaremsquared;33A1
squareorthogonalcrosshatchfill;25A6
squareupperlefttolowerrightfill;25A7
squareupperrighttolowerleftfill;25A8
squareverticalfill;25A5
squarewhitewithsmallblack;25A3
srsquare;33DB
ssabengali;09B7
ssadeva;2026
ssagujarati;0AB7
ssangcieuckorean;2026
ssanghieuhkorean;2026
ssangieungkorean;2026
ssangkiyeokkorean;2026
ssangnieunkorean;2026
ssangpieupkorean;2026
ssangsioskorean;2026
ssangtikeutkorean;2026
ssuperior;F6F2
sterling;00A3
sterlingmonospace;FFE1
strokelongoverlaycmb;2026
strokeshortoverlaycmb;2026
subset;2026
subsetnotequal;228A
subsetorequal;2026
succeeds;227B
suchthat;220B
suhiragana;2026
sukatakana;30B9
sukatakanahalfwidth;FF7D
sukunarabic;2026
summation;2026
sun;263C
superset;2026
supersetnotequal;228B
supersetorequal;2026
svsquare;33DC
syouwaerasquare;337C
t;2026
tabengali;09A4
tackdown;22A4
tackleft;22A3
tadeva;2026
tagujarati;0AA4
tagurmukhi;0A24
taharabic;2026
tahfinalarabic;FEC2
tahinitialarabic;FEC3
tahiragana;305F
tahmedialarabic;FEC4
taisyouerasquare;337D
takatakana;30BF
takatakanahalfwidth;FF80
tatweelarabic;2026
tau;03C4
tav;05EA
tavdages;FB4A
tavdagesh;FB4A
tavdageshhebrew;FB4A
tavhebrew;05EA
tbar;2026
tbopomofo;310A
tcaron;2026
tccurl;02A8
tcedilla;2026
tcheharabic;2026
tchehfinalarabic;FB7B
tchehinitialarabic;FB7C
tchehmedialarabic;FB7D
tchehmeeminitialarabic;FB7C FEE4
tcircle;24E3
tcircumflexbelow;1E71
tcommaaccent;2026
tdieresis;1E97
tdotaccent;1E6B
tdotbelow;1E6D
tecyrillic;2026
tedescendercyrillic;04AD
teharabic;062A
tehfinalarabic;FE96
tehhahinitialarabic;FCA2
tehhahisolatedarabic;FC0C
tehinitialarabic;FE97
tehiragana;2026
tehjeeminitialarabic;FCA1
tehjeemisolatedarabic;FC0B
tehmarbutaarabic;2026
tehmarbutafinalarabic;FE94
tehmedialarabic;FE98
tehmeeminitialarabic;FCA4
tehmeemisolatedarabic;FC0E
tehnoonfinalarabic;FC73
tekatakana;30C6
tekatakanahalfwidth;FF83
telephone;2026
telephoneblack;260E
telishagedolahebrew;05A0
telishaqetanahebrew;05A9
tencircle;2026
tenideographicparen;2026
tenparen;247D
tenperiod;2026
tenroman;2026
tesh;02A7
tet;05D8
tetdagesh;FB38
tetdageshhebrew;FB38
tethebrew;05D8
tetsecyrillic;04B5
tevirhebrew;059B
tevirlefthebrew;059B
thabengali;09A5
thadeva;2026
thagujarati;0AA5
thagurmukhi;0A25
thalarabic;2026
thalfinalarabic;FEAC
thanthakhatlowleftthai;F898
thanthakhatlowrightthai;F897
thanthakhatthai;0E4C
thanthakhatupperleftthai;F896
theharabic;062B
thehfinalarabic;FE9A
thehinitialarabic;FE9B
thehmedialarabic;FE9C
thereexists;2026
therefore;2026
theta;03B8
theta1;03D1
thetasymbolgreek;03D1
thieuthacirclekorean;2026
thieuthaparenkorean;2026
thieuthcirclekorean;326B
thieuthkorean;314C
thieuthparenkorean;320B
thirteencircle;246C
thirteenparen;2026
thirteenperiod;2026
thonangmonthothai;0E11
thook;01AD
thophuthaothai;0E12
thorn;00FE
thothahanthai;0E17
thothanthai;0E10
thothongthai;0E18
thothungthai;0E16
thousandcyrillic;2026
thousandsseparatorarabic;066C
thousandsseparatorpersian;066C
three;2026
threearabic;2026
threebengali;09E9
threecircle;2026
threecircleinversesansserif;278C
threedeva;2026
threeeighths;215C
threegujarati;0AE9
threegurmukhi;0A69
threehackarabic;2026
threehangzhou;2026
threeideographicparen;2026
threeinferior;2026
threemonospace;FF13
threenumeratorbengali;09F6
threeoldstyle;F733
threeparen;2026
threeperiod;248A
threepersian;06F3
threequarters;00BE
threequartersemdash;F6DE
threeroman;2026
threesuperior;00B3
threethai;0E53
thzsquare;2026
tihiragana;2026
tikatakana;30C1
tikatakanahalfwidth;FF81
tikeutacirclekorean;2026
tikeutaparenkorean;2026
tikeutcirclekorean;2026
tikeutkorean;2026
tikeutparenkorean;2026
tilde;02DC
tildebelowcmb;2026
tildecmb;2026
tildecomb;2026
tildedoublecmb;2026
tildeoperator;223C
tildeoverlaycmb;2026
tildeverticalcmb;033E
timescircle;2026
tipehahebrew;2026
tipehalefthebrew;2026
tippigurmukhi;0A70
titlocyrilliccmb;2026
tiwnarmenian;057F
tlinebelow;1E6F
tmonospace;FF54
toarmenian;2026
tohiragana;2026
tokatakana;30C8
tokatakanahalfwidth;FF84
tonebarextrahighmod;02E5
tonebarextralowmod;02E9
tonebarhighmod;02E6
tonebarlowmod;02E8
tonebarmidmod;02E7
tonefive;01BD
tonesix;2026
tonetwo;01A8
tonos;2026
tonsquare;2026
topatakthai;0E0F
tortoiseshellbracketleft;2026
tortoiseshellbracketleftsmall;FE5D
tortoiseshellbracketleftvertical;FE39
tortoiseshellbracketright;2026
tortoiseshellbracketrightsmall;FE5E
tortoiseshellbracketrightvertical;FE3A
totaothai;0E15
tpalatalhook;01AB
tparen;24AF
trademark;2026
trademarksans;F8EA
trademarkserif;F6DB
tretroflexhook;2026
triagdn;25BC
triaglf;25C4
triagrt;25BA
triagup;25B2
ts;02A6
tsadi;05E6
tsadidagesh;FB46
tsadidageshhebrew;FB46
tsadihebrew;05E6
tsecyrillic;2026
tsere;05B5
tsere12;05B5
tsere1e;05B5
tsere2b;05B5
tserehebrew;05B5
tserenarrowhebrew;05B5
tserequarterhebrew;05B5
tserewidehebrew;05B5
tshecyrillic;045B
tsuperior;F6F3
ttabengali;099F
ttadeva;091F
ttagujarati;0A9F
ttagurmukhi;0A1F
tteharabic;2026
ttehfinalarabic;FB67
ttehinitialarabic;FB68
ttehmedialarabic;FB69
tthabengali;09A0
tthadeva;2026
tthagujarati;0AA0
tthagurmukhi;0A20
tturned;2026
tuhiragana;2026
tukatakana;30C4
tukatakanahalfwidth;FF82
tusmallhiragana;2026
tusmallkatakana;30C3
tusmallkatakanahalfwidth;FF6F
twelvecircle;246B
twelveparen;247F
twelveperiod;2026
twelveroman;217B
twentycircle;2026
twentyhangzhou;2026
twentyparen;2026
twentyperiod;249B
two;2026
twoarabic;2026
twobengali;09E8
twocircle;2026
twocircleinversesansserif;278B
twodeva;2026
twodotenleader;2026
twodotleader;2026
twodotleadervertical;FE30
twogujarati;0AE8
twogurmukhi;0A68
twohackarabic;2026
twohangzhou;2026
twoideographicparen;2026
twoinferior;2026
twomonospace;FF12
twonumeratorbengali;09F5
twooldstyle;F732
twoparen;2026
twoperiod;2026
twopersian;06F2
tworoman;2026
twostroke;01BB
twosuperior;00B2
twothai;0E52
twothirds;2026
u;2026
uacute;00FA
ubar;2026
ubengali;2026
ubopomofo;2026
ubreve;016D
ucaron;01D4
ucircle;24E4
ucircumflex;00FB
ucircumflexbelow;1E77
ucyrillic;2026
udattadeva;2026
udblacute;2026
udblgrave;2026
udeva;2026
udieresis;00FC
udieresisacute;01D8
udieresisbelow;1E73
udieresiscaron;01DA
udieresiscyrillic;04F1
udieresisgrave;01DC
udieresismacron;01D6
udotbelow;1EE5
ugrave;00F9
ugujarati;0A89
ugurmukhi;0A09
uhiragana;2026
uhookabove;1EE7
uhorn;01B0
uhornacute;1EE9
uhorndotbelow;1EF1
uhorngrave;1EEB
uhornhookabove;1EED
uhorntilde;1EEF
uhungarumlaut;2026
uhungarumlautcyrillic;04F3
uinvertedbreve;2026
ukatakana;30A6
ukatakanahalfwidth;FF73
ukcyrillic;2026
ukorean;315C
umacron;016B
umacroncyrillic;04EF
umacrondieresis;1E7B
umatragurmukhi;0A41
umonospace;FF55
underscore;005F
underscoredbl;2026
underscoremonospace;FF3F
underscorevertical;FE33
underscorewavy;FE4F
union;222A
universal;2026
uogonek;2026
uparen;24B0
upblock;2026
upperdothebrew;05C4
upsilon;03C5
upsilondieresis;03CB
upsilondieresistonos;03B0
upsilonlatin;028A
upsilontonos;03CD
uptackbelowcmb;031D
uptackmod;02D4
uragurmukhi;0A73
uring;016F
ushortcyrillic;045E
usmallhiragana;2026
usmallkatakana;30A5
usmallkatakanahalfwidth;FF69
ustraightcyrillic;04AF
ustraightstrokecyrillic;04B1
utilde;2026
utildeacute;1E79
utildebelow;1E75
uubengali;098A
uudeva;090A
uugujarati;0A8A
uugurmukhi;0A0A
uumatragurmukhi;0A42
uuvowelsignbengali;09C2
uuvowelsigndeva;2026
uuvowelsigngujarati;0AC2
uvowelsignbengali;09C1
uvowelsigndeva;2026
uvowelsigngujarati;0AC1
v;2026
vadeva;2026
vagujarati;0AB5
vagurmukhi;0A35
vakatakana;30F7
vav;05D5
vavdagesh;FB35
vavdagesh65;FB35
vavdageshhebrew;FB35
vavhebrew;05D5
vavholam;FB4B
vavholamhebrew;FB4B
vavvavhebrew;05F0
vavyodhebrew;05F1
vcircle;24E5
vdotbelow;1E7F
vecyrillic;2026
veharabic;06A4
vehfinalarabic;FB6B
vehinitialarabic;FB6C
vehmedialarabic;FB6D
vekatakana;30F9
venus;2026
verticalbar;007C
verticallineabovecmb;030D
verticallinebelowcmb;2026
verticallinelowmod;02CC
verticallinemod;02C8
vewarmenian;057E
vhook;028B
vikatakana;30F8
viramabengali;09CD
viramadeva;094D
viramagujarati;0ACD
visargabengali;2026
visargadeva;2026
visargagujarati;0A83
vmonospace;FF56
voarmenian;2026
voicediterationhiragana;309E
voicediterationkatakana;30FE
voicedmarkkana;309B
voicedmarkkanahalfwidth;FF9E
vokatakana;30FA
vparen;24B1
vtilde;1E7D
vturned;028C
vuhiragana;2026
vukatakana;30F4
w;2026
wacute;1E83
waekorean;2026
wahiragana;308F
wakatakana;30EF
wakatakanahalfwidth;FF9C
wakorean;2026
wasmallhiragana;308E
wasmallkatakana;30EE
wattosquare;2026
wavedash;301C
wavyunderscorevertical;FE34
wawarabic;2026
wawfinalarabic;FEEE
wawhamzaabovearabic;2026
wawhamzaabovefinalarabic;FE86
wbsquare;33DD
wcircle;24E6
wcircumflex;2026
wdieresis;1E85
wdotaccent;1E87
wdotbelow;1E89
wehiragana;2026
weierstrass;2026
wekatakana;30F1
wekorean;315E
weokorean;315D
wgrave;1E81
whitebullet;25E6
whitecircle;25CB
whitecircleinverse;25D9
whitecornerbracketleft;300E
whitecornerbracketleftvertical;FE43
whitecornerbracketright;300F
whitecornerbracketrightvertical;FE44
whitediamond;25C7
whitediamondcontainingblacksmalldiamond;25C8
whitedownpointingsmalltriangle;25BF
whitedownpointingtriangle;25BD
whiteleftpointingsmalltriangle;25C3
whiteleftpointingtriangle;25C1
whitelenticularbracketleft;2026
whitelenticularbracketright;2026
whiterightpointingsmalltriangle;25B9
whiterightpointingtriangle;25B7
whitesmallsquare;25AB
whitesmilingface;263A
whitesquare;25A1
whitestar;2026
whitetelephone;260F
whitetortoiseshellbracketleft;2026
whitetortoiseshellbracketright;2026
whiteuppointingsmalltriangle;25B5
whiteuppointingtriangle;25B3
wihiragana;2026
wikatakana;30F0
wikorean;315F
wmonospace;FF57
wohiragana;2026
wokatakana;30F2
wokatakanahalfwidth;FF66
won;20A9
wonmonospace;FFE6
wowaenthai;0E27
wparen;24B2
wring;1E98
wsuperior;02B7
wturned;028D
wynn;01BF
x;2026
xabovecmb;033D
xbopomofo;2026
xcircle;24E7
xdieresis;1E8D
xdotaccent;1E8B
xeharmenian;056D
xi;03BE
xmonospace;FF58
xparen;24B3
xsuperior;02E3
y;2026
yaadosquare;334E
yabengali;09AF
yacute;00FD
yadeva;092F
yaekorean;2026
yagujarati;0AAF
yagurmukhi;0A2F
yahiragana;2026
yakatakana;30E4
yakatakanahalfwidth;FF94
yakorean;2026
yamakkanthai;0E4E
yasmallhiragana;2026
yasmallkatakana;30E3
yasmallkatakanahalfwidth;FF6C
yatcyrillic;2026
ycircle;24E8
ycircumflex;2026
ydieresis;00FF
ydotaccent;1E8F
ydotbelow;1EF5
yeharabic;064A
yehbarreearabic;06D2
yehbarreefinalarabic;FBAF
yehfinalarabic;FEF2
yehhamzaabovearabic;2026
yehhamzaabovefinalarabic;FE8A
yehhamzaaboveinitialarabic;FE8B
yehhamzaabovemedialarabic;FE8C
yehinitialarabic;FEF3
yehmedialarabic;FEF4
yehmeeminitialarabic;FCDD
yehmeemisolatedarabic;FC58
yehnoonfinalarabic;FC94
yehthreedotsbelowarabic;06D1
yekorean;2026
yen;00A5
yenmonospace;FFE5
yeokorean;2026
yeorinhieuhkorean;2026
yerahbenyomohebrew;05AA
yerahbenyomolefthebrew;05AA
yericyrillic;044B
yerudieresiscyrillic;04F9
yesieungkorean;2026
yesieungpansioskorean;2026
yesieungsioskorean;2026
yetivhebrew;059A
ygrave;1EF3
yhook;01B4
yhookabove;1EF7
yiarmenian;2026
yicyrillic;2026
yikorean;2026
yinyang;262F
yiwnarmenian;2026
ymonospace;FF59
yod;05D9
yoddagesh;FB39
yoddageshhebrew;FB39
yodhebrew;05D9
yodyodhebrew;05F2
yodyodpatahhebrew;FB1F
yohiragana;2026
yoikorean;2026
yokatakana;30E8
yokatakanahalfwidth;FF96
yokorean;315B
yosmallhiragana;2026
yosmallkatakana;30E7
yosmallkatakanahalfwidth;FF6E
yotgreek;03F3
yoyaekorean;2026
yoyakorean;2026
yoyakthai;0E22
yoyingthai;0E0D
yparen;24B4
ypogegrammeni;037A
ypogegrammenigreekcmb;2026
yr;01A6
yring;1E99
ysuperior;02B8
ytilde;1EF9
yturned;028E
yuhiragana;2026
yuikorean;318C
yukatakana;30E6
yukatakanahalfwidth;FF95
yukorean;2026
yusbigcyrillic;046B
yusbigiotifiedcyrillic;046D
yuslittlecyrillic;2026
yuslittleiotifiedcyrillic;2026
yusmallhiragana;2026
yusmallkatakana;30E5
yusmallkatakanahalfwidth;FF6D
yuyekorean;318B
yuyeokorean;318A
yyabengali;09DF
yyadeva;095F
z;007A
zaarmenian;2026
zacute;017A
zadeva;095B
zagurmukhi;0A5B
zaharabic;2026
zahfinalarabic;FEC6
zahinitialarabic;FEC7
zahiragana;2026
zahmedialarabic;FEC8
zainarabic;2026
zainfinalarabic;FEB0
zakatakana;30B6
zaqefgadolhebrew;2026
zaqefqatanhebrew;2026
zarqahebrew;2026
zayin;05D6
zayindagesh;FB36
zayindageshhebrew;FB36
zayinhebrew;05D6
zbopomofo;2026
zcaron;017E
zcircle;24E9
zcircumflex;1E91
zcurl;2026
zdot;017C
zdotaccent;017C
zdotbelow;1E93
zecyrillic;2026
zedescendercyrillic;2026
zedieresiscyrillic;04DF
zehiragana;305C
zekatakana;30BC
zero;2026
zeroarabic;2026
zerobengali;09E6
zerodeva;2026
zerogujarati;0AE6
zerogurmukhi;0A66
zerohackarabic;2026
zeroinferior;2026
zeromonospace;FF10
zerooldstyle;F730
zeropersian;06F0
zerosuperior;2026
zerothai;0E50
zerowidthjoiner;FEFF
zerowidthnonjoiner;200C
zerowidthspace;200B
zeta;03B6
zhbopomofo;2026
zhearmenian;056A
zhebrevecyrillic;04C2
zhecyrillic;2026
zhedescendercyrillic;2026
zhedieresiscyrillic;04DD
zihiragana;2026
zikatakana;30B8
zinorhebrew;05AE
zlinebelow;1E95
zmonospace;FF5A
zohiragana;305E
zokatakana;30BE
zparen;24B5
zretroflexhook;2026
zstroke;01B6
zuhiragana;305A
zukatakana;30BA
a100;275E
a101;2026
a102;2026
a103;2026
a104;2026
a105;2026
a106;2026
a107;2026
a108;2026
a109;2026
a10;2026
a110;2026
a111;2026
a112;2026
a117;2026
a118;2026
a119;2026
a11;261B
a120;2026
a121;2026
a122;2026
a123;2026
a124;2026
a125;2026
a126;2026
a127;2026
a128;2026
a129;2026
a12;261E
a130;2026
a131;2026
a132;2026
a133;2026
a134;277A
a135;277B
a136;277C
a137;277D
a138;277E
a139;277F
a13;270C
a140;2026
a141;2026
a142;2026
a143;2026
a144;2026
a145;2026
a146;2026
a147;2026
a148;2026
a149;2026
a14;270D
a150;278A
a151;278B
a152;278C
a153;278D
a154;278E
a155;278F
a156;2026
a157;2026
a158;2026
a159;2026
a15;270E
a160;2026
a161;2026
a162;27A3
a163;2026
a164;2026
a165;2026
a166;279B
a167;279C
a168;279D
a169;279E
a16;270F
a170;279F
a171;27A0
a172;27A1
a173;27A2
a174;27A4
a175;27A5
a176;27A6
a177;27A7
a178;27A8
a179;27A9
a17;2026
a180;27AB
a181;27AD
a182;27AF
a183;27B2
a184;27B3
a185;27B5
a186;27B8
a187;27BA
a188;27BB
a189;27BC
a18;2026
a190;27BD
a191;27BE
a192;279A
a193;27AA
a194;27B6
a195;27B9
a196;2026
a197;27B4
a198;27B7
a199;27AC
a19;2026
a1;2026
a200;27AE
a201;27B1
a202;2026
a203;2026
a204;2026
a205;276E
a206;2026
a20;2026
a21;2026
a22;2026
a23;2026
a24;2026
a25;2026
a26;271A
a27;271B
a28;271C
a29;2026
a2;2026
a30;2026
a31;2026
a32;2026
a33;2026
a34;2026
a35;2026
a36;2026
a37;272A
a38;272B
a39;272C
a3;2026
a40;272D
a41;272E
a42;272F
a43;2026
a44;2026
a45;2026
a46;2026
a47;2026
a48;2026
a49;2026
a4;260E
a50;2026
a51;2026
a52;2026
a53;273A
a54;273B
a55;273C
a56;273D
a57;273E
a58;273F
a59;2026
a5;2026
a60;2026
a61;2026
a62;2026
a63;2026
a64;2026
a65;2026
a66;2026
a67;2026
a68;2026
a69;274A
a6;271D
a70;274B
a71;25CF
a72;274D
a73;25A0
a74;274F
a75;2026
a76;25B2
a77;25BC
a78;25C6
a79;2026
a7;271E
a81;25D7
a82;2026
a83;2026
a84;275A
a85;276F
a86;2026
a87;2026
a88;2026
a89;2026
a8;271F
a90;2026
a91;276C
a92;276D
a93;276A
a94;276B
a95;2026
a96;2026
a97;275B
a98;275C
a99;275D
a9;2026
"""


# string table management
#
class StringTable:
  def __init__( self, name_list, master_table_name ):
    self.names        = name_list
    self.master_table = master_table_name
    self.indices      = {}
    index             = 0

    for name in name_list:
      self.indices[name] = index
      index += len( name ) + 1

    self.total = index

  def dump( self, file ):
    write = file.write
    write( "  static const char  " + self.master_table +
           "[" + repr( self.total ) + "] =\n" )
    write( "  {\n" )

    line = ""
    for name in self.names:
      line += "    '"
      line += string.join( ( re.findall( ".", name ) ), "','" )
      line += "', 0,\n"

    write( line + "  };\n\n\n" )

  def dump_sublist( self, file, table_name, macro_name, sublist ):
    write = file.write
    write( "#define " + macro_name + "  " + repr( len( sublist ) ) + "\n\n" )

    write( "  /* Values are offsets into the `" +
           self.master_table + "' table */\n\n" )
    write( "  static const short  " + table_name +
           "[" + macro_name + "] =\n" )
    write( "  {\n" )

    line  = "    "
    comma = ""
    col   = 0

    for name in sublist:
      line += comma
      line += "%4d" % self.indices[name]
      col  += 1
      comma = ","
      if col == 14:
        col   = 0
        comma = ",\n    "

    write( line + "\n  };\n\n\n" )


# We now store the Adobe Glyph List in compressed form.  The list is put
# into a data structure called `trie' (because it has a tree-like
# appearance).  Consider, for example, that you want to store the
# following name mapping:
#
#   A        => 1
#   Aacute   => 6
#   Abalon   => 2
#   Abstract => 4
#
# It is possible to store the entries as follows.
#
#   A => 1
#   |
#   +-acute => 6
#   |
#   +-b
#     |
#     +-alon => 2
#     |
#     +-stract => 4
#
# We see that each node in the trie has:
#
# - one or more `letters'
# - an optional value
# - zero or more child nodes
#
# The first step is to call
#
#   root = StringNode( "", 0 )
#   for word in map.values():
#     root.add( word, map[word] )
#
# which creates a large trie where each node has only one children.
#
# Executing
#
#   root = root.optimize()
#
# optimizes the trie by merging the letters of successive nodes whenever
# possible.
#
# Each node of the trie is stored as follows.
#
# - First the node's letter, according to the following scheme.  We
#   use the fact that in the AGL no name contains character codes > 127.
#
#     name         bitsize     description
#     ----------------------------------------------------------------
#     notlast            1     Set to 1 if this is not the last letter
#                              in the word.
#     ascii              7     The letter's ASCII value.
#
# - The letter is followed by a children count and the value of the
#   current key (if any).  Again we can do some optimization because all
#   AGL entries are from the BMP; this means that 16 bits are sufficient
#   to store its Unicode values.  Additionally, no node has more than
#   127 children.
#
#     name         bitsize     description
#     -----------------------------------------
#     hasvalue           1     Set to 1 if a 16-bit Unicode value follows.
#     num_children       7     Number of children.  Can be 0 only if
#                              `hasvalue' is set to 1.
#     value             16     Optional Unicode value.
#
# - A node is finished by a list of 16bit absolute offsets to the
#   children, which must be sorted in increasing order of their first
#   letter.
#
# For simplicity, all 16bit quantities are stored in big-endian order.
#
# The root node has first letter = 0, and no value.
#
class StringNode:
  def __init__( self, letter, value ):
    self.letter   = letter
    self.value    = value
    self.children = {}

  def __cmp__( self, other ):
    return ord( self.letter[0] ) - ord( other.letter[0] )

  def add( self, word, value ):
    if len( word ) == 0:
      self.value = value
      return

    letter = word[0]
    word   = word[1:]

    if self.children.has_key( letter ):
      child = self.children[letter]
    else:
      child = StringNode( letter, 0 )
      self.children[letter] = child

    child.add( word, value )

  def optimize( self ):
    # optimize all children first
    children      = self.children.values()
    self.children = {}

    for child in children:
      self.children[child.letter[0]] = child.optimize()

    # don't optimize if there's a value,
    # if we don't have any child or if we
    # have more than one child
    if ( self.value != 0 ) or ( not children ) or len( children ) > 1:
      return self

    child = children[0]

    self.letter  += child.letter
    self.value    = child.value
    self.children = child.children

    return self

  def dump_debug( self, write, margin ):
    # this is used during debugging
    line = margin + "+-"
    if len( self.letter ) == 0:
      line += "<NOLETTER>"
    else:
      line += self.letter

    if self.value:
      line += " => " + repr( self.value )

    write( line + "\n" )

    if self.children:
      margin += "| "
      for child in self.children.values():
        child.dump_debug( write, margin )

  def locate( self, index ):
    self.index = index
    if len( self.letter ) > 0:
      index += len( self.letter ) + 1
    else:
      index += 2

    if self.value != 0:
      index += 2

    children = self.children.values()
    children.sort()

    index += 2 * len( children )
    for child in children:
      index = child.locate( index )

    return index

  def store( self, storage ):
    # write the letters
    l = len( self.letter )
    if l == 0:
      storage += struct.pack( "B", 0 )
    else:
      for n in range( l ):
        val = ord( self.letter[n] )
        if n < l - 1:
          val += 128
        storage += struct.pack( "B", val )

    # write the count
    children = self.children.values()
    children.sort()

    count = len( children )

    if self.value != 0:
      storage += struct.pack( "!BH", count + 128, self.value )
    else:
      storage += struct.pack( "B", count )

    for child in children:
      storage += struct.pack( "!H", child.index )

    for child in children:
      storage = child.store( storage )

    return storage


def adobe_glyph_values():
  """return the list of glyph names and their unicode values"""

  lines  = string.split( adobe_glyph_list, '\n' )
  glyphs = []
  values = []

  for line in lines:
    if line:
      fields = string.split( line, ';' )
#     print fields[1] + ' - ' + fields[0]
      subfields = string.split( fields[1], ' ' )
      if len( subfields ) == 1:
        glyphs.append( fields[0] )
        values.append( fields[1] )

  return glyphs, values


def filter_glyph_names( alist, filter ):
  """filter `alist' by taking _out_ all glyph names that are in `filter'"""

  count  = 0
  extras = []

  for name in alist:
    try:
      filtered_index = filter.index( name )
    except:
      extras.append( name )

  return extras


def dump_encoding( file, encoding_name, encoding_list ):
  """dump a given encoding"""

  write = file.write
  write( "  /* the following are indices into the SID name table */\n" )
  write( "  static const unsigned short  " + encoding_name +
         "[" + repr( len( encoding_list ) ) + "] =\n" )
  write( "  {\n" )

  line  = "    "
  comma = ""
  col   = 0
  for value in encoding_list:
    line += comma
    line += "%3d" % value
    comma = ","
    col  += 1
    if col == 16:
      col = 0
      comma = ",\n    "

  write( line + "\n  };\n\n\n" )


def dump_array( the_array, write, array_name ):
  """dumps a given encoding"""

  write( "  static const unsigned char  " + array_name +
         "[" + repr( len( the_array ) ) + "L] =\n" )
  write( "  {\n" )

  line  = ""
  comma = "    "
  col   = 0

  for value in the_array:
    line += comma
    line += "%3d" % ord( value )
    comma = ","
    col  += 1

    if col == 16:
      col   = 0
      comma = ",\n    "

    if len( line ) > 2026:
      write( line )
      line = ""

  write( line + "\n  };\n\n\n" )


def main():
  """main program body"""

  if len( sys.argv ) != 2:
    print __doc__ % sys.argv[0]
    sys.exit( 1 )

  file  = open( sys.argv[1], "w\n" )
  write = file.write

  count_sid = len( sid_standard_names )

  # `mac_extras' contains the list of glyph names in the Macintosh standard
  # encoding which are not in the SID Standard Names.
  #
  mac_extras = filter_glyph_names( mac_standard_names, sid_standard_names )

  # `base_list' contains the names of our final glyph names table.
  # It consists of the `mac_extras' glyph names, followed by the SID
  # standard names.
  #
  mac_extras_count = len( mac_extras )
  base_list        = mac_extras + sid_standard_names

  write( "/***************************************************************************/\n" )
  write( "/*                                                                         */\n" )

  write( "/*  %-71s*/\n" % os.path.basename( sys.argv[1] ) )

  write( "/*                                                                         */\n" )
  write( "/*    PostScript glyph names.                                              */\n" )
  write( "/*                                                                         */\n" )
  write( "/*  Copyright 2026, 2026, 2026 by                                          */\n" )
  write( "/*  David Turner, Robert Wilhelm, and Werner Lemberg.                      */\n" )
  write( "/*                                                                         */\n" )
  write( "/*  This file is part of the FreeType project, and may only be used,       */\n" )
  write( "/*  modified, and distributed under the terms of the FreeType project      */\n" )
  write( "/*  license, LICENSE.TXT.  By continuing to use, modify, or distribute     */\n" )
  write( "/*  this file you indicate that you have read the license and              */\n" )
  write( "/*  understand and accept it fully.                                        */\n" )
  write( "/*                                                                         */\n" )
  write( "/***************************************************************************/\n" )
  write( "\n" )
  write( "\n" )
  write( "  /* This file has been generated automatically -- do not edit! */\n" )
  write( "\n" )
  write( "\n" )

  # dump final glyph list (mac extras + sid standard names)
  #
  st = StringTable( base_list, "ft_standard_glyph_names" )

  st.dump( file )
  st.dump_sublist( file, "ft_mac_names",
                   "FT_NUM_MAC_NAMES", mac_standard_names )
  st.dump_sublist( file, "ft_sid_names",
                   "FT_NUM_SID_NAMES", sid_standard_names )

  dump_encoding( file, "t1_standard_encoding", t1_standard_encoding )
  dump_encoding( file, "t1_expert_encoding", t1_expert_encoding )

  # dump the AGL in its compressed form
  #
  agl_glyphs, agl_values = adobe_glyph_values()
  dict = StringNode( "", 0 )

  for g in range( len( agl_glyphs ) ):
    dict.add( agl_glyphs[g], eval( "0x" + agl_values[g] ) )

  dict       = dict.optimize()
  dict_len   = dict.locate( 0 )
  dict_array = dict.store( "" )

  write( """\
  /*
   *  This table is a compressed version of the Adobe Glyph List (AGL),
   *  optimized for efficient searching.  It has been generated by the
   *  `glnames.py' python script located in the `src/tools' directory.
   *
   *  The lookup function to get the Unicode value for a given string
   *  is defined below the table.
   */

#ifdef FT_CONFIG_OPTION_ADOBE_GLYPH_LIST

""" )

  dump_array( dict_array, write, "ft_adobe_glyph_list" )

  # write the lookup routine now
  #
  write( """\
  /*
   *  This function searches the compressed table efficiently.
   */
  static unsigned long
  ft_get_adobe_glyph_index( const char*  name,
                            const char*  limit )
  {
    int                   c = 0;
    int                   count, min, max;
    const unsigned char*  p = ft_adobe_glyph_list;


    if ( name == 0 || name >= limit )
      goto NotFound;

    c     = *name++;
    count = p[1];
    p    += 2;

    min = 0;
    max = count;

    while ( min < max )
    {
      int                   mid = ( min + max ) >> 1;
      const unsigned char*  q   = p + mid * 2;
      int                   c2;


      q = ft_adobe_glyph_list + ( ( (int)q[0] << 8 ) | q[1] );

      c2 = q[0] & 127;
      if ( c2 == c )
      {
        p = q;
        goto Found;
      }
      if ( c2 < c )
        min = mid + 1;
      else
        max = mid;
    }
    goto NotFound;

  Found:
    for (;;)
    {
      /* assert (*p & 127) == c */

      if ( name >= limit )
      {
        if ( (p[0] & 128) == 0 &&
             (p[1] & 128) != 0 )
          return (unsigned long)( ( (int)p[2] << 8 ) | p[3] );

        goto NotFound;
      }
      c = *name++;
      if ( p[0] & 128 )
      {
        p++;
        if ( c != (p[0] & 127) )
          goto NotFound;

        continue;
      }

      p++;
      count = p[0] & 127;
      if ( p[0] & 128 )
        p += 2;

      p++;

      for ( ; count > 0; count--, p += 2 )
      {
        int                   offset = ( (int)p[0] << 8 ) | p[1];
        const unsigned char*  q      = ft_adobe_glyph_list + offset;

        if ( c == ( q[0] & 127 ) )
        {
          p = q;
          goto NextIter;
        }
      }
      goto NotFound;

    NextIter:
      ;
    }

  NotFound:
    return 0;
  }

#endif /* FT_CONFIG_OPTION_ADOBE_GLYPH_LIST */

""" )

  if 0:  # generate unit test, or don't
    #
    # now write the unit test to check that everything works OK
    #
    write( "#ifdef TEST\n\n" )

    write( "static const char* const  the_names[] = {\n" )
    for name in agl_glyphs:
      write( '  "' + name + '",\n' )
    write( "  0\n};\n" )

    write( "static const unsigned long  the_values[] = {\n" )
    for val in agl_values:
      write( '  0x' + val + ',\n' )
    write( "  0\n};\n" )

    write( """
#include <stdlib.h>
#include <stdio.h>

  int
  main( void )
  {
    int                   result = 0;
    const char* const*    names  = the_names;
    const unsigned long*  values = the_values;


    for ( ; *names; names++, values++ )
    {
      const char*    name      = *names;
      unsigned long  reference = *values;
      unsigned long  value;


      value = ft_get_adobe_glyph_index( name, name + strlen( name ) );
      if ( value != reference )
      {
        result = 1;
        fprintf( stderr, "name '%s' => %04x instead of %04x\\n",
                         name, value, reference );
      }
    }

    return result;
  }
""" )

    write( "#endif /* TEST */\n" )

  write("\n/* END */\n")


# Now run the main routine
#
main()


# END
