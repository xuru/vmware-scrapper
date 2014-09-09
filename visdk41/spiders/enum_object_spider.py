from visdk41.items import EnumObject
from .base import Base

class EnumSpider(Base):
    name = 'enum_spider'
    start_urls = [
                  Base.SMS + "index-e_types.html",
                  Base.VIM + "index-e_types.html"
                 ]
    object_class = EnumObject
