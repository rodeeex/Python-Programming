# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cdivision=True
# initializedcheck=False

from libc.math cimport sin as c_sin
from cython.parallel cimport prange

cdef double c_integrate(double (*f)(double) noexcept nogil, double a, double b, int n_iter) nogil:
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef double half_step = step / 2.0
    cdef int i
    for i in range(n_iter):
        acc += f(a + i * step + half_step) * step
    return acc

def integrate_sin_nogil_threads(double a, double b, int n_jobs=2, int n_iter=10000000):
    cdef double step_chunk = (b - a) / n_jobs
    cdef double[64] results
    cdef int i
    cdef double total = 0.0
    cdef int iter_per_chunk = n_iter // n_jobs

    with nogil:
        for i in prange(n_jobs, num_threads=n_jobs, schedule='static'):
            results[i] = c_integrate(c_sin, a + i * step_chunk, a + (i + 1) * step_chunk, iter_per_chunk)

    for i in range(n_jobs):
        total += results[i]
    return total