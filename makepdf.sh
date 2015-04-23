#requires pandoc
pandoc -D latex > template.tex 
pandoc --variable mainfont=Georgia --template template.tex --latex-engine xelatex -o README.pdf README.md 
