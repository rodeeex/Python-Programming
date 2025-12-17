# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cdivision=True
# initializedcheck=False

from libc.math cimport sin as c_sin
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

cdef double c_integrate(double (*f)(double), double a, double b, int n_iter):
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef double half_step = step / 2.0
    cdef int i
    for i in range(n_iter):
        acc += f(a + i * step + half_step) * step
    return acc

def integrate_sin(double a, double b, int n_iter=10000000):
    return c_integrate(c_sin, a, b, n_iter)

def integrate_sin_with_threads(double a, double b, int n_jobs=2, int n_iter=10000000):
    cdef double step = (b - a) / n_jobs
    cdef int iter_per_job = n_iter // n_jobs

    with ThreadPoolExecutor(max_workers=n_jobs) as executor:
        fs = [executor.submit(integrate_sin, a + i * step, a + (i + 1) * step, iter_per_job)
              for i in range(n_jobs)]
        return sum(f.result() for f in as_completed(fs))

def integrate_sin_with_processes(double a, double b, int n_jobs=2, int n_iter=10000000):
    cdef double step = (b - a) / n_jobs
    cdef int iter_per_job = n_iter // n_jobs

    with ProcessPoolExecutor(max_workers=n_jobs) as executor:
        fs = [executor.submit(integrate_sin, a + i * step, a + (i + 1) * step, iter_per_job)
              for i in range(n_jobs)]
        return sum(f.result() for f in as_completed(fs))