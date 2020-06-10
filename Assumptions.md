# General assumptions and comments

[README](README.md)

----

Those are my general assumptions and comments regarding my implementation of this project:

* I decided to create three django apps for organizing the API: accounts, companies and reviews. I thought for the project description this separation would make sense.

* This API does not allow update or delete operations because it was not formally required on the Acceptance Criteria of this project. For the same reason those operations are not covered in the tests of this project. Because of this I disallowed `PUT`, `PATCH` and `DELETE` methods in all endpoints.

* I decided to use urls in the API objects because it improves navigation over the API and I think this is helpful for developers that might use this API.

* I decided to use `username` as the lookup for `users` endpoint as this field uses database unique constraint and adds "human touch" to the API. I took care to validate the username for being safe used as a url path. It would be even better to use a [custom User model](https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#substituting-a-custom-user-model) with [custom username validator](https://docs.djangoproject.com/en/3.0/ref/contrib/auth/#validators) but I only realised this when I was reviewing the project and decided to do not change it and keep the delivery in time.

* I decided to keep users reviews inside the `users` endpoint as it makes sense that the review data belongs to its user owner. Others endpoints would alse list reviews like the company's endpoint, a search or a review endpoint.

* I decided to use a plain markdown file for the API DOCS for simplicity as I had already many API calls that I could use as an example. But for a more professionally API Docs I may choose a tool like the [dynamic OpenAPI Schema](https://www.django-rest-framework.org/api-guide/schemas/#generating-a-dynamic-schema-with-schemaview) with [ReDoc or Swagger UI](https://www.django-rest-framework.org/topics/documenting-your-api/#generating-documentation-from-openapi-schemas) that can generate the API dynamically using the API schema and python docstrings.

* I never worked with Django REST Framework professionally.
