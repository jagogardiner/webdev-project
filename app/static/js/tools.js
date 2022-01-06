/* eslint-disable no-unused-vars */
/**
 * Function to load header and footer using jQuery.
 * Uses a callback so elements inside these HTML files can be
 * modified on the fly.
 * @param {Function} callback Callback used to make header elements active.
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
 * Adds a certain amount of days onto a Date object.
 *
 * @param {Date} date Date to add days onto
 * @param {Number} days Amount of days to add
 * @returns date as ISO string
 */
function addDays(date, days) {
  // make new Date object from
  const result = new Date(date)
  // set date in the future with days added on
  result.setDate(result.getDate() + days)
  // return resulting date in ISO string format
  return result.toISOString().split('T')[0]
}

/**
 * Gets the costs for a booking.
 *
 * @param {Number} hotel_id
 * @param {Date} start_date
 * @param {Date} end_date
 * @param {String} room_type
 * @returns {Promise}
 */
async function getCosts(hotel_id, start_date, end_date, room_type) {
  // Make a fetch request to the API endpoint
  const resp = await fetch('/api/costs', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      // Contains the valid information needed for the API endpoint
      hotel_id: hotel_id,
      start_date: start_date,
      end_date: end_date,
      room_type: room_type,
    }),
  })
  // Recieve the JSON
  return resp.json()
}

/**
 * Gets the total paid as for one Booking.
 *
 * @returns {Promise}
 */
async function getBookingPrices() {
  const resp = await fetch('/api/member/bookingprices', {
    // POST request with no body
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  })
  return resp.json()
}
