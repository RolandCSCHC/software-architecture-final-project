# 🏦 Personal Finance Management System

A Flask-based personal finance management system with Google OAuth authentication and Fintoc API integration for real-time banking data, featuring secure user authentication, financial dashboard, and comprehensive transaction management.

## ✨ Features

- 🔐 **Google OAuth Authentication**: Secure login with Google accounts
- 🏦 **Fintoc API Integration**: Connect to Chilean, Colombian, and Mexican banks
- 💰 **Real-time Banking Data**: Access account balances and transaction history
- 📊 **Financial Dashboard**: Visualize your financial data with interactive charts
- 🔄 **Data Synchronization**: Refresh bank data on-demand
- 👤 **User Profile Management**: View and manage user profile information
- 🏠 **Multiple Routes**: Home, About, Profile, Banking Dashboard, and API endpoints
- 🎨 **Template Inheritance**: Jinja2 templates with base layout
- 💅 **Modern UI**: Bootstrap 5 integration with custom CSS and Font Awesome icons
- 📱 **Responsive Design**: Mobile-friendly interface
- 🔌 **RESTful API**: JSON API endpoints for financial data
- ❌ **Error Handling**: Custom 404 error pages and comprehensive error handling
- 🔒 **Session Management**: Secure user session handling with Flask-Login


## Project Structure

```
personal-finance-system/
├── app.py                    # Main Flask application with OAuth and Fintoc
├── fintoc_service.py         # Fintoc API integration service
├── requirements.txt          # Python dependencies (includes Fintoc SDK)
├── Dockerfile               # Docker container configuration
├── docker-compose.yml       # Docker Compose with environment variables
├── .env                    # Environment variables (OAuth + Fintoc credentials)
├── .env.example           # Environment variables template
├── .dockerignore          # Docker build exclusions
├── templates/             # Jinja2 templates
│   ├── base.html         # Base template with auth navigation
│   ├── index.html        # Home page with financial features
│   ├── about.html        # About page
│   ├── profile.html      # User profile page
│   ├── 404.html          # Error page
│   └── fintoc/           # Fintoc-specific templates
│       ├── dashboard.html    # Financial dashboard
│       └── account_detail.html # Account transaction details
└── static/               # Static files
    ├── css/
    │   └── style.css     # Custom styles
    └── js/
        └── main.js       # JavaScript functions
```

## Setup Instructions

#### Prerequisites

- Docker and Docker Compose installed on your system

#### Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/RolandCSCHC/software-architecture-final-project.git
   cd software-architecture-final-project
   ```

2. **Set up environment variables**

   Copy the example environment file and configure your credentials:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file with your actual credentials:
   ```bash
   # Google OAuth Configuration
   GOOGLE_CLIENT_ID=your_google_client_id_here
   GOOGLE_CLIENT_SECRET=your_google_client_secret_here
   
   # Fintoc API Configuration
   FINTOC_API_KEY=your_fintoc_api_key_here
   FINTOC_BASE_URL=https://api.fintoc.com
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

The application will be running in debug mode, which means:

- Automatic reloading when you make changes
- Detailed error messages
- Available on all network interfaces (0.0.0.0)

## Available Routes

### Web Routes

- **`/`** - Home page with financial features overview
- **`/about`** - About page with project information
- **`/login`** - Google OAuth login
- **`/logout`** - User logout (requires authentication)
- **`/profile`** - User profile page (requires authentication)
- **`/callback`** - OAuth callback handler
- **`/fintoc`** - Financial dashboard with connected accounts
- **`/fintoc/connect`** - Initiate bank account connection
- **`/fintoc/callback`** - Handle bank connection callback
- **`/fintoc/account/<account_id>`** - Detailed account view with transactions

### API Routes

- **`/api/data`** - General API endpoint
- **`/api/fintoc/accounts/<link_id>`** - Get accounts for a bank link
- **`/api/fintoc/movements/<account_id>`** - Get transactions for an account
- **`/api/fintoc/refresh/<account_id>`** - Refresh account data

### Error Handling

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
   {% extends "base.html" %} 
   {% block content %}
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

## API Setup

### Google OAuth Setup

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create a new project** or select an existing one
3. **Enable Google+ API** or Google Identity Services API
4. **Create OAuth 2.0 credentials**:
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:5001/callback`
5. **Copy your Client ID and Client Secret** to the `.env` file

### Fintoc API Setup

1. **Sign up for Fintoc**: https://fintoc.com/
2. **Go to Fintoc Dashboard**: https://app.fintoc.com/
3. **Create a new application** in your dashboard
4. **Get your API key** from the dashboard
5. **Copy your API key** to the `.env` file as `FINTOC_API_KEY`

#### Supported Countries and Banks

- **🇨🇱 Chile**: Banco de Chile, BancoEstado, Santander, BCI, and more
- **🇨🇴 Colombia**: Bancolombia, Banco de Bogotá, Davivienda, and more  
- **🇲🇽 Mexico**: BBVA México, Santander México, Banorte, and more

#### Test Mode

Fintoc provides a test mode for development. Use test credentials provided in their documentation to test the integration without real bank accounts.

## Technologies Used

- **Backend**: Flask 2.3.3, Flask-Login 0.6.3
- **Authentication**: Google OAuth 2.0, google-auth-oauthlib
- **Financial API**: Fintoc Python SDK 3.0.0
- **Frontend**: Bootstrap 5, Font Awesome 6, Custom CSS/JS
- **Template Engine**: Jinja2
- **Development**: Python 3.x, Virtual Environment
- **Deployment**: Docker, Docker Compose

## Financial Features

### Bank Account Integration
- **Multi-country Support**: Chile, Colombia, Mexico
- **Real-time Data**: Account balances and transaction history
- **Secure Connection**: Bank-level security with OAuth flow
- **Multiple Banks**: Support for major banks in each country

### Dashboard Features
- **Account Overview**: Summary of all connected accounts
- **Balance Visualization**: Real-time balance display with currency formatting
- **Transaction History**: Detailed transaction lists with filtering
- **Data Refresh**: On-demand account data updates
- **Export Options**: Transaction data export capabilities

### Security & Privacy
- **OAuth Authentication**: Secure user login with Google
- **API Key Management**: Secure storage of API credentials
- **Session Management**: Secure user sessions with Flask-Login
- **Data Encryption**: All API communications are encrypted

## Useful Docker Commands

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Clean up completely
docker-compose down --rmi all --volumes --remove-orphans
```

## Troubleshooting

### Common Issues

1. **Widget doesn't load**: Verify that `FINTOC_API_KEY` is configured correctly
2. **OAuth fails**: Check redirect URI in Google Console matches `http://localhost:5001/callback`
3. **Session lost**: Ensure `FLASK_SECRET_KEY` is consistent
4. **Docker won't start**: Verify that `.env` file exists and has correct variables

## License

This project is created for educational purposes as part of a Software Architecture course.

---

**Developed with ❤️ for learning financial API integration and modern software architecture.**
