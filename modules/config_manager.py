#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import logging
from datetime import datetime

class ConfigManager:
    """Gerenciador de configurações da aplicação"""
    
    def __init__(self, config_path):
        """
        Inicializa o gerenciador de configurações.
        
        Args:
            config_path (str): Caminho para o arquivo de configurações
        """
        self.config_path = config_path
        self.logger = logging.getLogger("XMLSender.ConfigManager")
    
    def load_config(self):
        """
        Carrega as configurações do arquivo.
        
        Returns:
            dict: Dicionário com as configurações carregadas ou configurações padrão
        """
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.logger.info(f"Configurações carregadas de {self.config_path}")
                return config
            else:
                # Criar diretório se não existir
                os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
                
                # Configurações padrão
                default_config = self._get_default_config()
                
                # Salvar configurações padrão
                self.save_config(default_config)
                self.logger.info("Configurações padrão criadas")
                return default_config
        
        except Exception as e:
            self.logger.error(f"Erro ao carregar configurações: {e}")
            return self._get_default_config()
    
    def save_config(self, config):
        """
        Salva as configurações no arquivo.
        
        Args:
            config (dict): Configurações a serem salvas
        """
        try:
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            self.logger.info(f"Configurações salvas em {self.config_path}")
        
        except Exception as e:
            self.logger.error(f"Erro ao salvar configurações: {e}")
            raise Exception(f"Não foi possível salvar as configurações: {e}")
    
    def _get_default_config(self):
        """
        Retorna as configurações padrão.
        
        Returns:
            dict: Configurações padrão
        """
        return {
            "smtp": {
                "server": "",
                "port": 587,
                "username": "",
                "password": "",
                "use_ssl": False
            },
            "cnpj": "",
            "company_name": "",
            "email": "",
            "last_period": "",
            "base_path": "C:\\DigiSat\\SuiteG6\\Servidor\\DFe"
        }