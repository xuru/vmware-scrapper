from visdk41.items import ManagedObject
from .base import Base

class MOSpider(Base):
    name = 'mo_spider'
    start_urls = [
                  Base.SMS + "index-mo_types.html",
                  Base.VIM + "index-mo_types.html"
                 ]
    object_class = ManagedObject
