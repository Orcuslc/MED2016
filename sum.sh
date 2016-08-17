#!/usr/bin/bash
rm count.txt
cd training-1/txt/ && ls -l|wc -l >> ../../count.txt
cd ../../training-2/txt/ && ls -l|wc -l >> ../../count.txt
cd ../../test-1/txt/ && ls -l|wc -l >> ../../count.txt
cd ../../test-2/txt/ && ls -l|wc -l >> ../../count.txt
cd ../../test-3/txt/ && ls -l|wc -l >> ../../count.txt
cd ../../ && cat count.txt
