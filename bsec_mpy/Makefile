
bsec.mpy: objs/Bsec.o mpy_ld.py
	python3 mpy_ld.py objs/*.o --arch armv7m --output bsec.mpy

libalgobsec.lib:
	@echo "Please download libalgobsec.lib from bosch website!"
	exit 1

objs/Bsec.o: libalgobsec.lib
	@mkdir -p objs
	cd objs; ar x ../libalgobsec.lib; cd ..

mpy_ld.py:
	wget "https://raw.githubusercontent.com/adafruit/circuitpython/main/tools/mpy_ld.py"
	wget "https://raw.githubusercontent.com/adafruit/circuitpython/main/py/makeqstrdata.py"
	echo "Make sure you have pyelftools installed (try pip install pyelftools)"
	echo "Make sure you have huffman installed (try pip install huffman)"


