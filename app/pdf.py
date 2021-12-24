from fpdf import FPDF, FlexTemplate
import qrcode
from .model import Booking
from .costs import Costs


class PDF(FPDF):
    def __init__(
        self,
        booking: Booking,
        orientation="portrait",
        unit="mm",
        format="A4",
        font_cache_dir=True,
    ) -> None:
        self.booking = booking
        super().__init__(
            orientation=orientation,
            unit=unit,
            format=format,
            font_cache_dir=font_cache_dir,
        )

    def header(self) -> None:
        self.set_font("Helvetica", "B", 20)
        img = qrcode.make(self.booking.booking_reference)
        self.image(img.get_image(), x=150, y=0, w=50, h=50)
        self.cell(30, 10, "Horizon Hotels")

    def footer(self) -> None:
        elements = [
            {
                "name": "barcode",
                "type": "C39",
                "x1": 20.0,
                "y1": 260.0,
                "x2": 140.0,
                "y2": 278.5,
                "font": "Code 39",
                "size": 0.75,
                "bold": 0,
                "italic": 0,
                "underline": 0,
                "foreground": 0,
                "background": 0,
                "align": "I",
                "text": "*" + self.booking.booking_reference + "*",
                "priority": 3,
            },
        ]
        tpl = FlexTemplate(self, elements=elements)
        tpl.render()
        self.set_y(-15)
        # Arial italic 8
        self.set_font("Helvetica", size=8)
        # Page number
        self.cell(0, 10, "Page " + str(self.page_no()) + "/{nb}", 0, 0, "C")


class Receipt(FPDF):
    def __init__(self, booking: Booking):
        self.pdf = PDF(booking, format="A4", orientation="portrait")
        self.pdf.add_page()
        self.__add_info(booking)

    def __add_info(self, booking: Booking) -> None:
        costs = Costs(booking=booking)
        self.pdf.set_font("Helvetica", size=16)
        self.pdf.ln(20)
        self.pdf.cell(0, self.pdf.y + 20, "You are staying at: " + booking.hotel.city)
        self.pdf.ln(32)
        self.pdf.set_font("Helvetica", size=12)
        self.pdf.cell(0, 0, "Transaction date: " + str(booking.transaction_date))
        self.pdf.ln(7)
        self.pdf.cell(0, 0, "Check-in date: " + str(booking.start_date))
        self.pdf.ln(7)
        self.pdf.cell(0, 0, "Check-out date: " + str(booking.end_date))
        self.pdf.ln(7)
        self.pdf.cell(0, 0, "Total nights: " + str(costs.nights))
        self.pdf.ln(7)
        self.pdf.cell(0, 0, "Guests: " + str(booking.guests))
        self.pdf.ln(7)
        self.pdf.cell(0, 0, "Room type: " + str(booking.room_type))
        self.pdf.ln(7)
        self.pdf.cell(0, 0, "Room price p/n: " + str(costs.price_pn))
        self.pdf.ln(7)
        self.pdf.cell(0, 0, "Total discount: " + str(costs.discount))
        self.pdf.ln(7)
        self.pdf.cell(0, 0, "Total paid: " + str(costs.paid))
