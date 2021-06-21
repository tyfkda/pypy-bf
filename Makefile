
PYPY_SRC_PATH:=$(HOME)/Downloads/pypy3.7-v7.3.5-src
XBYAK_INC_PATH:=$(INCLUDE_PATH)/xbyak

for_rpython-c:	for_rpython.py bf.py
	$(PYPY_SRC_PATH)/rpython/bin/rpython for_rpython.py

bf_c:	bf_c.cpp
	$(CXX) -o $@ -std=c++17 -O3 $<

bf_xbyak:	bf_xbyak.cpp
	$(CXX) -o $@ -I $(XBYAK_INC_PATH) -O3 $<

for_rpython-jit:	for_rpython.py bf.py
	PYTHONPATH=$(PYPY_SRC_PATH) $(PYPY_SRC_PATH)/rpython/bin/rpython --opt=jit --output $@ for_rpython.py

.PHONY:	clean
clean:
	rm -rf a.out bf_c bf_xbyak *.pyc __pycache__ for_rpython-c for_rpython-jit


SOURCE_BF:=examples/mandelbrot.b

.PHONY:	run-cpython-mandelbrot
run-cpython-mandelbrot:
	@time python for_cpython.py $(SOURCE_BF)

.PHONY:	run-pypy-mandelbrot
run-pypy-mandelbrot:
	@time pypy for_cpython.py $(SOURCE_BF)

.PHONY:	run-rpython-mandelbrot
run-rpython-mandelbrot:	for_rpython-c
	@time ./for_rpython-c $(SOURCE_BF)

.PHONY:	run-jit-mandelbrot
run-jit-mandelbrot:	for_rpython-jit
	@time ./for_rpython-jit $(SOURCE_BF)

.PHONY:	run-bf_c
run-bf_c:	bf_c
	@time ./bf_c $(SOURCE_BF)

.PHONY:	run-bf_xbyak
run-bf_xbyak:	bf_xbyak
	@cat $(SOURCE_BF) | time ./bf_xbyak
