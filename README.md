# Orex

Orex is a package designed to simplify regular expressions in Python. It provides a high-level interface for constructing and working with regular expressions, making it easier and more intuitive to use.

The package is heavily inspired by Richy Cotton's `rebus` package for the `R` language.

## Installation

You can install Orex using pip:

```shell
pip install orex
```

To use Orex, import the `orex` package into your Python script:

```python
import orex as ox
```


## Creating regular expressions

The easiest regular expression is just a literal string to be found.

```python
s = 'Hello World'
pattern = ox.literal('Hello')
pattern.is_match(s)
```
```python
[] True
```

Orex regular expressions are extended by simply using a `+`.
A slightly more useful example is to find a hex colour

```python
pattern = ox.literal('#') + ox.HEXDIGIT + ox.HEXDIGIT +\
 ox.HEXDIGIT + ox.HEXDIGIT + ox.HEXDIGIT + ox.HEXDIGIT

s_hex = 'This package is #a83232 hot'
pattern.is_match(s_hex)
```
```python
[] True
```
```python
pattern.findall(s_hex)
```

```python
[] ['#a83232']
```

On the other hand
```python
s_nonhex = 'Just a twitter handle: #Red123'
pattern.is_match(s_nonhex)
```

```python
[] False
```
```python
pattern.findall(s_nonhex)
```

```python
[] []
```
