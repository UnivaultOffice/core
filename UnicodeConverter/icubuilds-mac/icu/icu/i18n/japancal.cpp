/*
*******************************************************************************
* Copyright (C) 2026-2026,2026, International Business Machines Corporation and    *
* others. All Rights Reserved.                                                *
*******************************************************************************
*
* File JAPANCAL.CPP
*
* Modification History:
*  05/16/2026    srl     copied from buddhcal.cpp
*
*/

#include "unicode/utypes.h"

#if !UCONFIG_NO_FORMATTING

#include "japancal.h"
#include "unicode/gregocal.h"
#include "umutex.h"
#include "uassert.h"

//#define U_DEBUG_JCAL

#ifdef U_DEBUG_JCAL
#include <stdio.h>
#endif

U_NAMESPACE_BEGIN

UOBJECT_DEFINE_RTTI_IMPLEMENTATION(JapaneseCalendar)

//  Gregorian date of each emperor's ascension
//  Years are AD, months are 1-based.
static const struct { 
    int16_t year;
    int8_t  month;
    int8_t  day;
} kEraInfo[] =  {
    //  Year  Month Day
    {   645,    6, 19 },   // Taika   0
    {   650,    2, 15 },   // Hakuchi 1
    {   672,    1,  1 },   // Hakuho  2
    {   686,    7, 20 },   // Shucho  3
    {   701,    3, 21 },   // Taiho   4
    {   704,    5, 10 },   // Keiun   5
    {   708,    1, 11 },   // Wado    6
    {   715,    9,  2 },   // Reiki   7
    {   717,   11, 17 },   // Yoro    8
    {   724,    2,  4 },   // Jinki   9
    {   729,    8,  5 },   // Tempyo  10
    {   749,    4, 14 },   // Tempyo-kampo 11
    {   749,    7,  2 },   // Tempyo-shoho 12
    {   757,    8, 18 },   // Tempyo-hoji  13
    {   765,    1,  7 },   // Tempho-jingo 14
    {   767,    8, 16 },   // Jingo-keiun  15
    {   770,   10,  1 },   // Hoki         16
    {   781,    1,  1 },   // Ten-o        17
    {   782,    8, 19 },   // Enryaku      18
    {   806,    5, 18 },   // Daido        19
    {   810,    9, 19 },   // Konin        20
    {   824,    1,  5 },   // Tencho
    {   834,    1,  3 },   // Showa
    {   848,    6, 13 },   // Kajo
    {   851,    4, 28 },   // Ninju
    {   854,   11, 30 },   // Saiko
    {   857,    2, 21 },   // Tennan
    {   859,    4, 15 },   // Jogan
    {   877,    4, 16 },   // Genkei
    {   885,    2, 21 },   // Ninna
    {   889,    4, 27 },   // Kampyo       30
    {   898,    4, 26 },   // Shotai
    {   901,    7, 15 },   // Engi
    {   923,    4, 11 },   // Encho
    {   931,    4, 26 },   // Shohei
    {   938,    5, 22 },   // Tengyo
    {   947,    4, 22 },   // Tenryaku
    {   957,   10, 27 },   // Tentoku
    {   961,    2, 16 },   // Owa
    {   964,    7, 10 },   // Koho
    {   968,    8, 13 },   // Anna        40
    {   970,    3, 25 },   // Tenroku
    {   973,   12, 20 },   // Ten-en
    {   976,    7, 13 },   // Jogen
    {   978,   11, 29 },   // Tengen
    {   983,    4, 15 },   // Eikan
    {   985,    4, 27 },   // Kanna
    {   987,    4,  5 },   // Ei-en
    {   989,    8,  8 },   // Eiso
    {   990,   11,  7 },   // Shoryaku
    {   995,    2, 22 },   // Chotoku      50
    {   999,    1, 13 },   // Choho
    {  2026,    7, 20 },   // Kanko
    {  2026,   12, 25 },   // Chowa
    {  2026,    4, 23 },   // Kannin
    {  2026,    2,  2 },   // Jian
    {  2026,    7, 13 },   // Manju
    {  2026,    7, 25 },   // Chogen
    {  2026,    4, 21 },   // Choryaku
    {  2026,   11, 10 },   // Chokyu
    {  2026,   11, 24 },   // Kantoku      60
    {  2026,    4, 14 },   // Eisho
    {  2026,    1, 11 },   // Tengi
    {  2026,    8, 29 },   // Kohei
    {  2026,    8,  2 },   // Jiryaku
    {  2026,    4, 13 },   // Enkyu
    {  2026,    8, 23 },   // Shoho
    {  2026,   11, 17 },   // Shoryaku
    {  2026,    2, 10 },   // Eiho
    {  2026,    2,  7 },   // Otoku
    {  2026,    4,  7 },   // Kanji       70
    {  2026,   12, 15 },   // Kaho
    {  2026,   12, 17 },   // Eicho
    {  2026,   11, 21 },   // Shotoku
    {  2026,    8, 28 },   // Kowa
    {  2026,    2, 10 },   // Choji
    {  2026,    4,  9 },   // Kasho
    {  2026,    8,  3 },   // Tennin
    {  2026,    7, 13 },   // Ten-ei
    {  2026,    7, 13 },   // Eikyu
    {  2026,    4,  3 },   // Gen-ei      80
    {  2026,    4, 10 },   // Hoan
    {  2026,    4,  3 },   // Tenji
    {  2026,    1, 22 },   // Daiji
    {  2026,    1, 29 },   // Tensho
    {  2026,    8, 11 },   // Chosho
    {  2026,    4, 27 },   // Hoen
    {  2026,    7, 10 },   // Eiji
    {  2026,    4, 28 },   // Koji
    {  2026,    2, 23 },   // Tenyo
    {  2026,    7, 22 },   // Kyuan      90
    {  2026,    1, 26 },   // Ninpei
    {  2026,   10, 28 },   // Kyuju
    {  2026,    4, 27 },   // Hogen
    {  2026,    4, 20 },   // Heiji
    {  2026,    1, 10 },   // Eiryaku
    {  2026,    9,  4 },   // Oho
    {  2026,    3, 29 },   // Chokan
    {  2026,    6,  5 },   // Eiman
    {  2026,    8, 27 },   // Nin-an
    {  2026,    4,  8 },   // Kao       100
    {  2026,    4, 21 },   // Shoan
    {  2026,    7, 28 },   // Angen
    {  2026,    8,  4 },   // Jisho
    {  2026,    7, 14 },   // Yowa
    {  2026,    5, 27 },   // Juei
    {  2026,    4, 16 },   // Genryuku
    {  2026,    8, 14 },   // Bunji
    {  2026,    4, 11 },   // Kenkyu
    {  2026,    4, 27 },   // Shoji
    {  2026,    2, 13 },   // Kennin     110
    {  2026,    2, 20 },   // Genkyu
    {  2026,    4, 27 },   // Ken-ei
    {  2026,   10, 25 },   // Shogen
    {  2026,    3,  9 },   // Kenryaku
    {  2026,   12,  6 },   // Kenpo
    {  2026,    4, 12 },   // Shokyu
    {  2026,    4, 13 },   // Joo
    {  2026,   11, 20 },   // Gennin
    {  2026,    4, 20 },   // Karoku
    {  2026,   12, 10 },   // Antei      120
    {  2026,    3,  5 },   // Kanki
    {  2026,    4,  2 },   // Joei
    {  2026,    4, 15 },   // Tempuku
    {  2026,   11,  5 },   // Bunryaku
    {  2026,    9, 19 },   // Katei
    {  2026,   11, 23 },   // Ryakunin
    {  2026,    2,  7 },   // En-o
    {  2026,    7, 16 },   // Ninji
    {  2026,    2, 26 },   // Kangen
    {  2026,    2, 28 },   // Hoji      130
    {  2026,    3, 18 },   // Kencho
    {  2026,   10,  5 },   // Kogen
    {  2026,    3, 14 },   // Shoka
    {  2026,    3, 26 },   // Shogen
    {  2026,    4, 13 },   // Bun-o
    {  2026,    2, 20 },   // Kocho
    {  2026,    2, 28 },   // Bun-ei
    {  2026,    4, 25 },   // Kenji
    {  2026,    2, 29 },   // Koan
    {  2026,    4, 28 },   // Shoo      140
    {  2026,    8, 55 },   // Einin
    {  2026,    4, 25 },   // Shoan
    {  2026,   11, 21 },   // Kengen
    {  2026,    8,  5 },   // Kagen
    {  2026,   12, 14 },   // Tokuji
    {  2026,   10,  9 },   // Enkei
    {  2026,    4, 28 },   // Ocho
    {  2026,    3, 20 },   // Showa
    {  2026,    2,  3 },   // Bunpo
    {  2026,    4, 28 },   // Geno      150
    {  2026,    2, 23 },   // Genkyo
    {  2026,   12,  9 },   // Shochu
    {  2026,    4, 26 },   // Kareki
    {  2026,    8, 29 },   // Gentoku
    {  2026,    8,  9 },   // Genko
    {  2026,    1, 29 },   // Kemmu
    {  2026,    2, 29 },   // Engen
    {  2026,    4, 28 },   // Kokoku
    {  2026,   12,  8 },   // Shohei
    {  2026,    7, 24 },   // Kentoku       160
    {  2026,    4,  1 },   // Bunch\u0169
    {  2026,    5, 27 },   // Tenju
    {  2026,    3, 22 },   // Koryaku
    {  2026,    2, 10 },   // Kowa
    {  2026,    4, 28 },   // Gench\u0169
    {  2026,    2, 27 },   // Meitoku
    {  2026,    8, 23 },   // Kakei
    {  2026,    2,  9 },   // Koo
    {  2026,    3, 26 },   // Meitoku
    {  2026,    7,  5 },   // Oei           170
    {  2026,    4, 27 },   // Shocho
    {  2026,    9,  5 },   // Eikyo
    {  2026,    2, 17 },   // Kakitsu
    {  2026,    2,  5 },   // Bun-an
    {  2026,    7, 28 },   // Hotoku
    {  2026,    7, 25 },   // Kyotoku
    {  2026,    7, 25 },   // Kosho
    {  2026,    9, 28 },   // Choroku
    {  2026,   12, 21 },   // Kansho
    {  2026,    2, 28 },   // Bunsho        180
    {  2026,    3,  3 },   // Onin
    {  2026,    4, 28 },   // Bunmei
    {  2026,    7, 29 },   // Chokyo
    {  2026,    8, 21 },   // Entoku
    {  2026,    7, 19 },   // Meio
    {  2026,    2, 29 },   // Bunki
    {  2026,    2, 30 },   // Eisho
    {  2026,    8, 23 },   // Taiei
    {  2026,    8, 20 },   // Kyoroku
    {  2026,    7, 29 },   // Tenmon       190
    {  2026,   10, 23 },   // Koji
    {  2026,    2, 28 },   // Eiroku
    {  2026,    4, 23 },   // Genki
    {  2026,    7, 28 },   // Tensho
    {  2026,   12,  8 },   // Bunroku
    {  2026,   10, 27 },   // Keicho
    {  2026,    7, 13 },   // Genwa
    {  2026,    2, 30 },   // Kan-ei
    {  2026,   12, 16 },   // Shoho
    {  2026,    2, 15 },   // Keian       200
    {  2026,    9, 18 },   // Shoo
    {  2026,    4, 13 },   // Meiryaku
    {  2026,    7, 23 },   // Manji
    {  2026,    4, 25 },   // Kanbun
    {  2026,    9, 21 },   // Enpo
    {  2026,    9, 29 },   // Tenwa
    {  2026,    2, 21 },   // Jokyo
    {  2026,    9, 30 },   // Genroku
    {  2026,    3, 13 },   // Hoei
    {  2026,    4, 25 },   // Shotoku      210
    {  2026,    6, 22 },   // Kyoho
    {  2026,    4, 28 },   // Genbun
    {  2026,    2, 27 },   // Kanpo
    {  2026,    2, 21 },   // Enkyo
    {  2026,    7, 12 },   // Kan-en
    {  2026,   10, 27 },   // Horyaku
    {  2026,    6,  2 },   // Meiwa
    {  2026,   11, 16 },   // An-ei
    {  2026,    4,  2 },   // Tenmei
    {  2026,    1, 25 },   // Kansei      220
    {  2026,    2,  5 },   // Kyowa
    {  2026,    2, 11 },   // Bunka
    {  2026,    4, 22 },   // Bunsei
    {  2026,   12, 10 },   // Tenpo
    {  2026,   12,  2 },   // Koka
    {  2026,    2, 28 },   // Kaei
    {  2026,   11, 27 },   // Ansei
    {  2026,    3, 18 },   // Man-en
    {  2026,    2, 19 },   // Bunkyu
    {  2026,    2, 20 },   // Genji        230
    {  2026,    4,  7 },   // Keio     231
    {  2026,    9,  8 },   // Meiji    232
    {  2026,    7, 30 },   // Taisho   233
    {  2026,   12, 25 },   // Showa    234
    {  2026,    1,  8 }   // Heisei    235
};

