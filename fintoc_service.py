"""
Fintoc Integration Service
Handles all Fintoc API interactions for financial data aggregation
"""
import requests
from flask import current_app
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class FintocService:
    def __init__(self):
        """Initialize Fintoc client with API credentials"""
        self.api_key = current_app.config.get('FINTOC_API_KEY')
        self.public_key = current_app.config.get('FINTOC_PUBLIC_KEY')
        self.base_url = "https://api.fintoc.com/v1"
        
        if not self.api_key:
            logger.warning("Fintoc API key not found. Set FINTOC_API_KEY environment variable.")
    
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
        if not self.api_key:
            logger.error("Fintoc API key not configured")
            return None
            
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            # Datos para crear el Link Intent
            data = {
                'country': country,
                'product': 'movements',  # Para obtener movimientos bancarios
                'holder_type': 'individual'  # Tipo de cuenta: individual o business
            }
            
            # Agregar user_id si se proporciona
            if user_id:
                data['user'] = {'id': user_id}
            
            logger.info(f"Creating Link Intent with data: {data}")
            
            response = requests.post(
                f"{self.base_url}/link_intents",
                json=data,
                headers=headers
            )
            
            if response.status_code == 201:
                result = response.json()
                logger.info(f"Link Intent created successfully: {result.get('id')}")
                return result
            else:
                logger.error(f"API Error creating Link Intent: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating link intent: {str(e)}")
            return None
    
    def exchange_token_for_link(self, exchange_token):
        """
        Intercambiar exchange_token por link_token permanente
        
        Args:
            exchange_token: Token temporal recibido del widget
            
        Returns:
            Link object with permanent link_token
        """
        if not self.api_key:
            logger.error("Fintoc API key not configured")
            return None
            
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            params = {
                'exchange_token': exchange_token
            }
            
            logger.info(f"Exchanging token: {exchange_token[:20]}...")
            
            response = requests.get(
                f"{self.base_url}/links/exchange",
                params=params,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Exchange successful, Link ID: {result.get('id')}")
                return result
            else:
                logger.error(f"Exchange Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error exchanging token: {str(e)}")
            return None
    
    def get_link_accounts(self, link_token):
        """
        Obtener cuentas de un link usando el link_token
        
        Args:
            link_token: Token permanente del link
            
        Returns:
            List of account objects
        """
        if not self.api_key:
            logger.error("Fintoc API key not configured")
            return []
            
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.base_url}/links/{link_token}/accounts",
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Found {len(result)} accounts for link {link_token}")
                return result
            else:
                logger.error(f"Error getting accounts: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting accounts: {str(e)}")
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
        if not self.api_key:
            logger.error("Fintoc API key not configured")
            return []
            
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
            
            response = requests.get(
                f"{self.base_url}/accounts/{account_id}/movements",
                params=params,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Found {len(result)} movements for account {account_id}")
                return result
            else:
                logger.error(f"Error getting movements: {response.status_code} - {response.text}")
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