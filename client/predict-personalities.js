const rootUrl = "http://localhost";
const tagsTableBodyElement = document.getElementById("tagsTableBody");

const addTagsElement = document.getElementById("add-tags");
addTagsElement.addEventListener("submit", addTag);

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
            <td>Funny, witty, exciting</td>
            <td><span style="color: gray;">&#10007;</span></td>
        </tr>`;
	} else {
		for (var i = 0; i < 3 - tags.length; i++) {
			tagsTableBodyElement.innerHTML += `
            <tr style="color: gray" class="placeholder">
                <td>Funny, witty, exciting</td>
                <td><span style="color: gray;">&#10007;</span></td>
            </tr>`;
		}
	}
}
updateTable(JSON.parse(window.localStorage.getItem("tags")));

async function predictRating() {
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
		const predictedRating = data.predicted_rating;
		console.log(predictedRating);
		predictedRatingElement.innerHTML = `
        <b>Predicted rating:</b>
        ${Math.round(predictedRating * 100) / 100}/5`;

		// console.log("1999");
	}
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
		console.log(predictedPersonality);
		console.log(predictedPersonality.agreeableness);
		predictedPersonalityElement.innerHTML = `
        <b>Predicted agreeableness: </b>
        ${predictedPersonality.agreeableness}<br/>
        <b>Predicted conscientiousness: </b>
        ${predictedPersonality.conscientiousness}<br/>
        <b>Predicted emotional_stability: </b>
        ${predictedPersonality.emotional_stability}<br/>
        <b>Predicted extraversion: </b>
        ${predictedPersonality.extraversion}<br/>
        <b>Predicted openness: </b>
        ${predictedPersonality.openness}<br/>
        `;

		// console.log("1999");
	}
}
