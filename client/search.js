const rootUrl = "http://localhost";

// HTML "Sort By" element
const sortByElement = document.getElementById("sortBy");
const ascendingElement = document.getElementById("ascending");
const searchHeaderElement = document.getElementById("search-header");

// HTML "movies table body" element
const moviesTableBody = document.getElementById("moviesTableBody");

// onchange handler for HTML "Sort By" element
sortByElement.onchange = function () {
	const sortByValue = sortByElement.value;
	updatePage(sortByValue);

	// store value of "Sort By" to localStorage
	// this enables us to persist the "Sort By" value through page refreshes
	window.localStorage.setItem(
		"search-sortByValue",
		JSON.stringify(sortByValue)
	);
};

ascendingElement.onchange = function () {
	const ascending = ascendingElement.value;

	updatePage(null, null, null, null, ascending);

	// store value of "Sort By" to localStorage
	// this enables us to persist the "Sort By" value through page refreshes
	window.localStorage.setItem("search-ascending", JSON.stringify(ascending));
};

async function updateDisplay(
	sortByValue,
	limit,
	page,
	searchTerm,
	ascending,
	searchHeader
) {
	// most calls to updateDisplay will be through updatePage()
	// updatePage() handles sets sortByValue and limit to non-null/non-undefined values, so
	// sortByValue and limit will never be undefined
	searchHeaderElement.innerHTML = `<h1>${searchHeader}</h1>`;

	// clear moviesTableBody
	moviesTableBody.innerHTML = "";

	let url =
		`${rootUrl}/${searchTerm ? "search" : "movies"}?limit=` +
		limit +
		"&sortBy=" +
		sortByValue +
		"&page=" +
		page +
		"&ascending=" +
		ascending +
		"&search_criteria=" +
		searchTerm;

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
		let rating_val;
		let polarity_index;
		for (const movie of data.movies) {
			let tr = document.createElement("tr");
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
			<td>${movie.release_year != -1 ? movie.release_year : "Unknown"}</td>
			<td>${rating_val}</td>
			<td>${movie.votes}</td>
			<td>${polarity_index}</td>
			`;
			moviesTableBody.appendChild(tr);
		}
	}
}

function updatePagination(page) {
	// HTML "Sort By" element
	const pagination = document.getElementById("pagination");
	// <li class="page-item active"><a class="page-link" href="#" onclick="updatePage(null, null, 1)">${page}</a></li>
	pagination.innerHTML = `
	<li class="page-item"><a class="page-link" href="#" onclick="updatePage(null, null, 1)">&laquo;</a></li>
	 <li class="page-item">
		<a class="page-link" href="#" onclick="updatePage(null, null, ${
			page - 1
		})" aria-label="Previous">
                <span aria-hidden="true"><</span>
		</a>
	</li>`;

	if (page == 1) {
		pagination.innerHTML += `
       
        <li class="page-item active"><a class="page-link" href="#">${page}</a></li>
        <li class="page-item"><a class="page-link" href="#" onclick="updatePage(null, null, ${
			page + 1
		})">${page + 1}</a></li>
        <li class="page-item"><a class="page-link" href="#" onclick="updatePage(null, null, ${
			page + 2
		})">${page + 2}</a></li>`;
	} else {
		pagination.innerHTML += `
       
        <li class="page-item"><a class="page-link" href="#" onclick="updatePage(null, null, ${
			page - 1
		})">${page - 1}</a></li>
        <li class="page-item active"><a class="page-link" href="#" onclick="updatePage(null, null, ${page})">${page}</a></li>
        <li class="page-item"><a class="page-link" href="#" onclick="updatePage(null, null, ${
			page + 1
		})">${page + 1}</a></li>
        `;
	}
	pagination.innerHTML += `
	<li class="page-item">
            <a class="page-link" href="#" onclick="updatePage(null, null, ${
				page + 1
			})" aria-label="Next">
                <span aria-hidden="true">></span>
            </a>
	</li>`;
}

// this function handles the sanity check for sortByValue, limit, page before passing on to updateDisplay(..)
function updatePage(sortByValue, limit, page, searchTerm, ascending) {
	// if sortByValue is null, then we check if it is stored in localStorage
	// if it is not stored in localStorage, we use the value "default"

	if (!sortByValue) {
		sortByValue = window.localStorage.getItem("search-sortByValue")
			? JSON.parse(window.localStorage.getItem("search-sortByValue"))
			: "popularity";
	}

	// update "selected" attribute in sortBy HTML element
	document.querySelector(
		'#sortBy [value="' + sortByValue + '"]'
	).selected = true;

	// if limit is null, then we check if it is stored in localStorage
	// if it is not stored in localStorage, we use the value 10
	if (!limit) {
		limit = window.localStorage.getItem("search-limit")
			? JSON.parse(window.localStorage.getItem("search-limit"))
			: 10;
	} else {
		// store value of limit in localStorage
		// the reason why the `if (!sortByValue) {..}` block above does not need this line
		// is because the storing to localStorage is handled by the onchange handler
		window.localStorage.setItem("search-limit", JSON.stringify(limit));
	}

	if (!page) {
		page = window.localStorage.getItem("search-page")
			? JSON.parse(window.localStorage.getItem("search-page"))
			: 1;
	} else {
		window.localStorage.setItem("search-page", JSON.stringify(page));
	}

	const pageLimitButtons = document.getElementsByClassName("page-limit-btn");

	for (const btn of pageLimitButtons) {
		btn.classList.remove("active");
		if (btn.textContent == limit) {
			btn.classList.add("active");
		}
	}
	let searchHeader;

	if (!searchTerm || searchTerm == "") {
		searchTerm = window.localStorage.getItem("search-searchTerm")
			? JSON.parse(window.localStorage.getItem("search-searchTerm"))
			: "";
		if (searchTerm == "") {
			searchHeader = "All Movies";
		} else {
			searchHeader = `Search results for: ${searchTerm}`;
		}
	} else {
		window.localStorage.setItem(
			"search-searchTerm",
			JSON.stringify(searchTerm)
		);
	}

	if (!ascending) {
		ascending = window.localStorage.getItem("search-ascending")
			? JSON.parse(window.localStorage.getItem("search-ascending"))
			: 1;
	} else {
		window.localStorage.setItem(
			"search-ascending",
			JSON.stringify(ascending)
		);
	}
	// update "selected" attribute in sortBy HTML element
	document.querySelector(
		'#ascending [value="' + ascending + '"]'
	).selected = true;

	console.log(sortByValue);

	updateDisplay(
		sortByValue,
		limit,
		page,
		searchTerm,
		ascending,
		searchHeader
	);
	updatePagination(page);
}

// call updatePage() on every page load
updatePage();
