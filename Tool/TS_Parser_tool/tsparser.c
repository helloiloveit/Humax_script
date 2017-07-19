/*
 Sergey Bodrov 2012, serbod@gmail.com 
 */

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define MAX_BUFFER 102400
#define PKT_SIZE 188

/* pids */
#define PAT_PID                 0x0000
#define CAT_PID                 0x0001
#define TSDT_PID                0x0002
#define NIT_PID                 0x0010
#define SDT_PID                 0x0011

#define STREAM_TYPE_VIDEO_MPEG1     0x01
#define STREAM_TYPE_VIDEO_MPEG2     0x02
#define STREAM_TYPE_AUDIO_MPEG1     0x03
#define STREAM_TYPE_AUDIO_MPEG2     0x04
#define STREAM_TYPE_PRIVATE_SECTION 0x05
#define STREAM_TYPE_PRIVATE_DATA    0x06
#define STREAM_TYPE_AUDIO_AAC       0x0f
#define STREAM_TYPE_AUDIO_AAC_LATM  0x11
#define STREAM_TYPE_VIDEO_MPEG4     0x10
#define STREAM_TYPE_VIDEO_H264      0x1b
#define STREAM_TYPE_VIDEO_VC1       0xea
#define STREAM_TYPE_VIDEO_DIRAC     0xd1

#define STREAM_TYPE_AUDIO_AC3       0x81
#define STREAM_TYPE_AUDIO_DTS       0x8a

# define get_bit(val,bit) ((val & (1 << (bit))) >> (bit))

# define dump_flag(flag,text) if ( (flag) ) printf(" %s", (text))

static int _verbose = 0;

static uint8_t get_8(uint8_t *buf, int *pos)
{
    uint8_t tmp8;
    tmp8 = buf[*pos];
    *pos += 1;
    return tmp8;
}

static uint16_t get_16(uint8_t *buf, int *pos)
{
    uint16_t tmp16;
    tmp16 = buf[*pos + 1] + (buf[*pos] << 8);
    *pos += 2;
    return tmp16;

}

static uint32_t get_32(uint8_t *buf, int *pos)
{
    uint32_t tmp32;
    tmp32 = buf[*pos + 3] + (buf[*pos + 2] << 8) + (buf[*pos + 1] << 16) + (buf[*pos] << 24);
    *pos += 4;
    return tmp32;

}

static char *get_str8(uint8_t *buf, int *pos)
{
    int len;
    uint8_t tmp8;
    char *str;

    len = get_8(buf, pos);
    if (len < 0)
        return NULL;
    str = malloc(len + 1);
    if (!str)
        return NULL;
    memcpy(str, &buf[*pos], len);
    str[len] = '\0';
    *pos += len;
    return str;
}

void dump_bits16(uint16_t n)
{
    int i;
    //printf("%u=",n);
    for (i = 15; i >= 0; i--) {
        printf("%u", ((n & (1 << i)) >> i));
        if ((i % 4) == 0)
            printf(" ");
    }
}

typedef struct {
    int pid;
    uint64_t last_pts;
    uint64_t last_dts;
} MpegTsPid;

// MPEG-TS transport packet
typedef struct {
    int len;            // 8 Number of bytes in the adaptation field immediately following this byte
    int discont;        // 1 Set to 1 if current TS packet is in a discontinuity state
    int random_access; // 1 Set to 1 if the PES packet in this TS packet starts a video/audio sequence
    int es_prior;       // 1 higher priority)
    int pcr_flag;       // 1 adaptation field does contain a PCR field
    int opcr_flag;      // 1 adaptation field does contain an OPCR field
    int splice_flag;    // 1 splice countdown field in adaptation field
    int priv_flag;      // 1 private data bytes in adaptation field
    int ext_flag;       // 1 adaptation field extension
    uint64_t pcr;       // 33+6+9 Program clock reference (90 kHz base)
    int pcr_ext;        // PCR extension (27 MHz)
    uint64_t opcr; // 33+6+9 Original Program clock reference. Helps when one TS is copied into another
    int opcr_ext;       // OPCR extension (27 MHz)
    int splice; // 8 Indicates how many TS packets from this one a splicing point occurs (may be negative)
} MpegTsAdaptField;

typedef struct {
    int idx;
    int error_flag;     // 1  Transport Error Indicator
    int payload_flag;   // 1  Payload Unit Start Indicator
    int priority_flag;  // 1  Transport Priority
    int pid;            // 13 Packet ID
    int scramble;       // 2  Transport scrambling control (0,1,2,3)
    int adapt_field;    // 2  Adaptation field control (1,2,3)
    int cc;             // 4  Continuity counter
    MpegTsAdaptField af;
} MpegTsPacket;

