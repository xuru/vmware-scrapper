# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

import re
from scrapy.item import Item, Field
from scrapy.selector import HtmlXPathSelector
from scrapy.selector.list import XPathSelectorList

class ManagedItem(Item):
    name = Field()
    type = Field()
    info = Field()
    description = Field()
    methods = Field()
    properties = Field()

class DataItem(Item):
    name = Field()
    type = Field()
    info = Field()
    description = Field()
    properties = Field()
    namespace = Field()

class EnumItem(Item):
    # define the fields for your item here like:
    name = Field()
    type = Field()
    description = Field()
    constants = Field()


def _clean(selector):
    if isinstance(selector, list):
        rv = []
        for row in selector:
            row = _clean(row)
            if row:
                rv.append(row)
        if len(rv) == 1:
            return rv[0]
        if len(rv) == 0:
            return ''
        return rv
    elif isinstance(selector, unicode) or isinstance(selector, str):
        return selector.strip().replace('<p>', '').replace('</p>', '').replace('<h1>', '').replace('</h1>', '').strip()
    else:
        return _clean(selector.extract())

class IteratorObject(object):
    def __init__(self):
        self.data = []

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        for value in self.data:
            yield value

    def __str__(self):
        return str(self.data)


class Fault(object):
    """ A fault that can be raised from a method """
    def __init__(self, type, description=""):
        self.type = type
        self.description = description

    def __str__(self):
        return self.type

class Faults(IteratorObject):
    """ Faults that can be raised from a method """
    def __init__(self):
        super(Faults, self).__init__()

    def parse(self, table):
        for row in table.select('.//tr')[1:]:
            cols = row.select('./td')
            if len(cols) > 1:
                _type = _clean(cols[0].select('./text()'))
                desc = _clean(cols[1].select('./text()'))
                if isinstance(desc, list):
                    desc = ' '.join(desc)

                self.data.append( Fault(_type, desc) )
        return self.data

class ReturnValue(object):
    """return value from a method """
    def __init__(self):
        self.type = None
        self.description = ""

    def parse(self, table):
        rv = []
        for row in table.select('.//tr')[1:]:
            cols = row.select('./td')

            if len(cols) > 1:
                self.type = _clean(cols[0].select('./text()'))
                if self.type and isinstance(self.type, list):
                    self.type = ' '.join(self.type)
                else:
                    self.type = ""
                self.description = _clean(cols[1].select('./text()'))
                if self.description and isinstance(self.description, list):
                    self.description = ' '.join(self.description)
                else:
                    self.description = ""
        return self

    def __str__(self):
        return str(self.type if not None else self.description)

class Argument(object):
    """ An argument to a method """
    def __init__(self, name, type, description="", optional=False):
        self.name = name
        self.type = type
        self.description = description
        self.optional = optional

    def __str__(self):
        return self.name

class Arguments(IteratorObject):
    """ the arguments of a method """
    def __init__(self):
        super(Arguments, self).__init__()

    def parse(self, table):
        for row in table.select('.//tr')[1:]:
            optional=False
            if row.re(r"""(title="Need not be set")"""):
                optional = True
            cols = []
            for col in row.select('./td/text()'):
                col = _clean(col)
                if col:
                    cols.append(col)
            if len(cols) < 3:
                cols.append(' ')

            desc = ""
            if len(cols) > 3:
                for x in _clean(cols[2:]):
                    desc += x
            else:
                desc = _clean(cols[2])

            name        = _clean(cols[0])
            if name == u'_this':
                continue

            self.data.append( Argument(name, _clean(cols[1]), desc, optional) )
        return self.data

class Method(object):
    """ The method of a class """
    def __init__(self, name, description="", arguments=[], return_value=None, faults=[]):
        self.name = name
        self.description = description
        self.arguments = arguments
        self.return_value = return_value
        self.faults = faults

    def __str__(self):
        return self.name

class Methods(IteratorObject):
    """ the methods of a class """
    def __init__(self):
        super(Methods, self).__init__()

    def parse(self, hxs):
        method_selectors = hxs.select("//h1")

        if isinstance(method_selectors, XPathSelectorList):
            # gather up all method descriptions
            for s in method_selectors:
                name = _clean(s)
                if ' ' in name:
                    continue
                desc = ""
                index = 0
                nodes = s.select('following::*')
                for node in nodes:
                    try:
                        ntype = _clean(node.select('name()')[0])
                    except:
                        break
                    if not ntype in ['text', 'p']:
                        break
                    else:
                        if ntype == 'p':
                            x = _clean(nodes[index])
                            if isinstance(x, list):
                                x = ' '.join(x)
                            desc += x
                        else:
                            x = _clean(nodes[index].select('./text()'))
                            if isinstance(x, list):
                                x = ' '.join(x)
                            desc += x

                # the next three tables are for args, return and faults
                args_table, return_table, faults_table = self._findParameters(s)

                args    = Arguments().parse(args_table)
                rv      = ReturnValue().parse(return_table)
                faults  = Faults().parse(faults_table)

                self.data.append( Method(name, desc, args, rv, faults) )
        return self.data

    def _findParameters(self, selector):
        args_table = rv_table = faults_table = None
        paras = selector.select('following::p')
        for para in paras:
            if para.re('Parameters'):
                args_table = para.select('following::table[1]')[0]
            if 'Return Value' in _clean(para.select('./text()')):
                rv_table = para.select('following::table[1]')[0]
            if 'Faults' in _clean(para.select('./text()')):
                faults_table = para.select('following::table[1]')[0]
            if args_table and rv_table and faults_table:
                break
        return args_table, rv_table, faults_table

