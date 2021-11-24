// TODO: Refactor and comment script properly
function addDays(date, days) {
	var result = new Date(date);
	result.setDate(result.getDate() + days);
	return result.toISOString().split("T")[0];
}

$("#bookingForm").submit(function (e) {
	e.preventDefault(); // avoid to execute the actual submit of the form.
	$.ajax({
		type: "POST",
		url: $(document).url,
		data: $("#bookingForm").serialize(), // serializes the form's elements.
		success: function (data) {
			console.log(data);
		},
	});
});

$("#startDate").attr("min", new Date().toISOString().split("T")[0]); // Set minimum value to today.
$("#startDate").attr("max", addDays(new Date(), 90)); // set max value to 90 days or 3 months in advance.
$("#startDate").on("change", function () {
	// on change:
	var startVal = new Date($("#startDate").val()).toISOString().split("T")[0]; // get startDate's value as DateObject
	// Add one day as minimum booking can't be same day
	$("#endDate").val(addDays(startVal, 1)); // set end date value to the same date as start date, plus one
	$("#endDate").attr("min", addDays(startVal, 1)); // set minimum value to same date as start date, plus one
});

$("#roomType").on("change", function () {
	$("#guestAmount").empty();
	$("#guestAmount").removeAttr("disabled");
	if (this.value == "double") {
		for (let i = 1; i <= 2; i++) {
			$("#guestAmount").append(
				$("<option>", {
					value: i,
					text: i,
				})
			);
		}
	} else if (this.value == "family") {
		for (let i = 1; i <= 5; i++) {
			$("#guestAmount").append(
				$("<option>", {
					value: i,
					text: i,
				})
			);
		}
	} else {
		$("#guestAmount").append(
			$("<option>", {
				value: 1,
				text: "1",
			})
		);
		$("#guestAmount").attr("disabled", true);
	}
});

function differenceInDays(date1, date2) {
	return Math.round(
		// Subtracting two days gives you time in milliseconds - divide this
		Math.abs((date1 - date2) / (24 * 60 * 60 * 1000))
	);
}

// Calculate booking cost and their numbers from peak price or off peak price.
function calculateBookingCost(peakPrice, offPeakPrice) {
	// Make new date object.
	var bookingStartDate = new Date($("#startDate").val());
	var bookingEndDate = new Date($("#endDate").val());
	// Get current month number - JS date does this from 0 - 11
	var month = bookingStartDate.getMonth();
	// If month is from April - September:
	if (month >= 3 && month <= 9) {
		// Set price p/n to peak price
		var pricePn = peakPrice;
	} else {
		// Set price p/n to off-peak price.
		var pricePn = offPeakPrice;
	}

	// If room type is either double or family, add on respective price increase
	if ($("#roomType").val() == "double") {
		pricePn *= 1.2;
	} else if ($("#roomType").val() == "family") {
		pricePn *= 1.5;
	}

	$("#roomPricePerNight").text("Room price: £" + pricePn.toFixed(2) + " p/n");

	// Find the difference in days.
	// Rounding and using the absolute brings the total number of
	// days between the two days, used for calculating the price discount.
	const diffDaysBooking = differenceInDays(bookingStartDate, bookingEndDate);
	const diffDays = differenceInDays(bookingStartDate, new Date()) + 1;
	// Find the room total from this
	var roomTotal = (pricePn * diffDaysBooking).toFixed(2);
	if (diffDaysBooking == 1) {
		$("#roomPriceTotal").text(diffDaysBooking + " night: £" + roomTotal);
	} else {
		$("#roomPriceTotal").text(diffDaysBooking + " nights: £" + roomTotal);
	}

	// Calculate the discount for booking in advance.
	var discount = 0;
	if (diffDays >= 80) {
		discount = roomTotal;
		roomTotal *= 0.8;
		discount -= roomTotal;
	} else if (diffDays >= 60) {
		discount = roomTotal;
		roomTotal *= 0.9;
		discount -= roomTotal;
	} else if (diffDays >= 45) {
		discount = roomTotal;
		roomTotal *= 0.95;
		discount -= roomTotal;
	}

	// Show money saved and the full booking total.
	$("#roomPriceDiscount").text("Advance booking discount: -£" + discount);
	$("#priceTotal").text("Full total: £" + roomTotal);
}
