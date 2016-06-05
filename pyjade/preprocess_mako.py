from mako.template import Template
from pyjade.ext.mako import preprocessor

jade_source = """
p #{greeting}, #{guest_name}!

- todo = ['laundry', 'call Amy back', 'write memoirs']

ul
    each item in todo
        li= item

"""

tmpl = Template(jade_source, preprocessor=preprocessor)
html = tmpl.render(
    greeting='Good morning',
    guest_name='Mr Bojangles',
)
print(html)
