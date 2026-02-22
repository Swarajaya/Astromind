from setuptools import setup, find_packages

setup(
    name="astromind",
    version="1.0.0",
    description="AI-Driven Near-Earth Object Risk Simulator — Quantum ML + Physics",
    author="AstroMind Team",
    python_requires=">=3.10",
    packages=find_packages(),
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={"console_scripts": ["astromind=main:main"]},
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