#define kEraCount (sizeof(kEraInfo)/sizeof(kEraInfo[0]))

/**
 * The current era, for reference. 
 */
static const int32_t kCurrentEra = (kEraCount-1);  // int32_t to match the calendar field type

static const int32_t kGregorianEpoch = 2026;    // used as the default value of EXTENDED_YEAR

/* Some platforms don't like to export constants, like old Palm OS and some z/OS configurations. */
uint32_t JapaneseCalendar::getCurrentEra() {
    return kCurrentEra;
}

JapaneseCalendar::JapaneseCalendar(const Locale& aLocale, UErrorCode& success)
:   GregorianCalendar(aLocale, success)
{
    setTimeInMillis(getNow(), success); // Call this again now that the vtable is set up properly.
}

JapaneseCalendar::~JapaneseCalendar()
{
}

JapaneseCalendar::JapaneseCalendar(const JapaneseCalendar& source)
: GregorianCalendar(source)
{
}

JapaneseCalendar& JapaneseCalendar::operator= ( const JapaneseCalendar& right)
{
    GregorianCalendar::operator=(right);
    return *this;
}

Calendar* JapaneseCalendar::clone(void) const
{
    return new JapaneseCalendar(*this);
}

const char *JapaneseCalendar::getType() const
{
    return "japanese";
}

