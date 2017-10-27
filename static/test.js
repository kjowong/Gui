#!/usr/bin/node
// function myFunction() {
//     var x = document.getElementById("myForm").elements[0].value;
//     console.log("Hi there", x)
//     document.getElementById("zip").innerHTML = x;
// 
// $.ajax({
// 	url:'http://0.0.0.0:5000/search/{}'.format(x)
// 
// }
var request = require('axios');

request.get('http://0.0.0.0:5000/search/94118')
	.then (function (response) {
		console.log(response.data);
	})
	.catch (function (error) {
		console.log(error);
	});
