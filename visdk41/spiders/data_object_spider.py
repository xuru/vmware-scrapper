from visdk41.items import DataObject
from .base import Base

class DOSpider(Base):
    name = 'do_spider'
    start_urls = [
                  Base.SMS + "index-do_types.html",
                  Base.VIM + "index-do_types.html"
                 ]
    object_class = DataObject
