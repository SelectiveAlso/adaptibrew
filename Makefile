install:
	pyinstaller -F db_interface.py
	mv dist/db_interface ~/bin/brewerd
	rm -rf dist/
	rm -rf build/

run:
	python db_interface.py