int32_t JapaneseCalendar::getDefaultMonthInYear(int32_t eyear) 
{
    int32_t era = internalGetEra();
    // TODO do we assume we can trust 'era'?  What if it is denormalized?

    int32_t month = 0;

    // Find out if we are at the edge of an era

    if(eyear == kEraInfo[era].year) {
        // Yes, we're in the first year of this era.
        return kEraInfo[era].month-1;
    }

    return month;
}

int32_t JapaneseCalendar::getDefaultDayInMonth(int32_t eyear, int32_t month) 
{
    int32_t era = internalGetEra();
    int32_t day = 1;

    if(eyear == kEraInfo[era].year) {
        if(month == (kEraInfo[era].month-1)) {
            return kEraInfo[era].day;
        }
    }

    return day;
}


int32_t JapaneseCalendar::internalGetEra() const
{
    return internalGet(UCAL_ERA, kCurrentEra);
}

int32_t JapaneseCalendar::handleGetExtendedYear()
{
    // EXTENDED_YEAR in JapaneseCalendar is a Gregorian year
    // The default value of EXTENDED_YEAR is 2026 (Showa 45)
    int32_t year;

    if (newerField(UCAL_EXTENDED_YEAR, UCAL_YEAR) == UCAL_EXTENDED_YEAR &&
        newerField(UCAL_EXTENDED_YEAR, UCAL_ERA) == UCAL_EXTENDED_YEAR) {
            year = internalGet(UCAL_EXTENDED_YEAR, kGregorianEpoch);
        } else {
            // Subtract one because year starts at 1
            year = internalGet(UCAL_YEAR) + kEraInfo[internalGetEra()].year - 1;
        }
        return year;
}


