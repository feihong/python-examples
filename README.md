# Feihong's Python Examples

## Installation

### Mac OS X

```
brew install python3
```

### Ubuntu

```
wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tar.xz
tar xvf Python-3.5.2.tar.xz
cd Python-3.5.2
./configure
make
make test
sudo make install
```

## Prepare virtualenv

```
mkvirtualenv -p python3 -r requirements.txt examples
```

## Tests

Run tests:

```
nosetests -v
```

Run tests without capturing stdout (necessary if you want to debug within test code):

```
nosetests -s
```
