// HTML "Sort By" element
const sortByElement = document.getElementById("sortBy");

// HTML "movies table body" element
const moviesTableBody = document.getElementById("moviesTableBody");

// onchange handler for HTML "Sort By" element
sortByElement.onchange = function () {
	const sortByValue = sortByElement.value;
	updatePage(sortByValue);

	// store value of "Sort By" to localStorage
	// this enables us to persist the "Sort By" value through page refreshes
	window.localStorage.setItem("sortByValue", JSON.stringify(sortByValue));
};

async function updateDisplay(sortByValue, limit) {
	// most calls to updateDisplay will be through updatePage()
	// updatePage() handles sets sortByValue and limit to non-null/non-undefined values, so
	// sortByValue and limit will never be undefined

	// clear moviesTableBody
	moviesTableBody.innerHTML = "";

	let url =
		"http://localhost:5000?limit=" +
		limit +
		"&sortBy=" +
		(sortByValue == "default" ? "movieId" : sortByValue);
	console.log(url);

	const response = await fetch(url);

	if (!response.ok) {
		// TODO: graceful handling
		console.error(
			"Error response from server. Error code: ",
			response.status
		);
	} else {
		const data = await response.json();

		for (const movie of data.movies) {
			let tr = document.createElement("tr");

			let movieId = document.createElement("td");
			movieId.innerHTML = movie.movieId;

			let movieName = document.createElement("td");
			movieName.innerHTML = movie.movieTitle;

			tr.appendChild(movieId);
			tr.appendChild(movieName);
			moviesTableBody.appendChild(tr);
		}
	}
}

function updatePage(sortByValue, limit) {
	// if sortByValue is null, then we check if it is stored in localStorage
	// if it is not stored in localStorage, we use the value "default"
	if (!sortByValue) {
		sortByValue = window.localStorage.getItem("sortByValue")
			? JSON.parse(window.localStorage.getItem("sortByValue"))
			: "default";
	}

	// update "selected" attribute in sortBy HTML element
	document.querySelector(
		'#sortBy [value="' + sortByValue + '"]'
	).selected = true;

	// if limit is null, then we check if it is stored in localStorage
	// if it is not stored in localStorage, we use the value 10
	if (!limit) {
		limit = window.localStorage.getItem("limit")
			? JSON.parse(window.localStorage.getItem("limit"))
			: 10;
	} else {
		// store value of limit in localStorage
		// the reason why the `if (!sortByValue) {..}` block above does not need this line
		// is because the storing to localStorage is handled by the onchange handler
		window.localStorage.setItem("limit", JSON.stringify(limit));
	}

	const pageLimitButtons = document.getElementsByClassName("page-limit-btn");

	for (const btn of pageLimitButtons) {
		btn.classList.remove("active");
		if (btn.textContent == limit) {
			btn.classList.add("active");
		}
	}

	updateDisplay(sortByValue, limit);
}

// call updatePage() on every page load
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
