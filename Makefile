# generate lab 3 writeup

all: lab3.pdf

pngs=*.png

lab3.pdf: main.tex $(pngs)
	pdflatex main.tex 

%.png: main.py
	python main.py functions.py

.PHONY : clean
clean:
	rm -f *.log
	rm -f *.png
	rm -f *.aux
