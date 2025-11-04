from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
)
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from fintoc_service import FintocService
import os
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "your-secret-key-here")

# Configure Fintoc API keys
app.config["FINTOC_API_KEY"] = os.environ.get("FINTOC_API_KEY")
app.config["FINTOC_PUBLIC_KEY"] = os.environ.get("FINTOC_PUBLIC_KEY")
app.config["FINTOC_BASE_URL"] = os.environ.get("FINTOC_BASE_URL", "https://api.fintoc.com/v1")

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "your-google-client-id")
GOOGLE_CLIENT_SECRET = os.environ.get(
    "GOOGLE_CLIENT_SECRET", "your-google-client-secret"
)
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid_configuration"

# Disable HTTPS requirement for local development
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Simple user class for demonstration
class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic


# In-memory user storage (use database in production)
users = {}

# Global variable for Fintoc service - initialized later
fintoc_service = None

def get_fintoc_service():
    """Get or create Fintoc service instance"""
    global fintoc_service
    if fintoc_service is None:
        fintoc_service = FintocService()
    return fintoc_service


@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)


@app.route("/")
@login_required
def index():
    return render_template("index.html", title="Home")


@app.route("/about")
@login_required
def about():
    return render_template("about.html", title="About")



@app.route("/login")
def login():
    """Mostrar página de login"""
    return render_template("login.html", title="Iniciar Sesión")

@app.route("/google-login")
def google_login():
    """Iniciar proceso de OAuth con Google"""
    # Create flow instance for Google OAuth
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost:5001/callback"],
            }
        },
        scopes=[
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ],
    )
    flow.redirect_uri = url_for("callback", _external=True)

    authorization_url, state = flow.authorization_url(
        access_type="offline", 
        include_granted_scopes="true",
        prompt="select_account"  # Fuerza mostrar selector de cuenta
    )

    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    # Verify state parameter
    if request.args.get("state") != session.get("state"):
        return "Invalid state parameter", 400

    # Create flow instance
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost:5001/callback"],
            }
        },
        scopes=[
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ],
    )
    flow.redirect_uri = url_for("callback", _external=True)

    # Fetch token
    flow.fetch_token(authorization_response=request.url)

    # Get user info from Google
    credentials = flow.credentials
    request_session = google_requests.Request()

    # Verify and decode the JWT token
    idinfo = id_token.verify_oauth2_token(
        credentials.id_token, request_session, GOOGLE_CLIENT_ID
    )

    # Create user object
    user_id = idinfo["sub"]
    user_email = idinfo["email"]
    user_name = idinfo["name"]
    user_picture = idinfo.get("picture", "")

    # Store user in memory (use database in production)
    user = User(user_id, user_name, user_email, user_picture)
    users[user_id] = user

    # Log in the user
    login_user(user)

    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/profile")
@login_required
def profile():
    # Usar datos de sesión en lugar de current_user
    user_data = {
        'name': session.get('user_name', 'Usuario'),
        'email': session.get('user_email', 'usuario@email.com'),
        'id': session.get('user_id', 'unknown')
    }
    return render_template("profile.html", title="Profile", user=user_data)


@app.route("/api/data")
@login_required
def api_data():
    # Example API endpoint - now requires authentication
    data = {
        "message": f"Hello {session.get('user_name', 'Usuario')} from Flask API!",
        "status": "success",
        "user_email": session.get('user_email', 'usuario@email.com'),
        "data": [1, 2, 3, 4, 5],
    }
    return jsonify(data)


