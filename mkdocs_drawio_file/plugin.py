
import os
import logging
import mkdocs
import mkdocs.plugins
from mkdocs.structure.files import File
from mkdocs.structure.files import get_files
import re
import string


# This global is a hack to keep track of the last time the plugin rendered diagrams.
# A global is required because plugins are reinitialized each time a change is detected.
last_run_timestamp = 0

    

    
class drawio_file_plugin(mkdocs.plugins.BasePlugin):
    config_scheme = (
        (
            "file_extension",
            mkdocs.config.config_options.Type(str, default=".drawio"),
        ),
    )

    TEMPLATE = string.Template("<div class=\"mxgraph\" style=\"max-width:100%;border:1px solid transparent;\" data-mxgraph=\"{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;$xml_drawio&quot;}\"></div>")

    def __init__(self):
        self.log = logging.getLogger("mkdocs.plugins.diagrams")
        self.pool = None



    def escape( str_xml: str ):
        str_xml = str_xml.replace("&", "&amp;")
        str_xml = str_xml.replace("<", "&lt;")
        str_xml = str_xml.replace(">", "&gt;")
        str_xml = str_xml.replace("\"", "\&quot;")
        str_xml = str_xml.replace("'", "&apos;")
        return str_xml

    def conver_file( file_name: str):
        with open(file_name, 'r') as q_data:
            q_lines = q_data.readlines()

        drawio_text = ''.join([ item.strip() for item in q_lines])

        drawio_text_ecaped = drawio_file_plugin.escape(drawio_text)

        drawio_html = drawio_file_plugin.TEMPLATE.substitute(xml_drawio = drawio_text_ecaped )
        return drawio_html

    def convert_match(match,config,path):
        file_tag = match.group()
        file_name = file_tag[file_tag.find("(")+1:file_tag.find(")")]
        converted = drawio_file_plugin.conver_file(os.path.join(path,file_name ))
        return converted 

    def on_page_markdown(self, markdown, page,files,config) -> str:
        def file_sub(match):
            return drawio_file_plugin.convert_match(match,config,os.path.dirname(page.file.abs_src_path))

        pattern = re.compile(r'!\[(.*?)\]\((.*?.drawio)\)', flags=re.IGNORECASE)
        
        markdown = pattern.sub( file_sub, markdown)    
        markdown = markdown + "<script type=\"text/javascript\" src=\"https://viewer.diagrams.net/js/viewer-static.min.js\"></script>"
        return markdown