typedef struct {
    uint8_t buf[MAX_BUFFER];
    int pos;
    int pids_count;
    MpegTsPid pids[32];       // stream pids from PAT/PMT
    MpegTsPid *cur_pid;       // current pid
    uint64_t last_pcr;
    MpegTsPacket *cur_pkt;    // current transport packet
} MpegTS;
static MpegTS ts;

typedef struct sectionfilter_config_s {
    int table_id;
    int pid;
    const char *name;
} sectionfilter_config_t;

/* BCM CDI */
#define BYTES_TO_READ (14) // 12 byes we can filter for plus 2 bytes for section size
#define GET_SECTION_LENGTH( BUF ) (uint16_t) ((((BUF)[1] << 8 | (BUF)[2]) & 0x0FFF) + 3)

int parse_si_header(uint8_t *buf, int *pos, MpegTsPacket *pkt)
{
    uint8_t i, section[BYTES_TO_READ];
    int pid_array[10];
    (*pos)++;

    memcpy(section, &buf[*pos], BYTES_TO_READ);

    /*
    if (pkt->pid == 5847) {
        if ((section[0] == 0x3b) && (section[3] == 0x00) && ((section[4] == 0x00) || (section[4] == 0x01))) {
            printf("PID: %4u, size %4u, ", pkt->pid, GET_SECTION_LENGTH(section));
            printf("packet %8u ,", pkt->idx);
            printf("data: ");
            for (i = 0; i < BYTES_TO_READ; i++) {
                printf("0x%02X ", section[i]);
            }
            printf("\n");
        }
    }
    */
    /*  table id 0
    if (pkt->pid == 0) {
        if ((section[0] == 0x00) && (section[3] == 0x00) && ((section[4] == 0x0e) || (section[4] == 0x01))) {
            printf("PID: %4u, size %4u, ", pkt->pid, GET_SECTION_LENGTH(section));
            printf("packet %8u ,", pkt->idx);
            printf("data: ");
            for (i = 0; i < BYTES_TO_READ; i++) {
                printf("0x%02X ", section[i]);
            }
            printf("\n");
        }
    }
    */
    //printf ("pid value = %d\n", pkt->pid);
    //if (pkt->pid == 5847) {
    //if (1) {
    if (pkt->pid == 802) {
        if ((section[0] == 0x3b) && (section[3] == 0x00) && ((section[4] == 0x7d) || (section[4] == 0x01))) {
            printf("PID: %4u, size %4u, ", pkt->pid, GET_SECTION_LENGTH(section));
            printf("packet %8u ,", pkt->idx);
            printf("data: ");
            for (i = 0; i < BYTES_TO_READ; i++) {
                printf("0x%02X ", section[i]);
            }
            printf("\n");
        }
    }
    
    
    


    return 0;
}

// PCR field value
uint64_t parse_pcr(uint8_t *buf, int *pos, int *ext)
{
    // 33 base
    // 06 reserved
    // 09 extension
    uint64_t tmp64 = 0;
    uint8_t tmp8 = 0;

    int i;
    for (i = 0; i < 4; i++) {
        tmp64 |= get_8(buf, pos) << (8 * (3 - i));
    }
    tmp8 = get_8(buf, pos);
    tmp64 = (tmp64 << 1) | get_bit(tmp8, 7);

    *ext = (get_bit(tmp8, 0) << 8) | get_8(buf, pos);
    return tmp64;
}

