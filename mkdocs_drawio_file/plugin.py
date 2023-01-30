import os
import re
import string
import logging
import mkdocs
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

    def substitute_file(self, file_name: str):
        with open(file_name, 'r') as q_data:
            q_lines = q_data.readlines()

        drawio_text = ''.join([item.strip() for item in q_lines])
        drawio_text_ecaped = self.escape(drawio_text)

        return SUB_TEMPLATE.substitute(xml_drawio=drawio_text_ecaped)

    def substitute_files(self, match, path):
        file_tag = match.group()
        file_name = file_tag[file_tag.find("(")+1:file_tag.find(")")]

        return self.substitute_file(os.path.join(path, file_name))

    def on_page_markdown(self, markdown, page, files, config) -> str:
        def substitution(match):
            return self.substitute_files(match, os.path.dirname(page.file.abs_src_path))

        pattern = re.compile(RE_PATTERN, flags=re.IGNORECASE)

        return pattern.sub(substitution, markdown) + "<script type=\"text/javascript\" src=\"https://viewer.diagrams.net/js/viewer-static.min.js\"></script>"
