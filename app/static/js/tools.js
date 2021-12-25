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

async function getCosts(hotel_id, start_date, end_date, room_type) {
  const resp = await fetch('/api/costs', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      hotel_id: hotel_id,
      start_date: start_date,
      end_date: end_date,
      room_type: room_type,
    }),
  })
  return resp.json()
}

async function getBookingPrices() {
  const resp = await fetch('/api/bookings', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  })
  return resp.json()
}
