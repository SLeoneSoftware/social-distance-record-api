# social-distance-record-api


## Project Description

This is an API created to check contact among users; it was paired with an android app with a location listener in the background. Anytime two users are within 6 feet, this will mark down contact. If a user tested postive, then all users they contacted within the past 2 weeks is sent an email warning them.

## Technologies

This API was created using Python3, Flask, SQLite3 and various libraries for various tasks including smtplib for sending emails.

## Use

To run:

1) Clone the Project and cd into it
2) python (or python3) main.py

Call API's as normal (using postman, for example) to use the endpoints.




