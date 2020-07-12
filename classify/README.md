# Classify example using numba for speed-up #
This directory contains benchmark code, derived from the second example provided in [this blog post](https://www.experfy.com/blog/why-you-should-forget-loops-and-embrace-vectorization-for-data-science/). Implemented are six variants:

* Python for loop.
* Python numpy vectorized.
* Python calling C implementation, wrapped to return a list.
* Python numba vectorized.
* Java stream-based.
* Java loop-based.


### Usage instructions ###
Open a command line, clone the repository and go to it.

	git clone git@bitbucket.org:fdenijs/fdn-python-demo.git
	cd fdn-python-demo

Set up a temporary Python venv virtual environment and activate it.

	py -3 -m venv tempenv
	.\tempenv\Scripts\activate

Install and/or update pip, numpy, disttools. On Windows, this assumes [Microsoft Visual C++ build tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) installed.

	python -m pip install --upgrade pip numpy numba disttools

Build and install self-built C package implementing the demo function

	cd classify\demo
	python setup.py build
	python setup.py install --record files.txt
	cd ..\..

Compile Java benchmark

	javac classify\BenchJava.java

Run the Python benchmarks

	start /B /high python classify\bench_python.py >> python.txt

Run the Java benchmarks

	start /B /high java -cp classify BenchJava >> java.txt

Deactivate the python virtual environment

	.\tempenv\Scripts\deactivate


### Expected output ###
In the python.txt file, per variant, 10 lines like:

	Vanilla     594034.19us, checksum 163795.072368, head [ 0.00, 1.00, 0.00, 0.00, 0.00, ...]
	Numpy vec   203011.51us, checksum 163795.072368, head [ 0.00, 1.00, 0.00, 0.00, 0.00, ...]
	Native-c      7000.00us, checksum 163795.072368, head [ 0.00, 1.00, 0.00, 0.00, 0.00, ...]
	Wrapping c  135007.86us, checksum 163795.072368, head [ 0.00, 1.00, 0.00, 0.00, 0.00, ...]
	Numba vec     9000.54us, checksum 163795.072368, head [ 0.00, 1.00, 0.00, 0.00, 0.00, ...]

In the java.txt file, per variant, 10 lines like:

	Stream       18781.74us, checksum 163775.621873, head [ 0.00, 0.92, 2.00, 0.00, 0.74, ...]
	Loop         11228.22us, checksum 163775.621873, head [ 0.00, 0.92, 2.00, 0.00, 0.74, ...]
