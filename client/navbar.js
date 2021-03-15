const navbar = document.getElementById("navbar");
navbar.innerHTML = `
<nav class="navbar navbar-expand-lg navbar-light bg-light">
	<a class="navbar-brand" href="index.html">Home</a>
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
            <!--<li class="nav-item active">
				<a class="nav-link" href="index.html"
					>Movies <span class="sr-only">(current)</span></a
				>
			</li> 

			<li class="nav-item dropdown">
				<a
					class="nav-link dropdown-toggle"
					href="#"
					id="navbarDropdown"
					role="button"
					data-toggle="dropdown"
					aria-haspopup="true"
					aria-expanded="false"
				>
					Genres
				</a>
				<div
					class="dropdown-menu dropdown-multicol"
					aria-labelledby="dropdownMenuButton"
				>
					<div class="dropdown-row">
						<a class="dropdown-item" href="#">Action</a
						><a class="dropdown-item" href="#">Adventure</a>
					</div>
					<div class="dropdown-row">
						<a class="dropdown-item" href="#">Animation</a
						><a class="dropdown-item" href="#">Children</a>
					</div>
					<div class="dropdown-row">
						<a class="dropdown-item" href="#">Comedy</a
						><a class="dropdown-item" href="#">Crime</a>
					</div>
					<div class="dropdown-row">
						<a class="dropdown-item" href="#">Documentary</a
						><a class="dropdown-item" href="#">Drama</a>
					</div>
					<div class="dropdown-row">
						<a class="dropdown-item" href="#">Fantasy</a
						><a class="dropdown-item" href="#">Film-Noir</a>
					</div>
					<div class="dropdown-row">
						<a class="dropdown-item" href="#">Horror</a
						><a class="dropdown-item" href="#">IMAX</a>
					</div>
					<div class="dropdown-row">
						<a class="dropdown-item" href="#">Musical</a
						><a class="dropdown-item" href="#">Mystery</a>
					</div>
					<div class="dropdown-row">
						<a class="dropdown-item" href="#">Romance</a
						><a class="dropdown-item" href="#">Sci-Fi</a>
					</div>
					<div class="dropdown-row">
						<a class="dropdown-item" href="#">Thriller</a
						><a class="dropdown-item" href="#">War</a>
					</div>
					<div class="dropdown-row">
						<a class="dropdown-item" href="#">Western</a>
					</div>
				</div>
			</li> -->   
            <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                Predict
                </a>
                <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                    <a class="dropdown-item" href="predict-ratings.html">Ratings</a>
                    <a class="dropdown-item" href="predict-personality.html">Personality Traits</a>
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
	window.location.href = "search.html";
}
async function searchMovie(event) {
	event.preventDefault();
	const searchTerm = event.target.elements.search.value;
	window.localStorage.setItem(
		"search-searchTerm",
		JSON.stringify(searchTerm)
	);
	window.location.href = "search.html";
}

const form = document.getElementById("search");
form.addEventListener("submit", searchMovie);
