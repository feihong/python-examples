import urwid
from urwid import (Padding, AttrMap,
    Edit, Text, CheckBox, Button,
    LineBox, Pile, Columns)


frame = None
counter = 0

def main():
    header = AttrMap(Text('GitHub Project Starter'), 'header')
    lbox = listbox([
        edit('Username (required): '),
        edit('Organization: '),
        edit('Project name (required): '),
        edit('Description: '),
        linebox('Attributes for README & web page', [
            edit('Long title: '),
            edit('Long description: ', multiline=True),
        ]),
        checkbox('Create branch for GitHub Pages'),
        Columns([
            button('Submit', on_press=submit),
            button('Exit (ESC)', on_press=exit)
        ])
    ])
    global frame
    frame = urwid.Frame(urwid.AttrMap(lbox, 'body'), header=header)
    loop = urwid.MainLoop(frame, palette, unhandled_input=exit_on_esc)
    loop.run()


def listbox(widgets):
    widget_list = []
    for w in widgets:
        widget_list.append(divider)
        widget_list.append(w)
    return urwid.ListBox(urwid.SimpleListWalker(widget_list))

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
    w = Padding(w, width=len(label) + 4 )
    return w

def checkbox(label):
    w = AttrMap(CheckBox(label), 'button', 'buttonfocus')
    w = Padding(w, width=len(label) + 5)
    return w

def edit(caption, multiline=False):
    caption = ('editcaption', caption)
    return AttrMap(Edit(caption, '', multiline=multiline), 'edit', 'editfocus')

palette = [
    ('body', 'black', 'light gray', 'standout'),
    ('header', 'white','dark red', 'bold'),
    ('editfocus', 'white', 'dark blue', 'bold'),
    ('edit', 'light gray', 'dark blue'),
    ('editcaption', 'black', 'light gray', 'standout'),
    ('button', 'black', 'dark cyan'),
    ('buttonfocus', 'white', 'dark blue', 'bold'),
]

divider = urwid.Divider()


def submit(button):
    global counter
    counter += 1
    frame.footer = AttrMap(Text('You pressed Submit %s times' % counter), 'header')

def exit(button):
    raise urwid.ExitMainLoop()

def exit_on_esc(key):
    if isinstance(key, str) and key.lower() == 'esc':
        exit()

if __name__ == '__main__':
    main()
