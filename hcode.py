from heapify import *
from bt import *
from bitarray import bitarray
import os
from sys import argv

script, action, inputfile, outputfile = argv


class Huffman(object):
    def __init__(self):
        self.data = None
        self.header = None
        self.footer = None
        self.bitstream = None
        self.asciitocode = {}
        self.codetoascii = {}
        self.bt = BT()

    def string_to_tree(self):
        # Converts self.data to Huffman BT
        freq_dict = self.get_freq(self.data)
        heap = Heap(h_type='max')
        for key in freq_dict.keys():
            n = Node(None, None, None, key, freq_dict[key])
            heap.insert((freq_dict[key], n))
            self.bt.leaves.append(n)
        while len(heap) > 1:
            x = heap.pop()
            y = heap.pop()
            n = Node(None, x[1], y[1], None, x[0]+y[0])
            x[1].parent = n
            y[1].parent = n
            heap.insert((x[0]+y[0], n))
            if not self.bt.root:
                self.bt.root = n
            elif self.bt.root.key < n.key:
                self.bt.root = n
            if n is not self.bt.root:
                n.parent = self.bt.root

    def serialize_tree(self, x, header=[]):
        # Encodes the Huffman tree structure as a string
        if x:
            if x.letter:
                y = '1' + bin(ord(x.letter))[2:].zfill(8)
                header.append(y)
            else:
                header.append(0)
                self.serialize_tree(x.left)
                self.serialize_tree(x.right)
        return header

    def deserialize_tree(self, header, prev=None):
        # Creates a Huffman tree from header
        while True:
            try:
                y = str(int(next(header)))
                if y == '1':
                    buf = ''
                    for _ in xrange(8):
                        buf += str(int(next(header)))
                    letter = chr(int(buf, 2))
                    n = Node(prev, None, None, letter, 0)
                    self.bt.leaves.append(n)
                else:
                    n = Node(prev, None, None, 0, None)
                    if not self.bt.root:
                        self.bt.root = n
                    prev = n
                    n.left = self.deserialize_tree(header, prev)
                    n.right = self.deserialize_tree(header, prev)
                return n
            except (StopIteration):
                return self.bt.root

    def code(self):
        # Fill the ascii-to-code dictionary.
        for x in self.bt.leaves:
            letter = x.letter
            s, ht = 0, 0
            n = x
            while n:
                if n.parent:
                    if n == n.parent.right:
                        s |= (1 << ht)
                n = n.parent
                ht += 1
            self.asciitocode[letter] = bitarray(bin(s)[2:].zfill(ht-1))
        if action == 'c':
            fmt = []
            for c in self.data:
                fmt.append(c)
            self.bitstream = bitarray()
            self.bitstream.encode(self.asciitocode, fmt)
                     
    def get_freq(self, string):
        # A character frequency counter to create the Huffman tree
        freq_dict = {}
        for c in string:
            try:
                freq_dict[c] += 1
            except (KeyError):
                freq_dict[c] = 1
        return freq_dict

    
def main():
    H = Huffman()
    
    # Compression
    if action == 'c':
        with open(inputfile, 'rb') as fi:
            H.data = fi.read()
        H.string_to_tree()
        H.code()

        # Determine byte alignment and create footer
        b_align = len(H.bitstream) % 8
        if b_align == 0:
            footer = bitarray('00001000')
        else:
            footer = bitarray(str(bin(b_align)[2:]).zfill(8))

        # Pack the end the of bitstream
        while len(H.bitstream) % 8 != 0:
            H.bitstream += '0'

        # Create the header
        header = H.serialize_tree(H.bt.root)
        header = ''.join(str(z) for z in header)
        while len(header) % 8 != 0:
            header += '0'
        header_byte_len = str(bin(len(header)/8))[2:].zfill(16)
        header = bitarray(header_byte_len + header)

        # Put header byte len, header, data, and footer together and write file
        H.bitstream = header + H.bitstream + footer
        with open(outputfile, 'wb') as of:
            H.bitstream.tofile(of)
            
    # Decompression
    elif action == 'd':
        with open(inputfile, "rb") as fi:
            header_len = ''
            for _ in xrange(2):
                byte = fi.read(1)
                header_len += bin(ord(byte))[2:].zfill(8)
            header_len = int(header_len,2)
            header = fi.read(header_len)
            data_start_byte = fi.tell()
            fi.seek(-1,2)
            data_end_byte = fi.tell()-1
            H.footer = ord(fi.read(1))
            fi.seek(data_start_byte)
            data = fi.read(data_end_byte-data_start_byte+1)

        # Apportion the chunks read from the file
        H.header = bitarray()
        for byte in header:
            H.header += bitarray(bin(ord(byte))[2:].zfill(8))
        H.bitstream = bitarray()
        for byte in data:
            H.bitstream += bitarray(bin(ord(byte))[2:].zfill(8))

        # End the bitstream according to footer
        H.bitstream = H.bitstream[:(len(H.bitstream)-(8-H.footer))]
       
        # Deserialize Huffman tree, decode, write file
        H.bt.root = H.deserialize_tree(iter(H.header))
        H.code()
        decoded = H.bitstream.decode(H.asciitocode)
        output_string = ''.join(c for c in decoded)
        with open(outputfile, 'wb') as of:
            of.write(output_string)

        part = float(os.path.getsize(outputfile))/os.path.getsize(inputfile)
        print("File compression ratio: %f:1" % part)
    else:
        raise Exception("Use: python hcode.py <c/d> <inputfile> <outputfile>")

    
if __name__ == "__main__":
    main()
    
