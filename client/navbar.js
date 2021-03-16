let navbar;
let root;

if (document.getElementById("navbar")) {
	navbar = document.getElementById("navbar");
	root = ".";
} else {
	navbar = document.getElementById("navbar-movie");
	root = "..";
}

navbar.innerHTML = `
<nav class="navbar navbar-expand-lg navbar-light bg-light">
	<a class="navbar-brand" href="${root}/index.html">Home</a>
	<button
		class="navbar-toggler"
		type="button"
		data-toggle="collapse"
		data-target="#navbarSupportedContent"
		aria-controls="navbarSupportedContent"
		aria-expanded="false"
		aria-label="Toggle navigation"
	>
		<span class="navbar-toggler-icon"></span>
	</button>

	<div class="collapse navbar-collapse" id="navbarSupportedContent">
		<ul class="navbar-nav mr-auto">
            <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                Predict
                </a>
                <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                    <a class="dropdown-item" href="${root}/predict-ratings.html">Ratings</a>
                    <a class="dropdown-item" href="${root}/predict-personality.html">Personality Traits</a>
                </div>
            </li>
			
		</ul>
		<form class="form-inline my-2 my-lg-0" id="search">
			<input
				class="form-control mr-sm-2"
				type="search"
				placeholder="Search"
				aria-label="Search"
                name="search"
			/>
			<button class="btn btn-outline-success my-2 my-sm-0" type="submit">
				Search
			</button>
            <button class="btn btn-outline-success my-2 my-sm-0" onclick="handleAllMovies()">
				All Movies
			</button>
		</form>
	</div>
</nav>
`;

function handleAllMovies() {
	window.localStorage.setItem("search-searchTerm", JSON.stringify(""));
	window.localStorage.setItem(
		"search-sortByValue",
		JSON.stringify("popularity")
	);
	window.localStorage.setItem("search-limit", JSON.stringify(10));
	window.localStorage.setItem("search-page", JSON.stringify(1));
	window.location.href = `${root}/search.html`;
}
async function searchMovie(event) {
	event.preventDefault();
	const searchTerm = event.target.elements.search.value;
	window.localStorage.setItem(
		"search-searchTerm",
		JSON.stringify(searchTerm)
	);
	window.location.href = `${root}/search.html`;
}

const form = document.getElementById("search");
form.addEventListener("submit", searchMovie);
