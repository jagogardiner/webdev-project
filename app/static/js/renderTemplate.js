function load(callback) {
	$("#header").load("/header", function () {
		typeof callback === "function" && callback();
	});
	$("#footer").load("/footer");
}