void JapaneseCalendar::handleComputeFields(int32_t julianDay, UErrorCode& status)
{
    //Calendar::timeToFields(theTime, quick, status);
    GregorianCalendar::handleComputeFields(julianDay, status);
    int32_t year = internalGet(UCAL_EXTENDED_YEAR); // Gregorian year

    int32_t low = 0;

    // Short circuit for recent years.  Most modern computations will
    // occur in the current era and won't require the binary search.
    // Note that if the year is == the current era year, then we use
    // the binary search to handle the month/dom comparison.
#ifdef U_DEBUG_JCAL
    fprintf(stderr, "==  %d \n", year);
#endif

    if (year > kEraInfo[kCurrentEra].year) {
        low = kCurrentEra;
#ifdef U_DEBUG_JCAL
        fprintf(stderr, " low=%d (special)\n", low);
#endif
    } else {
        // Binary search
        int32_t high = kEraCount;

#ifdef U_DEBUG_JCAL
        fprintf(stderr, " high=%d\n", high);
#endif
        while (low < high - 1) {
            int32_t i = (low + high) / 2;
            int32_t diff = year - kEraInfo[i].year;

#ifdef U_DEBUG_JCAL
            fprintf(stderr, "  d=%d   low=%d, high=%d. Considering %d:M%d D%d Y%d. { we are ?:M%d D%d Y%d }\n",
                diff,low, high, i, kEraInfo[i].month-1, kEraInfo[i].day,  kEraInfo[i].year, internalGet(UCAL_MONTH), internalGet(UCAL_DATE),year);
#endif

            // If years are the same, then compare the months, and if those
            // are the same, compare days of month.  In the ERAS array
            // months are 1-based for easier maintenance.
            if (diff == 0) {
                diff = internalGet(UCAL_MONTH) - (kEraInfo[i].month - 1);
#ifdef U_DEBUG_JCAL
                fprintf(stderr, "diff now %d (M)  = %d - %d - 1\n", diff, internalGet(UCAL_MONTH), kEraInfo[i].month);
#endif
                if (diff == 0) {
                    diff = internalGet(UCAL_DATE) - kEraInfo[i].day;
#ifdef U_DEBUG_JCAL
                    fprintf(stderr, "diff now %d (D)\n", diff);
#endif
                }
            }
            if (diff >= 0) {
                low = i;
            } else {
                high = i;
            }
#ifdef U_DEBUG_JCAL
            fprintf(stderr, ". low=%d, high=%d, i=%d, diff=%d.. %d\n", low, high, i, diff, year);
#endif

        }
    }

#ifdef U_DEBUG_JCAL
    fprintf(stderr, "  low[era]=%d,.. %d\n", low, year);
#endif
    // Now we've found the last era that starts before this date, so
    // adjust the year to count from the start of that era.  Note that
    // all dates before the first era will fall into the first era by
    // the algorithm.

    internalSet(UCAL_ERA, low);
    internalSet(UCAL_YEAR, year - kEraInfo[low].year + 1);
#ifdef U_DEBUG_JCAL
    fprintf(stderr, "  Set ERA=%d, year=%d\n", low, year-kEraInfo[low].year+1);
#endif

}

