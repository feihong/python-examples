from clint.textui import puts, colored
from clint.textui import columns


def get_rows():
    yield ('jan', 1400, 350)
    yield ('feb', 1500, 380)
    yield ('mar', 1390, 340)
    yield ('apr', 1375, 333)
    yield ('may', 1405, 357)


column_widths = [5, 20, 15]


def zipl(*args):
    for tup in zip(*args):
        yield list(tup)


def print_headers(*args):
    output = zipl(args, column_widths)
    puts(columns(*output))

    lines = ['='*len(s) for s in args]
    lines = zipl(lines, column_widths)
    puts(columns(*lines))


def print_row(month, total, rent):
    values = [
        month,
        '{:0.2f}'.format(total),
        colored.green('{:0.2f}'.format(rent)),
    ]
    output = zipl(values, column_widths)
    puts(columns(*output))


print_headers('Month', 'Monthly total', 'Office rent')
for row in get_rows():
    print_row(*row)
