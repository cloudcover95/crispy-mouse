build:
	pio run -e micro

flash:
	pio run -e micro --target upload

hub:
	python3 crispy_hub.py
