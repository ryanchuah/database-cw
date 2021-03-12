const rootUrl = "http://localhost";

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

async function updateDisplay(sortByValue, limit, page) {
	// most calls to updateDisplay will be through updatePage()
	// updatePage() handles sets sortByValue and limit to non-null/non-undefined values, so
	// sortByValue and limit will never be undefined

	// clear moviesTableBody
	moviesTableBody.innerHTML = "";

	let url =
		`${rootUrl}/movies?limit=` +
		limit +
		"&sortBy=" +
		sortByValue +
		"&page=" +
		page +
		"&ascending=" +
		1;

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
		for (const movie of data.movies) {
			let tr = document.createElement("tr");
			rating_val = parseFloat(movie.avg_ratings);
			rating_val = rating_val
				? Math.round(rating_val * 2) / 2
				: "Unknown"; //round to nearest 0.5
			tr.innerHTML = `
			<td>${movie.movieId}</td>
			<td><a href="movies/movie.html?movieId=${movie.movieId}">${movie.title}</a></td>
			<td>${movie.release_year}</td>
			<td>${rating_val}</td>
			<td>${movie.votes}</td>
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
function updatePage(sortByValue, limit, page) {
	// if sortByValue is null, then we check if it is stored in localStorage
	// if it is not stored in localStorage, we use the value "default"
	if (!sortByValue) {
		sortByValue = window.localStorage.getItem("sortByValue")
			? JSON.parse(window.localStorage.getItem("sortByValue"))
			: "popularity";
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

	// if (!page) {
	// 	page = window.localStorage.getItem("page")
	// 		? JSON.parse(window.localStorage.getItem("page"))
	// 		: 1;
	// }
	// if (!page) {
	// 	page = 1;
	// }

	// let column;
	// if (sortByValue != "polarity" && sortByValue != "popularity") {
	// 	console.log("HERE");

	// 	// means we are sorting by column name
	// 	column = sortByValue;
	// 	sortByValue = "column";
	// }

	updateDisplay(sortByValue, limit, page);
	updatePagination(page);
}

// call updatePage() on every page load
updatePage();
