CFLAGS=-Wall

CC=cc
LD=cc
RM=rm -f
PDFLATEX=pdflatex

# Point d'entrée principal
all: rapport.pdf #tp-shell.pdf

clean:
	$(RM) *.o ch *.aux *.log *.pdf

.SUFFIXES: .tex .pdf

# Règle simpliste pour générer le PDF à partir du source LaTeX.
.tex.pdf:
	$(PDFLATEX) $<

