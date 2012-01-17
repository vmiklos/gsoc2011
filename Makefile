all: HEADER.html

HEADER.html: gsoc-2k11.txt Makefile
	asciidoc -o HEADER.html -a toc -a numbered -a sectids gsoc-2k11.txt
