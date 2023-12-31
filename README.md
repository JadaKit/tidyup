# Tidy Up

## Tech

- Django
- HTML
- CSS
- Boostrap
- Boostrap Icons
- Javascript
- Jinja2
- django forms

## Initialization

To get started with this project, follow these steps:

If you don't have `virtualenv` installed, you can install it by following the instructions [here](https://medium.com/datacat/a-simple-guide-to-creating-a-virtual-environment-in-python-for-windows-and-mac-1079f40be518).

Create a virtual environment
```bash
virtualenv venv
```
Change Directory to the project folder where `manage.py` file exisits
```bash
cd tidy-up
```

Install all the dependencies
```bash
pip install -r requirements.txt
```

Run command to start development server
```bash
python manage.py runserver
```

admin users
```bash
username: admin
password: 12345
```

Here are available users on local db
```bash
room 1 pass: wA3Np7EW32wCDNIffgonR1VhN5Y9MW
user1room1
user2room1
user3roomwaiting1

Kingsmen786

```

```bash
room 2 pass: ukhFJSKiPo0bgUgXEMz7RLh2AGscbT
user1room2
user2room2
user3roomwaiting2

password: Kingsmen786
```

## Features

### Signup
- User sign up, if `Room pass` is provided, user atomatically added to room
- User can only see tasks and other room related stuff, if someone from the same room approves the entry
- Roomates can approve someone's entry to room


Here are the main fields in the database used by this project:

| Field Name | Description                              | Required |
|------------|------------------------------------------|----------|
| first name | User's first name   | No      |
| last name       | User's last name       | No      |
| username       | User's username       | Yes      |
| password       | User's password       | Yes      |
| Room Pass       | Room pass will only be evaluated if value provided, if it is not valid room pass, user will recieve validation error on UI. If it is empty, new room `untitled` will be created for the user| No      |
> Make sure to leave empty if you don't have valid room pass

> `username should not exist in database

> Password must be at least 8 characters long and contain at least one capital letter and one number.

> If `Room Pass` is not provided, a new room will be created with `approved entry`

> Users with existing room will require approval from people already living there, with `approved entry`


### Login

| Field Name | Description                              | Required |
|------------|------------------------------------------|----------|
| username       | User's username       | Yes      |
| password       | User's password       | Yes      |

## Room
You can click `+ Task` to create a new task, give a title and some description, add due date, assign to someone in room, you will be the reporter.
Room mates can create tasks and the tasks can only be assigned to roommates only.
Everybody can change anything on tasks.

Room page has 3 main sections

- Tasks
- Roomates
- People - Requsted Entry

### Room Tasks
All the tasks related to room will be there. Clicking on task can show full page of that task and roommates can update task details, like title, description etc.

### Roomates
You can see all the roommates with `approved entry`

### People - Requsted Entry
If you are approved roomate, you can approve other people as well, if someone has requested entry.

## Tasks Page
The page were you can see room tasks for which you are either a `reporter` or task is `assigned_to` you.
