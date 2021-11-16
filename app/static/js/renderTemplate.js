/*
@function load()
Function to load header and footer using jQuery.
Uses a callback so elements inside these HTML files can be
modified on the fly.
*/
function load(callback) {
	// Load header
	$("#header").load("/header", function () {
		// Make sure we run callback ONLY if it is a type "function".
		// Callbacks are used here to make elements active.
		typeof callback === "function" && callback();
	});
	// Load footer
	$("#footer").load("/footer"); // Footer does not have a callback as we do not modify elements inside the header.
}
