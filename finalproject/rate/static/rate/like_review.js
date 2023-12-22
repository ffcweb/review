function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

function updateLikeUI(data) {
  const new_like_count = data.new_like_count;
  const review_id = data.review_id;
  const spanReviewLikeCount = document.getElementById(
    `review_${review_id}_like_count`
  );
  spanReviewLikeCount.innerHTML = new_like_count;
}

function handleToggleLike(review_id) {
  // console.log('Follow/Unfollow button clicked!');
  const csrftoken = getCookie("csrftoken");

  // Make the POST request
  fetch(`/rate/toggle_like/${review_id}/`, {
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

      // Check if updateFollowUI is defined before calling it.
      if (typeof updateLikeUI === "function") {
        updateLikeUI(data);
      } else {
        console.error("Check if updateLikeUI is defined before calling it");
      }
    })
    .catch((error) => console.error("Error:", error.message));
}
