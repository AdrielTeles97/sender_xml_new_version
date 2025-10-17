#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import logging
from packaging import version
import webbrowser

class UpdateChecker:
    """Verifica atualizações disponíveis no GitHub Releases"""
    
    def __init__(self, repo_owner, repo_name, current_version):
        """
        Inicializa o verificador de atualizações.
        
        Args:
            repo_owner (str): Dono do repositório (ex: "adrielteles")
            repo_name (str): Nome do repositório (ex: "sender_xml")
            current_version (str): Versão atual da aplicação (ex: "1.0.0")
        """
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = current_version
        self.logger = logging.getLogger("XMLSender.UpdateChecker")
        
        # URL da API do GitHub
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    
    def check_for_updates(self, timeout=10):
        """
        Verifica se há atualizações disponíveis.
        
        Args:
            timeout (int): Tempo máximo de espera em segundos
            
        Returns:
            dict: {
                'has_update': bool,
                'latest_version': str,
                'download_url': str,
                'release_notes': str,
                'error': str (se houver erro)
            }
        """
        try:
            self.logger.info(f"Verificando atualizações... (versão atual: {self.current_version})")
            
            # Fazer requisição à API do GitHub
            response = requests.get(self.api_url, timeout=timeout)
            
            # Se não encontrou releases (404), não há atualizações
            if response.status_code == 404:
                self.logger.info("Nenhum release encontrado no repositório")
                return {
                    'has_update': False,
                    'latest_version': self.current_version,
                    'download_url': None,
                    'release_notes': '',
                    'error': None
                }
            
            # Verificar se a requisição foi bem-sucedida
            response.raise_for_status()
            
            # Parsear resposta
            release_data = response.json()
            
            # Extrair informações
            latest_version = release_data.get('tag_name', '').lstrip('v')  # Remove 'v' do início
            release_notes = release_data.get('body', '')
            
            # Procurar o .exe nos assets
            download_url = None
            assets = release_data.get('assets', [])
            for asset in assets:
                if asset['name'].endswith('.exe'):
                    download_url = asset['browser_download_url']
                    break
            
            # Se não encontrou .exe, usar a página do release
            if not download_url:
                download_url = release_data.get('html_url')
            
            # Comparar versões
            has_update = version.parse(latest_version) > version.parse(self.current_version)
            
            if has_update:
                self.logger.info(f"Nova versão disponível: {latest_version}")
            else:
                self.logger.info("Aplicação está atualizada")
            
            return {
                'has_update': has_update,
                'latest_version': latest_version,
                'download_url': download_url,
                'release_notes': release_notes,
                'error': None
            }
            
        except requests.exceptions.Timeout:
            error_msg = "Tempo esgotado ao verificar atualizações"
            self.logger.warning(error_msg)
            return {'has_update': False, 'error': error_msg}
            
        except requests.exceptions.ConnectionError:
            error_msg = "Sem conexão com a internet"
            self.logger.warning(error_msg)
            return {'has_update': False, 'error': error_msg}
            
        except Exception as e:
            error_msg = f"Erro ao verificar atualizações: {str(e)}"
            self.logger.error(error_msg)
            return {'has_update': False, 'error': error_msg}
    
    def download_update(self, download_url):
        """
        Abre o navegador para baixar a atualização.
        
        Args:
            download_url (str): URL de download
        """
        try:
            webbrowser.open(download_url)
            self.logger.info(f"Abrindo navegador para download: {download_url}")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao abrir navegador: {e}")
            return False

