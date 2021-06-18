
PYPY_SRC_PATH:=$(HOME)/Downloads/pypy3.7-v7.3.5-src

for_rpython-c:	for_rpython.py bf.py
	$(PYPY_SRC_PATH)/rpython/bin/rpython for_rpython.py

bf_c:	bf_c.cpp
	$(CXX) -o $@ -std=c++17 -O3 $<

.PHONY:	clean
clean:
	rm -rf a.out bf_c *.pyc __pycache__ for_rpython-c


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

.PHONY:	run-bf_c
run-bf_c:	bf_c
	@time ./bf_c $(SOURCE_BF)
