from visdk41.items import DataObject
from .base import Base

class FaultSpider(Base):
    name = 'fault_spider'
    start_urls = [
                  Base.SMS + "index-faults.html",
                  Base.VIM + "index-faults.html"
                 ]
    object_class = DataObject
