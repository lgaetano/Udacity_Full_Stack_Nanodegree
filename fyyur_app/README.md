Fyyur
-----

## Overview

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.                                       

## Tech Stack (Dependencies)
You can download and install all dependencies mentioned above using:
```
python -m pip install -r requirements.txt
```

### 1. Backend Dependencies
Our tech stack will include the following:
 * **virtualenv** for isolated Python environment
 * **SQLAlchemy ORM** for ORM library
 * **PostgreSQL** for database
 * **Python3** and **Flask** for server language and server framework
 * **Flask-Migrate** for creating and running schema migrations

### 2. Frontend Dependencies
You must have the **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend. Bootstrap can only be installed by Node Package Manager (NPM). Therefore, if not already, download and install the [Node.js](https://nodejs.org/en/download/). Windows users must run the executable as an Administrator, and restart the computer after installation. After successfully installing the Node, verify the installation as shown below.
```
node -v
npm -v
```
Install [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/) for the website's frontend:
```
npm init -y
npm install bootstrap@3
```


## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py
  ├── config.py
  ├── error.log
  ├── forms.py
  ├── requirements.txt
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```
