# README #
This repository contains benchmark code, derived from the second example provided in [this blog post](https://www.experfy.com/blog/why-you-should-forget-loops-and-embrace-vectorization-for-data-science/).

Implemented are six variants:
* Python for loop.
* Python numpy vectorized.
* Python calling C implementation.
* Python numba vectorized.
* Java stream-based.
* Java loop-based.


### Usage instructions ###
Set up a Python venv virtual environment and activate it.
`py -3 -m venv tempenv
`.\tempenv\Scripts\activate

Install and/or update pip, numpy, disttools. On Windows, this assumes [Microsoft Visual C++ build tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) installed.
`python -m pip install --upgrade pip numpy numba disttools

Build and install self-built C package implementing the demo function
`cd src\demo
`python setup.py build
`python setup.py install --record files.txt
`cd ..\..

Compile Java benchmark
`javac src\BenchJava.java

Run the Python benchmarks
`start /B /high python src\bench_numpy.py >> python.txt

Run the Java benchmarks
`start /B /high java -cp src BenchJava >> java.txt


### Expected output ###
In the python.txt file, lines like:
`Vanilla     641036.75us, checksum 163457.228047, head [ 0.89, 0.48, 1.00, 0.00, 0.00, ...]
`Numpy vec   285016.06us, checksum 163457.228047, head [ 0.89, 0.48, 1.00, 0.00, 0.00, ...]
`Native-c     11000.00us, checksum 163457.228047, head [ 0.89, 0.48, 1.00, 0.00, 0.00, ...]
`Wrapping c  175009.97us, checksum 163457.228047, head [ 0.89, 0.48, 1.00, 0.00, 0.00, ...]
`Numba vec    10000.47us, checksum 163457.228047, head [ 0.89, 0.48, 1.00, 0.00, 0.00, ...]

In the java.txt file, lines like:
`Stream       25672.04us, checksum 164080.174512, head [ 0.83, 0.97,-1.65, 0.00, 0.53, ...]
`Loop         11064.05us, checksum 164080.174512, head [ 0.83, 0.97,-1.65, 0.00, 0.53, ...]