# Fintoc Integration Routes
@app.route("/fintoc")
@login_required
def fintoc_dashboard():
    """Fintoc dashboard showing connected accounts and financial data"""
    service = get_fintoc_service()
    if not service.is_configured():
        flash("Fintoc service is not configured. Please check your API credentials.", "warning")
        return render_template("fintoc/dashboard.html", 
                             title="Financial Dashboard", 
                             configured=False)
    
    # Debug: Mostrar contenido de la sesión
    app.logger.info(f"Session keys: {list(session.keys())}")
    app.logger.info(f"Session content: {dict(session)}")
    
    # Get user's connected links from session
    links = []
    financial_data = []
    
    # Verificar si hay un link token en la sesión
    if 'fintoc_link_token' in session and session['fintoc_link_token']:
        try:
            link_token = session['fintoc_link_token']
            link_data = session.get('fintoc_link_data', {})
            
            app.logger.info(f"Found link token in session: {link_token}")
            
            # Obtener información del link usando datos de sesión
            link_info = link_data or {'id': link_token, 'status': 'connected'}
            links.append(link_info)
            
            # Obtener cuentas del link
            accounts = service.get_link_accounts(link_token)
            if accounts:
                # Obtener resumen del link
                summary = service.get_link_summary(link_token)
                if not summary:
                    # Calcular resumen básico si no está disponible
                    summary = {
                        'total_balance': sum(acc.get('balance', {}).get('current', 0) for acc in accounts),
                        'currency': accounts[0].get('balance', {}).get('currency', 'CLP') if accounts else 'CLP',
                        'accounts_count': len(accounts)
                    }
                
                financial_data.append({
                    'link': link_info,
                    'accounts': accounts,
                    'summary': summary
                })
                
                app.logger.info(f"Loaded {len(accounts)} accounts for link {link_token}")
            else:
                app.logger.warning(f"No accounts found for link {link_token}")
                
        except Exception as e:
            app.logger.error(f"Error loading financial data: {str(e)}")
            flash("Error al cargar datos financieros. Intenta reconectar tu cuenta.", "warning")
    else:
        app.logger.info("No fintoc_link_token found in session")
        
        # DEBUG: Intentar obtener links directamente (si estuviéramos usando una DB)
        # En producción, aquí consultaríamos una base de datos de links por usuario
        app.logger.info("Session does not contain link token. User needs to connect bank account.")
        
    return render_template("fintoc/dashboard.html", 
                         title="Financial Dashboard",
                         configured=True,
                         links=links,
                         financial_data=financial_data)


@app.route("/fintoc/connect")
@login_required
def fintoc_connect():
    """Conectar cuenta bancaria usando Fintoc - Solo bancos chilenos"""
    try:
        # Verificar configuración de Fintoc
        service = get_fintoc_service()
        if not service.is_configured():
            flash("Fintoc service is not configured.", "error")
            return redirect(url_for('fintoc_dashboard'))
        
        country = 'cl'  # Solo Chile - sin opción de cambiar país
        
        # Crear el link intent para bancos chilenos únicamente
        link_intent = service.create_link_intent(country, session.get('user_id'))
        
        if not link_intent:
            flash('Error al crear el link intent. Por favor, verifica la configuración de Fintoc.', 'error')
            return redirect(url_for('fintoc_dashboard'))
        
        # Obtener el widget_token del link intent
        widget_token = link_intent.get('widget_token')
        public_key = os.getenv('FINTOC_PUBLIC_KEY', 'pk_test_demo')
        
        if not widget_token:
            flash('Error: No se pudo obtener el token del widget.', 'error')
            return redirect(url_for('fintoc_dashboard'))
        
        app.logger.info(f"Link Intent created: {link_intent.get('id')}, Widget Token: {widget_token[:20]}...")
        app.logger.info(f"Public Key: {public_key[:20]}... (length: {len(public_key) if public_key else 0})")
        app.logger.info(f"Environment check - FINTOC_PUBLIC_KEY exists: {bool(os.getenv('FINTOC_PUBLIC_KEY'))}")
        
        # Guardar información en sesión para el callback
        session['fintoc_link_intent_id'] = link_intent.get('id')
        session['fintoc_country'] = country
        
        # Renderizar template con widget_token
        return render_template('fintoc/connect.html',
                               widget_token=widget_token,
                               public_key=public_key,
                               link_intent=link_intent,
                               country=country,
                               debug_info=True)
        
    except Exception as e:
        app.logger.error(f'Error in fintoc_connect: {str(e)}')
        flash('Error al conectar con Fintoc. Por favor, intenta nuevamente.', 'error')
        return redirect(url_for('fintoc_dashboard'))


