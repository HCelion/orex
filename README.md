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
True
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
True
```
```python
pattern.findall(s_hex)
```

```python
['#a83232']
```

On the other hand
```python
s_nonhex = 'Just a twitter handle: #Red123'
pattern.is_match(s_nonhex)
```

```python
False
```
```python
pattern.findall(s_nonhex)
```

```python
[]
```

Clearly, the pattern is somewhat burdensome. We can alternatively write it like this
```python
pattern = ox.literal('#') + ox.repeat(ox.HEXDIGIT, 6)
```
or
```python
pattern = ox.literal('#') + ox.n_or_more(ox.HEXDIGIT, min=6, max=6)
```

## Subpatterns

Most of `orex` functions accept other regular expressions as characters.

Say we want to find a regex to parse emails. We can define first all email allowed characters
```python
allowed_characters = ox.character_class(ox.ALNUM + ox.DASH + '_' + ox.DOT)
```
where `ox.ALNUM` are just all letters and numbers. Note that the `_` is just used as a string.
In Orex it is okay to use strings as part of the pattern, unless they are at the start, where we use `ox.literal` to show python that we mean pattern business. Whenever we want to use the `.` or `_` explicitly, it is best to use `ox.DOT` or `ox.DASH`, since `.` and `-` can have a special meaning in regular expression.

Next we define

```python
user_name = ox.one_or_more(allowed_characters)
domain_name = ox.one_or_more(allowed_characters)
extension = ox.n_or_more(ox.ALPHA,2,4)

email_pattern =  user_name + '@' + domain_name + ox.DOT + extension
```
```python
email = 'captainspamalot@funnyspammail.com'
```
And indeed

```python
email_pattern.is_match(email)
```
```
True
```

## Capturing

If we want to extract the individual components of a match, we have to capture them first.
Using the email example above, we can just change the code to

```
email_pattern =  ox.capture(user_name) + '@' + ox.capture(domain_name) \
                + ox.DOT + ox.capture(extension)
```

```
email_pattern.findall(email)
```
returns
```
[('captainspamalot', 'funnyspammail', 'com')]
```
Handy indeed! We can also name the individual components for even easier extraction

```python
email_pattern =  ox.capture(user_name,'user') \
              + '@' + ox.capture(domain_name,'domain') \
              + ox.DOT + ox.capture(extension,'ext')
```

We can now use the `group_dict` method for even easier access
```python
email_pattern.group_dict(email)
```
```
{'user': 'captainspamalot', 'domain': 'funnyspammail', 'ext': 'com'}
```

Capturing has another benefit, namely that we can use it to find repeated patterns
```python
tag_name = ox.one_or_more(allowed_characters)
content = ox.one_or_more(ox.ANY_CHAR)
tag_pattern = ox.literal('<') + ox.capture(tag_name, 'tag') + '>' \
          + ox.capture(content,'content') + '</' +ox.backreference(name='tag')+'>'

message = '<name>Sir Snakington</name>'
tag_pattern.group_dict(message)
```

```
{'tag': 'name', 'content': 'Sir Snakington'}
```
