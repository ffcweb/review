document.addEventListener("DOMContentLoaded", function () {
  // Define the updateProfileImage function
  function updateProfileImage() {
    // Include the CSRF token in the request body
    var formData = new FormData(document.getElementById("updateProfileForm"));
    formData.append("csrfmiddlewaretoken", csrf_token);

    var newImageUrl = document.getElementById("id_new_image_url").value;

    if (!newImageUrl) {
      alert("Please enter a valid image URL.");
      return;
    }

    // Show loading spinner
    document.getElementById("loadingSpinner").style.display = "block";

    fetch(window.location.pathname, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": csrf_token, // Make sure csrf_token is defined
      },
      body: "new_image_url=" + encodeURIComponent(newImageUrl),
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
        // Hide loading spinner after processing
        document.getElementById("loadingSpinner").style.display = "none";
      });
  }

  // Make the function accessible globally
  window.updateProfileImage = updateProfileImage;
});
