# Sistema de Gestão Documental Escolar

Este repositório contém o código-fonte de um sistema simples para controle de protocolos e ofícios, desenvolvido em Python com integração a um banco de dados MySQL. O projeto foi criado como parte da disciplina de Projeto Integrador do curso de Ciências de Dados da Universidade Virtual do Estado de São Paulo (UNIVESP), com o objetivo de otimizar a gestão documental na Escola Cooperativa Educacional de Novo Horizonte, substituindo processos manuais ineficientes.

## Autores

* **Vinícius Franco Ferreira** 
* **Márcio José Valderrama** 
* **Gabriel Pereira Job** 
* **André Henrique Torres de Araújo** 
* **Benício Rogério de Oliveira** 

## Sobre o Projeto

O sistema foi concebido para resolver desafios específicos enfrentados pela Escola Cooperativa Educacional de Novo Horizonte, como a desorganização, a potencial perda de informações e a dificuldade no acompanhamento de documentos (protocolos, ofícios e remessas). A solução proposta é um sistema informatizado que oferece funcionalidades para registro, organização, busca, acompanhamento e geração de relatórios de documentos, visando aumentar a eficiência e a transparência administrativa da escola.

## Funcionalidades Implementadas

O protótipo inicial do sistema, desenvolvido em Python, oferece as seguintes funcionalidades através de uma interface de linha de comando:

* **Login de Usuário:** Autenticação para acesso seguro ao sistema.
* **Listagem de Protocolos:** Exibe todos os protocolos registrados no banco de dados.
* **Adicionar Protocolo:** Permite o registro de novos documentos com informações detalhadas (número, data, tipo, remetente, destinatário, assunto, status).
* **Editar Protocolo:** Possibilita a atualização de dados de um protocolo existente.
* **Deletar Protocolo:** Remove um protocolo do sistema.
* **Detalhes do Protocolo:** Exibe todas as informações de um protocolo específico.
* **Relatórios em Tela:** Gera estatísticas e resumos dos protocolos por status e tipo diretamente no console.
* **Gerar Relatório PDF:** Exporta os dados dos protocolos para um arquivo PDF, facilitando a impressão e o arquivamento.

## Tecnologias Utilizadas

* **Python:** Linguagem de programação principal para o desenvolvimento do sistema.
* **MySQL:** Sistema de Gerenciamento de Banco de Dados Relacional (SGBD) utilizado para armazenar e gerenciar as informações dos protocolos.
* **`mysql.connector`:** Biblioteca Python para conexão e interação com o banco de dados MySQL.
* **`fpdf`:** Biblioteca Python para geração de arquivos PDF.
* **`getpass`:** Módulo Python para entrada de senha de forma segura.
* **`traceback` e `sys`:** Módulos para tratamento e exibição de erros.

## Como Executar o Projeto

### Pré-requisitos

Para executar este projeto, você precisará ter instalado em seu ambiente:

* **Python 3.x**
* **MySQL Server** (ou acesso a um servidor MySQL remoto)

### Instalação das Dependências

Utilize `pip` para instalar as bibliotecas Python necessárias:

```bash
pip install mysql-connector-python fpdf
