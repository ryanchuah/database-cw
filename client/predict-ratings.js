const rootUrl = "http://localhost";
const userTableBodyElement = document.getElementById("userTableBody");

const addUserElement = document.getElementById("add-user");
addUserElement.addEventListener("submit", addUser);

const predictedRatingElement = document.getElementById("predicted-rating");

if (!window.localStorage.getItem("users")) {
	window.localStorage.setItem("users", JSON.stringify([]));
}

function titleCase(str) {
	str = str.toLowerCase().split(" ");
	for (var i = 0; i < str.length; i++) {
		str[i] = str[i].charAt(0).toUpperCase() + str[i].slice(1);
	}
	return str.join(" ");
}

function isUnique(userId, users) {
	for (usr of users) {
		if (user.userId == userId) {
			return false;
		}
	}
	return true;
}

function addUser(event) {
	event.preventDefault();
	const users = JSON.parse(window.localStorage.getItem("users"));
	console.log(users);

	let isValid = true;
	const userIdInvalid = document.getElementById("user-id-invalid");
	const ratingInvalid = document.getElementById("rating-invalid");
	const tagsInvalid = document.getElementById("tags-invalid");

	const userId = event.target.elements.userId.value;
	const rating = event.target.elements.rating.value;
	var tags = event.target.elements.tags.value;
	const tagSplit = tags.split(",").map((item) => titleCase(item.trim()));

	console.log(tagSplit);
	console.log(tagSplit == true);
	if (!userId) {
		isValid = false;
		userIdInvalid.innerHTML = `<p style="color: red">Required field</p>`;
	} else if (!parseInt(userId) || userId.includes(".")) {
		isValid = false;
		userIdInvalid.innerHTML = `<p style="color: red">User ID must be an integer</p>`;
	} else if (!isUnique(userId, users)) {
		isValid = false;
		userIdInvalid.innerHTML = `<p style="color: red">User IDs must be unique</p>`;
	} else {
		userIdInvalid.innerHTML = "";
	}

	if (!rating && !tags) {
		isValid = false;
		ratingInvalid.innerHTML = `<p style="color: red">Rating and tags cannot both be empty</p>`;
		tagsInvalid.innerHTML = `<p style="color: red">Rating and tags cannot both be empty</p>`;
	} else if (!parseFloat(rating)) {
		isValid = false;
		ratingInvalid.innerHTML = `<p style="color: red">Rating must be a number</p>`;
	} else {
		ratingInvalid.innerHTML = "";
		tagsInvalid.innerHTML = "";
	}

	if (!isValid) return;
	users.push({ userId, rating, tags: tagSplit });
	window.localStorage.setItem("users", JSON.stringify(users));
	updateTable(users);
	addUserElement.reset();
}

function removeUser(userId) {
	var users = JSON.parse(window.localStorage.getItem("users"));
	users = users.filter((user) => user.userId != userId);
	window.localStorage.setItem("users", JSON.stringify(users));
	updateTable(users);
}

function clearUsers() {
	window.localStorage.setItem("users", JSON.stringify([]));
	updateTable([]);
}

function updateTable(users) {
	userTableBodyElement.innerHTML = "";
	for (user of users) {
		userTableBodyElement.innerHTML += `
        <tr>
            <td>${user.userId}</td>
            <td>${user.rating}</td>
            <td>${user.tags.join(", ")}</td>
            <td><a href="#" onclick="removeUser('${
				user.userId
			}')">&#10007;</a></td>
            </tr>`;
	}
	if (3 - users.length == 0) {
		userTableBodyElement.innerHTML += `
        <tr style="color: gray" class="placeholder">
            <td>1234</td>
            <td>4.3</td>
            <td>Funny, witty, exciting</td>
            <td><span style="color: gray;">&#10007;</span></td>
        </tr>`;
	} else {
		for (var i = 0; i < 3 - users.length; i++) {
			userTableBodyElement.innerHTML += `
            <tr style="color: gray" class="placeholder">
                <td>1234</td>
                <td>4.3</td>
                <td>Funny, witty, exciting</td>
                <td><span style="color: gray;">&#10007;</span></td>
            </tr>`;
		}
	}
}
updateTable(JSON.parse(window.localStorage.getItem("users")));

async function predictRating() {
	const users = JSON.parse(window.localStorage.getItem("users"));

	const url = `${rootUrl}/predict_rating`;
	console.log(url);

	console.log(JSON.stringify({ users }));

	const response = await fetch(url, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ users }),
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
	}
}
