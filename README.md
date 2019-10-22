## Installation

It is a single file. You just need `matplotlib`.

## Overview
Pixtegral is a fast\* and accurate\* integrator
for 1-dimensional functions.

## Usage
```python
from pixtegral import pixtegrate
print(pixtegrate(lambda x: -3+x**2, bounds=[-3,4]))
```
Additionally, pixtegrate is so fast that there is a 
keyword argument that tells pixtegrate to sleep for a bit
in case it is too fast for your taste.
```python
# sleep 
print(pixtegrate(lambda x: -3+x**2, bounds=[-3,4], sleep=1.0))
```

## Method

Pixtegral takes a graphical approach to computing integrals.  It
eliminates the overhead associated with fancy adaptive and
iterative methods by plotting the function over the specified
range, converting it into an image, and then counting pixels to
determine the integral. It is blazingly fast\*.

## Benchmarks

To benchmark the speed and accuracy of the integrator, three
functions (x<sup>2</sup>-3, 0.5+sin(10x), and
some random Bessel function) were evaluated with
pixtegrate, numpy (`np.trapz()`), scipy (`scipy.integrate.quad`),
and pen/paper (Holiday Inn pen + A4 paper).

The times per integration (in milliseconds) below show
that pixtegrate blows the pen/paper method out of the water,
but is slightly slower than numpy/scipy.


| method          | polynomial | sinusoid | bessel |
| :-               | -          | -        | -      |
| pixtegrate (ms) | 42.0       | 34.6     | 40.8   |
| numpy (ms)      | 0.096      | 0.187    | 6.302  |
| scipy (ms)      | 0.018      | 0.03     | 0.23   |
| pen/paper (ms)  | 49000.0    | 19000.0  | nan    |

The integrals calculated from pixtegrate are compared with scipy below.
For all 3 functions, pixtegrate offers percent-level accuracy.

| method           | polynomial | sinusoid | bessel |
| :-                | -          | -        | -      |
| pixtegrate       | 9.3308     | 1.5466   | 2.7483 |
| scipy            | 9.3333     | 1.5708   | 2.8286 |
| *difference (%)* | -0.03      | -1.54    | -2.84  |
