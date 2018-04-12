from heapify import *
import bitstring
from collections import deque
import binascii
import os
from sys import argv

script, action, inputfile, outputfile = argv


class Node(object):
    def __init__(self, parent, left, right, letter, key):
        self.parent = parent
        self.letter = letter
        self.left = left
        self.right = right
        self.key = key

        
class BT(object):
    def __init__(self):
        self.root = None
        self.leaves = []

        
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
        freq = self.get_freq(self.data)
        heap = Heap(h_type='max')
        for x in freq:
            n = Node(None, None, None, x[0], x[1])
            heap.insert((x[1], n))
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
                y = next(header)
                if y == '1':
                    buf = ''
                    for _ in xrange(8):
                        buf += next(header)
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
        # Fill the ascii-to-code or code-to-ascii dictionary.
        for x in self.bt.leaves:
            letter = x.letter
            s = deque([])
            n = x
            while n:
                if n.parent:
                    if n == n.parent.right:
                        s.appendleft('1')
                    else:
                        s.appendleft('0')
                n = n.parent
            s = ''.join(c for c in s)
            if action == 'c':
                s = '0b' + s
                self.asciitocode[str(ord(letter))] = s
            else:
                self.codetoascii[s] = ord(letter)
        if action == 'c':
            fmt = ''
            for c in self.data:
                fmt += str(ord(c)) + ','
            self.bitstream = bitstring.pack(fmt, **self.asciitocode)
        
    def decode(self):
        # Passes the binary data stream through the code-to-ascii dictionary.
        output = ''
        j = 0
        buf = ''
        read_chunk_size = 8
        while j < len(self.bitstream):
            byte = '0x' + self.bitstream[j:j+2]
            bits = bin(int(byte, 16))[2:].zfill(8)
            if j >= len(self.bitstream) - 2:
                read_chunk_size = self.footer
            for i in xrange(read_chunk_size):
                buf += bits[i]
                if buf in self.codetoascii:
                    output += str(chr(self.codetoascii[buf]))
                    buf = ''
            j += 2
        return output
    
    def get_freq(self, string):
        # A character frequency counter to create the Huffman tree
        freq_dict = {}
        for c in string:
            try:
                freq_dict[c] += 1
            except (KeyError):
                freq_dict[c] = 1
        freq = []
        for x in freq_dict.keys():
            freq.append((x, freq_dict[x]))
        return freq

    
def main():
    H = Huffman()
    if action == 'c':
        with open(inputfile, 'rb') as fi:
            H.data = fi.read()
        H.string_to_tree()
        H.code()

        # determine byte alignment and create footer
        b_align = len(H.bitstream) % 8
        if b_align == 0:
            footer = bitstring.BitArray('0b00001000')
        else:
            footer = bitstring.BitArray('0b' + str(bin(b_align)[2:]).zfill(8))

        # pack the end the of bitstream
        while len(H.bitstream.bin) % 8 != 0:
            H.bitstream.bin += '0'

        # create the header
        header = H.serialize_tree(H.bt.root)
        header = ''.join(str(z) for z in header)
        while len(header) % 8 != 0:
            header += '0'
        header_byte_len = str(bin(len(header)/8))[2:].zfill(16)
        header = '0b' + header_byte_len + header

        # put header byte len, header, data, and footer together and write file
        H.bitstream = bitstring.BitArray(header) + H.bitstream + footer
        with open(outputfile, 'wb') as of:
            H.bitstream.tofile(of)
    elif action == 'd':
        with open(inputfile, "rb") as fi:
            hexdata = binascii.hexlify(fi.read())
            
        # read header and footer
        header_len = int(hexdata[:4], 16)
        header = '0x'+ hexdata[4:4+2*header_len]
        H.header = bin(int(header, 16))[2:].zfill(header_len*8)
        H.footer = int('0x'+hexdata[len(hexdata)-2:], 16)

        # deserialize Huffman tree, decode, write file
        H.bitstream = hexdata[4+2*header_len:len(hexdata)-2]
        H.bt.root = H.deserialize_tree(iter(H.header))
        H.code()
        H.data = H.decode()
        with open(outputfile, 'wb') as of:
            of.write(H.data)

        part = float(os.path.getsize(outputfile))/os.path.getsize(inputfile)
        print "File compression ratio: %f:1" % part
    else:
        raise Exception("Use: python hcode.py <c/d> <inputfile> <outputfile>")

if __name__=="__main__":
    main()
    
