from mako.template import Template
import plim

template_string = """
doctype html
html
    head
        title Plim Example

    body
        header
            h1 Plim Example

        p Hello ${user}! Do you like my page?

        footer
            p Copyright 1998 Capcom
"""

template = Template(template_string, preprocessor=plim.preprocessor)
print(template.render(user='Megaman'))
