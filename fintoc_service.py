"""
Fintoc Integration Service
Handles all Fintoc API interactions for financial data aggregation
"""
import requests
from flask import current_app
import logging
from typing import Dict, List, Optional
import fintoc

logger = logging.getLogger(__name__)

class FintocService:
    def __init__(self):
        """Initialize Fintoc client with API credentials"""
        self.api_key = current_app.config.get('FINTOC_API_KEY')
        self.public_key = current_app.config.get('FINTOC_PUBLIC_KEY')
        self.base_url = "https://api.fintoc.com/v1"
        
        # Configurar la biblioteca oficial de Fintoc
        if self.api_key:
            self.client = fintoc.Fintoc(api_key=self.api_key)
        else:
            logger.warning("Fintoc API key not found. Set FINTOC_API_KEY environment variable.")
            self.client = None
    
    def is_configured(self) -> bool:
        """Check if Fintoc is properly configured"""
        return self.api_key is not None
    
    def create_link_intent(self, country: str = 'cl', user_id: str = None):
        """
        Crear un Link Intent para obtener widget_token
        
        Args:
            country: Country code (cl, co, mx)
            user_id: Internal user ID for tracking
            
        Returns:
            Link Intent object with widget_token
        """
        if not self.client:
            logger.error("Fintoc client not configured")
            return None
            
        try:
            # Por ahora usar método manual hasta entender mejor la API
            logger.info(f"Using manual method for Link Intent creation")
            return self._create_link_intent_manual(country, user_id)
                
        except Exception as e:
            logger.error(f"Error creating link intent: {str(e)}")
            # Fallback a método manual si falla la biblioteca
            return self._create_link_intent_manual(country, user_id)
    
    def _create_link_intent_manual(self, country: str = 'cl', user_id: str = None):
        """Método manual fallback para crear Link Intent"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'country': country,
                'product': 'movements',  # Singular, no plural
                'holder_type': 'individual'
            }
            
            if user_id:
                data['user'] = {'id': user_id}
            
            response = requests.post(
                f"{self.base_url}/link_intents",
                json=data,
                headers=headers
            )
            
            if response.status_code == 201:
                result = response.json()
                logger.info(f"Manual Link Intent created: {result.get('id')}")
                return result
            else:
                logger.error(f"Manual API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Manual error creating link intent: {str(e)}")
            return None
    
    def exchange_token_for_link(self, exchange_token):
        """
        Intercambiar exchange_token por link_token permanente
        
        Args:
            exchange_token: Token temporal recibido del widget
            
        Returns:
            Link object with permanent link_token
        """
        if not self.client:
            logger.error("Fintoc client not configured")
            return None
            
        try:
            logger.info(f"Exchanging token: {exchange_token[:20]}...")
            
            # Usar método manual por ahora
            logger.info(f"Using manual method for token exchange")
            return self._exchange_token_manual(exchange_token)
                
        except Exception as e:
            logger.error(f"Error exchanging token with library: {str(e)}")
            # Fallback a método manual
            return self._exchange_token_manual(exchange_token)
    
    def _exchange_token_manual(self, exchange_token):
        """Método manual fallback para intercambio"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            params = {'exchange_token': exchange_token}
            
            response = requests.get(
                f"{self.base_url}/links/exchange",
                params=params,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Manual exchange successful: {result}")
                
                # Importante: construir el link_token completo si no viene en la respuesta
                if 'link_token' not in result and 'id' in result:
                    # El link_token completo incluye el access_token
                    # Necesitamos obtenerlo de otro campo o construirlo
                    logger.info(f"Response keys: {list(result.keys())}")
                    
                    # Buscar el access_token en la respuesta
                    access_token = result.get('access_token')
                    if access_token:
                        result['link_token'] = f"{result['id']}_token_{access_token}"
                        logger.info(f"Constructed link_token: {result['link_token'][:30]}...")
                    else:
                        # Si no hay access_token, usar solo el ID por ahora
                        result['link_token'] = result['id']
                        logger.warning(f"No access_token found, using ID only: {result['id']}")
                
                return result
            else:
                logger.error(f"Manual exchange error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Manual exchange error: {str(e)}")
            return None
    
    def get_link_accounts(self, link_token):
        """
        Obtener cuentas de un link usando el link_token
        
        Args:
            link_token: Token permanente del link
            
        Returns:
            List of account objects
        """
        if not self.client:
            logger.error("Fintoc client not configured")
            return []
            
        try:
            logger.info(f"Requesting accounts for link {link_token}")
            
            # Usar método manual por ahora
            logger.info(f"Using manual method for getting accounts")
            return self._get_link_accounts_manual(link_token)
                
        except Exception as e:
            logger.error(f"Error getting accounts with library: {str(e)}")
            # Fallback a método manual
            return self._get_link_accounts_manual(link_token)
    
    def _get_link_accounts_manual(self, link_token):
        """Método manual fallback para obtener cuentas"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            logger.info(f"Manual: Requesting accounts for link {link_token}")
            
            # Intentar diferentes endpoints
            endpoints_to_try = [
                f"{self.base_url}/accounts?link_token={link_token}",
                f"{self.base_url}/links/{link_token}/accounts"
            ]
            
            for endpoint in endpoints_to_try:
                logger.info(f"Trying endpoint: {endpoint}")
                response = requests.get(endpoint, headers=headers, timeout=30)
                
                logger.info(f"Response status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"Manual: Found {len(result)} accounts")
                    return result
                elif response.status_code != 404:
                    logger.error(f"Unexpected error: {response.status_code} - {response.text}")
            
            logger.error("All manual endpoints failed")
            return []
                
        except Exception as e:
            logger.error(f"Manual accounts error: {str(e)}")
            return []
    
    def get_account_movements(self, account_id, limit=50, since=None, until=None):
        """
        Obtener movimientos de una cuenta específica
        
        Args:
            account_id: ID de la cuenta
            limit: Número de movimientos a obtener (max 200)
            since: Fecha de inicio (YYYY-MM-DD)
            until: Fecha de fin (YYYY-MM-DD)
            
        Returns:
            List of movement objects
        """
        if not self.client:
            logger.error("Fintoc client not configured")
            return []
            
        try:
            logger.info(f"Requesting movements for account {account_id}, limit: {limit}")
            
            # Usar método manual por ahora
            logger.info(f"Using manual method for getting movements")
            return self._get_account_movements_manual(account_id, limit, since, until)
                
        except Exception as e:
            logger.error(f"Error getting movements with library: {str(e)}")
            # Fallback a método manual
            return self._get_account_movements_manual(account_id, limit, since, until)
    
    def _get_account_movements_manual(self, account_id, limit=50, since=None, until=None):
        """Método manual fallback para obtener movimientos"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            params = {'limit': min(limit, 200)}
            if since:
                params['since'] = since
            if until:
                params['until'] = until
            
            logger.info(f"Manual: Requesting movements for account {account_id}")
            
            response = requests.get(
                f"{self.base_url}/accounts/{account_id}/movements",
                params=params,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Manual: Found {len(result)} movements")
                return result
            else:
                logger.error(f"Manual movements error: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Manual movements error: {str(e)}")
            return []
    
    def get_movements(self, account_id, limit=50, since=None, until=None):
        """
        Alias para get_account_movements para compatibilidad
        """
        return self.get_account_movements(account_id, limit, since, until)
    
    def get_account_movements_with_link(self, account_id, link_token, limit=50, since=None, until=None):
        """
        Obtener movimientos de una cuenta específica usando link_token
        
        Args:
            account_id: ID de la cuenta
            link_token: Token del link para autenticación
            limit: Número de movimientos a obtener (max 200)
            since: Fecha de inicio (YYYY-MM-DD)
            until: Fecha de fin (YYYY-MM-DD)
            
        Returns:
            List of movement objects
        """
        if not self.api_key:
            logger.error("Fintoc API key not configured")
            return []
            
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            params = {
                'limit': min(limit, 200),
                'link_token': link_token
            }
            if since:
                params['since'] = since
            if until:
                params['until'] = until
            
            logger.info(f"Requesting movements for account {account_id} with link_token {link_token[:30]}...")
            
            response = requests.get(
                f"{self.base_url}/accounts/{account_id}/movements",
                params=params,
                headers=headers,
                timeout=30
            )
            
            logger.info(f"Movements API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Found {len(result)} movements for account {account_id}")
                return result
            elif response.status_code == 404:
                logger.error(f"Account {account_id} not found")
                return []
            elif response.status_code == 401:
                logger.error(f"Unauthorized access - check API key")
                return []
            elif response.status_code == 403:
                logger.error(f"Forbidden access to account {account_id}")
                return []
            else:
                logger.error(f"Error getting movements: {response.status_code} - {response.text}")
                return []
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout getting movements for account {account_id}")
            return []
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error getting movements for account {account_id}")
            return []
        except Exception as e:
            logger.error(f"Error getting movements: {str(e)}")
            return []
    
    def get_link_summary(self, link_token):
        """
        Obtener resumen completo de un link con cuentas y balances
        
        Args:
            link_token: Token permanente del link
            
        Returns:
            Dict with link summary including accounts and total balance
        """
        accounts = self.get_link_accounts(link_token)
        
        if not accounts:
            return {
                'link_token': link_token,
                'total_balance': 0,
                'accounts_count': 0,
                'accounts': [],
                'currency': 'CLP'
            }
        
        total_balance = 0
        currency = 'CLP'
        
        # Sumar balances de todas las cuentas
        for account in accounts:
            if account.get('balance') and account['balance'].get('current'):
                if account['balance'].get('currency'):
                    currency = account['balance']['currency']
                total_balance += account['balance']['current']
        
        return {
            'link_token': link_token,
            'total_balance': total_balance,
            'currency': currency,
            'accounts_count': len(accounts),
            'accounts': accounts
        }
    
    def verify_link(self, link_token):
        """
        Verificar que un link existe y está activo
        
        Args:
            link_token: Token permanente del link
            
        Returns:
            Dict with link information or None if not found
        """
        if not self.api_key:
            logger.error("Fintoc API key not configured")
            return None
            
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.base_url}/links/{link_token}",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Link {link_token} verified successfully")
                return result
            elif response.status_code == 404:
                logger.error(f"Link {link_token} not found")
                return None
            elif response.status_code == 401:
                logger.error(f"Unauthorized access - check API key")
                return None
            else:
                logger.error(f"Error verifying link: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error verifying link: {str(e)}")
            return None