# djangoRecipes


`djangoRecipes` is a recipe management platform built using Django. It provides functionality for managing user profiles, categories, and recipes. It combines Django Template Language, Django REST Framework, and JavaScript for a seamless user experience. The project includes both public and private sections with a robust permissions system.
https://djangorecipes-cuhtc6erfnargja2.italynorth-01.azurewebsites.net/

## Table of Contents
1.  [About](#about)
2.  [Technologies Used](#technologies-used)
3.  [Features](#features)
    - [Public Features](#public-features)
    - [Private Features](#private-features)
4.  [Setup Instructions](#setup-instructions)
5.  [Detailed App Functionality](#detailed-app-functionality)
    - [Accounts](#accounts)
    - [Categories](#categories)
    - [Recipes](#recipes)
    - [Photos](#photos)
    - [Common](#common)
6.  [Permissions and Groups](#permissions-and-groups)
    - [Groups](#groups)
    - [Permissions](#permissions)
7.  [Signals](#signals)
8.  [Conclusion](#conclusion)

---
## About
`djangoRecipes`allows users to:
- Register and manage profiles.
- Create, view, and manage categories and recipes.
- Interact with recipes by commenting, liking, or uploading photos.
- Search for recipes using a search form.
- Perform CRUD operations through modals with JavaScript for a dynamic user experience.

## Technologies Used

- **Backend**: Django Framework, Django REST Framework, Django ORM
- **Frontend**: Django Template Language (HTML), CSS, Javascipt for modals and UI interactions
- **Database**: PostgreSQL
- **Cloud Storage**: Cloudinary for image storage


## Features

### Public Features
- **Authentication**: User login and registration via /login/ and /register/.
- **Recipe Dashboard**: Displays approved recipes
- **Recipe Details**: View recipe information, including related comments, likes, and photos.
- **Categories**: List available categories and their associated recipes.

### Private Features
- **Profile Management**: View, edit and delete own profiles.
- **Add and Manage Recipes**: Users can create, edit, delete, and manage their recipes.
- **Photos Management**: Upload photos for profiles and recipes with Cloudinary integration.
- **Comments and Likes**: Add, edit, and delete comments; like/unlike recipes.
- **Moderation**: Staff or superusers can approve recipes, and manage categories - add, edit, delete.

## Setup Instructions 

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/DZalim/djangoRecipes.git
    cd djangoRecipes
    ```
    
2. **Set up a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/macOS
    venv\Scripts\activate     # For Windows
    ```

3. **Install Requirements**:
    ```bash
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

   4. **Create a `.env` File**:
       - In the project root, create a `.env` file with the following keys:
         ```plaintext
           DB_USER=postgres
           DB_PASSWORD=YOUR_PASSWORD
           DB_HOST=YOUR_HOST
           DB_PORT=YOUR_PORT
           DB_NAME=YOUR_DB_NAME
           SECRET_KEY=YOUR_SECRET_KEY
           CLOUD_NAME=YOUR_CLOUDINARY_CLOUD_NAME
           API_KEY=YOUR_CLOUDINARY_API_KEY
           API_SECRET=YOUR_CLOUDINARY_API_SECRET
           DEBUG=YOUR_DEBUG
           ALLOWED_HOSTS=YOUR_ALLOWED_HOSTS
           MAILJET_API_KEY=YOUR_MAILJET_API_KEY
           MAILJET_SECRET_KEY=YOUR_MAILJET_API_KEY
           EMAIL_HOST=MAILJET_EMAIL_HOST
           EMAIL_PORT=MAILJET_EMAIL_PORT
           EMAIL_USE_TLS=True
           FROM_EMAIL=YOUR_SENDER_EMAIL
           CSRF_TRUSTED_ORIGINS=https://djangorecipes-cuhtc6erfnargja2.italynorth-01.azurewebsites.net
         ```

5. **Configure Cloudinary**:
   - Register at [Cloudinary](https://cloudinary.com) to get API credentials.
   - Add your Cloudinary API credentials to the `.env` file.


6. **Set up the database and apply migrations**:
   - BE SURE YOU ARE CONNECTING TO AN EXISTING DATABASE
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
7. **Create a superuser for the admin panel**:
    ```bash
    python manage.py createsuperuser
    ```

8. **Run the development server**:
    ```bash
    python manage.py runserver
    ```
9. **Project access**:
    Access the project at `http://127.0.0.1:8000`

10. **Admin Panel**:
    Visit `/admin` and log in using the superuser credentials to manage categories, recipes, and users.


## Detailed App Functionality 

### Accounts
  - **Authentication**:
    - Login via email
    - Login via username
  - **Profile Management**:
    - View, edit, and delete own profiles.
    - Modals used for edit and delete actions.

### Categories
  - Add, edit, or delete categories (restricted to staff and superusers).
  - View categories and filter recipes by category.

### Recipes
  - Add, edit, delete recipes (owners only).
  - Approve recipes (staff and superusers only).
  - View approved recipes on the public dashboard. (staff and superusers can view all recipes)

### Photos
  - Upload and manage user profile photos.
  - Add recipe photos and browse them using a gallery.

### Common
  - **Comments**:
    - Add, edit, and delete comments.
    - Permissions restrict comment editing to the creator.
  - **Likes**:
    - Like or unlike recipes.
  - **Search Functionality**:
    - The dashboard includes a search form that allows users to filter recipes by name.


## Permissions and Groups

### Groups
  - **SimpleUserGroup**: Basic access (add recipes, photos, like/comment recipes).
  - **StaffGroup**: Moderate access (include SimpleUserGroup + manage categories and approve recipes).
  - **SuperUsersGroup**: Full access to all actions.

### Permissions
Custom view permissions include:
  - **SameUserPermissions**: Actions restricted to object owners.
  - **StaffAndSuperUserPermissions**: Access for staff and superusers.

## Signals
- Automatically create a profile when a new user registers.
- Remove photos from Cloudinary when they’re deleted from the database.

## Conclusion
1. **Dynamic UI**
   - Modals for editing and deleting objects, providing a seamless user experience.
   - JavaScript enables dynamic actions like modal interactions and photo galleries.
2. **Backend Logic**
   - Relationships between models ensure that cascading deletions occur naturally.
   - Signals ensure that external systems (e.g., Cloudinary) are updated automatically.
3. **API Integration**
   - Django REST Framework is used for creating, editing, and deleting comments and categories.
  
  

