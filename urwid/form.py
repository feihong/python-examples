import string
import urwid
from urwid import (Padding, AttrMap,
    Edit, Text, CheckBox, Button,
    ListBox, LineBox, Pile, Columns)


PALETTE = [
    ('body', 'black', 'light gray', 'standout'),
    ('header', 'white','dark red', 'bold'),
    ('editfocus', 'white', 'light blue', 'bold'),
    ('edit', 'light gray', 'dark blue'),
    ('editcaption', 'black', 'light gray', 'standout'),
    ('button', 'black', 'dark cyan'),
    ('buttonfocus', 'white', 'light blue', 'bold'),
]


class App:
    def __init__(self, header_text):
        self.header = AttrMap(Text(header_text), 'header')
        self.frame = None
        self.placeholder = urwid.WidgetPlaceholder(None)
        self.default_form = None
        self.forms = {}

    def add_form(self, key, form):
        if not self.default_form:
            self.default_form = form
        self.forms[key] = form
        form.app = self

    def switch(self, key, values=None):
        form = self.forms[key]
        form.on_switch(values)
        self.placeholder.original_widget = form

    def run(self):
        self.placeholder.original_widget = self.default_form
        body = urwid.AttrMap(self.placeholder, 'body')
        self.frame = frame = urwid.Frame(body, header=self.header)
        loop = urwid.MainLoop(self.frame, PALETTE)
        loop.run()


class Form(ListBox):
    current_instance = None

    def __init__(self):
        self.values = {}
        Form.current_instance = self
        super(Form, self).__init__(self.get_contents())
        Form.current_instance = None

    def get_contents(self):
        return listwalker(self.get_field_widgets() + [self.get_buttonrow()])

    def get_field_widgets():
        return []

    def get_buttonrow(self):
        return buttonrow(
            button('Cancel', on_press=lambda x: self.on_cancel()),
            button('OK', on_press=lambda x: self.on_ok()),
        )

    def connect_widget(self, key, value, widget):
        self.values[key] = value
        def callback(widget, new_value):
            self.values[key] = new_value
        urwid.connect_signal(widget, 'change', callback)

    def on_switch(self, values=None): pass
    def on_ok(self): pass
    def on_cancel(self): pass


class MainForm(Form):
    def get_field_widgets(self):
        return [
            edit('username', 'Username (required)'),
            edit('organization', 'Organization'),
            edit('project', 'Project name (required)'),
            edit('desc', 'Description'),
            linebox('Attributes for README & web page', [
                edit('long_title', 'Long title'),
                edit('long_desc', 'Long description', multiline=True),
            ]),
            checkbox('gh_branch', 'Create branch for GitHub Pages'),
        ]

    def on_ok(self):
        self.app.switch('confirm', self.values)


class ConfirmationForm(Form):
    def get_field_widgets(self):
        self.text = Text('')
        return [
            self.text
        ]

    def on_switch(self, values):
        lines = [
            'Are you sure you want to:\n',
            '- Create a project at http://github.com/${username}/${project}/',
            '- Turn the current directory into a git repository'
        ]
        if values['gh_branch']:
            lines.append('- Create a gh-pages branch')
        template = string.Template('\n'.join(lines))
        self.text.set_text(template.substitute(**values))

    def on_cancel(self):
        self.app.switch('main')


divider = urwid.Divider()

def listwalker(widgets):
    widget_list = []
    for w in widgets:
        widget_list.append(divider)
        widget_list.append(w)
    return urwid.SimpleListWalker(widget_list)

def linebox(title, widgets):
    widget_list = []
    for w in widgets:
        widget_list.append(w)
        widget_list.append(divider)
    del widget_list[-1]     # no need for last divider
    pile = Padding(urwid.Pile(widget_list), left=1, right=1)
    return urwid.LineBox(pile, title)

def button(label, on_press=None):
    w = Button(label, on_press=on_press)
    w = AttrMap(w, 'button', 'buttonfocus')
    w = Padding(w, width=len(label) + 4)
    return w

def buttonrow(*buttons):
    return Columns(
        [(b.width, b) for b in buttons],
        dividechars=4,
        focus_column=0)

def checkbox(key, label):
    w = CheckBox(label)
    Form.current_instance.connect_widget(key, False, w)
    w = AttrMap(w, 'button', 'buttonfocus')
    w = Padding(w, width=len(label) + 5)
    return w

def edit(key, label, multiline=False):
    caption = ('editcaption', label + ': ')
    w = Edit(caption, '', multiline=multiline)
    Form.current_instance.connect_widget(key, '', w)
    w = AttrMap(w, 'edit', 'editfocus')
    return w


if __name__ == '__main__':
    app = App('GitHub Project Starter')
    app.add_form('main', MainForm())
    app.add_form('confirm', ConfirmationForm())
    app.run()
