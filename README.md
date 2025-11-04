# 🏦 Sistema de Gestión Financiera Personal con Fintoc# Personal Finance Management System



Una aplicación Flask para gestión de finanzas personales con autenticación Google OAuth e integración con la API de Fintoc para datos bancarios en tiempo real de Chile.A Flask-based personal finance management system with Google OAuth authentication and Fintoc API integration for real-time banking data, featuring secure user authentication, financial dashboard, and comprehensive transaction management.



## ✨ Características Principales## Features



- 🔐 **Autenticación Google OAuth**: Login seguro con cuentas de Google- 🔐 **Google OAuth Authentication**: Secure login with Google accounts

- 🏦 **Integración Fintoc**: Conexión con bancos chilenos en tiempo real- 🏦 **Fintoc API Integration**: Connect to Chilean, Colombian, and Mexican banks

- 💰 **Datos Bancarios**: Acceso a saldos y movimientos de cuentas- 💰 **Real-time Banking Data**: Access account balances and transaction history

- 📊 **Dashboard Financiero**: Visualización de datos financieros- 📊 **Financial Dashboard**: Visualize your financial data with interactive charts

- 🔄 **Sincronización**: Actualización de datos bancarios bajo demanda- 🔄 **Data Synchronization**: Refresh bank data on-demand

- 👤 **Gestión de Usuario**: Perfil y administración de sesiones- 👤 **User Profile Management**: View and manage user profile information

- 🎨 **UI Moderna**: Diseño responsivo con Bootstrap 5- 🏠 **Multiple Routes**: Home, About, Profile, Banking Dashboard, and API endpoints

- 🐳 **Dockerizado**: Contenedor completo listo para producción- 🎨 **Template Inheritance**: Jinja2 templates with base layout

- 💅 **Modern UI**: Bootstrap 5 integration with custom CSS and Font Awesome icons

## 🚀 Inicio Rápido con Docker- 📱 **Responsive Design**: Mobile-friendly interface

- 🔌 **RESTful API**: JSON API endpoints for financial data

### Pre-requisitos- ❌ **Error Handling**: Custom 404 error pages and comprehensive error handling

- Docker y Docker Compose instalados- 🔒 **Session Management**: Secure user session handling with Flask-Login



### Instalación## Project Structure



1. **Clonar el repositorio**```

   ```bashpersonal-finance-system/

   git clone https://github.com/RolandCSCHC/software-architecture-final-project.git├── app.py                    # Main Flask application with OAuth and Fintoc

   cd software-architecture-final-project├── fintoc_service.py         # Fintoc API integration service

   ```├── requirements.txt          # Python dependencies (includes Fintoc SDK)

├── Dockerfile               # Docker container configuration

2. **Configurar variables de entorno**├── docker-compose.yml       # Docker Compose with environment variables

   ```bash├── .env                    # Environment variables (OAuth + Fintoc credentials)

   cp .env.example .env├── .env.example           # Environment variables template

   ```├── .dockerignore          # Docker build exclusions

   ├── templates/             # Jinja2 templates

   Editar `.env` con tus credenciales:│   ├── base.html         # Base template with auth navigation

   ```bash│   ├── index.html        # Home page with financial features

   # Google OAuth (obtener en https://console.developers.google.com/)│   ├── about.html        # About page

   GOOGLE_CLIENT_ID=tu-client-id.apps.googleusercontent.com│   ├── profile.html      # User profile page

   GOOGLE_CLIENT_SECRET=GOCSPX-tu-client-secret│   ├── 404.html          # Error page

   │   └── fintoc/           # Fintoc-specific templates

   # Fintoc API (obtener en https://dashboard.fintoc.com/)│       ├── dashboard.html    # Financial dashboard

   FINTOC_API_KEY=sk_live_tu-api-key│       └── account_detail.html # Account transaction details

   FINTOC_PUBLIC_KEY=pk_live_tu-public-key└── static/               # Static files

       ├── css/

   # Flask    │   └── style.css     # Custom styles

   FLASK_SECRET_KEY=tu-clave-secreta-segura    └── js/

   ```        └── main.js       # JavaScript functions

```

3. **Construir y ejecutar**

   ```bash## Setup Instructions

   docker-compose up --build

   ```### Option 1: Docker Setup (Recommended)



4. **Acceder a la aplicación**#### Prerequisites

   ```

   http://127.0.0.1:5001- Docker and Docker Compose installed on your system

   ```

