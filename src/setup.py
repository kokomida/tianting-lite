from setuptools import setup, find_packages

setup(
    name="memoryhub-ti",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "pyroaring>=0.3.0",
    ],
    extras_require={
        "dev": ["pytest", "pysimdjson"],
    },
    python_requires=">=3.10",
)