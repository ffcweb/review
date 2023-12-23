# Review Web Application

---

## Overview

- The Review web application is a platform that allows users to write and share reviews for stores. Users can rate stores, provide feedback, and include images, spending and links in their reviews. The application also features user authentication, user profiles, store profiles, and various functionalities to enhance the user experience.

## Distinctiveness and Complexity

- Enhanced Navigation Bar with User Profile Image
  In the Review web application, the navigation bar has been enhanced to provide a personalized experience for users who are logged in. The modification includes the display of the user's profile image at the top of the website, contributing to a more user-friendly and visually appealing interface.

- Changes Made
  Profile Image Integration:

- Purpose: Enhance user recognition and personalization by displaying the user's profile image in the navigation bar.
  ... Implementation:
  ... A dedicated list item (<li>) has been added to the navigation bar specifically for the user's profile image.
  ... The {% if user.is_authenticated %} condition ensures that the profile image is displayed only when the user is logged in.
  ... The user's profile image is retrieved from the user.image_url attribute, providing a visual representation of the user.

### Styling Enhancement:

... Purpose: Ensure a visually appealing presentation of the profile image.

1.  Implementation:

- The profile image is styled with a border-radius property to create a circular appearance.
  Adjustments to the width and height attributes can be made to achieve the desired dimensions.
  User Experience
  Logged-In Users:

- When a user is authenticated and logged in, their profile image is prominently displayed at the top of the website, offering a personalized touch to the navigation bar.

- The inclusion of the profile image is intended to make users feel recognized and connected to the application.

2. Consistent Design:

- The integration of the user's profile image aligns with the overall design principles of the application, ensuring a consistent and cohesive user experience.

... This enhancement contributes to a more engaging and personalized user interface, making the Review web application stand out in terms of user experience and design considerations.

3.  Why it's Distinctive

- The Review web application stands out due to its comprehensive features and user-centric design. Here are some distinctive aspects:

- Rich Reviews: Users can write detailed reviews that include images, spending details, and star ratings. This provides a comprehensive overview of their experience with a particular store.

- User Profiles: The application includes user profiles, allowing users to see their own reviews and track their activity on the platform.

- Store Profiles: Each store has its own profile, aggregating reviews and displaying important information such as average ratings and the number of reviews.

- Follow System: Users can follow stores and other users, creating a social aspect to the platform. The follower count is displayed on store profiles.

- Like System: Users can like reviews, contributing to a review's popularity. The number of likes is visible on each review.

- Search Functionality: The application includes a search feature that allows users to find stores based on their names.

- Sorting Stores: Users can sort stores based on criteria such as ratings, reviews, and joining date, providing flexibility in exploring stores.

### Complexity

- The complexity of the application is evident in the following areas:

- Pagination: The use of pagination for reviews and stores enhances performance and user experience, especially as the dataset grows.

- User Authentication: The application features user registration, login, and logout functionalities, ensuring a secure and personalized experience for users.

- Database Relationships: The use of Django models establishes relationships between users, stores, reviews, likes, and followers, creating a well-organized and relational database structure.

- AJAX Requests: The application employs AJAX requests for functionalities such as liking reviews, following stores, updating user images, and deleting reviews. This contributes to a seamless and dynamic user interface.

- Django Class-Based Views: The adoption of class-based views in Django enhances code organization and readability, making it easier to manage and extend the application.

## File Contents

1. Models.py
   ... Purpose: Handles user authentication, including login, logout, and registration.

2. views.py:
   ... This file contains the views for handling different functionalities, including rendering pages, user authentication, store and user profiles, creating and deleting reviews, and more.

3. admin.py

- The admin.py file in the Review web application is responsible for registering the application's models with the Django admin interface. This allows administrators to manage and manipulate data directly from the admin panel. Here's an overview of the purpose of each registration:

- Project admin.py Description
  ... Category
  ... Purpose: Manage and view categories in the admin panel.

- Store
  ... Purpose: Administer store-related data in the admin panel.

- Review
  ... Purpose: Oversee user reviews through the admin panel.

- LikeReview
  ... Purpose: Manage data related to likes on reviews.

- StoreFollowers
  ... Purpose: Manage data related to store followers.

- By registering these models in the admin.py file, the Review web application ensures that administrators can easily access and manipulate data relevant to categories, stores, reviews, likes, comments, store followers, and favorite stores through the Django admin interface. This contributes to efficient data management and system administration.

