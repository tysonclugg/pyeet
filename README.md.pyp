# Pyeet! Yeet All the Python!
{~~
import unicodedata
import pyeet
~~}

Pyeet is a general-purpose language to embed asynchronous Python in *ALL* your files.

Pyeet takes the source from FILE and compiles it to a Python module, then runs it.

~~~ python
Source content...                       ...compiled into Python
------------------                      -----------------------
{~~
src = """\{~# Welcome to Pyeet! #~}
😊

\{~~
text = "Hello, World!"
\~~}
\{~= text =~}

\{~~
for x in [99, 98, 97]:
    print(f"{x} bottles of beer…")

from datetime import datetime
now = datetime.now()
\~~}
The time is {~= now() =~}
""".replace('\\', '')
compiled = src.encode('utf-8').decode('pyeet')
for a, b in zip(src.split('\n'), compiled.split('\n') + (10 * [''])):
    width = 40 - sum([
        1 if unicodedata.east_asian_width(char) == 'W' else 0
        for char in a
    ])
    print(f"{a:<{width}}{b}".rstrip(' '))
~~}
~~~
Pyeet is dogfooding, this `README.md` is generated from `README.md.pyp`.

## Installation

Installation with pip:
~~~ shell
$ pip install pyeet
~~~

## Usage

~~~
usage: python -m pyeet [-h] [--dump] FILE

positional arguments:
  FILE        Source file with Pyeet tags

optional arguments:
  -h, --help  show this help message and exit
  --dump      Dump generated python module
~~~

## Examples

### Insert the current date and time into PostScript

PostScript sadly doesn't have any function that can get the current time.  We can fix that!

In the repo there is a `tests` folder that contains the following file:

#### [`current_date_and_time_in_postscript.ps`](https://github.com/tysonclugg/pyeet/blob/main/tests/current_date_and_time_in_postscript.ps)
~~~ python
{~~
print(open('tests/current_date_and_time_in_postscript.ps').read().strip())
~~}
~~~

We can use `pyeet` and `gs` (ghostscript) to render our source with the current time:
~~~ shell
$ python -m pyeet tests/current_date_and_time_in_postscript.ps \
  | gs -sDEVICE=png16m -sOutputFile=tests/current_date_and_time_in_postscript.png -
~~~

The result:

![tests/current_date_and_time_in_postscript.png](https://github.com/tysonclugg/pyeet/raw/main/tests/current_date_and_time_in_postscript.png "tests/current_date_and_time_in_postscript.png")

If you're curious, you can dump the compiled Python source using the `--dump` argument:
~~~ shell
$ python -m pyeet --dump tests/current_date_and_time_in_postscript.ps
~~~
~~~ python
{~~
print(
    open(
        'tests/current_date_and_time_in_postscript.ps'
    ).read().strip().encode('utf-8').decode('pyeet')
)
~~}
~~~
