# monitorbookprices
Monitor book prices for some italian, english, and german online bookshops.



# Installation
We recommend using the provided environment `environment.yml` to set up a Python environment using [mamba](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html) environment with the necessary dependencies.
Once the environment is installed, one need to activate it before using it (i.e., before running python scripts and notebooks).
This is done via
```shell
mamba activate monitor
```

Run the following command to install the package (after having activated the environment):
```shell
pip install .
```


## `geckodriver`
To scrape [osiander](https://www.osiander.de) we use [Selenium WebDriver](https://selenium-python.readthedocs.io/).
To use it correctly, we need the web browser engine [GeckoDriver](https://github.com/mozilla/geckodriver).
We summarize here the steps to install GeckoDriver:
1. Download the latest release of GeckoDriver from [here](https://github.com/mozilla/geckodriver/releases).
2. Extract the tarball with `tar -xvzf geckodriver*`.
3. Make it executable with `chmod +x geckodriver`.
4. Move the executable into a folder in PATH. Examples are:
    - `mv geckodriver <path_to_conda_environment>/bin` if you have a conda/mamba environment setup.
    - `sudo mv geckodriver /usr/local/bin` (su priviliges needed)



# Development
```shell
pip install -e .
```



# Pre-commits
```shell
pip install .[pre-commit,testing]  # install extra dependencies. For zsh use .'[pre-commit,testing]'
pre-commit install  # install pre-commit hooks
```



# Tests
```shell
pytest -v # discover and run all tests
```



# Supported websites:
- [adelphi](https://www.adelphi.it/)
- [buecher](https://www.buecher.de/)
- [feltrinelli](https://www.lafeltrinelli.it/)
- [ibs](https://www.ibs.it/)
- [libraccio](https://www.libraccio.it/)
- [mondadori](https://www.mondadoristore.it/)
- [osiander](https://www.osiander.de/)
