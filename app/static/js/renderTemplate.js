function load(callback) {
	$("#header").load("/header", function () {
		callback();
	});
	$("#footer").load("/footer");
}
