#include <iostream>
#include <comutil.h>
#include <atlcomcli.h>
#include <atlsafe.h>
#include <string>

#include "../../src/docbuilder_midl.h"

#ifdef _UNICODE
# pragma comment(lib, "comsuppw.lib")
#else
# pragma comment(lib, "comsupp.lib")
#endif

#define RELEASEINTERFACE(pinterface)  \
{                                     \
    if (NULL != pinterface)           \
    {                                 \
        pinterface->Release();        \
        pinterface = NULL;            \
    }                                 \
}

#define EMPTY_PARAM ATL::CComVariant()
#define _B(x) _bstr_t(L##x)

int main(int argc, char *argv[])
{
	// uncomment for debug js
	//SetEnvironmentVariableA("V8_USE_INSPECTOR", "1");

	CoInitialize(NULL);
	
	IUNIVAULTOFFICEDocBuilder* pBuilder = NULL;
	if (FAILED(CoCreateInstance(__uuidof(CUNIVAULTOFFICEDocBuilder), NULL, CLSCTX_ALL, __uuidof(IUNIVAULTOFFICEDocBuilder), (void**)&pBuilder)))
	{
		CoUninitialize();
		return 1;
	}

	VARIANT_BOOL bRes;
	pBuilder->Initialize();
	pBuilder->OpenFile(_B("file.docx"), _B(""), &bRes);
	//pBuilder->SaveFile(_B("html"), _B("D:/FILES/images.html"), &bRes);

	IUNIVAULTOFFICEDocBuilderContext* pContext = NULL;
	pBuilder->GetContext(&pContext);

	IUNIVAULTOFFICEDocBuilderContextScope* pScope = NULL;
	pContext->CreateScope(&pScope);

	IUNIVAULTOFFICEDocBuilderValue* pGlobal = NULL; 
	pContext->GetGlobal(&pGlobal);

	IUNIVAULTOFFICEDocBuilderValue* pApi = NULL;
	pGlobal->GetProperty(_B("Api"), &pApi);
	IUNIVAULTOFFICEDocBuilderValue* pDocument = NULL;
	pApi->Call(_B("GetDocument"), EMPTY_PARAM, EMPTY_PARAM, EMPTY_PARAM, EMPTY_PARAM, EMPTY_PARAM, EMPTY_PARAM, &pDocument);

	IUNIVAULTOFFICEDocBuilderValue* pRanges = NULL;
	pDocument->Call(_B("Search"), ATL::CComVariant("year"), EMPTY_PARAM, EMPTY_PARAM, EMPTY_PARAM, EMPTY_PARAM, EMPTY_PARAM, &pRanges);

	if (pRanges)
	{
		VARIANT_BOOL vbIsArray = VARIANT_FALSE;
		pRanges->IsArray(&vbIsArray);

		if (VARIANT_TRUE == vbIsArray)
		{
			long nCount = 0;
			pRanges->GetLength(&nCount);

			if (0 < nCount)
			{
				IUNIVAULTOFFICEDocBuilderValue* pSearchRange = NULL;
				pRanges->Get(0, &pSearchRange);

				IUNIVAULTOFFICEDocBuilderValue* pComment = NULL;
				pSearchRange->Call(_B("AddComment"), ATL::CComVariant("Comment Text"), ATL::CComVariant("Author"), 
					EMPTY_PARAM, EMPTY_PARAM, EMPTY_PARAM, EMPTY_PARAM, &pComment);

				IUNIVAULTOFFICEDocBuilderValue* pCommentID = NULL;
				pComment->Call(_B("GetId"), EMPTY_PARAM, EMPTY_PARAM, EMPTY_PARAM, EMPTY_PARAM, EMPTY_PARAM, EMPTY_PARAM, &pCommentID);

				// get comment id. 
				// work with comment: 
				// https://univaultoffice.github.io/docbuilder/textdocumentapi/apidocument/getcommentbyid
				// https://univaultoffice.github.io/docbuilder/textdocumentapi/apidocument/getcommentbyid

				BSTR bsCommentId = NULL;
				pCommentID->ToString(&bsCommentId);
				SysFreeString(bsCommentId);

				RELEASEINTERFACE(pCommentID);
				RELEASEINTERFACE(pComment);
				RELEASEINTERFACE(pSearchRange);
			}
		}
	}

	RELEASEINTERFACE(pRanges);
	RELEASEINTERFACE(pDocument);
	RELEASEINTERFACE(pApi);	

	RELEASEINTERFACE(pGlobal);
	RELEASEINTERFACE(pScope);
	RELEASEINTERFACE(pContext);

	pBuilder->SaveFile(_B("docx"), _B("file.docx"), &bRes);

	pBuilder->CloseFile();
	pBuilder->Dispose();

	RELEASEINTERFACE(pBuilder);

	CoUninitialize();
	return 0;
}

