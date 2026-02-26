function openModal(id) {
	document.getElementById(id).style.display = "flex";
}

function closeModal(id) {
	document.getElementById(id).style.display = "none";
}

function openEditModal(id, name, emoji) {
	document.getElementById("editMoodForm").action = "/edit_mood/" + id;
	document.getElementById("edit_mood_name").value = name;
	document.getElementById("edit_mood_emoji").value = emoji;
	openModal("editMoodModal");
}
