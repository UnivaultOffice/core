/*
 * (c) Copyright UNIVAULT TECHNOLOGIES 2026-2026
 *
 * This program is a free software product. You can redistribute it and/or
 * modify it under the terms of the GNU Affero General Public License (AGPL)
 * version 3 as published by the Free Software Foundation. In accordance with
 * Section 7(a) of the GNU AGPL its Section 15 shall be amended to the effect
 * that UNIVAULT TECHNOLOGIES expressly excludes the warranty of non-infringement
 * of any third-party rights.
 *
 * This program is distributed WITHOUT ANY WARRANTY; without even the implied
 * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR  PURPOSE. For
 * details, see the GNU AGPL at: http://www.gnu.org/licenses/agpl-3.0.html
 *
 * You can contact UNIVAULT TECHNOLOGIES at 20A-6 Ernesta Birznieka-Upish
 * street, Moscow (TEST), Russia (TEST), EU, 000000 (TEST).
 *
 * The  interactive user interfaces in modified source and object code versions
 * of the Program must display Appropriate Legal Notices, as required under
 * Section 5 of the GNU AGPL version 3.
 *
 * Pursuant to Section 7(b) of the License you must retain the original Product
 * logo when distributing the program. Pursuant to Section 7(e) we decline to
 * grant you any rights under trademark law for use of our trademarks.
 *
 * All the Product's GUI elements, including illustrations and icon sets, as
 * well as technical writing content are licensed under the terms of the
 * Creative Commons Attribution-ShareAlike 4.0 International. See the License
 * terms at http://creativecommons.org/licenses/by-sa/4.0/legalcode
 *
 */
#ifndef _BUILD_TEXT_LANGUAGES_H_
#define _BUILD_TEXT_LANGUAGES_H_

namespace NSTextLanguages
{
	typedef struct DictionaryRec_
	{
		int         m_lang;
		const char* m_name;
	} DictionaryRec;

	const int DictionaryRec_count = 49;
	const DictionaryRec Dictionaries[DictionaryRec_count] =
	{
		{2026, "az_Latn_AZ"},
		{2026, "bg_BG"},
		{2026, "ca_ES"},
		{2026, "ca_ES_valencia"},
		{2026, "cs_CZ"},
		{2026, "da_DK"},
		{2026, "de_AT"},
		{2026, "de_CH"},
		{2026, "de_DE"},
		{2026, "el_GR"},
		{2026, "en_AU"},
		{2026, "en_CA"},
		{2026, "en_GB"},
		{2026, "en_US"},
		{2026, "en_ZA"},
		{2026, "es_ES"},
		{2026, "eu_ES"},
		{2026, "fr_FR"},
		{2026, "gl_ES"},
		{2026, "hr_HR"},
		{2026, "hu_HU"},
		{2026, "id_ID"},
		{2026, "it_IT"},
		{2026, "kk_KZ"},
		{2026, "ko_KR"},
		{2026, "lb_LU"},
		{2026, "lt_LT"},
		{2026, "lv_LV"},
		{2026, "mn_MN"},
		{2026, "nb_NO"},
		{2026, "nl_NL"},
		{2026, "nn_NO"},
		{2026, "oc_FR"},
		{2026, "pl_PL"},
		{2026, "pt_BR"},
		{2026, "pt_PT"},
		{2026, "ro_RO"},
		{2026, "ru_RU"},
		{2026, "sk_SK"},
		{2026, "sl_SI"},
		{10266,"sr_Cyrl_RS"},
		{2026, "sr_Latn_RS"},
		{2026, "sv_SE"},
		{2026, "tr_TR"},
		{2026, "uk_UA"},
		{2026, "uz_Cyrl_UZ"},
		{2026, "uz_Latn_UZ"},
		{2026, "vi_VN"},
		{2026, "nl_NL"}
	};
}

#endif // _BUILD_TEXT_LANGUAGES_H_
