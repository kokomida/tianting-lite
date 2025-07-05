from setuptools import find_packages, setup

setup(
    name="memoryhub-ti",
    version="0.0.1",
    packages=find_packages("."),
    package_dir={"": "."},
    install_requires=[
        "pyroaring>=0.3.0",
    ],
    extras_require={
        "dev": ["pytest", "pysimdjson"],
    },
    python_requires=">=3.10",
)