@app.route("/fintoc/exchange", methods=['POST'])
@login_required
def fintoc_exchange():
    """Intercambiar exchange_token por link permanente"""
    try:
        data = request.get_json()
        exchange_token = data.get('exchange_token')
        
        if not exchange_token:
            return jsonify({'success': False, 'error': 'Exchange token no proporcionado'})
        
        app.logger.info(f"Exchanging token: {exchange_token[:20]}...")
        
        # Intercambiar el token
        service = get_fintoc_service()
        link = service.exchange_token_for_link(exchange_token)
        
        if not link:
            return jsonify({'success': False, 'error': 'Error al intercambiar el token'})
        
        # Guardar link_token en la sesión o base de datos
        session['fintoc_link_token'] = link.get('id')
        session['fintoc_link_data'] = link
        
        app.logger.info(f"Link created successfully: {link.get('id')}")
        
        return jsonify({
            'success': True,
            'link_id': link.get('id'),
            'message': 'Cuenta bancaria conectada exitosamente'
        })
        
    except Exception as e:
        app.logger.error(f'Error in fintoc_exchange: {str(e)}')
        return jsonify({'success': False, 'error': str(e)})

@app.route("/fintoc/callback", methods=['GET', 'POST'])
@login_required
def fintoc_callback():
    """Handle callback after user connects their bank account"""
    
    if request.method == 'POST':
        # Handle widget callback with link_id
        data = request.get_json()
        link_id = data.get('link_id')
        country = data.get('country') or session.get('fintoc_country', 'cl')
        
        if not link_id:
            return jsonify({'status': 'error', 'message': 'Missing link_id'}), 400
        
        # Verify session
        session_user_id = session.get('user_id')
        if not session_user_id:
            return jsonify({'status': 'error', 'message': 'User not logged in'}), 401
        
        # Por ahora, simplemente registrar el link_id como exitoso
        session['fintoc_link_id'] = link_id
        session.pop('fintoc_country', None)
        session.pop('fintoc_user_id', None)
        
        app.logger.info(f"Bank connection successful for user {session_user_id}, link_id: {link_id}")
        
        return jsonify({
            'status': 'success',
            'message': 'Bank account connected successfully',
            'link_id': link_id
        })
    
    # Handle GET callback - redirigir al dashboard
    return redirect(url_for('fintoc_dashboard'))


@app.route("/api/fintoc/accounts/<link_id>")
@login_required
def api_fintoc_accounts(link_id):
    """API endpoint to get accounts for a specific link"""
    if not fintoc_service.is_configured():
        return jsonify({"error": "Fintoc service not configured"}), 500
    
    accounts = fintoc_service.get_accounts(link_id)
    return jsonify({
        "status": "success",
        "accounts": accounts,
        "count": len(accounts)
    })


@app.route("/api/fintoc/movements/<account_id>")
@login_required
def api_fintoc_movements(account_id):
    """API endpoint to get movements for a specific account"""
    if not fintoc_service.is_configured():
        return jsonify({"error": "Fintoc service not configured"}), 500
    
    # Get query parameters
    limit = min(int(request.args.get('limit', 50)), 200)
    since = request.args.get('since')  # YYYY-MM-DD format
    until = request.args.get('until')  # YYYY-MM-DD format
    
    movements = fintoc_service.get_movements(account_id, limit=limit, since=since, until=until)
    
    return jsonify({
        "status": "success",
        "movements": movements,
        "count": len(movements),
        "account_id": account_id
    })


@app.route("/api/fintoc/refresh/<account_id>", methods=['POST'])
@login_required
def api_fintoc_refresh(account_id):
    """API endpoint to refresh account data"""
    if not fintoc_service.is_configured():
        return jsonify({"error": "Fintoc service not configured"}), 500
    
    success = fintoc_service.refresh_account(account_id)
    
    if success:
        return jsonify({
            "status": "success",
            "message": "Account data refresh initiated"
        })
    else:
        return jsonify({
            "status": "error", 
            "message": "Failed to refresh account data"
        }), 500


@app.route("/fintoc/account/<account_id>")
@login_required
def fintoc_account_detail(account_id):
    """Show detailed view of a specific account with movements"""
    if not fintoc_service.is_configured():
        flash("Fintoc service is not configured.", "warning")
        return redirect(url_for('fintoc_dashboard'))
    
    # Get recent movements (last 30 days)
    since_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    movements = fintoc_service.get_movements(account_id, limit=100, since=since_date)
    
    # Get account info from first movement or make separate API call
    # For simplicity, we'll pass the account_id and get details via AJAX
    
    return render_template("fintoc/account_detail.html",
                         title="Account Details",
                         account_id=account_id,
                         movements=movements)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", title="Page Not Found"), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
