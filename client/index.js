const rootUrl = "http://localhost";

// HTML "Sort By" element
const sortByElement = document.getElementById("sortBy");

// HTML "movies table body" element
const popularMoviesTableBody = document.getElementById(
	"popularMoviesTableBody"
);
const polarizingMoviesTableBody = document.getElementById(
	"polarizingMoviesTableBody"
);

// // onchange handler for HTML "Sort By" element
// sortByElement.onchange = function () {
// 	const sortByValue = sortByElement.value;
// 	updatePage(sortByValue);

// 	// store value of "Sort By" to localStorage
// 	// this enables us to persist the "Sort By" value through page refreshes
// 	window.localStorage.setItem("sortByValue", JSON.stringify(sortByValue));
// };

function updateTables(data, elem) {
	for (const movie of data.movies) {
		let tr = document.createElement("tr");
		let rating_val = parseFloat(movie.avg_ratings);
		let polarity_index = parseFloat(movie.polarity_index);

		rating_val = parseFloat(movie.avg_ratings);
		rating_val = rating_val
			? Math.round(rating_val * 100) / 100
			: "Unknown"; //round to nearest 0.5
		polarity_index = parseFloat(movie.polarity_index);
		polarity_index = polarity_index
			? Math.round(polarity_index * 100) / 100
			: "Unknown"; //round to nearest 0.5
		tr.innerHTML = `
			<td>${movie.movieId}</td>
			<td><a href="movies/movie.html?movieId=${movie.movieId}">${movie.title}</a></td>
			<td>${movie.release_year}</td>
			<td>${rating_val}</td>
			<td>${movie.votes}</td>
			<td>${polarity_index}</td>
			`;
		elem.appendChild(tr);
	}
}

async function updateDisplay(sortByValue, limit, page) {
	// most calls to updateDisplay will be through updatePage()
	// updatePage() handles sets sortByValue and limit to non-null/non-undefined values, so
	// sortByValue and limit will never be undefined

	// clear moviesTableBody
	popularMoviesTableBody.innerHTML = "";
	polarizingMoviesTableBody.innerHTML = "";

	const popularUrl =
		`${rootUrl}/movies?limit=10` +
		"&sortBy=popularity" +
		"&page=1" +
		"&ascending=1";

	const polarizingUrl =
		`${rootUrl}/movies?limit=10` +
		"&sortBy=polarity_index" +
		"&page=1" +
		"&ascending=1";

	console.log("Popular url:");
	console.log(popularUrl);

	console.log("Polarizing url:");
	console.log(polarizingUrl);

	const popularResponse = await fetch(popularUrl);
	const polarizingResponse = await fetch(polarizingUrl);
	if (!popularResponse.ok) {
		// TODO: graceful handling
		console.error(
			"Error response from server. Error code: ",
			popularResponse.status
		);
	} else {
		const popularData = await popularResponse.json();
		updateTables(popularData, popularMoviesTableBody);
		console.log(popularData);
	}

	if (!polarizingResponse.ok) {
		// TODO: graceful handling
		console.error(
			"Error response from server. Error code: ",
			polarizingResponse.status
		);
	} else {
		const polarizingData = await polarizingResponse.json();
		console.log(polarizingData);

		updateTables(polarizingData, polarizingMoviesTableBody);
	}
}

// this function handles the sanity check for sortByValue, limit, page before passing on to updateDisplay(..)
function updatePage(sortByValue, limit, page) {
	// if sortByValue is null, then we check if it is stored in localStorage
	// if it is not stored in localStorage, we use the value "default"
	if (!sortByValue) {
		sortByValue = window.localStorage.getItem("sortByValue")
			? JSON.parse(window.localStorage.getItem("sortByValue"))
			: "popularity";
	}

	// // update "selected" attribute in sortBy HTML element
	// document.querySelector(
	// 	'#sortBy [value="' + sortByValue + '"]'
	// ).selected = true;

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

	if (!page) {
		page = window.localStorage.getItem("page")
			? JSON.parse(window.localStorage.getItem("page"))
			: 1;
	} else {
		window.localStorage.setItem("page", JSON.stringify(page));
	}

	const pageLimitButtons = document.getElementsByClassName("page-limit-btn");

	for (const btn of pageLimitButtons) {
		btn.classList.remove("active");
		if (btn.textContent == limit) {
			btn.classList.add("active");
		}
	}

	updateDisplay(sortByValue, limit, page);
}

// call updatePage() on every page load
updatePage();
