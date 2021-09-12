all :=

.DEFAULT: all
all: README.md

%: %.pyp
	python3 src/pyeet.py "$<" > "$@"
