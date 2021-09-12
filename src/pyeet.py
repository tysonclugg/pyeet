"""Pyeet! Yeet All the Python!

Pyeet is a general-purpose language to embed asynchronous Python in ALL your files.

Pyeet takes the source from FILE and compiles it to a Python module, then runs it:

Source content...                       ...compiled into Python
------------------                      -----------------------
{~# Welcome to Pyeet! #>                # Welcome to Pyeet!
😊                                      print("😊")

{~~
text = "Hello, World!"                  text = "Hello, World!"
~~}
{~= text =~}                            print(text)

{~~
for x in [99, 98, 97]:                  for x in [99, 98, 97]:
    print f"{x} bottles of beer…"           print f"{x} bottles of beer…"

from datetime import datetime           from datetime import datetime
now = datetime.now()                    now = datetime.now()
~~}
The time is {~= now() =~}               print("The time is ", now, sep='')
"""
import asyncio
import codecs
import encodings.utf_8
import enum
import importlib.abc, importlib.util
import io
import pathlib
import re
import sys
import typing


class State(enum.Enum):
    EMIT = 0
    CODE = 1
    COMMENT = 2
    ECHO = 3


def decode(input: bytes, errors: str = "strict") -> typing.Tuple[str, int]:
    source, encoding_state = encodings.utf_8.decode(input, errors)
    output_lines = []
    state = State.EMIT
    while source:
        if "\n" in source:
            line, source = source.split("\n", 1)
        else:
            line, source = source, None
        if state == state.CODE:
            if line == "~~}":
                output_lines.append("")
                state = State.EMIT
            else:
                output_lines.append(line)
        elif state == state.EMIT:
            if line == "{~~":
                state = state.CODE
                output_lines.append("")
                continue
            comment_match = re.match(r"^{~# *(.*) *#~}$", line)
            if comment_match:
                output_lines.append(f"# {comment_match.group(1)}")
                continue

            print_args = []
            parts = re.split(r"{~= *(.*?) *=~}", line)
            while parts:
                text = parts.pop(0)
                if text:
                    print_args.append(repr(text))
                if not parts:
                    break
                expr = parts.pop(0)
                if expr:
                    print_args.append(expr)
            if len(print_args) > 1:
                print_args.append("sep=''")
            emit = f"print({', '.join(print_args)})"
            output_lines.append(emit)
    return "\n".join(output_lines), encoding_state


CODEC = codecs.CodecInfo(
    encode=encodings.utf_8.encode,
    decode=decode,
)


def search_function(encoding):
    if encoding == "pyeet":
        return CODEC


codecs.register(search_function)


class PyeetLoader(importlib.abc.SourceLoader):
    def __init__(self, path: pathlib.Path):
        self.path = path

    def get_data(self, path):
        return self.path.read_bytes().decode("pyeet").encode("utf-8")

    def get_filename(self, path):
        return str(self.path)


async def connect_stdio(
    stdin: io.IOBase, stdout: io.IOBase, stderr: io.IOBase
) -> typing.Tuple[asyncio.StreamReader, asyncio.StreamWriter, asyncio.StreamWriter]:
    loop = asyncio.get_event_loop()
    # stdin
    stdin_reader = asyncio.StreamReader()
    stdin_protocol = asyncio.StreamReaderProtocol(stdin_reader)
    await loop.connect_read_pipe(lambda: stdin_protocol, stdin)
    # stdout
    stdout_transport, stdout_protocol = await loop.connect_write_pipe(
        asyncio.streams.FlowControlMixin, stdout
    )
    stdout_writer = asyncio.StreamWriter(
        stdout_transport, stdout_protocol, stdin_reader, loop
    )
    # stderr
    stderr_transport, stderr_protocol = await loop.connect_write_pipe(
        asyncio.streams.FlowControlMixin, stderr
    )
    stderr_writer = asyncio.StreamWriter(
        stderr_transport, stderr_protocol, stdin_reader, loop
    )
    return stdin_reader, stdout_writer, stderr_writer


async def main():
    import argparse
    import fileinput

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dump", action="store_true", help="Dump generated python module"
    )
    parser.epilog = __doc__
    parser.formatter_class = argparse.RawTextHelpFormatter

    parser.add_argument("file", metavar="FILE", help="Source file with Pyeet tags")

    opts = parser.parse_args()
    if opts.dump:
        print(open(opts.file, "rb").read().decode("pyeet"))
    else:
        pyeet(opts.file)


def pyeet(path):
    loader = PyeetLoader(pathlib.Path(path))
    spec = importlib.util.spec_from_loader(path, loader, origin="built-in")
    module = importlib.util.module_from_spec(spec)
    sys.modules[path] = module
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    asyncio.run(main())
