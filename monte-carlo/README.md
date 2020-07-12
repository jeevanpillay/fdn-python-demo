# Monte-Carlo example #
This directory contains stripped down version of the research problem I have studied
for a while, control of Thermostatically Controlled Loads. Implemented is a random
exploration of the control policy space (like a Reinforcement Learning method would
do), using a Monte-Carlo simulation of 10.000 days. Implemented are four variants:

* Python for loop, plain class using Numpy math,
* Python for loop, using Numba JIT class,
* Numba JIT loop using Numba JIT class,
* Java for loop as baseline.


### Usage instructions ###
Open a command line, clone the repository and go to it.

	git clone git@bitbucket.org:fdenijs/fdn-python-demo.git
	cd fdn-python-demo

Set up a temporary Python venv virtual environment and activate it.

	py -3 -m venv tempenv
	.\tempenv\Scripts\activate

Install and/or update pip, numpy, numba.

	python -m pip install --upgrade pip numpy numba

Compile Java benchmark

	javac monte-carlo\*.java

Run the benchmarks

	java -cp monte-carlo BenchmarkMonteCarlo && python monte-carlo\bench_mc.py

Deactivate the python virtual environment

	.\tempenv\Scripts\deactivate


### Expected output ###
On the command line, four prints like:

	Java OO     : per-run 0.0000077476s, total  0.28024s. (checksum -51084935.283986)
	JIT all     : per-run 0.0000493029s, total  0.69004s. (checksum -51495183.511094)
	JIT class   : per-run 0.0007409425s, total  7.65744s. (checksum -51495183.511094)
	Python OO   : per-run 0.0038871222s, total 39.19024s. (checksum -51495183.511094)
