from setuptools import setup

setup(
    name="caption-utils",
    version="0.1.0",
    author="serdarakarca",
    author_email="serdar@yuix.org",
    license="GNU",
    packages=["caption_utils"],
    install_requires=[
        "sentence-splitter==1.4",
        "Levenshtein==0.27.1",
        "big-phoney==1.0.1",
        "faster-whisper==1.2.0",
    ],
)
