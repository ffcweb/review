// // Define the updateFollowUI function
function updateFollowStoreUI(data) {
    // updated followers count.
    const followersCountElement = document.getElementById('followersCount');
    if (followersCountElement) {
        followersCountElement.textContent = `Followers: ${data.followers_count} | Following: ${data.following_count}`;
        console.log('Updating followers count:', data.followers_count);
    }
    // updated follow /unfollow button.
    const followButton = document.getElementById('followButton');
    const unfollowButton = document.getElementById('unfollowButton');
    if (followButton && unfollowButton) {
        followButton.style.display = data.is_following ? 'none' : 'inline-block';
        unfollowButton.style.display = data.is_following ? 'inline-block' : 'none';
    }
    console.log('Data received:', data);
}



function handleToggleFollowStore(username) {
    console.log('Follow/Unfollow button clicked!');
    const csrftoken = getCookie('csrftoken');
    const encodedUsername = encodeURIComponent(username);

    // Make the POST request
    fetch(`/toggle_follow_store/${encodedUsername}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server error: ${response.status} ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);

        // Check if updateFollowUI is defined before calling it.
        if (typeof updateFollowUI === 'function') {
            updateFollowUI(data);
        } else {
            console.error('Check if updateFollowUI is defined before calling it');
        }
    })
    .catch(error => console.error('Error:', error.message));
}