# API DOCS

[README](README.md)

----

This API works over HTTP REST architecture with data encoded in JSON format. Some endpoints are public and others need Authentication.

----

## Authentication

Some endpoints require authenticated access. This API uses Token Authentication for those endpoints. For making authenticated request just add a `Authorization` header in your requests according with the following pattern:

`Authorization: Token {api_token}`

The `api_token` is returned just after you create a new user account. You should be able to keep this token safe as a password. You will need this token for every authenticated request.

----

## API requests

Any user (anonymous included) can list or retrieve companies and list or create users. Only authenticated users can list, read or create their own reviews (not other users reviews). Only admins can create companies. Admins can read everything.

----

## Listing and retrieving companies

#### Listing companies

`GET /api/companies/`

For list companies just make an HTTP GET request to the companies endpoint:

```console
$ curl -X GET http://127.0.0.1:8000/api/companies/
```
```json
[
  {
    "id": 4,
    "name": "Amazon",
    "url": "http://127.0.0.1:8000/api/companies/4/"
  },
  {
    "id": 1,
    "name": "Apple",
    "url": "http://127.0.0.1:8000/api/companies/1/"
  }
]
```

#### Retrieve a company

`GET /api/companies/{id}/`

For retrieving a company object, do a GET request to it's endpoint. Each company has an `id` field which should be passed on request. In the following example the `id` is `1`:

```console
$ curl -X GET http://127.0.0.1:8000/api/companies/1/
```
```json
{
  "id": 1,
  "name": "Apple",
  "url": "http://127.0.0.1:8000/api/companies/1/"
}
```

----

## Listing, creating and retrieving users

#### Listing users

`GET /api/users/`

For list users just make an HTTP GET request to the user endpoint:

```console
$ curl -X GET http://127.0.0.1:8000/api/users/
```
```json
[
  {
    "username": "superuser",
    "url": "http://127.0.0.1:8000/api/users/superuser/",
    "reviews_url": "http://127.0.0.1:8000/api/users/superuser/reviews/"
  },
  {
    "username": "mary",
    "url": "http://127.0.0.1:8000/api/users/mary/",
    "reviews_url": "http://127.0.0.1:8000/api/users/mary/reviews/"
  }
]
```

#### Creating a new user

`POST /api/users/`

For creating a new user you will need to send a `JSON` payload with the user's `username` like the example below:

```console
$ curl -X POST http://127.0.0.1:8000/api/users/ \
-H 'Content-Type: application/json' \
-d '{"username": "john"}'
```
```json
{
  "username": "john",
  "api_token": "549b46f99c4cfec5e0e9cbfa073c0ce10f98f8bb",
  "url": "http://localhost:8000/api/users/john/",
  "reviews_url": "http://localhost:8000/api/users/john/reviews/"
}
```

#### Retrieve an existent user

`GET /api/users/{username}/`

For retrieve an user just make an HTTP GET request to the user's endpoint:

```console
$ curl -X GET http://127.0.0.1:8000/api/users/john/ \
-H 'Authorization: Token 549b46f99c4cfec5e0e9cbfa073c0ce10f98f8bb'
```
```json
{
  "username": "john",
  "api_token": "549b46f99c4cfec5e0e9cbfa073c0ce10f98f8bb",
  "url": "http://localhost:8000/api/users/john/",
  "reviews_url": "http://localhost:8000/api/users/john/reviews/"
}
```

----

## Listing, creating and retrieving reviews

#### Listing user reviews

`GET /api/users/{username}/reviews/`

For list reviews just make an HTTP GET request to the user's review endpoint:

```console
$ curl -X GET http://127.0.0.1:8000/api/users/mary/reviews/ \
-H 'Authorization: Token 511704bf6e41e0d2f60d4e66d274396a35fb4934'
```
```json
[
    {
        "id": 8,
        "reviewer": {
            "username": "mary",
            "url": "http://localhost:8000/api/users/mary/",
            "reviews_url": "http://localhost:8000/api/users/mary/reviews/"
        },
        "company": {
            "id": 2,
            "name": "Microsoft",
            "url": "http://localhost:8000/api/companies/2/"
        },
        "title": "Sed vestibulum dolor dolor, vitae.",
        "summary": "Donec sodales nibh ipsum, nec mollis at...",
        "rating": 3,
        "ipv4": "127.0.0.1",
        "created": "2020-06-09T14:06:27.286000Z",
        "url": "http://localhost:8000/api/users/mary/reviews/8/"
    },
    {
        "id": 5,
        "reviewer": {
            "username": "mary",
            "url": "http://localhost:8000/api/users/mary/",
            "reviews_url": "http://localhost:8000/api/users/mary/reviews/"
        },
        "company": {
            "id": 4,
            "name": "Amazon",
            "url": "http://localhost:8000/api/companies/4/"
        },
        "title": "Mauris porttitor mi quis nisl.",
        "summary": "Sed sed nunc mi. Etiam a arcu lobortis, ...",
        "rating": 2,
        "ipv4": "127.0.0.1",
        "created": "2020-06-09T14:02:55.251000Z",
        "url": "http://localhost:8000/api/users/mary/reviews/5/"
    },
]
```

#### Creating user reviews

`POST /api/users/{username}/reviews/`

For creating a user's review you will need to send a `JSON` payload with the the following fields: `company_id`, `title`, `summary` and `rating` as shown below:

```console
$ curl -X POST http://127.0.0.1:8000/api/users/mary/reviews/ \
-H 'Content-Type: application/json' \
-H 'Authorization: Token 511704bf6e41e0d2f60d4e66d274396a35fb4934' \
-d '{"company_id": 1, "title": "Morbi eget urna at diam", "summary": "Mauris in viverra sapien. Morbi a ...", "rating": 4}'
```
```json
{
  "id": 12,
  "reviewer": {
    "username": "mary",
    "url": "http://localhost:8000/api/users/mary/",
    "reviews_url": "http://localhost:8000/api/users/mary/reviews/"
  },
  "company": {
    "id": 1,
    "name": "Apple",
    "url": "http://localhost:8000/api/companies/1/"
  },
  "title": "Morbi eget urna at diam",
  "summary": "Mauris in viverra sapien. Morbi a ...",
  "rating": 4,
  "ipv4": "127.0.0.1",
  "created": "2020-06-10T13:00:17.766741Z",
  "url": "http://localhost:8000/api/users/mary/reviews/12/"
}
```

#### Retrieving user reviews

`GET /api/users/{username}/reviews/{id}`

For retrieve an user's review just make an HTTP GET request to the user's review endpoint:

```console
$ curl -X GET http://127.0.0.1:8000/api/users/mary/reviews/12/ \
-H 'Authorization: Token 511704bf6e41e0d2f60d4e66d274396a35fb4934'
```
```json
{
  "id": 12,
  "reviewer": {
    "username": "mary",
    "url": "http://localhost:8000/api/users/mary/",
    "reviews_url": "http://localhost:8000/api/users/mary/reviews/"
  },
  "company": {
    "id": 1,
    "name": "Apple",
    "url": "http://localhost:8000/api/companies/1/"
  },
  "title": "Morbi eget urna at diam",
  "summary": "Mauris in viverra sapien. Morbi a ...",
  "rating": 4,
  "ipv4": "127.0.0.1",
  "created": "2020-06-10T13:00:17.766741Z",
  "url": "http://localhost:8000/api/users/mary/reviews/12/"
}
```
