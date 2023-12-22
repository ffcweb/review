function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

function updateProfileImage() {
  var newImageUrl = document.getElementById("id_new_image_url").value;

  if (!newImageUrl) {
    alert("Please enter a valid image URL.");
    return;
  }

  fetch("/rate/update_user_image/", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-CSRFToken": getCookie("csrftoken"), // Make sure csrf_token is defined
    },
    body: "newImageUrl=" + encodeURIComponent(newImageUrl),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        alert(data.message);
        window.location.reload();
      } else {
        alert(data.message);
      }
    })
    .catch((error) => {
      console.error("Error updating profile image:", error);
      alert(
        "An error occurred while updating the profile image. Please try again."
      );
    })
    .finally(() => {
    });
}


