const rootUrl = "http://localhost:5000";

const poster = document.getElementById("poster");
const title = document.getElementById("title");
const genres = document.getElementById("genres");
const year = document.getElementById("year");
const rating = document.getElementById("rating");
const actors = document.getElementById("actors");
const tags = document.getElementById("tags");

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

		console.log(data);
		const lst_actors = data.actors.map((item) => item.actor[0]);

		poster.innerHTML = `<img src=https://image.tmdb.org/t/p/w500/cxN9kwQq086L9dT3R3i2OLasEOT.jpg />`;
		title.innerHTML = `<h1>${data.details[0].title}</h1>`;
		genres.innerHTML = `<p><b>Genres: </b>${data.genres.join(", ")}</p>`;
		year.innerHTML = `<p><b>Release year: </b>${data.details[0].release_year}</p>`;
		rating.innerHTML = `<p><b>Average rating: </b>${data.details[0].avg_rating}/10</p>`;
		actors.innerHTML = `<p><b>Actors: </b>${lst_actors.join(", ")}</p>`;
		tags.innerHTML = `<p><b>Most common tags: </b>${data.tags
			.map((tagItem) => titleCase(tagItem.tag))
			.join(", ")}</p>`;

		var ctx = document.getElementById("myChart").getContext("2d");

		let timestamps = [];
		let ratings = [];
		for (const item of data.ratings_date) {
			timestamps.push(getDate(item.timestamp));
			ratings.push(item.rating);
		}
		console.log(timestamps);
		console.log(ratings);

		var chart = new Chart(ctx, {
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
}

updateDisplay();
