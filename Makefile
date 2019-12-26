run: main.py view.py model.py controller.py decorator.py heatWindow.ui
	make test_all
	make clean
	python main.py

runx: main.py view.py model.py controller.py decorator.py heatWindow.ui
	make clean
	python main.py

testing: testing.py
	make clean
	python testing.py

clean:
	rm -f *.log

test_all: test_decorator.py decorator.py test_model.py model.py
	make clean
	python test_decorator.py
	python test_model.py
	python test_library.py

test_decorators: test_decorator.py decorator.py
	make clean
	python test_decorator.py
	
test_model: test_model.py model.py
	make clean
	python test_model.py

test_library: test_library.py library.py
	make clean
	python test_library.py

lint:
	pylint *.py