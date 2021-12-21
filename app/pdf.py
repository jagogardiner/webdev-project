from fpdf import FPDF, FlexTemplate
import qrcode


class Receipt:
    def __init__(self):
        pass

    def GeneratePDF(self, booking=None, hotel=None):
        # this will define the ELEMENTS that will compose the template.
        elements = [
            {
                "name": "company_name",
                "type": "T",
                "x1": 17.0,
                "y1": 32.5,
                "x2": 115.0,
                "y2": 37.5,
                "font": "Helvetica",
                "size": 12.0,
                "bold": 1,
                "italic": 0,
                "underline": 0,
                "foreground": 0,
                "background": 0,
                "align": "I",
                "text": "",
                "priority": 2,
            },
            {
                "name": "barcode",
                "type": "C39",
                "x1": 20.0,
                "y1": 246.5,
                "x2": 140.0,
                "y2": 254.0,
                "font": "Code 39",
                "size": 0.75,
                "bold": 0,
                "italic": 0,
                "underline": 0,
                "foreground": 0,
                "background": 0,
                "align": "I",
                "text": "*" + booking.booking_reference + "*",
                "priority": 3,
            },
        ]

        pdf = FPDF(format="A4", orientation="portrait")
        pdf.set_font("Helvetica", "B", 20)
        pdf.add_page()
        pdf.cell(30, 10, "Horizon Hotels")
        pdf.cell(100)
        img = qrcode.make(booking.booking_reference)
        pdf.image(img.get_image(), x=150, y=0, w=50, h=50)
        pdf.ln(20)
        pdf.set_font("Helvetica", size=12)

        # here we instantiate the template and define the HEADER
        tpl = FlexTemplate(pdf, elements=elements)
        tpl.render()

        return pdf
