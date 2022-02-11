
# bookorganizer
 
Web application to store your books collection online. Uses Flask and Bootstrap.  

## Technologies:

- Flask (Extensions: Login, Mail, Migrate, Moment)
- SQLAlchemy
- WTForms
- Faker
- Bootstrap

## Features

### Account features

- The user can register an account in the app using an email (must confirm the email)
- The user can log in to the account (or remind the password)
- The user can change the email and password

![2022-02-10 16 42 53 127 0 0 1 6bd08e917038](https://user-images.githubusercontent.com/34821903/153577608-d197cefd-6842-49f8-95d3-a812e1f29c54.png "Register page")

![2022-02-10 16 43 14 127 0 0 1 3ce4fede8a40](https://user-images.githubusercontent.com/34821903/153577703-bb0ca3f5-2653-4c33-91b3-7fcb42210fe0.png "Login page")

![2022-02-10 16 43 39 127 0 0 1 6b6e577db7a1](https://user-images.githubusercontent.com/34821903/153577753-37693d21-d937-4a73-8ed7-a93047000512.png "Unconfirmed User page")

![2022-02-10 15 58 27 outlook live com 650a27fde044](https://user-images.githubusercontent.com/34821903/153577914-79bb87d4-9918-4c86-a834-4b8302602898.png "Confirmation email")

### Profile features

- All users have their own profiles
- The user can add new information to his profile (name, location, description)
- The user can view the profiles of other users and their books
- The administrator user has access to additional information about other users and the ability to change the permissions of the selected user

![2022-02-10 15 52 35 127 0 0 1 392d205dca20](https://user-images.githubusercontent.com/34821903/153580809-1eac951a-31e6-4bac-90e4-d9cd004acb2a.png "Profile page (Logged in user)")

![2022-02-10 15 55 40 127 0 0 1 f71adad55c09](https://user-images.githubusercontent.com/34821903/153580961-5f4d6878-ec8e-42e7-83e8-12a76234ca7e.png "Profile page (other user)")

![2022-02-10 15 59 07 127 0 0 1 cc586a9fbfe4](https://user-images.githubusercontent.com/34821903/153581255-3eb639d3-7421-4f85-abc4-9d194f2c93cb.png "Profile page (administrator user)")

### Books features

- The user can add new books
- The user can edit existing books (title, author, description, book file, cover file)
- The user can delete existing books

![2022-02-10 15 53 41 127 0 0 1 8a79a23fca85](https://user-images.githubusercontent.com/34821903/153581589-9ffb0b76-450d-442e-aac7-d914a1f4c89e.png "Add Book page")

![2022-02-10 15 54 16 127 0 0 1 3efa51ea3258](https://user-images.githubusercontent.com/34821903/153581694-d72ae439-0248-42d5-9678-154d3e357fee.png "Edit Book page")

![2022-02-10 15 54 29 127 0 0 1 13c05ff092d6](https://user-images.githubusercontent.com/34821903/153581765-a358f7a3-47e4-47c7-8928-23a6d81a433a.png "Book page")

### Other features

- Mobile version
- Theme switcher

![2022-02-10 16 01 34 127 0 0 1 fd906767b575](https://user-images.githubusercontent.com/34821903/153582295-453c50e8-56df-44d4-8b46-8d6cb4e162c8.png "Mobile version of Profile page")

![2022-02-10 16 37 14 127 0 0 1 86fb5d34574b](https://user-images.githubusercontent.com/34821903/153582707-d432c1fb-9837-4cb0-a75b-4582b056fa9a.png "Mobile version of Profile page (light theme)")

## Installation

Bookorganizer requires Python v3.7+ to run.  
Installation tested on Windows PowerShell.  

### 1. Create and activate virtual environment. Install the requirements

```
PS (path-to-repo)> py -m venv venv
PS (path-to-repo)> .\venv\Scripts\activate
(venv) PS (path-to-repo)> py -m pip install -r requirements.txt
```


### 2. Set environment  variables

```
(venv) PS (path-to-repo)> $env:FLASK_APP='bookorganizer.py'
(venv) PS (path-to-repo)> $env:BOOKORGANIZER_ADMIN=(admin-user-email) # Optional. Needed to create an administrator user
(venv) PS (path-to-repo)> $env:MAIL_USERNAME=(google-email-address) # Optional. Needed for sending confirmation emails
(venv) PS (path-to-repo)> $env:MAIL_PASSWORD=(google-email-password) # Optional. Needed for sending confirmation emails
```

### 3. Create a database and fill it with test data

```
(venv) PS (path-to-repo)> flask db upgrade
(venv) PS (path-to-repo)> flask shell
>>> Role.insert_roles()
>>> from app import fake # Optional. Import fake module
>>> fake.users(count=20) # Optional. Create test users using fake module
>>> fake.books(count=400) # Optional. Create test books using fake module
```

### 4. Start the app

```
(venv) PS (path-to-repo)> flask run
```

## Tests

```
(venv) PS (path-to-repo)> flask test # Run all tests
(venv) PS (path-to-repo)> flask test tests.test_basics # Run one test file
```

## ToDo

- Add book categories
- Improve the book finder
- Improve the look of app
- Extend the administrator user experience
- And more...
