from mako.lookup import TemplateLookup
from pyjade.ext.mako import preprocessor


lookup = TemplateLookup(directories=['.'], preprocessor=preprocessor)
tmpl = lookup.get_template('pets.jade')
html = tmpl.render(
    title='My Awesome Pets!',
    pets=['gerbil', 'anaconda', 'pygmy pig', 'ninja koala'])
print(html)
