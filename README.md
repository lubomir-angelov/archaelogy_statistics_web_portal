# archaelogy_statistics_web_portal
An archaeological statistics web portal with visual representations and artifact enrollment.

The repo aims to achieve the following tasks:
1. Implement an the archaelogical statiscs app with TDD.
2. Write tests for and re-create the app found at: https://github.com/lubomir-angelov/ceramics
3. Implement the new features.


# setup
Installing pyenvv

```bash
curl -fsSL https://pyenv.run | bash

pyenv install 3.13.5
```

In case of issues with missing os packages run:
```bash
sudo apt-get update
sudo apt install tk-dev bzip2 build-essential sqlite3  libsqlite3-dev -y
sudo apt-get install build-essential zlib1g-dev libffi-dev libssl-dev libbz2-dev libreadline-dev libsqlite3-dev liblzma-dev libncurses-dev tk-dev -y
```

Setting the global python
```bash
pyenv global 3.13
```

Creating a venv
```bash
python -m venv ~/venvs/arch_stats_web
```

You can now use this venv in your preferred IDE. 

To install the required packages to run the app use:
```bash
pip install -r requirements.txt
```

To run the tests run:
```bash
pip install -r requirements.txt

# To see everything fail run:
pytest --maxfail=1 --disable-warnings -q
```