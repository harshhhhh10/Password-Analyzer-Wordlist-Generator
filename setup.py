from setuptools import setup, find_packages

setup(
    name="password-strength-analyzer",
    version="1.0.0",
    author="HARSH SONI",
    author_email="***",
    description="Password Strength Analyzer with Custom Wordlist Generator",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/harshhhhh10/Password-Analyzer-Wordlist-Generator",
    py_modules=[
        "main",
        "cli_app",
        "gui_app",
        "password_analyzer",
        "wordlist_generator",
        "common_passwords",
        "utils",
    ],
    python_requires=">=3.8",
    install_requires=[
        "zxcvbn-python>=4.4.24",
        "nltk>=3.8.1",
    ],
    entry_points={
        "console_scripts": [
            "passtool=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
    ],
    keywords="password strength analyzer wordlist generator security",
)
