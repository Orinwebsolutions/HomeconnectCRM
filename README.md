# Django Leads API

This project provides an API for managing and filtering leads, built with Django and Django Rest Framework (DRF). It includes JWT authentication for secure access, and the ability to filter leads by various attributes such as status, agent, source, and date range.

## Setup Instructions

Follow these steps to set up and run the project locally.

### Prerequisites

- Python 3.x
- Django 3.x or higher
- Django Rest Framework
- PostgreSQL or any other preferred database (Make sure to update the database settings in `settings.py` if needed).

### Installation

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd <project_directory>
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### Database Migration and Setup

Before running the server, you need to set up the database and apply migrations:

1. **Run migrations to set up the database:**

   ```bash
   python manage.py migrate
   ```

2. **Create a superuser to access the Django Admin:**

   ```bash
   python manage.py createsuperuser
   ```

3. **Seed the initial roles and data into the database:**

   ```bash
   python manage.py seed_roles
   python manage.py seed_data
   python manage.py seed_agents
   ```

### Running the Development Server

Once your database is set up, you can run the development server:

```bash
python manage.py runserver
```

The API should now be available at `http://127.0.0.1:8000/`.


### Note : On windows you might be difficult of running virtual environment try below steps for it.
![alt text](https://github.com/Orinwebsolutions/HomeconnectCRM/blob/main/windows-error.png?raw=true)

Try running this(This is to temporally unrestricted policy for current terminal )
```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Unrestricted
```

Use case diagram

https://www.figma.com/board/kVDjlMPlDtHHdj6FnH2Tml/Home-connect-ER?node-id=0-1&t=XFD41EtAbgIPtHSE-1

ER diagram

![alt text](https://github.com/Orinwebsolutions/HomeconnectCRM/blob/main/Home-connect-ER.png?raw=true)


This version is well-structured and should make it easy for users to follow the installation and setup steps. Reach out [me (amilapriyankara16@gmail.com)](mailto:(amilapriyankara16@gmail.com))  further adjustments!