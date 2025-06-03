#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from datetime import datetime

class XMLFinder:
    """Classe responsável por localizar arquivos XML"""
    
    def __init__(self, base_path=None):
        """
        Inicializa o localizador de arquivos XML.
        
        Args:
            base_path (str, optional): Caminho base para procurar os arquivos
        """
        self.base_path = base_path or "C:\\DigiSat\\SuiteG6\\Servidor\\DFe"
        self.logger = logging.getLogger("XMLSender.XMLFinder")

    def find_xml_files(self, document_id, period, document_type="all"):
        """
        Encontra arquivos XML para o CPF/CNPJ e período especificados.
        
        Args:
            document_id (str): CPF/CNPJ (apenas números)
            period (str): Período no formato AAAAMM (ex: 202501)
            document_type (str, optional): Tipo de documento ('nfce', 'nfe', 'all')
            
        Returns:
            dict: Dicionário com os arquivos encontrados para cada tipo de documento
        """
        # Garantir que o CNPJ tenha 14 dígitos
        document_id_clean = ''.join(filter(str.isdigit, document_id))
        if len(document_id_clean) == 11:
            # Se for CPF (11 dígitos), manter como está
            pass
        elif len(document_id_clean) == 14:
            # Se for CNPJ (14 dígitos), usar completo
            pass
        else:
            # Se não for nem CPF nem CNPJ válido, tentar usar como está
            self.logger.warning(f"Documento {document_id_clean} não tem formato padrão de CPF/CNPJ")
        
        self.logger.info(f"Buscando arquivos XML para Doc ID={document_id_clean}, período={period}")
        
        result = {
            'nfce': [],
            'nfe': []
        }
        
        try:
            # Buscar NFCe
            if document_type in ["all", "nfce"]:
                nfce_path = os.path.join(self.base_path, document_id_clean, "Enviado", "NFCe", period, "Autorizados")
                self.logger.info(f"Verificando caminho NFCe: {nfce_path}")
                
                if os.path.exists(nfce_path):
                    nfce_files = self._get_xml_files_from_dir(nfce_path)
                    result['nfce'] = [{'filename': f, 'path': os.path.join(nfce_path, f)} for f in nfce_files]
                    self.logger.info(f"Encontrados {len(nfce_files)} arquivos NFCe")
                else:
                    self.logger.warning(f"Diretório não encontrado: {nfce_path}")
                    
            # Buscar NFe - VERSÃO MELHORADA COM MÚLTIPLAS TENTATIVAS
            if document_type in ["all", "nfe"]:
                nfe_found = False
                # Lista de possíveis nomes para o diretório NFe
                nfe_dir_variations = ["NF-e", "NFe", "nfe", "NF_e", "NFE"]
                
                base_nfe_path = os.path.join(self.base_path, document_id_clean, "Enviado")
                
                for nfe_dir_name in nfe_dir_variations:
                    nfe_path = os.path.join(base_nfe_path, nfe_dir_name, period, "Autorizados")
                    self.logger.info(f"Tentando caminho NFe: {nfe_path}")
                    
                    if os.path.exists(nfe_path):
                        nfe_files = self._get_xml_files_from_dir(nfe_path)
                        result['nfe'] = [{'filename': f, 'path': os.path.join(nfe_path, f)} for f in nfe_files]
                        self.logger.info(f"Encontrados {len(nfe_files)} arquivos NFe em {nfe_path}")
                        nfe_found = True
                        break
                    else:
                        self.logger.debug(f"Caminho não existe: {nfe_path}")
                
                if not nfe_found:
                    # Tentar busca mais flexível - verificar se existe o diretório base e listar subdiretórios
                    self.logger.info(f"Tentando busca flexível em: {base_nfe_path}")
                    if os.path.exists(base_nfe_path):
                        subdirs = [d for d in os.listdir(base_nfe_path) 
                                 if os.path.isdir(os.path.join(base_nfe_path, d)) 
                                 and 'nf' in d.lower()]
                        self.logger.info(f"Subdiretórios encontrados contendo 'nf': {subdirs}")
                        
                        for subdir in subdirs:
                            if 'nf' in subdir.lower() and subdir not in ["NFCe"]:  # Evitar pegar NFCe
                                nfe_path = os.path.join(base_nfe_path, subdir, period, "Autorizados")
                                self.logger.info(f"Testando subdiretório encontrado: {nfe_path}")
                                
                                if os.path.exists(nfe_path):
                                    nfe_files = self._get_xml_files_from_dir(nfe_path)
                                    result['nfe'] = [{'filename': f, 'path': os.path.join(nfe_path, f)} for f in nfe_files]
                                    self.logger.info(f"Encontrados {len(nfe_files)} arquivos NFe em {nfe_path}")
                                    nfe_found = True
                                    break
                    
                    if not nfe_found:
                        self.logger.warning(f"Nenhum diretório NFe encontrado para o período {period}")
                        # Executar debug para mostrar estrutura
                        self._debug_nfe_structure(document_id_clean, period)
                    
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar arquivos XML: {e}")
            raise Exception(f"Erro ao buscar arquivos XML: {e}")

    def _get_xml_files_from_dir(self, directory):
        """
        Obtém todos os arquivos XML de um diretório.
        
        Args:
            directory (str): Caminho do diretório
            
        Returns:
            list: Lista de nomes de arquivos XML
        """
        try:
            files = [f for f in os.listdir(directory) if f.lower().endswith('.xml')]
            self.logger.info(f"Arquivos XML encontrados em {directory}: {files}")
            return files
        except Exception as e:
            self.logger.error(f"Erro ao listar arquivos do diretório {directory}: {e}")
            return []

    def _debug_nfe_structure(self, document_id_clean, period):
        """
        Debug específico para estrutura NFe
        """
        base_path = os.path.join(self.base_path, document_id_clean, "Enviado")
        self.logger.info(f"=== DEBUG NFe - Estrutura de diretórios ===")
        self.logger.info(f"Base path: {base_path}")
        
        if os.path.exists(base_path):
            subdirs = os.listdir(base_path)
            self.logger.info(f"Subdiretórios em 'Enviado': {subdirs}")
            
            for subdir in subdirs:
                subdir_path = os.path.join(base_path, subdir)
                if os.path.isdir(subdir_path):
                    self.logger.info(f"  Verificando: {subdir}")
                    try:
                        contents = os.listdir(subdir_path)
                        self.logger.info(f"    Conteúdo: {contents}")
                        
                        # Verificar se existe o período
                        if period in contents:
                            period_path = os.path.join(subdir_path, period)
                            period_contents = os.listdir(period_path)
                            self.logger.info(f"    Período {period} encontrado: {period_contents}")
                            
                            # Verificar subdiretórios do período
                            for item in period_contents:
                                item_path = os.path.join(period_path, item)
                                if os.path.isdir(item_path):
                                    item_contents = os.listdir(item_path)
                                    xml_count = len([f for f in item_contents if f.lower().endswith('.xml')])
                                    self.logger.info(f"      {item}/: {xml_count} arquivos XML")
                    except Exception as e:
                        self.logger.error(f"    Erro ao listar {subdir}: {e}")
        else:
            self.logger.warning(f"Base path não existe: {base_path}")

    def debug_path_search(self, document_id, period):
        """
        Método de debug para verificar caminhos possíveis
        """
        document_id_clean = ''.join(filter(str.isdigit, document_id))
        
        # Adicionar mais variações para NFe
        nfe_variations = ["NF-e", "NFe", "nfe", "NF_e", "NFE"]
        
        possible_paths = [
            os.path.join(self.base_path, document_id_clean),
            os.path.join(self.base_path, document_id_clean, "Enviado"),
            os.path.join(self.base_path, document_id_clean, "Enviado", "NFCe"),
            os.path.join(self.base_path, document_id_clean, "Enviado", "NFCe", period),
            os.path.join(self.base_path, document_id_clean, "Enviado", "NFCe", period, "Autorizados"),
        ]
        
        # Adicionar todas as variações de NFe
        for nfe_var in nfe_variations:
            possible_paths.extend([
                os.path.join(self.base_path, document_id_clean, "Enviado", nfe_var),
                os.path.join(self.base_path, document_id_clean, "Enviado", nfe_var, period),
                os.path.join(self.base_path, document_id_clean, "Enviado", nfe_var, period, "Autorizados"),
            ])
        
        print("=== DEBUG - Verificação de Caminhos ===")
        for path in possible_paths:
            exists = os.path.exists(path)
            print(f"{'✓' if exists else '✗'} {path}")
            if exists and os.path.isdir(path):
                try:
                    contents = os.listdir(path)
                    xml_files = [f for f in contents if f.lower().endswith('.xml')]
                    if xml_files:
                        print(f"    📁 Conteúdo: {contents[:3]}{'...' if len(contents) > 3 else ''}")
                        print(f"    🗄️  XML files: {len(xml_files)} arquivos")
                    else:
                        print(f"    📁 Conteúdo: {contents[:5]}{'...' if len(contents) > 5 else ''}")
                except Exception as e:
                    print(f"    ❌ Erro ao listar: {e}")
        print("=====================================")