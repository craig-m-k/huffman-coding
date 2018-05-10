# Huffman coding
File compression/decompression in Python 2.

### Command line:
```
python hcode.py <c/d> <inputfile> <outputfile>
```

where 'c' compresses inputfile to outputfile and
'd' decompresses inputfile to outputfile.

### Huffman class:

* .data : information to code/decode.

* .header : coded Huffman tree

* .footer : byte containing bit alignment of final data byte

* .bitstream: for reading/writing to file

* .asciitocode: code dictionary

* .bt: Huffman object (binary tree) for coding/decoding

### Compressed file structure:

*  bytes 1 - 2: bytes storing value x, the size in bytes of
  stored Huffman tree
  
*  bytes 3 - x+3: Huffman tree
  
*  bytes x+4 - len(file)-1 : data
  
*  byte len(file): a single byte indicating how many bits of the
   previous byte should be read

### Associated functions:
*  code(): Creates a dictionary for ascii-to-code

*  string_to_tree():
	Uses a heap in heapify.py to create the Huffman tree from the input file.

*  serialize_tree(): Creates a string representation of the Huffman tree.

*  deserialize_tree(string): Transforms string into Huffman binary tree.

*  get_freq(string): Returns a dictionary of character frequencies.

### Testing:

  test_hcode.py tests the implementation as follows: random file -> compress -> decompress -> diff against random file
  
