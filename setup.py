from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()

setup(
    name="pynorg",
    version="0.2.0",
    description="A brief description of your project",
    author="Junior Sundar",
    author_email="juniorsundar@gmail.com",
    url="https://github.com/juniorsundar/pynorg",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "pynorg=pynorg.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=install_requires,
    extras_require={
        "dev": [
            "pytest>=6.2",
            "black>=20.8b1",
        ],
    },
)

