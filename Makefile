# generate lab 3 writeup

all: lab3.pdf

pngs=*.png

lab3.pdf: main.tex $(pngs)
	pdflatex $^ > $@ 

%.png: main.py
	python functions.py main.py

.PHONY : clean
clean:
	rm -f *.log
	rm -f *.png
	rm -f *.aux
