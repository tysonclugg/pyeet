# Pyeet! Yeet All the Python!

Pyeet is a general-purpose language to embed asynchronous Python in *ALL* your files.

Pyeet takes the source from FILE and compiles it to a Python module, then runs it.

~~~ python
Source content...                       ...compiled into Python
------------------                      -----------------------
{~# Welcome to Pyeet! #~}               # Welcome to Pyeet!
😊                                      print('😊')
                                        print()
{~~
text = "Hello, World!"                  text = "Hello, World!"
~~}
{~= text =~}                            print(text)
                                        print()
{~~
for x in [99, 98, 97]:                  for x in [99, 98, 97]:
    print(f"{x} bottles of beer…")          print(f"{x} bottles of beer…")

from datetime import datetime           from datetime import datetime
now = datetime.now()                    now = datetime.now()
~~}
The time is {~= now() =~}               print('The time is ', now(), sep='')

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
%!PS
% 595 842 scale
/Times-Roman findfont
20 scalefont
setfont
newpath
70 750 moveto
{~~
from datetime import datetime
~~}
/({~= datetime.now() =~}) show
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
print('%!PS')
print('% 595 842 scale')
print('/Times-Roman findfont')
print('20 scalefont')
print('setfont')
print('newpath')
print('70 750 moveto')

from datetime import datetime

print('/(', datetime.now(), ') show', sep='')
~~~
