#ifndef VERSION_H
#define VERSION_H

#define VER_STRINGIFY(d)            #d
#define TO_STR(v)                   VER_STRINGIFY(v)

#ifndef INTVER
#define INTVER WIN_INTVER
#endif
#define VER_FILEVERSION             WIN_INTVER
#define VER_FILEVERSION_STR         TO_STR(INTVER)"\0"

#define VER_PRODUCTVERSION          VER_FILEVERSION
#define VER_PRODUCTVERSION_STR      TO_STR(INTVER)"\0"

#define VER_COMPANYNAME_STR         "UNIVAULT TECHNOLOGIES\0"
#define VER_LEGALCOPYRIGHT_STR      "UNIVAULT TECHNOLOGIES " TO_STR(COPYRIGHT_YEAR) "\0"
#define VER_COMPANYDOMAIN_STR       "https://univaultoffice.github.io/www/\0"
#define ABOUT_COPYRIGHT_STR         VER_LEGALCOPYRIGHT_STR

#define VER_FILEDESCRIPTION_STR     "UNIVAULTOFFICE Document Builder\0"
#define VER_INTERNALNAME_STR        "Document Builder\0"
#define VER_LEGALTRADEMARKS1_STR    "All Rights Reserved\0"
#define VER_LEGALTRADEMARKS2_STR    VER_LEGALTRADEMARKS1_STR
#define VER_ORIGINALFILENAME_STR    "docbuilder.exe\0"
#define VER_PRODUCTNAME_STR         "UNIVAULTOFFICE Document Builder\0"

#endif