class Property(object):
    """ The property of a class, i.e. obj.name """
    def __init__(self, name, type="", optional=False, description=""):
        self.name = name
        self.type = type
        self.optional = optional
        self.description = description

class Properties(IteratorObject):
    """ The properties of a class """
    def __init__(self):
        super(Properties, self).__init__()

    def parse(self, hxs):
        rows = self._findProperties(hxs).select(".//tr")[1:]
        for row in rows:
            self._parse_row(row)
        return self.data

    def _parse_row(self, row):
        if len(row.select('./td')) > 2:
            optional = False
            if row.re(r"""(title="Need not be set")"""):
                optional = True
            name = _clean(row.select("./td[1]/text()"))
            if isinstance(name, list):
                name = " ".join(name)
            _type = _clean(row.select("./td[2]/text()"))
            if isinstance(_type, list):
                _type = " ".join(name)
            desc = _clean(row.select("./td[3]/text()"))
            if isinstance(desc, list):
                try:
                    desc = desc[0]
                except:
                    desc = ""
            self.data.append( Property(name, _type, optional, desc) )

    def _findProperties(self, selector):
        props_table = None
        paras = selector.select('//p')
        for para in paras:
            if 'Properties' in para.extract():
                props_table = para.select('following::table[1]')[0]
                break
        return props_table

class Klass(object):
    def __init__(self):
        self.referer = None
        self.name = ""
        self.description = ""
        self.hxs = None
        self.referer = None

    def parse(self, response):
        self.hxs = HtmlXPathSelector(response)
        self.referer = response.request.headers['Referer']

        text = _clean(self.hxs.select('/html/body/h1[1]/text()')).strip()
        name_obj = re.search(r""".*\b.*?(?P<name>\w+)$""", text)
        self.name = name_obj.group('name')

        self.description = self._findDescription(self.hxs)

    def _gatherInfo(self):
        info = {}
        dts = self.hxs.select("/html/body/dl[1]/dt")
        dds = self.hxs.select("/html/body/dl[1]/dd")
        for dt, dd in zip(dts, dds):
            name = _clean(dt.select('./text()'))
            value = _clean(dd.select('./text()'))
            info[name] = value
        return info

    def _findDescription(self, selector):
        h2s = selector.select('//h2')
        for h2 in h2s:
            if " Description" in h2.extract():
                break

        # now we have our h2...
        paras = h2.select('following::p')
        desc = ''
        for para in paras:
            text = _clean(para.select('./text()'))
            if isinstance(text, list):
                text = " ".join([x.strip() for x in text])

            if 'Properties' == text:
                break
            elif 'Enum Constants' == text:
                break

            desc += text
        return desc

class ManagedObject(Klass):
    def __init__(self):
        super(ManagedObject, self).__init__()
        self.type = 'mo'
        self.item = None

    def parse(self, response):
        Klass.parse(self, response)

        if self.name == 'PropertyFilter':
            pass

        self.item = ManagedItem()
        self.item['name'] = self.name
        self.item['type'] = self.type
        self.item['info'] = self._gatherInfo()
        self.item['description'] = self.description
        self.item['methods'] = Methods().parse(self.hxs)
        self.item['properties'] = Properties().parse(self.hxs)
        return self.item

class DataObject(Klass):
    def __init__(self):
        super(DataObject, self).__init__()
        self.type = 'do'
        self.item = None

    def parse(self, response):
        Klass.parse(self, response)
        self.item = DataItem()
        self.item['namespace'] = 'urn:sms' if response.url.split('/')[-1].startswith('sms') else 'urn:vim25'
        self.item['name'] = self.name
        self.item['type'] = self.type
        self.item['info'] = self._gatherInfo()
        self.item['description'] = self.description
        self.item['properties'] = Properties().parse(self.hxs)
        return self.item

class EnumObject(Klass):
    def __init__(self):
        super(EnumObject, self).__init__()
        self.type = 'enum'
        self.item = None

    def parse(self, response):
        Klass.parse(self, response)

        self.item = EnumItem()
        self.item['name'] = self.name
        self.item['type'] = self.type
        self.item['description'] = self.description
        self.item['constants'] = Enums().parse(self.hxs)
        return self.item

class Enum(object):
    """ The enumeration """
    def __init__(self, name, description=""):
        self.name = name
        self.description = description

class Enums(IteratorObject):
    """ The enumerations """
    def __init__(self):
        super(Enums, self).__init__()

    def parse(self, selector):
        table = self._findEnumContants(selector)
        rows = table.select(".//tr")[1:]
        for row in rows:
            name = _clean(row.select("./td[1]/text()"))
            if isinstance(name, list):
                name = " ".join(name)

            desc = _clean(row.select("./td[2]/text()"))
            if isinstance(desc, list):
                desc = " ".join(desc)

            self.data.append( Enum(name, desc) )
        return self.data

    def _findEnumContants(self, selector):
        enum_table = None
        paras = selector.select('//p')
        for para in paras:
            if para.re('Enum Constants'):
                enum_table = para.select('following::table[1]')[0]
                break
        return enum_table

