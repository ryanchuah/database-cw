const todo = document.getElementById("todo");

async function insertTodo() {
    const response = await fetch("http://localhost:5000");
	// const response = await fetch("http://localhost:5000");
	if (!response.ok) {
		console.error(
			"Error response from server. Error code: ",
			response.status
		);
	} else {
        
		const data = await response.json();
		let tag = document.createElement("li");
		let text = document.createTextNode(data.text);
		tag.appendChild(text);
		console.log(tag);
		todo.appendChild(tag);
	}
}

insertTodo();
