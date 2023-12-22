function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}


function handleDeleteReview(review_id) {
  // console.log('Follow/Unfollow button clicked!');
  const csrftoken = getCookie("csrftoken");

  // Make the POST request
  fetch(`/rate/delete_review/${review_id}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(
          `Server error: ${response.status} ${response.statusText}`
        );
      }
      return response.json();
    })
    .then((data) => {
      console.log("Response data:", data);

      window.location.reload();

    })
    .catch((error) => console.error("Error:", error.message));
}
