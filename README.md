# store-backend-Django
This is an implementation of the back-end of an online store using Django and Django REST Framework.
All store endpoints are represented in the API root (localhost:8000/store/ if you’re using 8000 port).
In the products endpoint, all products are listed with their details. Each product can be accessed by entering its ID after the products endpoint.
This is true for other endpoints as well.

To access the review of each product, you can use the nested address “reviews” (e.g., http://localhost:8000/store/products/1/reviews/). You can also access a particular review by entering its ID after the reviews endpoint.

For security reasons, each endpoint only represents data related to the logged-in user (unless you logged in as an admin user) using permissions.

this back-end uses JWT (jason web token) for user authentication.

Users endpoint is represented in auth root (http://localhost:8000/auth/).
If you log in as an admin user, you can access the list of users through this endpoint.

Admin pannel is available to control data. 
