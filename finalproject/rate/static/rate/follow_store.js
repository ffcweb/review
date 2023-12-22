function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

function updateFollowerUI(data) {
  //   update the followers number
  const followers_count = document.getElementById("spanFollwerCount");
  followers_count.innerHTML = data.new_followers_count;

  const new_status = data.new_status;
  //   const store_id = data.store_id;
  const buttonFollowStore = document.getElementById(`follow_store`);

  const alert = document.getElementById("follow_alert");

  if (new_status == "Followed") {
    buttonFollowStore.innerHTML = "Unfollow";

    alert.innerHTML = `Successfully follwed ${data.store_name}`;
    alert.hidden = false;
    setTimeout(function () {
      alert.hidden = true;
    }, 5000);
  } else {
    buttonFollowStore.innerHTML = "Follow";
    alert.innerHTML = `Successfully Unfollwed ${data.store_name}`;
    alert.hidden = false;
    setTimeout(function () {
      alert.hidden = true;
    }, 5000);
  }
}

function handleToggleFollow(store_id) {
  // console.log('Follow/Unfollow button clicked!');
  const csrftoken = getCookie("csrftoken");

  // Make the POST request
  fetch(`/rate/toggle_follow/${store_id}/`, {
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
      if (typeof updateFollowerUI === "function") {
        updateFollowerUI(data);
      } else {
        console.error("Check if updateFollowerUI is defined before calling it");
      }
    })
    .catch((error) => console.error("Error:", error.message));
}