4. javaScript files

   - user_profile.js
   - like_review.js
   - follow_store.js
   - display_stars.js
   - delete_review.js

5. The urls.py file and Templates in the Review web application serves as a mapping between URL patterns and their corresponding views. Here's a comprehensive breakdown of the purpose of each URL pattern and the Templates:

- Home Page
- index.html
- Purpose: Maps to the home page of the application, displaying a list of reviews.
- View: index in views.py.

- Create Review
  ... create_review.html
  ... Purpose: Provides a page for users to create new reviews for stores.
  ... View: create_review in views.py.

. User Profile
... user_profile.html
⋅⋅⋅ Purpose: Displays the profile of a specific user, including their reviews and information.
⋅⋅⋅ View: user_profile in views.py.

... Update User Image
... Purpose: Handles the AJAX request to update the user's profile image.
... View: update_user_image in views.py.

. Store Profile and Reviews
... store_profile.html
... all_review.html
⋅⋅⋅ Purpose: Shows the profile of a specific store and lists all reviews.
⋅⋅⋅ Views: store_profile and all_reviews in views.py.

. Store List and Sorting
... store_list.html
⋅⋅⋅ Purpose: Displays a list of stores and provides sorting options based on date, ratings, or reviews.
⋅⋅⋅ View: store_list in views.py.

. User Authentication
... layout.html
... login.html
... register.html
... Purpose: Handles user authentication, including login, logout, and registration.
... Views: login_view, logout_view, and register in views.py.

. Store Search
... search_results.html
⋅⋅⋅ Purpose: Allows users to search for stores based on their names.
⋅⋅⋅ View: search_store in views.py.

. Categories
... category_list.html
⋅⋅⋅ Purpose: Provides functionality to view a list of categories and details of a specific category.
⋅⋅⋅ Views: category_list and category_detail in views.py.

. Toggle Follow and Like
... Purpose: Handles AJAX requests to toggle follow status for stores and toggle like status for reviews.
... Views: toggle_follow_store and toggle_like in views.py.

. Delete Review
... Purpose: Handles AJAX requests to delete a user's own review.
... View: delete_review in views.py.

6. Project urls.py Description

- Admin Interface
  ... Purpose: Directs to the Django admin interface.
  ... Usage: Enables administrators to manage the application's data and configurations.

- Rate App URLs
  ... Purpose: Includes URLs from the rate app.
  ... Usage: Defines the URL patterns specific to the functionalities of the rate app.

- These URL patterns serve as the main navigation routes for the Review web application, allowing users and administrators to access different sections of the application, including the admin panel for system management and the rate app for user interactions and reviews.

## How to run the web application

- To run a Django web application, you typically follow these steps. Please ensure you have Python and Django installed on your system:

1. Install Python:

- Make sure you have Python installed. You can download it from the official Python website.

2. Install Django:

- Open a terminal or command prompt and run the following command to install Django using pip:

`pip install Django`

3. To run a Django web application, you typically follow these steps. Please ensure you have Python and Django installed on your system:

4. Install Python:

- Make sure you have Python installed. You can download it from the official Python website.

5. Install Django:

- Open a terminal or command prompt and run the following command to install Django using pip:

6. Copy code
   `pip install Django`

7. Clone the Project:

- Clone the project repository or download the source code from where it is hosted (e.g., GitHub).

8. Navigate to Project Directory:

- Open a terminal or command prompt, navigate to the project directory using the cd command:
  `cd path/to/your/project`

8. Apply Migrations:

- Run the following commands to apply database migrations:

10. Copy code

```
python manage.py makemigrations
python manage.py migrate
```

11. Create a Superuser (Admin):

- Create a superuser account to access the Django admin interface:

`python manage.py createsuperuser`

12. Run the Development Server:

- Start the development server using the following command:

`python manage.py runserver`

### Access the Application:

Open a web browser and go to http://127.0.0.1:8000/ to view your application. For the admin interface, go to http://127.0.0.1:8000/admin/ and log in with the superuser credentials.

### Explore the Application:

Explore the different URLs and functionalities defined in your urls.py and interact with the application.

- Keep in mind that the steps may vary slightly depending on your project's structure and configuration. Ensure that your Django version matches the version used in the project, and adjust commands accordingly.
