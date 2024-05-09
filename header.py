import sys
import os

# JPEG marker definitions. refer to itu-t81 Table B.1
JPEG_MARKER_SOF0 = 0xc0    # Baseline DCT
JPEG_MARKER_SOF1 = 0xc1    # Extended sequential DCT
JPEG_MARKER_SOF2 = 0xc2    # Progressive DCT
JPEG_MARKER_SOF3 = 0xc3    # Lossless(sequential)

JPEG_MARKER_SOF4 = 0xc5    # Differential sequential DCT
JPEG_MARKER_SOF5 = 0xc6    # Differential progressive DCT
JPEG_MARKER_SOF6 = 0xc7    # Differential Lossless(sequential)

JPEG_MARKER_JPG = 0xc8     # Reserved for JPEG extensions
JPEG_MARKER_SOF9 = 0xc9    # Extended sequential DCT
JPEG_MARKER_SOF10 = 0xca   # Progressive DCT
JPEG_MARKER_SOF11 = 0xcb   # Lossless(dequential)

JPEG_MARKER_SOF13 = 0xcd   # Differential sequential DCT
JPEG_MARKER_SOF14 = 0xce   # Differential progressive DCT
JPEG_MARKER_SOF15 = 0xcf   # Differential lossless(sequential)

JPEG_MARKER_RST0 = 0xd0    # Restart ...
JPEG_MARKER_RST1 = 0xd1
JPEG_MARKER_RST2 = 0xd2
JPEG_MARKER_RST3 = 0xd3
JPEG_MARKER_RST4 = 0xd4
JPEG_MARKER_RST5 = 0xd5
JPEG_MARKER_RST6 = 0xd6
JPEG_MARKER_RST7 = 0xd7
JPEG_MARKER_RST8 = 0xd8
JPEG_MARKER_RST9 = 0xd9

JPEG_MARKER_DHT = 0xc4     # Define Huffman table(s)
JPEG_MARKER_DAC = 0xcc     # Define arithmetic coding conditioning(s)

JPEG_MARKER_SOI = 0xd8     # Start of image
JPEG_MARKER_EOI = 0xd9     # End of image
JPEG_MARKER_SOS = 0xda     # Start of scan
JPEG_MARKER_DQT = 0xdb     # Define quantization table(s)
JPEG_MARKER_DNL = 0xdc     # Define number of lines
JPEG_MARKER_DRI = 0xdd     # Define restart interval
JPEG_MARKER_DHP = 0xde     # Define hierarchial progression
JPEG_MARKER_EXP = 0xdf     # Expand reference component(s)
JPEG_MARKER_APP0 = 0xe0    # Application marker, JFIF/AVI1...
JPEG_MARKER_APP1 = 0xe1    # EXIF Metadata etc...
JPEG_MARKER_APP2 = 0xe2    # Not common...
JPEG_MARKER_APP13 = 0xed   # Photoshop Save As: IRB, 8BIM, IPTC
JPEG_MARKER_APP14 = 0xee   # Not common...
JPEG_MARKER_APP15 = 0xef   # Not common...

seg_name = [
    "Baseline DCT; Huffman",
    "Extended sequential DCT; Huffman",
    "Progressive DCT; Huffman",
    "Spatial lossless; Huffman",
    "Huffman table",
    "Differential sequential DCT; Huffman",
    "Differential progressive DCT; Huffman",
    "Differential spatial; Huffman",
    "[Reserved: JPEG extension]",
    "Extended sequential DCT; Arithmetic",
    "Progressive DCT; Arithmetic",
    "Spatial lossless; Arithmetic",
    "Arithmetic coding conditioning",
    "Differential sequential DCT; Arithmetic",
    "Differential progressive DCT; Arithmetic",
    "Differential spatial; Arithmetic",
    "Restart",
    "Restart",
    "Restart",
    "Restart",
    "Restart",
    "Restart",
    "Restart",
    "Restart",
    "Start of image",
    "End of image",
    "Start of scan",
    "Quantisation table",
    "Number of lines",
    "Restart interval",
    "Hierarchical progression",
    "Expand reference components",
    "JFIF header",
    "[Reserved: application extension]",
    "[Reserved: application extension]",
    "[Reserved: application extension]",
    "[Reserved: application extension]",
    "[Reserved: application extension]",
    "[Reserved: application extension]",
    "[Reserved: application extension]",
    "[Reserved: application extension]",
    "[Reserved: application extension]",
    "[Reserved: application extension]",
    "[Reserved: application extension]",
    "[Reserved: application extension]",
    "[Reserved: application extension]",
    "[Reserved: application extension]",
    "[Reserved: application extension]",
    "[Reserved: JPEG extension]",
    "[Reserved: JPEG extension]",
    "[Reserved: JPEG extension]",
    "[Reserved: JPEG extension]",
    "[Reserved: JPEG extension]",
    "[Reserved: JPEG extension]",
    "[Reserved: JPEG extension]",
    "[Reserved: JPEG extension]",
    "[Reserved: JPEG extension]",
    "[Reserved: JPEG extension]",
    "[Reserved: JPEG extension]",
    "[Reserved: JPEG extension]",
    "[Reserved: JPEG extension]",
    "[Reserved: JPEG extension]",
    "[Reserved: JPEG extension]",
    "Comment",
    "[Invalid]",
]

def show_segment(marker):
    index = marker - 0xc0
    if index < 0 or index >= len(seg_name):
        return
    print(seg_name[index])

def parse_jpeg_header(data, length):
    start = 0
    end = length
    cur = start
    found = False

    while cur < end:
        if data[cur] != 0xff:
            print("{:02x} {:02x} -> {:02x} {:02x}".format(data[cur-2], data[cur-1], data[cur], data[cur+1]))
            print("cur pos: 0x{:x}".format(cur - start))
            break

        marker = data[cur]
        cur += 1

        if marker == JPEG_MARKER_SOS:
            break

        show_segment(marker)

        if marker == JPEG_MARKER_SOI:
            pass
        elif marker == JPEG_MARKER_DRI:
            cur += 4  # |length[0..1]||rst_interval[2..3]|
        elif marker == JPEG_MARKER_SOF2:
            print("progressive JPEGs not suppoted")
        elif marker == JPEG_MARKER_SOF0:
            length = (data[cur] << 8) + data[cur+1]
            cur += 2
            length -= 2
            sample_precision = data[cur]
            cur += 1
            print("sample_precision = {}".format(sample_precision))
            height = (data[cur] << 8) + data[cur+1]
            cur += 2
            width = (data[cur] << 8) + data[cur+1]
            cur += 2
            length -= 5
            cur += length
            found = True
        else:
            length = (data[cur] << 8) + data[cur+1]
            cur += 2
            length -= 2
            cur += length

    print("parse jpeg header finish")
    return found

def main():
    if len(sys.argv) != 2:
        print("usage: jpeg_parse file")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        with open(file_path, "rb") as f:
            bs_mem = f.read()
            f_len = len(bs_mem)
            print("file length {} bytes".format(f_len))

            # parse jpeg header
            if parse_jpeg_header(bs_mem, f_len):
                print("picture width: {}, height: {}".format(width, height))
    except FileNotFoundError:
        print("File not found:", file_path)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
