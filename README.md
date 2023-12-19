# MkDocs Plugin for embedding Diagrams.net (Draw.io)

[![deployment badge](https://github.com/onixpro/mkdocs-drawio-file/workflows/Deploy/badge.svg)](https://github.com/onixpro/mkdocs-drawio-file/actions)
[![PyPI](https://img.shields.io/pypi/v/mkdocs-drawio-file)](https://pypi.org/project/mkdocs-drawio-file/)

[Buy me a 🍜](https://www.buymeacoffee.com/SergeyLukin)

## Features

This plugin enables you to embed interactive drawio diagrams in your documentation. Simple add your files like you would for any other image type:

```markdown
![](my-diagram.drawio)
```

Additionally this plugin supports multi page diagrams by using the `alt` text:

```markdown
![Page-2](my-diagram.drawio)
```

## Setup

Install plugin using pip:

```bash
pip install mkdocs-drawio-file
```

Add the plugin to your `mkdocs.yml`

```yaml
plugins:
  - drawio_file
```

### Configuration

To use a custom source for the drawio viewer JavaScript file you can overwritte the url.

```yaml
plugins:
  - drawio_file:
      viewer_js: "https://viewer.diagrams.net/js/viewer-static.min.js"
```

## How it works

After your mkdocs has generated the HTML for your documentation, the plugin adds the necessary diagram.net javascript library. Searches for `img` tags with a file ending of `*.drawio` and replaces them with the appropiate `mxgraph` html block. For further details, please look at the [official diagrams.net documentation](https://www.diagrams.net/doc/faq/embed-html).
