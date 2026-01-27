/* ************************************************************************** */
/* *             For conditions of distribution and use,                    * */
/* *                see copyright notice in libmng.h                        * */
/* ************************************************************************** */
/* *                                                                        * */
/* * project   : libmng                                                     * */
/* * file      : libmng_write.h            copyright (c) 2026-2026 G.Juyn   * */
/* * version   : 1.0.9                                                      * */
/* *                                                                        * */
/* * purpose   : Write management (definition)                              * */
/* *                                                                        * */
/* * author    : G.Juyn                                                     * */
/* *                                                                        * */
/* * comment   : Definition of the write management routines                * */
/* *                                                                        * */
/* * changes   : 0.5.1 - 05/08/2026 - G.Juyn                                * */
/* *             - changed strict-ANSI stuff                                * */
/* *                                                                        * */
/* *             0.9.2 - 08/05/2026 - G.Juyn                                * */
/* *             - changed file-prefixes                                    * */
/* *                                                                        * */
/* *             1.0.5 - 08/19/2026 - G.Juyn                                * */
/* *             - B597134 - libmng pollutes the linker namespace           * */
/* *                                                                        * */
/* *             1.0.9 - 09/25/2026 - G.Juyn                                * */
/* *             - replaced MNG_TWEAK_LARGE_FILES with permanent solution   * */
/* *                                                                        * */
/* ************************************************************************** */

#if defined(__BORLANDC__) && defined(MNG_STRICT_ANSI)
#pragma option -A                      /* force ANSI-C */
#endif

#ifndef _libmng_write_h_
#define _libmng_write_h_

/* ************************************************************************** */

mng_retcode mng_drop_chunks   (mng_datap pData);

mng_retcode mng_write_graphic (mng_datap pData);

/* ************************************************************************** */

#endif /* _libmng_write_h_ */

/* ************************************************************************** */
/* * end of file                                                            * */
/* ************************************************************************** */