#### Quick Start

## 🏗️ Estructura del Proyecto

1. **Clone the repository**

```

fintocApp/   ```bash

├── app.py                    # Aplicación Flask principal   git clone https://github.com/RolandCSCHC/software-architecture-final-project.git

├── fintoc_service.py         # Servicio de integración Fintoc   cd software-architecture-final-project

├── requirements.txt          # Dependencias Python   ```

├── Dockerfile               # Configuración Docker

├── docker-compose.yml       # Orquestación de servicios2. **Set up environment variables**

├── .env.example            # Template de variables de entorno

├── templates/              # Plantillas Jinja2   Copy the example environment file and configure your credentials:

│   ├── base.html          # Plantilla base con navegación   ```bash

│   ├── index.html         # Página principal   cp .env.example .env

│   ├── login.html         # Página de login   ```

│   ├── profile.html       # Perfil de usuario   

│   └── fintoc/           # Plantillas específicas de Fintoc   Edit `.env` file with your actual credentials:

│       ├── dashboard.html  # Dashboard financiero   ```bash

│       ├── connect.html   # Conexión bancaria   # Google OAuth Configuration

│       └── account_detail.html # Detalles de cuenta   GOOGLE_CLIENT_ID=your_google_client_id_here

└── static/               # Archivos estáticos   GOOGLE_CLIENT_SECRET=your_google_client_secret_here

    ├── css/style.css     # Estilos personalizados   

    └── js/main.js        # JavaScript personalizado   # Fintoc API Configuration

```   FINTOC_API_KEY=your_fintoc_api_key_here

   FINTOC_BASE_URL=https://api.fintoc.com

## 🔧 Configuración de APIs   ```



### Google OAuth Setup3. **Build and run with Docker Compose**



1. **Google Cloud Console**: https://console.developers.google.com/   ```bash

2. **Crear proyecto** nuevo o seleccionar existente   docker-compose up --build

3. **Habilitar Google+ API** o Google Identity Services API   ```

4. **Crear credenciales OAuth 2.0**:

   - Tipo: Aplicación web4. **Access the application**

   - URIs de redirección autorizadas: `http://localhost:5001/callback`   ```

5. **Copiar Client ID y Client Secret** al archivo `.env`   http://127.0.0.1:5001

   ```

### Fintoc API Setup

#### Docker Commands

1. **Registrarse en Fintoc**: https://dashboard.fintoc.com/

2. **Crear nueva aplicación** en el dashboard- **Run in background**: `docker-compose up -d --build`

3. **Obtener API Keys**:- **Stop services**: `docker-compose down`

   - Secret Key (sk_live_*): Para operaciones backend- **Rebuild**: `docker-compose up --build`

   - Public Key (pk_live_*): Para el widget frontend

4. **Configurar en `.env`**### Option 2: Local Development Setup



#### 🇨🇱 Bancos Soportados en Chile#### Prerequisites

- Banco de Chile

- BancoEstado  - Python 3.7 or higher

- Santander Chile- pip (Python package installer)

- BCI (Banco de Crédito e Inversiones)

- Banco Falabella#### Installation

- Banco Ripley

- Y muchos más...1. **Clone the project repository**



## 🛠️ Desarrollo Local   ```bash

   git clone https://github.com/RolandCSCHC/software-architecture-final-project.git

### Pre-requisitos   cd software-architecture-final-project

- Python 3.9 o superior   ```

- pip (instalador de paquetes Python)

2. **Activate the virtual environment** (if not already activated)

### Instalación Local

   ```bash

1. **Crear entorno virtual**   source venv/bin/activate  # On macOS/Linux

   ```bash   # or

   python -m venv venv   venv\Scripts\activate     # On Windows

   source venv/bin/activate  # Linux/Mac   ```

   # o

   venv\Scripts\activate     # Windows3. **Set up environment variables**

   ```

   Copy the example environment file and configure your credentials:

2. **Instalar dependencias**   ```bash

   ```bash   cp .env.example .env

   pip install -r requirements.txt   ```

   ```   

   Edit `.env` file with your actual credentials:

3. **Configurar variables de entorno** (igual que con Docker)   ```bash

   # Google OAuth Configuration

4. **Ejecutar aplicación**   GOOGLE_CLIENT_ID=your_google_client_id_here

   ```bash   GOOGLE_CLIENT_SECRET=your_google_client_secret_here

   python app.py   

   ```   # Fintoc API Configuration

   FINTOC_API_KEY=your_fintoc_api_key_here