int parse_pkt(uint8_t *buf, MpegTsPacket *pkt)
{
    int pos_value = 0;
    int *pos = &pos_value;
    int i, ii;
    uint16_t tmp16;
    uint8_t tmp8;
    MpegTsAdaptField *af = &pkt->af;

    if (buf[*pos] != 0x47)
        return -1;
    ts.cur_pkt = pkt;
    *pos += 1;
    tmp16 = get_16(buf, pos);
    // dump_16(tmp16); printf(" \n");
    pkt->error_flag = get_bit(tmp16, 15);
    pkt->payload_flag = get_bit(tmp16, 14);
    pkt->priority_flag = get_bit(tmp16, 13);
    pkt->pid = tmp16 & 0x1fff; // 0x1f = 0001 1111
    tmp8 = get_8(buf, pos);
    pkt->scramble = (tmp8 & 0xc0) >> 6; // 0xc0 = 1100 0000
    pkt->adapt_field = (tmp8 & 0x30) >> 4; // 0x30 = 0011 0000
    pkt->cc = tmp8 & 0x0f; // 0000 1111

    // dump packet
    if (_verbose) {
        printf("packet=%u, pid=%u\n", pkt->idx, pkt->pid);
        dump_flag(pkt->error_flag, "error");
        dump_flag(pkt->payload_flag, "PES/SI");
        dump_flag(pkt->priority_flag, "priority");
        dump_flag(pkt->scramble, "scramble");
        dump_flag(pkt->adapt_field > 1, "adapt");
        dump_flag(pkt->adapt_field & 1, "payload");
        printf("\n");
    }

    // adaptation field (optional)
    if (pkt->adapt_field > 1) {
        af->len = get_8(buf, pos);

        tmp8 = get_8(buf, pos);
        af->discont = (tmp8 & (1 << 7)) >> 7;
        af->random_access = (tmp8 & (1 << 6)) >> 6;
        af->es_prior = (tmp8 & (1 << 5)) >> 5;
        af->pcr_flag = (tmp8 & (1 << 4)) >> 4;
        af->opcr_flag = (tmp8 & (1 << 3)) >> 3;
        af->splice_flag = (tmp8 & (1 << 2)) >> 2;
        af->priv_flag = (tmp8 & (1 << 1)) >> 1;
        af->ext_flag = (tmp8 & (1 << 0)) >> 0;

        // dump adaptation field
        if (_verbose) {
            printf("  adapt_field length=%u", af->len);
            dump_flag(af->discont, "discontinuity");
            dump_flag(af->random_access, "random_access");
            dump_flag(af->es_prior, "es_priority");
            //dump_flag(af->pcr_flag, "PCR");
            //dump_flag(af->opcr_flag, "OPCR");
            //dump_flag(af->splice_flag, "splice");
            dump_flag(af->priv_flag, "private");
            dump_flag(af->ext_flag, "extension");
        }

        // optional header data
        if (af->pcr_flag) {
            ts.last_pcr = af->pcr;
            af->pcr = parse_pcr(buf, pos, &(af->pcr_ext));
            if (_verbose) {
                printf(" PCR=%llu (%+lli)", (long long unsigned) af->pcr,
                        (long long) (af->pcr - ts.last_pcr));
                if (af->pcr_ext != 0)
                    printf(" pcr_ext=%u", af->pcr_ext);
            }
        }
        if (af->opcr_flag) {
            af->opcr = parse_pcr(buf, pos, &(af->opcr_ext));
            if (_verbose) {
                printf(" OPCR=%llu", (long long unsigned) af->pcr);
                if (af->opcr_ext != 0)
                    printf(" opcr_ext=%u", af->opcr_ext);
            }
        }
        if (af->splice_flag) {
            af->splice = get_8(buf, pos);
            if (_verbose)
                printf(" splice_count=%i", af->splice);
        }

        if (_verbose)
            printf("\n");

        *pos = 4 + 1 + af->len; // skip after adaptation field

    }

    ts.cur_pid = NULL;
    if (pkt->payload_flag) {
        // packet have payload section
        parse_si_header(buf, pos, pkt);
    }

    return 0;
}

int do_some()
{
    int ir, i, idx = 1;
    MpegTsPacket pkt;
    uint8_t pkt_buf[PKT_SIZE];

    ts.last_pcr = 0;
    ts.pids_count = 0;
    ir = fread(ts.buf, 1, MAX_BUFFER, stdin);
    printf(" do some \n");
    while (ir) {
        for (i = 0; i < ir; i++) {
            if (ts.buf[i] == 0x47) {
                memcpy(&pkt_buf, &ts.buf[i], sizeof(pkt_buf));
                i += sizeof(pkt_buf) - 1;
                pkt.idx = idx++;
                parse_pkt(&pkt_buf[0], &pkt);

                fflush(stdout);

            }
        }

        ir = fread(ts.buf, 1, MAX_BUFFER, stdin);
    }
}

int main(int argc, char**argv)
{
    printf("Start Main %d argv[1] = %s , argv[2]  = %s\n", argc, argv[1], argv[2]);
    if (argc > 1) {
        if ((strcmp(argv[1], "--help") == 0) || (strcmp(argv[1], "-h") == 0)) {
            printf("  Usage: %s [-b] < input.ts > output.log\n", argv[0]);
            printf("Options:\n");
            printf("    -v - verbose mode\n");
            return 0;
        }
        if (strcmp(argv[1], "-v") == 0) {
            _verbose = 1;
        }
    }
    printf("act..\n");
    do_some();
    printf ("HUY Done ...\n");
    return 0;
}
