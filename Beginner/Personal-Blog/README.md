# Personal Blog

A simple personal blog built with Flask, allowing you to write and publish articles with basic admin functionality.

## Features

- **Guest Section**
  - View published articles on the home page
  - Read full articles on dedicated pages

- **Admin Section**
  - Secure login for admin access
  - Dashboard to manage articles
  - Add, edit, and delete articles

## Prerequisites

- Python 3.12+
- Flask

### Installation

1. Clone the repository:
```bash
git clone https://github.com/codefromlani/Roadmap.sh-Projects.git
cd beginner
cd personal-blog
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```
5. Access the blog at http://127.0.0.1:5000

## Admin Login

- Username: admin
- Password: password

## Project Structure

- `app.py` - Main Flask application
- `templates/` - HTML templates
- `articles/` - Article storage directory

## Technologies

- Backend: Python Flask
- Frontend: HTML, Bootstrap
- Storage: File-based (JSON)