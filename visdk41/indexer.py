import sys

TEMPLATE = """
<html>
    <body>
        <div class="content">
            {links}
        </div>
    </body>
</html>
"""


def main(argv=sys.argv[1:]):
    from glob import glob
    from os import path
    from re import search, DOTALL, MULTILINE
    from sre_constants import error
    basedir = argv[0]
    managed_objects = dict(links=[], pattern=r"<h1>Managed Object\s+-\s+(\w+)</h1>", basename="index-mo_types.html")
    data_objects = dict(links=[], pattern=r"<h1>Data Object\s+-\s+(\w+)</h1>", basename="index-do_types.html")
    enums = dict(links=[], pattern=r"<h1>Enum\s+-\s+(\w+)</h1>", basename="index-e_types.html")
    for filepath in [filepath for filepath in glob(path.join(basedir, '*.html'))
                     if 'index' not in filepath]:
        print 'Parsing {0}'.format(filepath)
        with open(filepath) as fd:
            content = fd.read()
        for item in [managed_objects, data_objects, enums]:
            try:
                match = search(item['pattern'], content, MULTILINE)
            except error:
                match = None
            if not match:
                continue
            link = '<a href="{0}">{1}</a>'.format(path.basename(filepath), match.group(1))
            item['links'].append(link)
    for item in [managed_objects, data_objects, enums]:
        with open(path.join(basedir, item['basename']), 'w') as fd:
            links = "\n            ".join(item['links'])
            fd.write(TEMPLATE.format(links=links))


if __name__ == "__main__":
    main()

