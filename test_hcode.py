import os
import subprocess
from random import randint

all_res = 0
for i in xrange(1,6):
    file_size = randint(10000000,20000000)
    with open('test_output.test', 'wb') as fout:
        fout.write(os.urandom(file_size))
    x = subprocess.call('python hcode.py c test_output.test test_output.comp'\
                        , shell=True)
    y = subprocess.call('python hcode.py d test_output.comp test_output.unc'\
                        , shell=True)
    z = subprocess.call('diff test_output.test test_output.unc', shell=True)

    test_res = (x | y) | z
    all_res |= test_res
    if test_res == 0:
        print "Test %d with size %d bytes PASSED.\n" % (i, file_size)
    else:
        print "Test %d with size %d bytes FAILED.\n" % (i, file_size)
            
    subprocess.call('rm test_output.test test_output.comp test_output.unc',shell=True)

if all_res == 0:
    print "All tests PASSED."
else:
    print "Test(s) FAILED."
