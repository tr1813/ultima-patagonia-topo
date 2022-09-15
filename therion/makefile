.PHONY: notes, survey

notes:	./data/*/*/NOTES.md
		for mdfile in ./data/*/*/NOTES.md; do \
			echo $$mdfile;\
			pandoc -f markdown --wrap=preserve --top-level-division=section $$mdfile -o "$$(dirname $$mdfile)/NOTES.html" -s -c BareCSS-v1/css/bare.min.css;\
		done

survey: ./data/*/*/*.th
		for thfile in ./data/*/*/*.th; do \
			echo $$thfile;\
			htmlfile=$$(basename $$thfile | sed 's/th/html/');\
			echo $$(dirname $$thfile)/$$htmlfile;\
			pandoc -f markdown_mmd --wrap=preserve $$thfile -o "$$(dirname $$thfile)/$$htmlfile";\
		done