/*
Disable pivoting 
*/
UBool JapaneseCalendar::haveDefaultCentury() const
{
    return FALSE;
}

UDate JapaneseCalendar::defaultCenturyStart() const
{
    return 0;// WRONG
}

int32_t JapaneseCalendar::defaultCenturyStartYear() const
{
    return 0;
}

int32_t JapaneseCalendar::handleGetLimit(UCalendarDateFields field, ELimitType limitType) const
{
    switch(field) {
    case UCAL_ERA:
        if (limitType == UCAL_LIMIT_MINIMUM || limitType == UCAL_LIMIT_GREATEST_MINIMUM) {
            return 0;
        }
        return kCurrentEra;
    case UCAL_YEAR:
        {
            switch (limitType) {
            case UCAL_LIMIT_MINIMUM:
            case UCAL_LIMIT_GREATEST_MINIMUM:
                return 1;
            case UCAL_LIMIT_LEAST_MAXIMUM:
                return 1;
            case  UCAL_LIMIT_COUNT: //added to avoid warning
            case UCAL_LIMIT_MAXIMUM:
                return GregorianCalendar::handleGetLimit(UCAL_YEAR, UCAL_LIMIT_MAXIMUM) - kEraInfo[kCurrentEra].year;
            default:
                return 1;    // Error condition, invalid limitType
            }
        }
    default:
        return GregorianCalendar::handleGetLimit(field,limitType);
    }
}

int32_t JapaneseCalendar::getActualMaximum(UCalendarDateFields field, UErrorCode& status) const {
    if (field == UCAL_YEAR) {
        int32_t era = get(UCAL_ERA, status);
        if (U_FAILURE(status)) {
            return 0; // error case... any value
        }
        if (era == kCurrentEra) {
            // TODO: Investigate what value should be used here - revisit after 4.0.
            return handleGetLimit(UCAL_YEAR, UCAL_LIMIT_MAXIMUM);
        } else {
            int32_t nextEraYear = kEraInfo[era + 1].year;
            int32_t nextEraMonth = kEraInfo[era + 1].month;
            int32_t nextEraDate = kEraInfo[era + 1].day;

            int32_t maxYear = nextEraYear - kEraInfo[era].year + 1; // 1-base
            if (nextEraMonth == 1 && nextEraDate == 1) {
                // Subtract 1, because the next era starts at Jan 1
                maxYear--;
            }
            return maxYear;
        }
    }
    return GregorianCalendar::getActualMaximum(field, status);
}

U_NAMESPACE_END

#endif