## 📋 Rutas Disponibles   FINTOC_BASE_URL=https://api.fintoc.com

   ```

### Rutas Web

- **`/`** - Página principal con características financieras4. **Install dependencies**

- **`/login`** - Página de login con Google OAuth     ```bash

- **`/google-login`** - Iniciar proceso OAuth   pip install -r requirements.txt

- **`/callback`** - Manejo de callback OAuth   ```

- **`/logout`** - Cerrar sesión

- **`/profile`** - Perfil de usuario (requiere autenticación)#### Running the Application

- **`/fintoc`** - Dashboard financiero

- **`/fintoc/connect`** - Conectar cuenta bancaria1. **Start the Flask development server**

- **`/fintoc/exchange`** - Intercambiar tokens de Fintoc

   ```bash

### Rutas API   python app.py

- **`/api/data`** - Endpoint API general   ```

- **`/api/fintoc/accounts/<link_id>`** - Obtener cuentas de un link

- **`/api/fintoc/movements/<account_id>`** - Obtener movimientos de cuenta2. **Open your browser and navigate to**

- **`/api/fintoc/refresh/<account_id>`** - Actualizar datos de cuenta   ```

   http://127.0.0.1:5001

## 🔒 Características de Seguridad   ```



- **Autenticación OAuth**: Login seguro con GoogleThe application will be running in debug mode, which means:

- **Gestión de Sesiones**: Sesiones seguras con Flask-Login

- **Claves API**: Almacenamiento seguro de credenciales- Automatic reloading when you make changes

- **Comunicaciones Encriptadas**: Todas las comunicaciones con APIs son HTTPS- Detailed error messages

- **Validación CORS**: Manejo correcto de comunicación cross-origin- Available on all network interfaces (0.0.0.0)

- **Tokens Temporales**: Uso de tokens de intercambio para máxima seguridad

## Available Routes

## 🏦 Flujo de Integración Bancaria

### Web Routes

1. **Crear Link Intent** → Genera token temporal para widget- **`/`** - Home page with financial features overview

2. **Mostrar Widget** → Usuario autentica con su banco- **`/about`** - About page with project information

3. **Exchange Token** → Intercambiar por token permanente- **`/login`** - Google OAuth login

4. **Obtener Datos** → Acceso a cuentas y movimientos- **`/logout`** - User logout (requires authentication)

5. **Dashboard** → Visualización de información financiera- **`/profile`** - User profile page (requires authentication)

- **`/callback`** - OAuth callback handler

## 🐳 Comandos Docker Útiles- **`/fintoc`** - Financial dashboard with connected accounts

- **`/fintoc/connect`** - Initiate bank account connection

```bash- **`/fintoc/callback`** - Handle bank connection callback

# Construir y ejecutar- **`/fintoc/account/<account_id>`** - Detailed account view with transactions

docker-compose up --build

### API Routes

# Ejecutar en background- **`/api/data`** - General API endpoint

docker-compose up -d- **`/api/fintoc/accounts/<link_id>`** - Get accounts for a bank link

- **`/api/fintoc/movements/<account_id>`** - Get transactions for an account

# Ver logs- **`/api/fintoc/refresh/<account_id>`** - Refresh account data

docker-compose logs -f

### Error Handling

# Detener servicios- **Custom 404** - Error handling for non-existent pages

docker-compose down

## Development

# Limpiar completamente

docker-compose down --rmi all --volumes --remove-orphans### Adding New Routes

```

Add new routes in `app.py`:

## 💻 Tecnologías Utilizadas

```python

- **Backend**: Flask 2.3.3, Flask-Login 0.6.3@app.route('/new-page')

- **Autenticación**: Google OAuth 2.0, google-auth-oauthlibdef new_page():

- **API Financiera**: Fintoc Python SDK, requests    return render_template('new_page.html', title='New Page')

- **Frontend**: Bootstrap 5, Font Awesome 6, JavaScript vanilla```

- **Motor de Templates**: Jinja2

- **Contenedores**: Docker, Docker Compose### Creating New Templates

- **Base de Datos**: Session-based (Flask sessions)

1. Create HTML file in `templates/` directory

