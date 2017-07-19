/*==============================================================================
 *     (c)2013 Broadcom Corporation
 *
 *  This program is the proprietary software of Broadcom Corporation and/or its licensors,
 *  and may only be used, duplicated, modified or distributed pursuant to the terms and
 *  conditions of a separate, written license agreement executed between you and Broadcom
 *  (an "Authorized License").  Except as set forth in an Authorized License, Broadcom grants
 *  no license (express or implied), right to use, or waiver of any kind with respect to the
 *  Software, and Broadcom expressly reserves all rights in and to the Software and all
 *  intellectual property rights therein.  IF YOU HAVE NO AUTHORIZED LICENSE, THEN YOU
 *  HAVE NO RIGHT TO USE THIS SOFTWARE IN ANY WAY, AND SHOULD IMMEDIATELY
 *  NOTIFY BROADCOM AND DISCONTINUE ALL USE OF THE SOFTWARE.
 *
 *  Except as expressly set forth in the Authorized License,
 *
 *  1.     This program, including its structure, sequence and organization, constitutes the valuable trade
 *  secrets of Broadcom, and you shall use all reasonable efforts to protect the confidentiality thereof,
 *  and to use this information only in connection with your use of Broadcom integrated circuit products.
 *
 *  2.     TO THE MAXIMUM EXTENT PERMITTED BY LAW, THE SOFTWARE IS PROVIDED "AS IS"
 *  AND WITH ALL FAULTS AND BROADCOM MAKES NO PROMISES, REPRESENTATIONS OR
 *  WARRANTIES, EITHER EXPRESS, IMPLIED, STATUTORY, OR OTHERWISE, WITH RESPECT TO
 *  THE SOFTWARE.  BROADCOM SPECIFICALLY DISCLAIMS ANY AND ALL IMPLIED WARRANTIES
 *  OF TITLE, MERCHANTABILITY, NONINFRINGEMENT, FITNESS FOR A PARTICULAR PURPOSE,
 *  LACK OF VIRUSES, ACCURACY OR COMPLETENESS, QUIET ENJOYMENT, QUIET POSSESSION
 *  OR CORRESPONDENCE TO DESCRIPTION. YOU ASSUME THE ENTIRE RISK ARISING OUT OF
 *  USE OR PERFORMANCE OF THE SOFTWARE.
 *
 *  3.     TO THE MAXIMUM EXTENT PERMITTED BY LAW, IN NO EVENT SHALL BROADCOM OR ITS
 *  LICENSORS BE LIABLE FOR (i) CONSEQUENTIAL, INCIDENTAL, SPECIAL, INDIRECT, OR
 *  EXEMPLARY DAMAGES WHATSOEVER ARISING OUT OF OR IN ANY WAY RELATING TO YOUR
 *  USE OF OR INABILITY TO USE THE SOFTWARE EVEN IF BROADCOM HAS BEEN ADVISED OF
 *  THE POSSIBILITY OF SUCH DAMAGES; OR (ii) ANY AMOUNT IN EXCESS OF THE AMOUNT
 *  ACTUALLY PAID FOR THE SOFTWARE ITSELF OR U.S. $1, WHICHEVER IS GREATER. THESE
 *  LIMITATIONS SHALL APPLY NOTWITHSTANDING ANY FAILURE OF ESSENTIAL PURPOSE OF
 *  ANY LIMITED REMEDY
 *
 * $brcm_Workfile: sectionfilter_test.cpp $
 * $brcm_Revision: 97401_DIRECTV_CDI2_Integration/NDSCDI_Integration/woodp_NDSCDI/1 $
 * $brcm_Date: 9/3/13 6:01p $
 *
 * Revision History:
 *
 *============================================================================*/

/*
 *  Section Filter test
 */

#include <string.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <assert.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <sys/poll.h>

/* NDS CDI API */

#include "demuxtpidfilter.h"
#include "demuxtschannel.h"
#include "demuxsectionfilter.h"
#include "demuxcommon.h"
#include "tuner.h"
#include "lnb.h"

#include "Thread.h"
#include "jh_types.h"
#include "logging.h"

