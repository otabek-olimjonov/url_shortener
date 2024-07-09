## Assignment: Implement a URL Shortening Service
### Overview
A URL shortening service provides functionality to shorten long URLs into shorter ones and redirect from the shortened URL to the original URL.
### Requirements
**1. Essential Features**
- **Create Shortened URL**
  - `POST /shorten`: Convert the received long URL into a unique short key and store it in the database.
  - Request body: `{"url": "<original_url>"}`
  - Response body: `{"short_url": "<shortened_url>"}`
  - **Algorithm Requirements**:
    - The short key must be unique and generate non-duplicate keys.
    - The key generation algorithm can be implemented freely, but security and efficiency should be considered.
  
- **Redirect to Original URL**
  - `GET /<short_key>`: Redirect to the original URL through the shortened key.
  - Response:
    - If the key exists, redirect to the original URL with a 301 status code.
    - If the key doesn't exist, return an error message with a 404 status code.
**2. Additional Requirements**
- **Database**: Use a database to store the mapping between original URLs and short keys. (Multiple databases can be used in combination)
  - Free to choose from SQLite, PostgreSQL, MongoDB, Redis, etc.
  - However, the most appropriate database(s) should be selected considering scalability, application characteristics, and ease of management, and briefly state the reasons when submitting the assignment. The DB stack must be designed considering that the number of users may increase significantly.
- **Documentation**: Generate Swagger documentation for the written API.
### Bonus Features (Additional points for implementing each feature)
**1. URL Key Expiration Feature**
- Allow specifying an expiration period when creating a key, and delete expired keys.
- `POST /shorten`: Should be able to optionally add an expiration period to the request body.
**2. Statistics Feature**
- Track the number of views for each short key and add a statistics endpoint to return this information.
- `GET /stats/<short_key>`: Return the number of views for the given key.
**3. Test Code**
- Include unit tests and integration test code.
### Development and Submission Guidelines
**1. Technology Stack**
- Implement the backend server using FastAPI
- Choose database freely from SQLite, PostgreSQL, MongoDB, etc. (However, the reason for the choice must be described in README.md)
- Free to choose and use necessary libraries for implementation
  
**2. Submission Format**
- Create a GitHub repository, upload, and submit the URL
- Write project description, installation, and execution methods in README.md
**3. Submission Deadline**
- By midnight 5 days after the assignment is given
- For example, if the assignment is given on 5/10, submit by midnight on 5/15