from setuptools import setup, Extension
from Cython.Build import cythonize
import sys

extensions = [
    Extension(
        "c_integrate",
        ["c_integrate.pyx"],
    ),
    Extension(
        "c_integrate_nogil",
        ["c_integrate_nogil.pyx"],
        extra_compile_args=['/openmp'],
        extra_link_args=['/openmp'],
    )
]

setup(
    ext_modules=cythonize(
        extensions,
        annotate=True,
        force=True,
        compiler_directives={'language_level': 3}
    ),
    script_args=['build_ext', '--inplace']
)