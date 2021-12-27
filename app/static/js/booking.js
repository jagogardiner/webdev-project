$('#bookingForm').submit((e) => {
  e.preventDefault() // Avoid to execute the actual submit of the form.
  // Set date to current date of transaction.
  $('#transactionDate').val(new Date().toISOString().split('T')[0])

  $('#bookingSuccessModal').modal('show')
  let booking
  $.ajax({
    type: 'POST',
    url: '/api/newBooking',
    data: $('#bookingForm').serialize(), // Serializes the form's elements.
    success(bookingdata) {
      booking = bookingdata
      $.ajax({
        type: 'POST',
        url: '/api/hotelinfo',
        contentType: 'application/json',
        data: JSON.stringify(bookingdata),
        success(hotel) {
          var modal = $('#bookingSuccessModal')
          modal.find('.modal-title').text('Booking complete!')
          modal
            .find('.modal-body')
            .html(
              '<p class="h5">Thanks for booking with Horizon Hotels!</p><p class="h6">You are staying at: ' +
                hotel.city +
                ', from ' +
                booking.start_date +
                ' to ' +
                booking.end_date +
                '.</p><p class="h6">When you arrive at reception, please bring valid ID and quote the booking reference: #' +
                booking.booking_reference +
                '</p>',
            )
        },
      })
    },
    error(e) {
      window.location = e.redirect
    },
  })
})

const todayDate = new Date().toISOString().split('T')[0]

$('#startDate').attr('min', todayDate) // Set minimum value to today.
$('#startDate').attr('max', addDays(new Date(), 90)) // Set max value to 90 days or 3 months in advance.
$('#startDate').on('change', () => {
  // On change:
  const startVal = new Date($('#startDate').val()).toISOString().split('T')[0] // Get startDate's value as DateObject
  // Add one day as minimum booking can't be same day
  $('#endDate').val(addDays(startVal, 1)) // Set end date value to the same date as start date, plus one
  $('#endDate').attr('min', addDays(startVal, 1)) // Set minimum value to same date as start date, plus one
})
$('#startDate').val(todayDate).trigger('change')
// TODO: Annotate and document
$('#roomType').on('change', function () {
  $('#guestAmount').empty()
  $('#guestAmount').removeAttr('disabled')
  if (this.value === 'double') {
    for (let i = 1; i <= 2; i++) {
      $('#guestAmount').append(
        $('<option>', {
          value: i,
          text: i,
        }),
      )
    }
  } else if (this.value === 'family') {
    for (let i = 1; i <= 5; i++) {
      $('#guestAmount').append(
        $('<option>', {
          value: i,
          text: i,
        }),
      )
    }
  } else {
    $('#guestAmount').append(
      $('<option>', {
        value: 1,
        text: '1',
      }),
    )
  }
})
