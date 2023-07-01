from distutils.core import setup  # pylint: disable=(deprecated-module)

setup(
    name="orex",
    packages=["orex"],
    version="1.0",
    license="MIT",
    description="Human-friendly regex",
    author="The collective",
    author_email="akingl2016@gmail.com",
    url="https://github.com/HCelion/orex",
    download_url="https://github.com/user/reponame/archive/v_01.tar.gz",  # I explain this later on
    keywords=["regex", "regular", "expressions"],
    install_requires=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",  #
        "Topic :: Software Development :: RegEx",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
