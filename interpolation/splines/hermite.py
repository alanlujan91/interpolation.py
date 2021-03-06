import numpy as np
from numba import jit


@jit(nopython=True)
def hermite_splines(lambda0):
    """Computes the cubic Hermite splines in lambda0
    Inputs: - float: lambda0
    Output: - tuple: cubic Hermite splines evaluated in lambda0"""
    h00 = 2*(lambda0**3) - 3*(lambda0**2) + 1
    h10 = (lambda0**3) - 2*(lambda0**2) + lambda0
    h01 = -2*(lambda0**3) + 3*(lambda0**2)
    h11 = (lambda0**3) - (lambda0**2)
    return (h00, h10, h01, h11)


@jit(nopython=True)
def hermite_interp(x0, xk, xkn, pk, pkn, mk, mkn):
    """Returns the interpolated value for x0.
    Inputs: - float: x0, abscissa of the point to interpolate
            - float: xk, abscissa of the nearest lowest point to x0 on the grid
            - float: xkn, abscissa of the nearest largest point to x0 on the grid
            - float: pk, value associated to xk
            - float: pkn, value associated to xkn
            - float: mk, tangent in xk
            - float: mkn, tangent in xkn
    Output: - float: interpolated value for x0
    """
    t = (x0-xk)/(xkn-xk)
    hsplines = hermite_splines(t)
    return (pk*hsplines[0] + mk*(xkn-xk)*hsplines[1] + pkn*hsplines[2] + mkn*(xkn-xk)*hsplines[3])


@jit(nopython=True)
def HermiteInterpolation(x0, x, y, tang):
    """Returns the interpolated value for x0
    Inputs: - float: x0, abscissa of the point to interpolate
            - np.ndarray: x, x-axis grid
            - np.ndarray: y, values of elements in x
            - np.ndarray: tang, tangents of the x elements
    Output: - float: interpolated value"""
    ###### Extrapolation case ######
    if x0 <= np.min(x):
        return y[0]
    elif x0 >= np.max(x):
        return y[-1]
    
    ###### Interpolation case ######
    indx = np.searchsorted(x, x0)
    xk, xkn = x[indx-1], x[indx]
    pk, pkn = y[indx-1], y[indx]
    mk, mkn = tang[indx-1], tang[indx]
    return hermite_interp(x0, xk, xkn, pk, pkn, mk, mkn)


@jit(nopython=True)
def HermiteInterpolationVect(xvect, x, y, tang):
    """Returns the interpolated value for all elements in xvect
    Inputs: - np.ndarray: xvect, vector of abscissa of the point to interpolate
            - np.ndarray: x, x-axis grid
            - np.ndarray: y, values of elements in x
            - np.ndarray: tang, tangents of the x elements
    Output: - np.ndarray: interpolated values"""
    N = len(xvect)
    out = np.zeros(N)
    for i in range(N):
        x0 = xvect[i]
        out[i] = HermiteInterpolation(x0, x, y, tang)
    return out