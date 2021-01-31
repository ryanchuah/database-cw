const color = document.getElementById("color");

async function insertColor() {
    const response = await fetch("http://localhost:5000/");
	if (!response.ok) {
		console.error(
			"Error response from server. Error code: ",
			response.status
		);
	} else {
		const data = await response.json();

		const fav_colors = data.favorite_colors;
		
		// fav_colors is an array of objects:
		console.log(fav_colors); // [{Zahra: "blue"}, {Chak: "yellow"}]
		
		let tag;
		let text;
		
		for(color_obj of fav_colors){ // iterate through array
			console.log(color_obj); // {Zahra: "blue"}
			// iterate through object
			for(const user in color_obj){
				console.log(user); // Zahra
				
				tag = document.createElement("li");
				
				text = document.createTextNode(`${user} likes ${color_obj[user]}`);
				tag.appendChild(text);
				
				color.appendChild(tag);
			}
		}
	}
}

insertColor();
