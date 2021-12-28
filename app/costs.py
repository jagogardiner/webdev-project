from .model import Booking


class Costs:
    def __init__(self, booking: Booking) -> None:
        self.nights = 0
        self.total = 0
        self.discount = 0
        self.paid = 0
        self.__calculateCosts(booking=booking)
        self.price_pn = self.total / self.nights
        pass

    # TODO: Comment, refactor
    def __calculateCosts(self, booking: Booking):
        """TODO: Comment

        Args:
            booking (Booking): [description]
        """
        if booking.start_date.month in range(4, 10):
            price_pn = booking.hotel.peakPrice
        else:
            price_pn = booking.hotel.offPeakPrice

        if booking.room_type == "double":
            if booking.guests == 2:
                price_pn *= 1.3
            else:
                price_pn *= 1.2
        elif booking.room_type == "family":
            price_pn *= 1.5

        self.nights = (booking.end_date - booking.start_date).days
        booking_advance = (booking.start_date - booking.transaction_date).days

        self.total = round((price_pn * self.nights), 2)
        if booking_advance >= 80:
            self.discount = (self.total) - (self.total * 0.8)
            self.paid = self.total * 0.8
        elif booking_advance >= 60:
            self.discount = (self.total) - (self.total * 0.9)
            self.paid = self.total * 0.9
        elif booking_advance >= 45:
            self.discount = (self.total) - (self.total * 0.95)
            self.paid = self.total * 0.95
        else:
            self.paid = self.total
