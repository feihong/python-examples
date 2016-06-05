"""
What happens if you try to make your Jade template inherit from a Mako template?
Unfortunately, bad things. It doesn't work at all unless you use the Template
constructor. Trying to include head.jade causes the actual code to be imported,
not the rendered results. It doesn't seem that you can mix template languages
very well.

"""
from mako.lookup import TemplateLookup, Template
from pyjade.ext.mako import preprocessor


lookup = TemplateLookup(directories=['.'])
# tmpl = lookup.get_template('pets.jade')
tmpl = Template(filename='pets.jade', lookup=lookup, preprocessor=preprocessor)
html = tmpl.render(
    title='My Awesome Pets!',
    pets=['gerbil', 'anaconda', 'pygmy pig', 'ninja koala'])
print(html)
