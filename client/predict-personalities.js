const rootUrl = "http://localhost";
const tagsTableBodyElement = document.getElementById("tagsTableBody");

const addTagsElement = document.getElementById("add-tags");
addTagsElement.addEventListener("submit", addTag);
const predictButtonElement = document.getElementById("predict-btn");
let personalityChart;
const predictedPersonalityElement = document.getElementById(
	"predicted-personality"
);

if (!window.localStorage.getItem("tags")) {
	window.localStorage.setItem("tags", JSON.stringify([]));
}

function uniqueId() {
	if (!window.localStorage.getItem("uid")) {
		window.localStorage.setItem("uid", JSON.stringify(0));
	}
	var uid = JSON.parse(window.localStorage.getItem("uid"));
	uid = uid + 1;
	window.localStorage.setItem("uid", JSON.stringify(uid));
	return uid;
}

function titleCase(str) {
	str = str.toLowerCase().split(" ");
	for (var i = 0; i < str.length; i++) {
		str[i] = str[i].charAt(0).toUpperCase() + str[i].slice(1);
	}
	return str.join(" ");
}

function addTag(event) {
	event.preventDefault();

	var inputtedTag = event.target.elements.tag.value;
	// const tagSplit = tags.split(",").map((item) => titleCase(item.trim()));

	const tags = JSON.parse(window.localStorage.getItem("tags"));

	tags.push({ uid: uniqueId(), tag: inputtedTag });
	window.localStorage.setItem("tags", JSON.stringify(tags));
	updateTable(tags);
	addTagsElement.reset();
}

function removeTag(tagId) {
	var tags = JSON.parse(window.localStorage.getItem("tags"));
	tags = tags.filter((t) => t.uid != tagId);
	window.localStorage.setItem("tags", JSON.stringify(tags));
	updateTable(tags);
}

function updateTable(tags) {
	if (tags.length == 0) {
		predictButtonElement.innerHTML = `
		<button
			type="button"
			class="btn btn-outline-danger btn-block mx-5"
			onclick="clearTags()"
		>
			Clear
		</button>
		<button
			type="button"
			class="btn btn-secondary btn-block mx-5"
			onclick="predictPersonality()"
			disabled
		>
			Predict Personality
		</button>`;
	} else {
		predictButtonElement.innerHTML = `
		<button
			type="button"
			class="btn btn-outline-danger btn-block mx-5"
			onclick="clearTags()"
		>
			Clear
		</button>
		<button
			type="button"
			class="btn btn-primary btn-block mx-5"
			onclick="predictPersonality()"
		>
			Predict Personality
		</button>`;
	}
	const exampleTags = ["Funny", "Witty", "Prison"];
	tagsTableBodyElement.innerHTML = "";
	for (t of tags) {
		tagsTableBodyElement.innerHTML += `
        <tr>
           
            <td>${t.tag}</td>
            <td><a href="#" onclick="removeTag('${t.uid}')">&#10007;</a></td>
            </tr>`;
	}
	if (3 - tags.length == 0) {
		tagsTableBodyElement.innerHTML += `
        <tr style="color: gray" class="placeholder">
            <td>Funny</td>
            <td><span style="color: gray;">&#10007;</span></td>
        </tr>`;
	} else {
		for (var i = 0; i < 3 - tags.length; i++) {
			tagsTableBodyElement.innerHTML += `
            <tr style="color: gray" class="placeholder">
                <td>${exampleTags[i]}</td>
                <td><span style="color: gray;">&#10007;</span></td>
            </tr>`;
		}
	}
}
updateTable(JSON.parse(window.localStorage.getItem("tags")));

function clearTags() {
	window.localStorage.setItem("tags", JSON.stringify([]));
	updateTable([]);
}

async function predictPersonality() {
	const tags = JSON.parse(window.localStorage.getItem("tags"));

	const url = `${rootUrl}/predict_personality`;
	console.log(url);
	console.log(JSON.stringify({ tags }));

	const response = await fetch(url, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ tags }),
	});

	if (!response.ok) {
		// TODO: graceful handling
		console.error(
			"Error response from server. Error code: ",
			response.status
		);
	} else {
		const data = await response.json();
		console.log(data);

		const predictedPersonality = data.personality[0];

		if (!predictedPersonality.agreeableness) {
			predictedPersonalityElement.innerHTML =
				"<p>Unfortunately, we do not have a personality analysis of the tags that you have inputted. Try using more common tags</p>";
			personalityChart.destroy();
			return;
		}

		predictedPersonalityElement.innerHTML = `
        <b>Predicted agreeableness: </b>
        ${
			Math.round(parseFloat(predictedPersonality.agreeableness) * 100) /
			100
		}<br/>
        <b>Predicted conscientiousness: </b>
        ${
			Math.round(
				parseFloat(predictedPersonality.conscientiousness) * 100
			) / 100
		}<br/>
        <b>Predicted emotional_stability: </b>
        ${
			Math.round(
				parseFloat(predictedPersonality.emotional_stability) * 100
			) / 100
		}<br/>
        <b>Predicted extraversion: </b>
        ${
			Math.round(parseFloat(predictedPersonality.extraversion) * 100) /
			100
		}<br/>
        <b>Predicted openness: </b>
        ${
			Math.round(parseFloat(predictedPersonality.openness) * 100) / 100
		}<br/>
        `;
		personalityRadar(predictedPersonality);

		// console.log("1999");
	}
}

function personalityRadar(personality) {
	var ctx = document.getElementById("personality-radar").getContext("2d");

	personalityChart = new Chart(ctx, {
		type: "radar",
		data: {
			labels: Object.keys(personality),
			datasets: [
				{
					label: "Predicted personality",
					backgroundColor: "rgba(3, 207, 252, 0.5)",
					borderColor: "rgba(3, 207, 252, 1)",
					data: Object.values(personality),
				},
			],
		},
		options: {
			legend: {
				labels: {
					// This more specific font property overrides the global property
					fontSize: 15,
				},
			},
			scale: {
				angleLines: {
					display: false,
				},
			},
		},
	});
}
