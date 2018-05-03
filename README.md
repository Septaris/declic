# Declic

Declic (DEcorator-oriented CLI Creator) is a tiny Python 3 package for creating command line interfaces using
decorators. It was inspired by the [click](http://click.pocoo.org/6/) package and is based on
[argparse](https://docs.python.org/3/library/argparse.html)

## Installation

```
pip install git+https://github.com/Septaris/declic.git
```

## Usage

Here is an example of Declic usage:

```python
from declic import group, argument, command
@group(description='my description')
@argument('--version', action='version', version='<the version>')
@argument('--foo', type=int, default=1)
def bar():
    print('bar')

@bar.group(invokable=True)
@argument('--toto', type=int, default=2)
@argument('--tata', type=str, default='aaa')
def sub_group(toto, tata):
    print(toto)
    print(tata)

@sub_group.command(chain=True)
def mop(toto, **kwargs):
    print(kwargs)
    print(toto)

@bar.command()
@argument('-x', type=int, default=1)
@argument('y', type=float)
def foo(x, y):
    print(x, y)


if __name__ == '__main__':
    import sys

    bar(sys.argv[1:])
    # or bar()
```

Running the cli:

```
python my_file.py --help
```

