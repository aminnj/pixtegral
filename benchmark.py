import os
import sys
import time
import numpy as np

from scipy.integrate import quad
from scipy.special import kn

from pixtegral import pixtegrate

def integrate_numpy(func,bounds,npoints=10000):
    xmin, xmax = bounds
    xvals = np.linspace(xmin,xmax,npoints)
    yvals = func(xvals)
    return np.trapz(yvals,xvals)


def integrate_scipy(func,bounds):
    xmin, xmax = bounds
    return quad(func,xmin,xmax)[0]

def avg_of_10(func, bounds, int_func):
    # return integral and time taken avg over 10
    int_func(func,bounds) # warmup
    t0 = time.time()
    for _ in range(10):
        integral = int_func(func,bounds) # warmup
    return integral, (time.time()-t0)/10.

if __name__ == "__main__":

    infos = [
            ("polynomial", lambda x: x**2-3, [-3,4], 49000),
            ("sinusoid", lambda x: np.sin(10*x)+0.5, [0,np.pi],19000),
            ("bessel", lambda x: kn(3,x), [1,10],np.nan),
            ]

    d_times = {}
    d_valaccs = {}
    for name,func,bounds,tpenpaper in infos:
        intpixtegrate = avg_of_10(func,bounds,pixtegrate)
        intscipy = avg_of_10(func,bounds,integrate_scipy)
        intnumpy = avg_of_10(func,bounds,integrate_numpy)
        d_times[name] = dict(
                pixtegrate=1.e3*intpixtegrate[1],
                scipy=1.e3*intscipy[1],
                numpy=1.e3*intnumpy[1],
                )
        d_times[name]["pen/paper"] = tpenpaper
        d_valaccs[name] = (
                intpixtegrate[0],
                intscipy[0],
                100.*(intpixtegrate[0]-intscipy[0])/intscipy[0],
                )

    print "| method | polynomial | sinusoid | bessel |"
    print "| :- | - | - | - |"
    for method in ["pixtegrate","numpy","scipy","pen/paper"]:
        unit = "ms"
        rounding = 3 if method in ["numpy","scipy"] else 1
        print "| {} ({}) | {} | {} | {} |".format(
                method,
                "ms",
                round(d_times["polynomial"][method],rounding),
                round(d_times["sinusoid"][method],rounding),
                round(d_times["bessel"][method],rounding),
                )

    print
    print "| method | polynomial | sinusoid | bessel |"
    print "| :- | - | - | - |"
    print "| pixtegrate | {:.4f} | {:.4f} | {:.4f} |".format(
            d_valaccs["polynomial"][0],
            d_valaccs["sinusoid"][0],
            d_valaccs["bessel"][0],
            )
    print "| scipy | {:.4f} | {:.4f} | {:.4f} |".format(
            d_valaccs["polynomial"][1],
            d_valaccs["sinusoid"][1],
            d_valaccs["bessel"][1],
            )
    print "| *difference (%)* | {:.2f} | {:.2f} | {:.2f} |".format(
            d_valaccs["polynomial"][2],
            d_valaccs["sinusoid"][2],
            d_valaccs["bessel"][2],
            )