SET_LOG_CAT (LOG_CAT_DEFAULT | LOG_CAT_TRACE);
/* SET_LOG_LEVEL(LOG_LVL_NOTICE); */
SET_LOG_LEVEL (LOG_LVL_INFO);

#define try_ioctl(fd, cmd, param)           \
    if (ioctl(fd, cmd, param) != 0)     \
    {                                       \
        LOG_ERR_PERROR("%s error", #cmd);   \
        return -1;                          \
    }

#define try_ioctl_noparam(fd, cmd)          \
    if (ioctl(fd, cmd) != 0)                \
    {                                       \
        LOG_ERR_PERROR("%s error", #cmd);   \
        return -1;                          \
    }

#define try_ioctl_printf(fd, cmd, param)            \
    if (ioctl(fd, cmd, param) != 0)     \
    {                                       \
        printf("%s error", #cmd); \
        perror("error");    \
        return NULL;                            \
    }

#define try_ioctl_noparam_printf(fd, cmd)           \
    if (ioctl(fd, cmd) != 0)                \
    {                                       \
        printf("%s error", #cmd); \
        perror("error");    \
        return NULL;                            \
    }

/* Test configuration */

#define USE_TUNER

/* Tuning Parameters */

#define PARAM_LNB_POLARISATION  LNB_POLARISATION_HORIZONTAL
#define PARAM_LNB_BAND          LNB_BAND_LOW
#define PARAM_TUNER_FREQUENCY   (1260000)
#define PARAM_TUNER_SYMBOLRATE  (27500000)
//#define PARAM_TUNER_FEC         TUNER_FEC_AUTO
#define PARAM_TUNER_FEC         TUNER_FEC_3_4

#define DEV_SECTION         "/dev/nds/demux0/sectionfilter"
#define DEV_TSCHANNEL       "/dev/nds/demux0/tschannel1"
#define DEV_TPIDFILTER_STR  "/dev/nds/demux0/tpidfilter%i"
#define DEV_TUNER           "/dev/nds/tuner1"
#define DEV_LNB             "/dev/nds/lnb0"
#define DEV_SECTIONFILTER   "/dev/nds/demux0/sectionfilter"

#define MAX_SECTION_LENGTH  4096*4
#define NUM_TPIDFILTER      5
#define NUM_TPIDFILTER_OFFSET (16)
#define NUM_SECTIONFILTER   (2 * NUM_TPIDFILTER)

#define TABLE_ID_PAT            (0x00U) /* program_association_section() table_id */
#define TABLE_ID_NIT_A          (0x40U) /* network_information_section() actual table_id */
#define TABLE_ID_NIT_O          (0x41U) /* network_information_section() other table_id */
#define TABLE_ID_SDT_A          (0x42U) /* service_descriptor_section() actual table_id */
#define TABLE_ID_BAT            (0x4AU) /* bouquet_association_section() table_id */
#define TABLE_ID_EIT_A_PF       (0x4EU) /* event_information_section() actual present/following */
#define TABLE_ID_TDT            (0x70U) /* time_date_section() table_id */
#define TABLE_ID_TOT            (0x73U) /* time_offset_section() table_id */

#define GET_SECTION_LENGTH( BUF ) (uint16_t) ((((BUF)[1] << 8 | (BUF)[2]) & 0x0FFF) + 3)

/* Prototypes */

void           *sectionfilter_threadfunc (void *data);
static int      setupTpidFilters (uint32_t tschannel);
static int      teardownTpidFilters (void);
static int      waitForSync (void);
static int      Tune_Channel (void);

/* Variables */

static int      lnb_fd = 0;
static uint8_t  lnb_id = 0;
static int      tuner_fd = 0;
static int      tschannel_fd = 0;

static int      pids[NUM_TPIDFILTER] = { 5847, 5849, 5851, 5852, 5853 };

static int      tpidfilter_fds[NUM_TPIDFILTER];

static char      masks[2][3] = {{ 0x3b, 0x00, 0x00}, { 0x3b, 0x00, 0x01}};

static bool      testing = true;;
static pthread_t threads[NUM_SECTIONFILTER];

/* Functions */

void           *sectionfilter_threadfunc (void *data)
{
    void           *ret = NULL;
    size_t          bufsize = 4096 * 4;
    uint8_t         tpidfilter_id;
    int             fd, thread_id;
    struct pollfd   poller;
    DemuxSectionfilter filter_params;
    uint8_t *buf = (uint8_t*)malloc(sizeof(uint8_t)*bufsize);

    thread_id = (unsigned long) data;
    printf (" Thread %i starting\n", thread_id);

    /* Sleep */
    printf ("Thread %i - opening sectionfilter\n", thread_id);
    fd = open (DEV_SECTIONFILTER, O_RDWR);
    if (fd < 0)
    {
        printf ("Couldn't open sectionfilter");
        return NULL;
    }

    printf ("Thread %i - set buffer size to %i bytes\n", thread_id, (int)bufsize);
    try_ioctl_printf (fd, DEMUX_SET_BUFFER_SIZE, &bufsize);

    /* Two sectionfilter per tpidfilter */
    tpidfilter_id = NUM_TPIDFILTER_OFFSET + (thread_id / 2);

    printf ("Thread %i - attaching to tpidfilter %i\n", thread_id, tpidfilter_id);
    try_ioctl_printf (fd, DEMUX_ATTACH_TPIDFILTER, &tpidfilter_id);

    memset (&filter_params, 0, sizeof (filter_params));
    filter_params.value[0] = masks[thread_id % 2][0];
    filter_params.value[1] = masks[thread_id % 2][1];
    filter_params.value[2] = masks[thread_id % 2][2];
    filter_params.mask[0] = 0xff;
    filter_params.mask[1] = 0xff;
    filter_params.mask[2] = 0xff;
    filter_params.control = DEMUX_SECTIONFILTER_CONTROL_CHECK_CRC;
    printf ("Thread %i - set filter\n", thread_id);
    try_ioctl_printf (fd, DEMUX_SECTIONFILTER_SET_FILTER, &filter_params);

    printf ("Thread %i - start demux\n", thread_id);
    try_ioctl_noparam_printf (fd, DEMUX_START);

    while (testing)
    {
        poller.fd = fd;
        poller.events = POLLIN;
        poll (&poller, 1, 1000);
        if (poller.revents & POLLIN)
        {
            printf ("Thread %i - sectionfilter caught some data!\n", thread_id);
            ssize_t size = read(fd, buf, bufsize);
            ssize_t bytesRead = 0;
            uint8_t *section = buf;

            while (bytesRead < size)
            {
                int message_length = GET_SECTION_LENGTH(section);
                if (*section != masks[thread_id % 2][0])
                {
                    printf ("Thread %u - INCORRECT DATA. Found %x, expected %x\n", thread_id, *section, masks[thread_id % 2][0]);
                    testing = false;
                    break;
                }

                bytesRead += message_length;
                section += message_length;
            }
        }
        else
            printf ("HUY Thread %i - sectionfilter empty 1...\n", thread_id);
    }

    printf ("Thread %i - stop demux\n", thread_id);
    try_ioctl_noparam_printf (fd, DEMUX_STOP);

    printf ("Thread %i - closing sectionfilter\n", thread_id);
    close (fd);

    free(buf);
    printf ("Thread %i ending\n", thread_id);

    return ret;
}

int spawnSFthreads (void)
{
    int i;
    int ret;

    TRACE_BEGIN (LOG_LVL_INFO);

    for (i = 0; i < NUM_SECTIONFILTER; i++)
    {
        LOG ("Creating thread %i", (int)i);
        ret = pthread_create (&threads[i], NULL, sectionfilter_threadfunc, (void *) (unsigned long)i);
        if (ret)
        {
            LOG_ERR_PERROR ("Couldn't create thread %i", i);
        }
        else
        {
            LOG_INFO ("Created thread %i", i);
        }
    }

    TRACE_END ();
    return ret;
}

int stopSFthreads (void)
{
    int             i, ret;

    TRACE_BEGIN (LOG_LVL_INFO);

    testing = false;
    for (i = 0; i < NUM_SECTIONFILTER; i++)
    {
        LOG ("Waiting for thread %i", i);
        ret = pthread_join (threads[i], NULL);
        if (ret)
        {
            LOG_ERR_PERROR ("Couldn't join thread %i", i);
        }
        else
        {
            LOG_INFO ("Stopped thread %i", i);
        }
    }

    TRACE_END ();
    return ret;
}

int wait_for_keypress (void)
{
    int             ret;
    uint8_t         tmp_u8;
    struct pollfd   fds[1];

    TRACE_BEGIN (LOG_LVL_INFO);

    fds[0].fd = fileno (stdin);
    fds[0].events = POLLPRI | POLLIN;
    ret = poll (fds, 1, -1);
    if (ret < 0)
    {
        LOG_ERR ("Error on poll");
    }
    else if (ret == 0)
    {
        LOG_ERR ("Timed out (system error)");
    }
    else
    {
        /* Empty stdin, else it goes to terminal after we quit. */
        do
        {
            ret = read (fileno (stdin), &tmp_u8, 1);
            fds[0].fd = fileno (stdin);
            fds[0].events = POLLPRI | POLLIN;
            ret = poll (fds, 1, 0);
        }
        while (ret != 0);
    }

    TRACE_END ();

    return 0;
}

int main (void)
{
    int status;
    DeviceName      tsChannelSource;

    TRACE_BEGIN (LOG_LVL_NOTICE);

    /* Check parameters for out of bounds */
    assert (NUM_TPIDFILTER <= sizeof(pids)/sizeof(int));
    assert (NUM_SECTIONFILTER <= (NUM_TPIDFILTER * (sizeof(masks) / 3)));

    LOG ("Open LNB %s...", DEV_LNB);
    lnb_fd = open (DEV_LNB, O_RDWR);
    if (lnb_fd < 0)
    {
        LOG_INFO ("Failed to open LNB. Hopefully we can reuse it...");
    }

    ////////////////////////////////////////////////////////////

    LOG ("Open Tuner...");
    tuner_fd = open (DEV_TUNER, O_RDWR);
    if (tuner_fd < 0)
    {
        LOG_ERR_PERROR ("Tuner open error.");
        return -1;
    }

    LOG ("Attach tuner to LNB %i", lnb_id);
    try_ioctl (tuner_fd, TUNER_ATTACH_LNB, lnb_id);

    if (lnb_fd >= 0)
    {
        uint32_t        volArg = 0;
        uint32_t        tonArg = 0;

        volArg = (PARAM_LNB_POLARISATION == LNB_POLARISATION_VERTICAL) ? LNB_VOLTAGE_13V : LNB_VOLTAGE_18V;
        try_ioctl (lnb_fd, LNB_VOLTAGE_CONTROL, (void *) &volArg);
        usleep (15 * 1000);

        tonArg = (PARAM_LNB_BAND == LNB_BAND_HIGH) ? LNB_TONE_CONTINUOUS : LNB_TONE_NONE;
        try_ioctl (lnb_fd, LNB_TONE_CONTROL, (void *) &tonArg);
        usleep (15 * 1000);
    }

    Tune_Channel ();

    status = waitForSync ();
    if (status) {
        return status;
    }

    LOG ("***BEGIN***");

    ////////////////////////////////////////////////////////////

    LOG ("Open TS Channel...");
    tschannel_fd = open (DEV_TSCHANNEL, O_RDWR);
    if (tschannel_fd < 0)
    {
        LOG_ERR_PERROR ("TS Channel open error.");
        return -1;
    }

    LOG ("Set TS Channel mode to MPEG");
    uint32_t        ts_mode = DEMUX_TS_MODE_MPEG;
    try_ioctl (tschannel_fd, DEMUX_SET_TS_MODE, &ts_mode);

    tsChannelSource.name = strdup (DEV_TUNER);
    tsChannelSource.length = strlen (tsChannelSource.name) + 1;
    LOG ("Attach source %s to TS Channel", tsChannelSource.name);
    try_ioctl (tschannel_fd, DEMUX_ATTACH_SOURCE, &tsChannelSource);
    free (tsChannelSource.name);

    ////////////////////////////////////////////////////////////

    srandom (time (NULL));

    setupTpidFilters (1);

    spawnSFthreads ();

    wait_for_keypress ();

    stopSFthreads ();

    teardownTpidFilters ();

    ////////////////////////////////////////////////////////////

    LOG ("Close TS Channel...");
    if (tschannel_fd)
        close (tschannel_fd);

    if (tuner_fd)
        close (tuner_fd);

    LOG ("***END***");
    TRACE_END ();
    return 0;
}

static int setupTpidFilters (uint32_t tschannel)
{
    int             i, ret, fd;
    char            devname[128];

    TRACE_BEGIN (LOG_LVL_INFO);

    ret = 0;
    memset (tpidfilter_fds, -1, sizeof (tpidfilter_fds));
    for (i = 0; i < NUM_TPIDFILTER; i++)
    {
        sprintf (devname, DEV_TPIDFILTER_STR, NUM_TPIDFILTER_OFFSET + i);
        LOG ("Open tpidfilter %s", devname);
        fd = open (devname, O_RDWR);
        if (fd < 0)
        {
            LOG_ERR_PERROR ("Couldn't open tpidfilter %i", NUM_TPIDFILTER_OFFSET + i);
            ret = -1;
            break;
        }
        else
        {
            LOG ("Attach TS channel %i to TPID filter", tschannel);
            try_ioctl (fd, DEMUX_ATTACH_TSCHANNEL, &tschannel);

            LOG ("Set TPID filter tpid to 0x%04x", pids[i]);
            try_ioctl (fd, DEMUX_TPIDFILTER_SET_TPID, &pids[i]);

            tpidfilter_fds[i] = fd;
        }
    }

    TRACE_END ();
    return ret;
}

static int teardownTpidFilters (void)
{
    int             i;

    TRACE_BEGIN (LOG_LVL_INFO);

    for (i = 0; i < NUM_TPIDFILTER; i++)
    {
        if (tpidfilter_fds[i] >= 0)
        {
            LOG ("Closing tpidfilter %i", i);
            close (tpidfilter_fds[i]);
        }
    }

    TRACE_END ();
    return 0;
}

static int waitForSync (void)
{
    int             i;
    int             result;
    TunerStatus     status;

    for (i = 0; i < 10; i++)
    {
        fprintf (stderr, "%d ", i);
        memset (&status, 0, sizeof (TunerStatus));
        status.mode = TUNER_MODE_SAT_DVB_S;
        result = ioctl (tuner_fd, TUNER_GET_STATUS, (void *) &status);
        if (result < 0)
        {
            perror ("TUNER_GET_STATUS ioctl failed");
            return (-1);
        }

        if (status.u.DVBS.signalStatus & (TUNER_SIGNAL_SYNC | TUNER_SIGNAL_DEMOD | TUNER_SIGNAL_CARRIER))
        {
            printf ("\n>>> Tuner locked<<<\n");
            return 0;
        }

        sleep (1);
    }

    printf ("\n>>> Tuner not locked!!!<<<\n");
    return (1);
}

static int Tune_Channel (void)
{
    TunerTune       tune;

    int             eventmask = TUNER_EVENT_CARRIER_LOCKED |
        TUNER_EVENT_CARRIER_UNLOCKED |
        TUNER_EVENT_DEMOD_LOCKED | TUNER_EVENT_DEMOD_UNLOCKED | TUNER_EVENT_SYNC_LOCKED | TUNER_EVENT_SYNC_UNLOCKED;

    try_ioctl (tuner_fd, TUNER_SUBSCRIBE_EVENTS, eventmask);

    tune.mode = TUNER_MODE_SAT_DVB_S;
    tune.u.DVBS.frequency = PARAM_TUNER_FREQUENCY;
    fprintf (stderr, "freq %d\n", tune.u.DVBS.frequency);
    tune.u.DVBS.symbolRate = PARAM_TUNER_SYMBOLRATE;
    tune.u.DVBS.fec = PARAM_TUNER_FEC;
    tune.u.DVBS.inversion = TUNER_INVERSION_AUTO;

    try_ioctl (tuner_fd, TUNER_TUNE, (void *) &tune);

    return (0);
}