from distutils.core import setup

install_requires = [
    "numpy",
    "opencv-python",
    "scipy",
    "numba"
]
setup(name='Connect4',
      version='1.0',
      author='Rudra Menon',
      author_email='rudra.p.menon@gmail.com',
      install_requires=install_requires
      )
