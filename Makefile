PYTHON?=python

all: build

build: managed data enums

managed:
	$(PYTHON) ./scrapy_ctl.py crawl mo_spider

data:
	$(PYTHON) ./scrapy_ctl.py crawl do_spider

enums:
	$(PYTHON) ./scrapy_ctl.py crawl enum_spider

clean:
	-find . \( -name '*.o' -o -name '*.so' -o -name '*.py[cod]' -o -name '*.dll' \) -exec rm -f {} \;

help:
	@echo 'Commonly used make targets:'
	@echo '  all          - build program and documentation'
	@echo '  clean        - remove files created by other targets'
	@echo '                 (except installed files or dist source tarball)'

.PHONY: help all build clean
