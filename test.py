from struct import unpack


marker_mapping = {
    0xffd8: "Start of Image",
    0xffe0: "Application Default Header",
    0xffdb: "Quantization Table",
    0xffc0: "Start of Frame",
    0xffc4: "Define Huffman Table",
    0xffda: "Start of Scan",
    0xffd9: "End of Image"
}


class JPEG:
    def __init__(self, image_file):
        with open(image_file, 'rb') as f:
            self.img_data = f.read()
    
    def decode(self):
        data = self.img_data
        while(True):
            marker, = unpack(">H", data[0:2])
            print(marker_mapping.get(marker))
            if marker == 0xffd8:  # soi
                data = data[2:]
            elif marker == 0xffd9:  # eoi
                return
            elif marker == 0xffda:  # sos
                self.decodeSOS(data[2:-2])
                data = data[-2:]
            else:
                lenchunk, = unpack(">H", data[2:4])
                chunk = data[4:2+lenchunk]
                data = data[2+lenchunk:]

                if marker == 0xffc4:
                    self.decodeHuffmanTable(chunk)
                elif marker == 0xffdb:
                    self.DefineQuantizationTables(chunk)
                elif marker == 0xffc0:
                    self.decodeFrameHeader(chunk)

            if len(data) == 0:
                break  

if __name__ == "__main__":
    img = JPEG('test2.jpg')
    img.decode()    