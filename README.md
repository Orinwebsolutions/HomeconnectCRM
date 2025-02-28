Sure! Here's the properly formatted version of your `README.md` file:

```markdown
# Django Leads API

This project provides an API for managing and filtering leads, built with Django and Django Rest Framework (DRF). It includes JWT authentication for secure access, and the ability to filter leads by various attributes such as status, agent, source, and date range.

## Setup Instructions

Follow these steps to set up and run the project locally.

### Prerequisites

- Python 3.x
- Django 3.x or higher
- Django Rest Framework
- `django-filter` for advanced filtering
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

2. **Seed the initial roles and data into the database:**

   ```bash
   python manage.py seed_roles
   python manage.py seed_data
   ```

3. **Create a superuser to access the Django Admin:**

   ```bash
   python manage.py createsuperuser
   ```

### Running the Development Server

Once your database is set up, you can run the development server:

```bash
python manage.py runserver
```

The API should now be available at `http://127.0.0.1:8000/`.
```

This version is well-structured and should make it easy for users to follow the installation and setup steps. Let me know if you need further adjustments!
