const color = document.getElementById("color");

let sortByElement = document.getElementById("sortBy");
const moviesTableBody = document.getElementById("moviesTableBody");

sortByElement.onchange = function () {
	const sortByValue = sortByElement.value;
	updatePage(sortByValue);
	window.localStorage.setItem("sortByValue", JSON.stringify(sortByValue));
};

async function updateDisplay(sortByValue, limit) {
	moviesTableBody.innerHTML = "";
	let url =
		"http://localhost:5000?limit=" +
		limit +
		"&sortBy=" +
		(sortByValue == "default" ? "movieId" : sortByValue);
	console.log(url);

	const response = await fetch(url);

	if (!response.ok) {
		console.error(
			"Error response from server. Error code: ",
			response.status
		);
	} else {
		const data = await response.json();

		for (const movie of data.movies) {
			let tr = document.createElement("tr");

			let movieId = document.createElement("td");
			movieId.innerHTML = movie[0];

			let movieName = document.createElement("td");
			movieName.innerHTML = movie[1];

			tr.appendChild(movieId);
			tr.appendChild(movieName);
			moviesTableBody.appendChild(tr);
		}
	}
}

function updatePage(sortByValue, limit) {
	if (!sortByValue) {
		sortByValue = window.localStorage.getItem("sortByValue")
			? JSON.parse(window.localStorage.getItem("sortByValue"))
			: "default";
	}
	// update "selected" attribute in sortBy HTML element
	document.querySelector(
		'#sortBy [value="' + sortByValue + '"]'
	).selected = true;

	if (!limit) {
		limit = window.localStorage.getItem("limit")
			? JSON.parse(window.localStorage.getItem("limit"))
			: 10;
	} else {
		window.localStorage.setItem("limit", JSON.stringify(limit));
	}

	updateDisplay(sortByValue, limit);
}

updatePage();

// tutorial function. This function is not actually used anywhere
// it's just meant to give a feel for JS
async function insertColor() {
	const response = await fetch("http://localhost:5000/");
	if (!response.ok) {
		console.error(
			"Error response from server. Error code: ",
			response.status
		);
	} else {
		const data = await response.json();

		const fav_colors = data.favorite_colors;

		// fav_colors is an array of objects:
		console.log(fav_colors); // [{Zahra: "blue"}, {Chak: "yellow"}]

		let tag;
		let text;

		for (color_obj of fav_colors) {
			// iterate through array
			console.log(color_obj); // {Zahra: "blue"}
			// iterate through object
			for (const user in color_obj) {
				console.log(user); // Zahra

				tag = document.createElement("li");

				text = document.createTextNode(
					`${user} likes ${color_obj[user]}`
				);
				tag.appendChild(text);

				color.appendChild(tag);
			}
		}
	}
}

// insertColor();
