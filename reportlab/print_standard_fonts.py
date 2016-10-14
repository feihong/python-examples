"""
Print out standard fonts.

"""

from reportlab.pdfbase import pdfmetrics


for font in pdfmetrics.standardFonts:
    print(font)
