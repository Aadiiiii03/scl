from setuptools import setup

setup(
    name="sclprogram",
    version="0.1",
    description="Swarm Computing Library",
    py_modules=["scl"], # This tells pip to look for scl.py
    install_requires=[], # Add numpy or other libraries here if needed
)
