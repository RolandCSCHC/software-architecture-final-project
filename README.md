# Personal Finance Management System

A Flask-based personal finance management system with Google OAuth authentication, featuring secure user authentication, profile management, and a modern responsive interface.

## Features

- 🔐 **Google OAuth Authentication**: Secure login with Google accounts
- 👤 **User Profile Management**: View and manage user profile information
- 🏠 **Multiple Routes**: Home, About, Profile, and API endpoints
- 🎨 **Template Inheritance**: Jinja2 templates with base layout
- 💅 **Modern UI**: Bootstrap 5 integration with custom CSS
- 📱 **Responsive Design**: Mobile-friendly interface
- 🔌 **API Endpoints**: JSON API for data exchange
- ❌ **Error Handling**: Custom 404 error pages
- 🔒 **Session Management**: Secure user session handling with Flask-Login

## Project Structure

```
personal-finance-system/
├── app.py              # Main Flask application with OAuth
├── requirements.txt    # Python dependencies (includes OAuth packages)
├── Dockerfile          # Docker container configuration
├── docker-compose.yml  # Docker Compose with environment variables
├── .env               # Environment variables (OAuth credentials)
├── .dockerignore      # Docker build exclusions
├── templates/         # Jinja2 templates
│   ├── base.html     # Base template with auth navigation
│   ├── index.html    # Home page
│   ├── about.html    # About page
│   ├── profile.html  # User profile page
│   └── 404.html      # Error page
└── static/           # Static files
    ├── css/
    │   └── style.css # Custom styles
    └── js/
        └── main.js   # JavaScript functions
```

## Setup Instructions

### Option 1: Docker Setup (Recommended)

#### Prerequisites

- Docker and Docker Compose installed on your system

#### Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/RolandCSCHC/software-architecture-final-project.git
   cd software-architecture-final-project
   ```

2. **Set up environment variables**

   Create a `.env` file in the project root:
   ```bash
   GOOGLE_CLIENT_ID=your_google_client_id_here
   GOOGLE_CLIENT_SECRET=your_google_client_secret_here
   ```

3. **Build and run with Docker Compose**

   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   ```
   http://127.0.0.1:5001
   ```

#### Docker Commands

- **Run in background**: `docker-compose up -d --build`
- **Stop services**: `docker-compose down`
- **Rebuild**: `docker-compose up --build`

### Option 2: Local Development Setup

#### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

#### Installation

1. **Clone the project repository**

   ```bash
   git clone https://github.com/RolandCSCHC/software-architecture-final-project.git
   cd software-architecture-final-project
   ```

2. **Activate the virtual environment** (if not already activated)

   ```bash
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Set up environment variables**

   Create a `.env` file in the project root:
   ```bash
   GOOGLE_CLIENT_ID=your_google_client_id_here
   GOOGLE_CLIENT_SECRET=your_google_client_secret_here
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

#### Running the Application

1. **Start the Flask development server**

   ```bash
   python app.py
   ```

2. **Open your browser and navigate to**
   ```
   http://127.0.0.1:5001
   ```

The application will be running in debug mode, which means:

- Automatic reloading when you make changes
- Detailed error messages
- Available on all network interfaces (0.0.0.0)

## Available Routes

- **`/`** - Home page with feature overview
- **`/about`** - About page with project information
- **`/login`** - Google OAuth login
- **`/logout`** - User logout (requires authentication)
- **`/profile`** - User profile page (requires authentication)
- **`/callback`** - OAuth callback handler
- **`/api/data`** - JSON API endpoint
- **Custom 404** - Error handling for non-existent pages

## Development

### Adding New Routes

Add new routes in `app.py`:

```python
@app.route('/new-page')
def new_page():
    return render_template('new_page.html', title='New Page')
```

### Creating New Templates

1. Create HTML file in `templates/` directory
2. Extend the base template:
   ```html
   {% extends "base.html" %} {% block content %}
   <!-- Your content here -->
   {% endblock %}
   ```

### Adding Static Files

- **CSS**: Add to `static/css/`
- **JavaScript**: Add to `static/js/`
- **Images**: Add to `static/images/` (create directory if needed)

## Docker Features

- **🐳 Containerized**: Fully dockerized Flask application
- **🔒 Security**: Non-root user, minimal base image
- **⚡ Performance**: Optimized layer caching and health checks
- **🔄 Development**: Volume mounts for live static file updates
- **📊 Monitoring**: Built-in health checks and restart policies

## Google OAuth Setup

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create a new project** or select an existing one
3. **Enable Google+ API** or Google Identity Services API
4. **Create OAuth 2.0 credentials**:
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:5001/callback`
5. **Copy your Client ID and Client Secret** to the `.env` file

## Technologies Used

- **Backend**: Flask 2.3.3, Flask-Login 0.6.3
- **Authentication**: Google OAuth 2.0, google-auth-oauthlib
- **Frontend**: Bootstrap 5, Custom CSS/JS
- **Template Engine**: Jinja2
- **Development**: Python 3.x, Virtual Environment
- **Deployment**: Docker, Docker Compose

## License

This project is created for educational purposes as part of a Software Architecture course.
