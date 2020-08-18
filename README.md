## URL Shortener

Simple URL Shortener coded with Flask, using MongoDB for storage and Docker for deployment.

To run this example, clone the repository then run `docker-compose up`.

In order to register an URL for shortening, you must issue a JSON request to the API on `/register_path`. The following command achieves that on the default configuration:

```
curl -v --header "Content-Type: application/json"                                 \
     --request POST                                                               \
     --data '{"admin_pwd":"phase-services","path_to":"https://phase.services/"}'  \
     http://127.0.0.1/register_path                                               \
```

It is now time to visit your newly created shortened URL by visiting the path provided in the response. For example:

`URL created for https://phase.services/ at /s3hdXH`

## Phase Services

At Phase Services, we help you achieve excellence with our dedicated solutions, professionally crafted to stimulate growth and deliver success.

Check us out at https://phase.services and follow us on social media!
