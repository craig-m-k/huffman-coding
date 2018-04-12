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

* .footer : byte containing good bits of final data byte

* .bitstream: for reading/writing to file

* .asciitocode: coder dictionary

* .codetoascii: decoder dictionary

* .bt: Huffman object (binary tree) for coding/decoding

### Compressed file structure:

*  bytes 1 - 2: bytes storing value x, the size in bytes of
  stored Huffman tree
  
*  bytes 3 - x: Huffman tree
  
*  bytes x+1 - len(file)-1 : data
  
*  byte len(file): a single byte indicating how many bits of the
   previous byte should be read

### Associated functions:
*  code(): Creates a dictionary for ascii-to-code or code-to-ascii.

* decode(): Passes the data stream through the code-to-ascii dictionary.

*  string_to_tree():
	Uses a heap to create the Huffman tree from the input file.

*  serialize_tree(): Creates a string representation of the Huffman tree.

*  deserialize_tree(string): Transforms string into Huffman binary tree.

*  get_freq(string): Returns a dictionary of character frequencies.

### Things to improve:

  The BitString library is not very fast, so we should probably try to 
  minimize or eliminate its use.
  
