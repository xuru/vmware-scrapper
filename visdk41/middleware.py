'''
Created on Jul 27, 2011

@author: eplaster
'''
import re, os, os.path
import tidylib
from tidylib import tidy_document
from visdk41.settings import DUMP_DIR


class LintMiddleware(object):
    '''
    Middleware to lint the html before processing
    '''
    link_re = re.compile(r"""<a href="(?:vim|sms).*?>(.*?)</a>""",  re.MULTILINE| re.DOTALL)
    vmodl_re = re.compile(r"""<a href="vmodl.*?>(.*?)</a>""",  re.MULTILINE| re.DOTALL)
    anchor_re = re.compile(r"""<a href="#.*?>(.*?)</a>""",  re.MULTILINE| re.DOTALL)
    strong_re = re.compile(r"""<strong>(.*?)</strong>""",  re.MULTILINE| re.DOTALL)
    script_re = re.compile(r"""<script.*?>.*?</.*?script>""",  re.MULTILINE| re.DOTALL)

    table_re = re.compile(r"""<table>(?P<outer>.*?<table.*?>.*?</table>.*?)</table>""",  re.MULTILINE| re.DOTALL)
    inner_table_re = re.compile(r"""(?P<inner><table>.*?</table>)""",  re.MULTILINE| re.DOTALL)

    empty_anchor_re = re.compile(r"""<a.*?></.*?a>""")
    ul_re = re.compile(r"""<ul>""")
    ul_end_re = re.compile(r"""<[/]ul>""")
    li_re = re.compile(r"""<li>""")
    li_end_re = re.compile(r"""<[/]li>""")
    #footnote_re = re.compile(r"""(<span title="Need not be set" class="footnote-ref">[*]<[/]span>)""",  re.IGNORECASE| re.DOTALL)
    br_re = re.compile(r"""<br>""", re.IGNORECASE)

    def process_response(self, request, response, spider):
        if 'index-mo' in response.url:
            return response
        if 'index-do' in response.url:
            return response
        if 'index-e_types' in response.url:
            return response

        body = response.body

        # VERY UGLY...  need to get this done, so it's ugly for now...
        index = body.find("<table")
        while index != -1:
            inner = body.find("<table", index+6)
            endtable = body.find("</table", index+6)
            if inner != -1 and inner < endtable:
                # we have an inner table...
                if body.find("<tr", inner, endtable) != -1:
                    break  # if it's truely a table

                else:
                    start = inner-1
                    end = body.find(">", inner)+1
                    body = body[:start] + body[end:]

                    endtable = body.find("</table", index+6)

                    start = endtable-1
                    end = body.find(">", endtable)+1
                    body = body[:start] + body[end:]

            index = body.find("<table", index+6)

        # remove any <br> before we tidy it up
        body = self.br_re.sub('', body)
        body = self.empty_anchor_re.sub('', body)

        tidylib.BASE_OPTIONS = {
            "output-xhtml": 0,     # XHTML instead of HTML4
            "indent": 1,           # Pretty; not too much of a performance hit
            "tidy-mark": 0,        # No tidy meta tag in output
            "wrap": 0,             # No wrapping
            "alt-text": "",        # Help ensure validation
            "doctype": 'omit',     # Little sense in transitional for tool-generated markup...
            "force-output": 1,     # May not get what you expect but you will get something
        }
        body, _ = tidy_document(body, options={'drop-empty-paras':1,
                    'drop-font-tags':1,'enclose-text':1,'merge-divs':1,'fix-bad-comments':1})

        body = self.link_re.sub('\g<1>', body)
        body = self.vmodl_re.sub('\g<1>', body)
        body = self.strong_re.sub('\g<1>', body)
        body = self.script_re.sub('', body)
        body = self.ul_re.sub('', body)
        body = self.li_end_re.sub('', body)
        body = self.li_re.sub('* ', body)
        body = self.ul_end_re.sub('', body)

        response = response.replace(body=body)
        return response

