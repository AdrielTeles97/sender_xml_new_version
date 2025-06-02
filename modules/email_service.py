#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import smtplib
import logging
import socket
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailService:
    """Serviço para envio de emails"""
    
    def __init__(self, smtp_config):
        """
        Inicializa o serviço de email.
        
        Args:
            smtp_config (dict): Configurações do servidor SMTP
        """
        self.smtp_config = smtp_config
        self.logger = logging.getLogger("XMLSender.EmailService")
    
    def send_email(self, to_email, subject, body, attachments=None, html_body=None, company_info=None, files_info=None):
        """
        Envia um email com anexos opcionais e formatação HTML.
        
        Args:
            to_email (str): Email do destinatário
            subject (str): Assunto do email
            body (str): Corpo do email (texto simples)
            attachments (list, optional): Lista de caminhos de arquivos para anexar
            html_body (str, optional): Corpo do email em formato HTML
            company_info (dict, optional): Informações da empresa para o email formatado
            files_info (dict, optional): Informações dos arquivos para o email formatado
            
        Returns:
            bool: True se o email foi enviado com sucesso, False caso contrário
        """
        try:
            # Validar configurações
            self._validate_config()
            
            # Criar mensagem com partes alternativas
            # Mudança: Usando 'mixed' em vez de 'alternative' para suportar anexos
            msg = MIMEMultipart('mixed')
            msg['From'] = self.smtp_config['username']
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Criar a parte alternativa para texto/html
            alt_part = MIMEMultipart('alternative')
            
            # Adicionar versão texto simples
            alt_part.attach(MIMEText(body, 'plain'))
            
            # Se tiver corpo HTML, usa ele
            if html_body:
                alt_part.attach(MIMEText(html_body, 'html'))
            # Caso contrário, se tiver informações da empresa, cria um HTML formatado
            elif company_info:
                html_content = self._create_formatted_email(company_info, files_info)
                alt_part.attach(MIMEText(html_content, 'html'))
            
            # Adiciona a parte alternativa à mensagem principal
            msg.attach(alt_part)
            
            # Adicionar anexos
            if attachments:
                for attachment_path in attachments:
                    self._attach_file(msg, attachment_path)
            
            # Conectar ao servidor SMTP
            server = self._connect_to_smtp()
            
            # Enviar email
            server.sendmail(msg['From'], to_email, msg.as_string())
            server.quit()
            
            self.logger.info(f"Email enviado com sucesso para {to_email}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao enviar email: {e}")
            return False
    
    def _create_formatted_email(self, company_info, files_info):
        """
        Cria um email formatado em HTML com as informações da empresa e dos arquivos.
        
        Args:
            company_info (dict): Informações da empresa
            files_info (dict): Informações dos arquivos
            
        Returns:
            str: Conteúdo HTML do email
        """
        # Extrair informações
        company_name = company_info.get('name', '')
        document_id = company_info.get('document_id', '')
        period = company_info.get('period', '')
        
        # Formatar lista de arquivos
        files_html = ""
        if files_info:
            found_nfce = files_info.get('nfce_count', 0)
            found_nfe = files_info.get('nfe_count', 0)
            
            files_html = f"<p><strong>Arquivos encontrados:</strong></p>"
            
            if found_nfce > 0:
                files_html += f"<p>NFC-e: {found_nfce} arquivo(s)</p>"
            else:
                files_html += "<p>NFC-e: Nenhum arquivo localizado</p>"
                
            if found_nfe > 0:
                files_html += f"<p>NF-e: {found_nfe} arquivo(s)</p>"
            else:
                files_html += "<p>NF-e: Nenhum arquivo localizado</p>"
        
        # Criar HTML
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                h2 {{ color: #2a5885; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .footer {{ margin-top: 30px; font-size: 12px; color: #777; border-top: 1px solid #eee; padding-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Arquivos XML</h2>
                <p>Olá,</p>
                <p>Segue em anexo os arquivos XML compactados para o período solicitado.</p>
                
                <table>
                    <tr>
                        <th>Empresa:</th>
                        <td>{company_name}</td>
                    </tr>
                    <tr>
                        <th>CNPJ:</th>
                        <td>{document_id}</td>
                    </tr>
                    <tr>
                        <th>Período(s):</th>
                        <td>{period}</td>
                    </tr>
                </table>
                
                {files_html}
                
                <div class="footer">
                    <p>Esta é uma mensagem automática, por favor não responda este e-mail.</p>
                    <p>Em caso de dúvidas, entre em contato com o suporte técnico: <a href="https://suportebel.com.br">suportebel.com.br</a></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def test_connection(self):
        """
        Testa a conexão com o servidor SMTP.
        
        Returns:
            bool: True se a conexão foi bem-sucedida, False caso contrário
        """
        try:
            self._validate_config()
            
            # Definir um timeout menor para testes
            original_timeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(15)
            
            try:
                server = self._connect_to_smtp()
                server.quit()
                
                self.logger.info("Teste de conexão SMTP realizado com sucesso")
                return True
            finally:
                # Restaurar timeout original
                socket.setdefaulttimeout(original_timeout)
        
        except Exception as e:
            self.logger.error(f"Falha no teste de conexão SMTP: {e}")
            return False
    
    def _validate_config(self):
        """
        Valida as configurações SMTP.
        
        Raises:
            ValueError: Se alguma configuração estiver faltando
        """
        required_fields = ['server', 'port', 'username', 'password']
        missing_fields = [field for field in required_fields if not self.smtp_config.get(field)]
        
        if missing_fields:
            error_msg = f"Configurações SMTP incompletas. Campos faltando: {', '.join(missing_fields)}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
    
    def _connect_to_smtp(self):
        """
        Conecta ao servidor SMTP.
        
        Returns:
            smtplib.SMTP: Objeto de conexão com servidor SMTP
            
        Raises:
            Exception: Se ocorrer um erro na conexão
        """
        server = self.smtp_config['server']
        port = int(self.smtp_config['port'])
        username = self.smtp_config['username']
        password = self.smtp_config['password']
        use_ssl = self.smtp_config.get('use_ssl', False)
        
        # Correção específica para o Gmail
        if 'gmail.com' in server.lower():
            return self._connect_to_gmail(server, port, username, password, use_ssl)
        
        # Log para depuração
        self.logger.debug(f"Tentando conectar ao servidor SMTP: {server}:{port}, SSL: {use_ssl}")
        
        try:
            # Conexão padrão
            if use_ssl:
                # Para conexões com SSL (geralmente porta 465)
                context = ssl.create_default_context()
                smtp = smtplib.SMTP_SSL(server, port, timeout=30, context=context)
                self.logger.debug("Conexão SSL estabelecida")
            else:
                # Para conexões com TLS (geralmente porta 587)
                smtp = smtplib.SMTP(server, port, timeout=30)
                smtp.ehlo()
                if smtp.has_extn('STARTTLS'):
                    context = ssl.create_default_context()
                    smtp.starttls(context=context)
                    smtp.ehlo()
                    self.logger.debug("Conexão TLS estabelecida")
                else:
                    self.logger.debug("Servidor não suporta STARTTLS")
            
            # Login
            self.logger.debug(f"Autenticando com usuário: {username}")
            smtp.login(username, password)
            self.logger.debug("Autenticação bem-sucedida")
            
            return smtp
        
        except smtplib.SMTPAuthenticationError as e:
            error_msg = (
                f"Erro de autenticação SMTP: {str(e)}. "
                "Verifique seu usuário e senha. "
                "Se estiver usando Gmail, certifique-se de ter gerado uma senha de aplicativo."
            )
            self.logger.error(error_msg)
            raise Exception(error_msg)
        
        except smtplib.SMTPException as e:
            error_msg = f"Erro SMTP: {str(e)}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
        
        except (socket.gaierror, socket.timeout) as e:
            error_msg = f"Erro de conexão: {str(e)}. Verifique o servidor e porta."
            self.logger.error(error_msg)
            raise Exception(error_msg)
        
        except ssl.SSLError as e:
            error_msg = f"Erro SSL: {str(e)}. Tente ajustar a configuração 'Usar SSL'."
            self.logger.error(error_msg)
            raise Exception(error_msg)
        
        except Exception as e:
            error_msg = f"Erro ao conectar ao servidor SMTP ({server}:{port}): {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
    
    def _connect_to_gmail(self, server, port, username, password, use_ssl):
        """
        Conexão específica para o Gmail.
        
        Args:
            server (str): Servidor SMTP
            port (int): Porta
            username (str): Usuário
            password (str): Senha
            use_ssl (bool): Se deve usar SSL
            
        Returns:
            smtplib.SMTP: Objeto de conexão com servidor SMTP
        """
        self.logger.debug("Detectado servidor Gmail. Usando configurações específicas.")
        
        # Para Gmail, recomendamos ajustar as portas de acordo com o protocolo
        if use_ssl:
            # Se usar SSL, força a porta 465
            if port != 465:
                self.logger.warning(f"Porta {port} não é recomendada para Gmail com SSL. Alterando para 465.")
                port = 465
        else:
            # Se não usar SSL (preferir TLS), força a porta 587
            if port != 587:
                self.logger.warning(f"Porta {port} não é recomendada para Gmail com TLS. Alterando para 587.")
                port = 587
        
        try:
            context = ssl.create_default_context()
            
            if use_ssl or port == 465:
                # Usar SSL (porta 465)
                self.logger.debug(f"Conectando ao Gmail via SSL na porta {port}")
                smtp = smtplib.SMTP_SSL(server, port, timeout=30, context=context)
            else:
                # Usar TLS (porta 587)
                self.logger.debug(f"Conectando ao Gmail via TLS na porta {port}")
                smtp = smtplib.SMTP(server, port, timeout=30)
                smtp.ehlo()
                smtp.starttls(context=context)
                smtp.ehlo()
            
            # Login
            self.logger.debug(f"Tentando login para: {username}")
            smtp.login(username, password)
            self.logger.debug("Login no Gmail bem-sucedido")
            
            return smtp
        
        except smtplib.SMTPAuthenticationError:
            error_msg = (
                "Erro de autenticação no Gmail. "
                "Verifique se você gerou uma senha de aplicativo nas configurações de segurança da sua conta Google. "
                "Acesse: https://myaccount.google.com/security > Verificação em duas etapas > Senhas de app"
            )
            self.logger.error(error_msg)
            raise Exception(error_msg)
        
        except ssl.SSLError as e:
            if "WRONG_VERSION_NUMBER" in str(e):
                error_msg = (
                    f"Erro SSL com o Gmail: {str(e)}. "
                    f"Este erro geralmente ocorre quando se tenta usar o protocolo errado para a porta {port}. "
                    "Para o Gmail: "
                    "- Use a porta 465 com SSL ligado, ou "
                    "- Use a porta 587 com SSL desligado (TLS)"
                )
            else:
                error_msg = f"Erro SSL ao conectar ao Gmail: {e}"
            
            self.logger.error(error_msg)
            raise Exception(error_msg)
        
        except Exception as e:
            error_msg = f"Erro ao conectar ao Gmail: {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
    
    def _attach_file(self, msg, file_path):
        """
        Anexa um arquivo à mensagem de email.
        
        Args:
            msg (MIMEMultipart): Mensagem de email
            file_path (str): Caminho do arquivo a ser anexado
            
        Raises:
            FileNotFoundError: Se o arquivo não existir
        """
        if not os.path.exists(file_path):
            error_msg = f"Arquivo não encontrado: {file_path}"
            self.logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        try:
            with open(file_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            
            # Adicionar cabeçalho ao anexo
            filename = os.path.basename(file_path)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{filename}"',
            )
            
            msg.attach(part)
            self.logger.debug(f"Arquivo anexado: {filename}")
        
        except Exception as e:
            error_msg = f"Erro ao anexar arquivo {file_path}: {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)