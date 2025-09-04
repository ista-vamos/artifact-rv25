The traces
for I in `seq 1 24040`; do ./gentr.py 1 data/test-$I-in.txt data/test-$I-out.txt > test-$I.tr; done
