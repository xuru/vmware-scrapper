# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import os, keyword
from jinja2 import Environment, PackageLoader
from scrapy.conf import settings
from utils import camel_to_under, quote
from visdk41.settings import config


class VisdkPipeline(object):
    mo_base = 'BaseEntity'
    do_base = 'BaseData'
    
    def _setup(self, item):
        # generate class code
        codedir = os.path.join(settings['OUTPUT_DIR'], config.get(item['type'], 'code_dir'))
        codename = codedir + '/%s.py' % camel_to_under(item['name'])
        
        docdir = os.path.join(settings['DOC_DIR'], config.get(item['type'], 'doc_dir'))
        docname = docdir + '/%s.rst' % camel_to_under(item['name'])
        
        if not os.path.exists(codedir):
            os.mkdir(codedir)
        if not os.path.exists(docdir):
            os.mkdir(docdir)
        
        return codename, docname
            
    def process_item(self, item, spider=None):
        #if item['type'] == 'mo':
        #    self.process_mo_item(item)
        # we no longer do this in the pipeline because we need to find out the parent
        # class to get a valid argument list...  it's now handled after scraping in extensions
        #elif item['type'] == 'do':
        #    self.process_do_item(item)
        return item

    def process_mo_item(self, item, items):
        props = []
        codename, docname = self._setup(item)
        
        env = Environment(loader=PackageLoader('visdk41', 'templates'))
        env.filters['uncamelcase'] = camel_to_under
        env.filters['quote'] = quote
        
        for prop in item['properties']:
            # beware of keywords...
            if prop.name in keyword.kwlist + ['property']:
                prop.name = prop.name + "_"
            props.append(prop)
            
        _type = item['type']
        _base = item['info'].get('Extends', self.mo_base)
        if _base == self.mo_base:
            _type = 'base'
            
        if item['name'] == 'PropertyFilter':
            pass

        with open(codename, 'w') as fp:
            template = env.get_template('mo.template')
            klass = template.render(
                    classname=item['name'], 
                    description=item['description'], 
                    type=_type,
                    props=props,
                    methods=item['methods'],
                    base=_base, 
                )
                
            klass = klass.encode("ascii", "ignore")
            fp.write(klass)
            
            self._generate_docs(docname, env, item)
        return item
    
       
    def process_do_item(self, item, items):
        codename, docname = self._setup(item)
        
        env = Environment(loader=PackageLoader('visdk41', 'templates'))
        env.filters['uncamelcase'] = camel_to_under
        env.filters['quote'] = quote
        
        _type = item['type']
        _base = item['info'].get('Extends', self.mo_base)
        if _base == self.mo_base:
            _type = 'base'

        if "VirtualEthernetCard" in item['name']:
            pass
            
        with open(codename, 'w') as fp:
                
            required = 0
            required_props = []
            optional_props = []
            props = self._get_props(item, items)
            for prop in props:
                if not prop.optional:
                    required += 1
                    required_props.append(prop)
                else:
                    optional_props.append(prop)
                    
            template = env.get_template('do.template')
            klass = template.render(
                    classname=item['name'],
                    description=item['description'],
                    required_props=[x.name for x in required_props],
                    optional_props=[x.name for x in optional_props],
                    required_len=required,
                    type=_type,
                    base=_base, 
                )
            klass = klass.encode("ascii", "ignore")
            fp.write(klass)
            
        self._generate_docs(docname, env, item)
        return item
    
    def process_enum_item(self, item, items):
        codename, docname = self._setup(item)
        
        env = Environment(loader=PackageLoader('visdk41', 'templates'))
        env.filters['uncamelcase'] = camel_to_under
        env.filters['quote'] = quote
        
        self._generate_docs(docname, env, item)
        return item
        
    def _get_props(self, item, items):
        props = []
        if item['info'].has_key('Extends'):
            extends = item['info']['Extends']
            
            # no multiple inheritence that I could see...
            parent = items.get(extends, None)
            if parent:
                props += self._get_props(parent, items)
                
        myprops = []
        for prop in item['properties']:
            # beware of keywords...
            if prop.name in keyword.kwlist + ['property']:
                prop.name = prop.name + "_"
            myprops.append(prop)
        return myprops + props
       
    def _generate_docs(self, docname, env, item):
        #########################################
        # generate documentation
        #########################################
        with open(docname, 'w') as fp:
            if item['type'] == 'mo':
                doc_template = env.get_template('mo_doc.template')
                t = doc_template.render(classname=item['name'], directives=self._get_directives(item), methods=item['methods'])
            elif item['type'] == 'do':
                doc_template = env.get_template('do_doc.template')
                t = doc_template.render(classname=item['name'], directives=self._get_directives(item), properties=item['properties'])
            elif item['type'] == 'enum':
                doc_template = env.get_template('enum_doc.template')
                t = doc_template.render(classname=item['name'], constants=item['constants'], description=item['description'])
            t = t.encode("ascii", "ignore")
            fp.write(t)
        return item
 
    def _get_directives(self, item):
        directives = []
        for name, value in item['info'].items():
            rvals = []
            values = [x.strip() for x in value.split(',')]
            for value in values:
                if name in ['Returned by', 'Parameter to']:
                    rvals.append(":py:meth:`~pyvisdk.do.%s.%s`" % (camel_to_under(value), value))
                    
                elif name in ['Extends']:
                    rvals.append(":py:class:`~pyvisdk.mo.%s.%s`" % (camel_to_under(value), value))
                    
                elif name in ['See also', 'Property of', 'Extended by']:
                    rvals.append(":py:class:`~pyvisdk.do.%s.%s`" % (camel_to_under(value), value))
                else:
                    rvals.append(value)
            directives.append( (name, rvals) )
        return directives
                        

