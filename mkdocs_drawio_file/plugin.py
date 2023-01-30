import os
import re
import string
import logging
import mkdocs
from bs4 import BeautifulSoup
from mkdocs.plugins import BasePlugin


# ------------------------
# Constants and utilities
# ------------------------
RE_PATTERN = r'!\[(.*?)\]\((.*?.drawio)\)'
SUB_TEMPLATE = string.Template(
        "<div class=\"mxgraph\" style=\"max-width:100%;border:1px solid transparent;\" data-mxgraph=\"{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;$xml_drawio&quot;}\"></div>")

# ------------------------
# Plugin
# ------------------------
class DrawioFilePlugin(BasePlugin):
    """
    Plugin for embedding DrawIO Diagrams into your Docs
    """
    config_scheme = (
        (
            "file_extension",
            mkdocs.config.config_options.Type(str, default=".drawio"),
        ),
    )

    def __init__(self):
        self.log = logging.getLogger("mkdocs.plugins.diagrams")
        self.pool = None

    def escape(self, str_xml: str):
        str_xml = str_xml.replace("&", "&amp;")
        str_xml = str_xml.replace("<", "&lt;")
        str_xml = str_xml.replace(">", "&gt;")
        str_xml = str_xml.replace("\"", "\&quot;")
        str_xml = str_xml.replace("'", "&apos;")
        return str_xml

    def substitute_image(self, path, src: str):
        file_name = os.path.join(path, src)

        with open(file_name, 'r') as q_data:
            q_lines = q_data.readlines()

        drawio_text = ''.join([item.strip() for item in q_lines])
        drawio_text_ecaped = self.escape(drawio_text)

        return SUB_TEMPLATE.substitute(xml_drawio=drawio_text_ecaped)

    def on_post_page(self, output_content, config, page, **kwargs):
        if ".drawio" not in output_content.lower():
            # Skip unecessary HTML parsing
            return output_content

        soup = BeautifulSoup(output_content, 'html.parser')

        # search for images using drawio extension
        diagrams = soup.findAll('img', src=re.compile('.*\.drawio', re.IGNORECASE))
        if len(diagrams) == 0:
            return output_content

        # add drawio library to body
        lib = soup.new_tag("script", src="https://viewer.diagrams.net/js/viewer-static.min.js")
        soup.body.append(lib)

        # substitute images with embedded drawio diagram
        path = os.path.dirname(page.file.abs_src_path)

        for diagram in diagrams:
            diagram.replace_with(BeautifulSoup(self.substitute_image(path, diagram['src']), 'html.parser'))

        return str(soup)
