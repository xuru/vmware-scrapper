'''
Created on Jul 29, 2011

@author: eplaster
'''
import os.path
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy import log
from scrapy.conf import settings
from utils import camel_to_under
from visdk41.settings import config
from visdk41.pipelines import VisdkPipeline

head = """
from pyvisdk.thirdparty import Enum

ManagedObjectTypes = Enum(
"""
head_do = """
from pyvisdk.thirdparty import Enum

DataObjectTypes = Enum()
DataObjectTypes.update( [
"""
enum_header = """
########################################
# Automatically generated, do not edit.
########################################


from pyvisdk.thirdparty import Enum

%s = Enum(
%s
)
"""

class GenConsts(object):
    def __init__(self):
        dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)
        dispatcher.connect(self.item_scraped, signal=signals.item_scraped)
        
        self.pipeline = VisdkPipeline()

    def spider_opened(self, spider):
        self.output_dir = settings['OUTPUT_DIR']
        self.mo_items = {}
        self.do_items = {}
        self.enum_items = {}
        log.msg("opened spider: %s" % spider.name, level=log.WARNING)

    def spider_closed(self, spider):
        if self.mo_items:
            self._write_mo_types()
            
        if self.do_items:
            self._write_do_types()
    
        if self.enum_items:
            self._write_enum_items()
            
        log.msg("closed spider: %s" % spider.name, level=log.WARNING)
    
    def _write_mo_types(self):
        typesdir = os.path.join(self.output_dir, config.get('mo', 'types_dir'))
        codedir  = os.path.join(self.output_dir, config.get('mo', 'code_dir'))
        
        names = self.mo_items.keys()
        names.sort()
        with open( os.path.join(typesdir, 'managed_object_types.py'), 'w') as fp:
            fp.write(head)
            for name in names[:-1]:
                fp.write('    "{0}",\n'.format(name))
            fp.write('    "{0}"\n'.format(names[-1]))
            fp.write(')\n\n')
        
        for item in self.mo_items.values():
            log.msg("Processing %s..." % item['name'], level=log.WARNING)
            self.pipeline.process_mo_item(item, self.mo_items)
            
        with open(os.path.join(codedir, '__init__.py'), 'w') as fp:
            fp.write("\n\n")
            for name in names:
                fp.write('from {0} import {1}\n'.format( 'pyvisdk.mo.' + camel_to_under(name), name))
            fp.write("\n\n")
            
            
    def _write_do_types(self):
        typesdir = os.path.join(self.output_dir, config.get('do', 'types_dir'))
        codedir  = os.path.join(self.output_dir, config.get('do', 'code_dir'))
        
        names = self.do_items.keys()
        names.sort()
        with open( os.path.join(typesdir, 'data_object_types.py'), 'w') as fp:
            fp.write(head_do)
            
            for name in names[:-1]:
                fp.write('    "{0}",\n'.format(name))
            fp.write('    "{0}"\n'.format(names[-1]))
            fp.write('])\n\n')
        
        for item in self.do_items.values():
            log.msg("Processing %s..." % item['name'], level=log.WARNING)
            self.pipeline.process_do_item(item, self.do_items)
            
        with open(os.path.join(codedir, '__init__.py'), 'w') as fp:
            fp.write("\n\n")
            for name in names:
                fp.write('from {0} import {1}\n'.format( 'pyvisdk.do.' + camel_to_under(name), name))
            fp.write("\n\n")
            
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
                        

    def _write_enum_items(self):
        enums_dir = os.path.join(self.output_dir, config.get('general', 'enums_dir'))
        
        for item in self.enum_items.values():
            print "Processing: %s" % item['name']+".py"
            with open(os.path.join(enums_dir, camel_to_under(item['name'])+".py"), 'w') as fp:
                content = ""
                for const in item['constants']:
                    content += "    '%s',\n" % const.name
                fp.write(enum_header % (item['name'], content.encode('ascii', 'replace')))
                        
            self.pipeline.process_enum_item(item, self.enum_items)


    def item_scraped(self, item):
        if item['type'] == 'mo':
            self.mo_items[item['name']] = item
        elif item['type'] == 'do':
            self.do_items[item['name']] = item
        elif item['type'] == 'enum':
            self.enum_items[item['name']] = item
            
        log.msg("item scraped: %s" % item['name'], level=log.WARNING)
        
        
        