/* eslint-disable no-unused-vars */
/* eslint-disable max-params */
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
  $('#header').load('/header', () => {
    // Make sure we run callback ONLY if it is a type "function".
    // Callbacks are used here to make elements active.
    if (typeof callback === 'function') {
      callback()
    }
  })
  // Load footer
  $('#footer').load('/footer') // Footer does not have a callback as we do not modify elements inside the header.
}

/**
 *
 * @param {*} date
 * @param {*} days
 * @returns
 */
function addDays(date, days) {
  const result = new Date(date)
  result.setDate(result.getDate() + days)
  return result.toISOString().split('T')[0]
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
    Math.abs((date1 - date2) / (24 * 60 * 60 * 1000)),
  )
}

/**
 *
 *
 * @param {*} peakPrice
 * @param {*} offPeakPrice
 * @param {*} startDate
 * @param {*} endDate
 * @param {*} roomType
 * @param {*} [bookingTransactionDate=new Date()]
 * @return {*}
 */
function calculateBookingCosts(
  peakPrice,
  offPeakPrice,
  startDate,
  endDate,
  roomType,
  bookingTransactionDate,
) {
  // Make new date object.
  const bookingStartDate = new Date(startDate)
  const bookingEndDate = new Date(endDate)
  // Get current month number - JS date does this from 0 - 11
  const month = bookingStartDate.getMonth()
  let pricePn
  // If month is from April - September:
  if (month >= 3 && month <= 9) {
    // Set price p/n to peak price
    pricePn = peakPrice
  } else {
    // Set price p/n to off-peak price.
    pricePn = offPeakPrice
  }

  // Track price before bedroom adjustment
  const beforePricePn = pricePn

  // If room type is either double or family, add on respective price increase
  if (roomType === 'double') {
    pricePn *= 1.2
  } else if (roomType === 'family') {
    pricePn *= 1.5
  }

  // Find the difference in days.
  // Rounding and using the absolute brings the total number of
  // days between the two days, used for calculating the price discount.
  const nights = differenceInDays(bookingStartDate, bookingEndDate)
  const diffDays =
    differenceInDays(bookingStartDate, bookingTransactionDate) + 1
  // Find the room total from this
  const roomTotal = (pricePn * nights).toFixed(2)

  // Calculate the discount for booking in advance.
  let discount = 0
  let totalCost = roomTotal
  if (diffDays >= 80) {
    discount = totalCost
    totalCost *= 0.8
    discount -= totalCost
  } else if (diffDays >= 60) {
    discount = totalCost
    totalCost *= 0.9
    discount -= totalCost
  } else if (diffDays >= 45) {
    discount = totalCost
    totalCost *= 0.95
    discount -= totalCost
  }

  return {
    pricePn,
    beforePricePn,
    roomTotal,
    totalCost,
    discount,
    nights,
  }
}
