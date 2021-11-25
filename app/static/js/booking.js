// TODO: Refactor and comment script properly
$("#bookingForm").submit(function (e) {
  e.preventDefault(); // avoid to execute the actual submit of the form.
  // Set date to current date of transaction.
  $("#transactionDate").val(new Date().toISOString().split("T")[0]);

  $("#bookingSuccessModal").modal("show");
  $.ajax({
    type: "POST",
    url: $(document).url,
    data: $("#bookingForm").serialize(), // serializes the form's elements.
    success: function (data) {
      // call 200 and set window location to booking page + booking ID
      window.location = data;
    },
  });
});

var todayDate = new Date().toISOString().split("T")[0];

$("#startDate").attr("min", todayDate); // Set minimum value to today.
$("#startDate").attr("max", addDays(new Date(), 90)); // set max value to 90 days or 3 months in advance.
$("#startDate").on("change", function () {
  // on change:
  var startVal = new Date($("#startDate").val()).toISOString().split("T")[0]; // get startDate's value as DateObject
  // Add one day as minimum booking can't be same day
  $("#endDate").val(addDays(startVal, 1)); // set end date value to the same date as start date, plus one
  $("#endDate").attr("min", addDays(startVal, 1)); // set minimum value to same date as start date, plus one
});
$("#startDate").val(todayDate).trigger("change");

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
  }
});