## 📈 Funcionalidades Implementadas2. Extend the base template:

   ```html

### ✅ Completadas   {% extends "base.html" %} {% block content %}

- [x] Autenticación Google OAuth   <!-- Your content here -->

- [x] Integración completa con Fintoc API   {% endblock %}

- [x] Widget de conexión bancaria funcional   ```

- [x] Dashboard financiero básico

- [x] Manejo de sesiones de usuario### Adding Static Files

- [x] Interfaz responsive en español

- [x] Contenedor Docker optimizado- **CSS**: Add to `static/css/`

- [x] Manejo de errores y logging- **JavaScript**: Add to `static/js/`

- **Images**: Add to `static/images/` (create directory if needed)

### 🚧 En Desarrollo

- [ ] Persistencia de datos con base de datos## Docker Features

- [ ] Webhooks de Fintoc para actualizaciones automáticas

- [ ] Análisis financiero avanzado- **🐳 Containerized**: Fully dockerized Flask application

- [ ] Exportación de datos- **🔒 Security**: Non-root user, minimal base image

- [ ] Notificaciones de transacciones- **⚡ Performance**: Optimized layer caching and health checks

- **🔄 Development**: Volume mounts for live static file updates

## 🤝 Contribución- **📊 Monitoring**: Built-in health checks and restart policies



Este proyecto fue creado como parte de un curso de Arquitectura de Software. ## API Setup



### Para contribuir:### Google OAuth Setup

1. Fork del proyecto

2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)1. **Go to Google Cloud Console**: https://console.cloud.google.com/

3. Commit de cambios (`git commit -m 'Agregar nueva funcionalidad'`)2. **Create a new project** or select an existing one

4. Push a la rama (`git push origin feature/nueva-funcionalidad`)3. **Enable Google+ API** or Google Identity Services API

5. Abrir Pull Request4. **Create OAuth 2.0 credentials**:

   - Application type: Web application

## 📝 Notas de Desarrollo   - Authorized redirect URIs: `http://localhost:5001/callback`

5. **Copy your Client ID and Client Secret** to the `.env` file

- **Sesiones**: Actualmente usa sesiones de Flask. Para producción, considerar base de datos.

- **Logs**: Configurados para desarrollo. Ajustar para producción.### Fintoc API Setup

- **Seguridad**: Claves en variables de entorno. No commitear archivos `.env`.

- **Testing**: Usar credenciales de prueba de Fintoc para desarrollo.1. **Sign up for Fintoc**: https://fintoc.com/

2. **Go to Fintoc Dashboard**: https://app.fintoc.com/

## 🔍 Troubleshooting3. **Create a new application** in your dashboard

4. **Get your API key** from the dashboard

### Problemas Comunes5. **Copy your API key** to the `.env` file as `FINTOC_API_KEY`



1. **Widget no carga**: Verificar que FINTOC_PUBLIC_KEY esté configurada correctamente#### Supported Countries and Banks

2. **OAuth falla**: Verificar redirect URI en Google Console- **🇨🇱 Chile**: Banco de Chile, BancoEstado, Santander, BCI, and more

3. **Sesión se pierde**: Verificar FLASK_SECRET_KEY consistente- **🇨🇴 Colombia**: Bancolombia, Banco de Bogotá, Davivienda, and more  

4. **Docker no inicia**: Verificar que .env exista y tenga variables correctas- **🇲🇽 Mexico**: BBVA México, Santander México, Banorte, and more



### Logs Útiles#### Test Mode

```bashFintoc provides a test mode for development. Use test credentials provided in their documentation to test the integration without real bank accounts.

# Ver logs de aplicación

docker-compose logs web## Technologies Used



# Ver logs en tiempo real- **Backend**: Flask 2.3.3, Flask-Login 0.6.3

docker-compose logs -f web- **Authentication**: Google OAuth 2.0, google-auth-oauthlib

```- **Financial API**: Fintoc Python SDK 3.0.0

- **Frontend**: Bootstrap 5, Font Awesome 6, Custom CSS/JS

## 📄 Licencia- **Template Engine**: Jinja2

- **Development**: Python 3.x, Virtual Environment

Este proyecto es creado con fines educativos como parte de un curso de Arquitectura de Software.- **Deployment**: Docker, Docker Compose



---## Financial Features



**Desarrollado con ❤️ para el aprendizaje de integración APIs financieras y arquitectura de software moderna.**### Bank Account Integration
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

## License

This project is created for educational purposes as part of a Software Architecture course.
