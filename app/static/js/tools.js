// Todo: Annotate all functions

/*
@function load()
Function to load header and footer using jQuery.
Uses a callback so elements inside these HTML files can be
modified on the fly.
*/
/**
 *
 * @param {*} callback
 */
function loadTemplate(callback) {
  // Load header
  $("#header").load("/header", function () {
    // Make sure we run callback ONLY if it is a type "function".
    // Callbacks are used here to make elements active.
    typeof callback === "function" && callback();
  });
  // Load footer
  $("#footer").load("/footer"); // Footer does not have a callback as we do not modify elements inside the header.
}

/**
 *
 * @param {*} date
 * @param {*} days
 * @returns
 */
function addDays(date, days) {
  var result = new Date(date);
  result.setDate(result.getDate() + days);
  return result.toISOString().split("T")[0];
}

/**
 *
 * @param {*} date1
 * @param {*} date2
 * @returns
 */
function differenceInDays(date1, date2) {
  return Math.round(
    // Subtracting two days gives you time in milliseconds - divide this
    Math.abs((date1 - date2) / (24 * 60 * 60 * 1000))
  );
}

/**
 * TODO: Please just annotate this
 * @param {*} peakPrice
 * @param {*} offPeakPrice
 * @param {*} startDate
 * @param {*} endDate
 * @param {*} roomType
 * @param {*} bookingTransactionDate
 * @returns
 */
function calculateBookingCosts(
  peakPrice,
  offPeakPrice,
  startDate,
  endDate,
  roomType,
  bookingTransactionDate = new Date()
) {
  // Make new date object.
  var bookingStartDate = new Date(startDate);
  var bookingEndDate = new Date(endDate);
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
  if (roomType == "double") {
    pricePn *= 1.2;
  } else if (roomType == "family") {
    pricePn *= 1.5;
  }

  // Find the difference in days.
  // Rounding and using the absolute brings the total number of
  // days between the two days, used for calculating the price discount.
  const nights = differenceInDays(bookingStartDate, bookingEndDate);
  const diffDays =
    differenceInDays(bookingStartDate, bookingTransactionDate) + 1;
  // Find the room total from this
  var roomTotal = (pricePn * nights).toFixed(2);

  // Calculate the discount for booking in advance.
  var discount = 0;
  var totalCost = roomTotal;
  if (diffDays >= 80) {
    discount = roomTotal;
    roomTotal *= 0.8;
    discount -= totalCost;
  } else if (diffDays >= 60) {
    discount = roomTotal;
    roomTotal *= 0.9;
    discount -= totalCost;
  } else if (diffDays >= 45) {
    discount = roomTotal;
    roomTotal *= 0.95;
    discount -= totalCost;
  }
  return {
    pricePn,
    roomTotal,
    totalCost,
    discount,
    nights,
  };
}