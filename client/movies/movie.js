const rootUrl = "http://localhost";

const poster = document.getElementById("poster");
const title = document.getElementById("title");
const genres = document.getElementById("genres");
const year = document.getElementById("year");
const rating = document.getElementById("rating");
const actors = document.getElementById("actors");
const tags = document.getElementById("tags");
const breakdownByGenres = document.getElementById("breakdown-genres");

function titleCase(str) {
	str = str.toLowerCase().split(" ");
	for (var i = 0; i < str.length; i++) {
		str[i] = str[i].charAt(0).toUpperCase() + str[i].slice(1);
	}
	return str.join(" ");
}

function getDate(dateTimeStr) {
	const months = {
		Jan: "01",
		Feb: "02",
		Mar: "03",
		Apr: "04",
		May: "05",
		Jun: "06",
		Jul: "07",
		Aug: "08",
		Sep: "09",
		Oct: "10",
		Nov: "11",
		Dec: "12",
	};
	var dtSplit = dateTimeStr.split(" ");
	dtSplit = dtSplit.slice(1, 4);

	return luxon.DateTime.local(
		parseInt(dtSplit[2]),
		parseInt(months[dtSplit[1]]),
		parseInt(dtSplit[0])
	);
}
async function updateDisplay() {
	let currUrl = new URL(window.location.href);

	let url = `${rootUrl}/movies/${currUrl.searchParams.get("movieId")}`;

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
		document.title = data.details[0].title;

		console.log(data);
		const lst_actors = data.actors.map((item) => item.actor[0]);

		poster.innerHTML = `<img src="https://image.tmdb.org/t/p/w500${data.details[0].poster_url}" id="poster" onerror="javascript:this.src='images/unavailable.png'"/>`;
		title.innerHTML = `<h1>${data.details[0].title}</h1>`;
		genres.innerHTML = `<p><b>Genres: </b>${data.genres.join(", ")}</p>`;
		year.innerHTML = `<p><b>Release year: </b>${data.details[0].release_year}</p>`;

		var rating_val = parseFloat(data.details[0].avg_rating);
		rating_val = rating_val ? Math.round(rating_val * 2) / 2 : "Unknown"; //round to nearest 0.5
		rating.innerHTML = `<p><b>Average rating: </b>${rating_val}/5</p>`;

		actors.innerHTML = `<p><b>Actors: </b>${lst_actors.join(", ")}</p>`;
		tags.innerHTML = `<p><b>Most common tags: </b>${data.tags
			.map((tagItem) => titleCase(tagItem.tag))
			.join(", ")}</p>`;

		chartRatingsOverTime(data.ratings_date);
		chartRatingsPie(data.ratings_date);
	}
}

function chartRatingsPie(ratings_date) {
	ratings = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
	for (const item of ratings_date) {
		const currRating = parseInt(item.rating);
		if (currRating) {
			ratings[currRating] += 1;
		}
	}

	ratings = Object.values(ratings);
	var ctx = document.getElementById("ratings-pie").getContext("2d");
	// And for a doughnut chart

	new Chart(ctx, {
		type: "doughnut",
		data: (data = {
			datasets: [
				{
					label: "Breakdown of movie ratings",
					data: ratings,
					backgroundColor: [
						"#3e95cd",
						"#8e5ea2",
						"#3cba9f",
						"#e8c3b9",
						"#c45850",
					],
				},
			],

			// These labels appear in the legend and in the tooltips when hovering different arcs
			labels: ["1/5", "2/5", "3/5", "4/5", "5/5"],
		}),
		options: {
			responsive: true,
			maintainAspectRatio: false,
			title: {
				display: true,
				text: "Breakdown of movie ratings",
			},
			legend: {
				labels: {
					// This more specific font property overrides the global property
					fontSize: 15,
				},
			},
		},
	});
}

function chartRatingsOverTime(ratings_date) {
	var ctx = document.getElementById("ratings-over-time").getContext("2d");

	let timestamps = [];
	let ratings = [];
	for (const item of ratings_date) {
		timestamps.push(getDate(item.timestamp));
		ratings.push(item.rating);
	}

	new Chart(ctx, {
		// The type of chart we want to create
		type: "line",

		// The data for our dataset
		data: {
			labels: timestamps,
			datasets: [
				{
					label: "Ratings over time",
					backgroundColor: "rgb(255, 99, 132)",
					borderColor: "rgb(255, 99, 132)",
					data: ratings,
				},
			],
		},
		options: {
			responsive: true,
			maintainAspectRatio: false,
			scales: {
				xAxes: [
					{
						type: "time",
					},
				],
			},
		},
	});
}
updateDisplay();
