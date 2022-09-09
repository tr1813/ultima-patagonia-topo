.PHONY: notes

notes:	./data/*/*/NOTES.md
		for mdfile in ./data/*/*/NOTES.md; do \
			echo $$mdfile;\
			pandoc -f markdown --wrap=preserve --top-level-division=section $$mdfile -o "$$(dirname $$mdfile)/NOTES.html" -s -c BareCSS-v1/css/bare.min.css;\
		done
