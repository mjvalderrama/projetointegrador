# seu_projeto/app.py

from flask import Flask, render_template, request, redirect, url_for, session, send_file
import mysql.connector
import getpass # getpass não é mais necessário para web, a senha virá do formulário
from fpdf import FPDF
import traceback
import sys
import os # Para manipulação de caminhos de arquivo, se necessário para PDF

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_super_segura' # Mude para uma chave secreta real!

# Configurações do Banco de Dados (coloque suas credenciais aqui)
DB_CONFIG = {
    'host':'127.0.0.1',  
    'user':'root',    
    'password':'',         
    'database':'protocolo' 
  }

# Conexão com o banco de dados MySQL
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print("\nERRO AO CONECTAR AO BANCO DE DADOS:")
        print(f"Tipo do erro: {type(e).__name__}")
        print(f"Descrição do erro: {str(e)}")
        print("\nDetalhes completos do erro:")
        traceback.print_exc()
        # Em uma aplicação web real, você pode querer renderizar uma página de erro ou logar isso de forma mais elegante.
        return None

# --- Rotas da Aplicação ---

@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        conn = get_db_connection()
        if conn is None:
            return render_template('login.html', error="Erro de conexão com o banco de dados.")

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s", (email, senha))
            usuario = cursor.fetchone()
            if usuario:
                session['logged_in'] = True
                session['user_id'] = usuario[0]
                session['user_name'] = usuario[1]
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error="Credenciais inválidas.")
        except Exception as e:
            print(f"Erro no login: {e}")
            traceback.print_exc()
            return render_template('login.html', error="Erro interno ao tentar fazer login.")
        finally:
            cursor.close()
            conn.close()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('login'))

@app.before_request
def require_login():
    if request.endpoint not in ['login', 'static'] and not session.get('logged_in'):
        return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', user_name=session.get('user_name'))

@app.route('/protocolos')
def listar_protocolos():
    conn = get_db_connection()
    if conn is None:
        return "Erro de conexão com o banco de dados.", 500
    cursor = conn.cursor()
    cursor.execute("SELECT id, numero, data, tipo, status FROM protocolos")
    protocolos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('listar_protocolos.html', protocolos=protocolos)

@app.route('/protocolos/adicionar', methods=['GET', 'POST'])
def adicionar_protocolo():
    if request.method == 'POST':
        numero = request.form['numero']
        data = request.form['data']
        tipo = request.form['tipo']
        remetente = request.form['remetente']
        destinatario = request.form['destinatario']
        assunto = request.form['assunto']
        status = request.form['status']

        conn = get_db_connection()
        if conn is None:
            return "Erro de conexão com o banco de dados.", 500
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO protocolos (numero, data, tipo, remetente, destinatario, assunto, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (numero, data, tipo, remetente, destinatario, assunto, status))
            conn.commit()
            return redirect(url_for('listar_protocolos'))
        except Exception as e:
            conn.rollback()
            print(f"Erro ao adicionar protocolo: {e}")
            traceback.print_exc()
            return render_template('adicionar_protocolo.html', error="Erro ao adicionar protocolo.")
        finally:
            cursor.close()
            conn.close()
    return render_template('adicionar_protocolo.html')

@app.route('/protocolos/editar/<int:id>', methods=['GET', 'POST'])
def editar_protocolo(id):
    conn = get_db_connection()
    if conn is None:
        return "Erro de conexão com o banco de dados.", 500
    cursor = conn.cursor(dictionary=True) # Retorna como dicionário para facilitar acesso
    
    if request.method == 'POST':
        numero = request.form['numero']
        data = request.form['data']
        tipo = request.form['tipo']
        remetente = request.form['remetente']
        destinatario = request.form['destinatario']
        assunto = request.form['assunto']
        status = request.form['status']

        try:
            cursor.execute("UPDATE protocolos SET numero=%s, data=%s, tipo=%s, remetente=%s, destinatario=%s, assunto=%s, status=%s WHERE id=%s",
                           (numero, data, tipo, remetente, destinatario, assunto, status, id))
            conn.commit()
            return redirect(url_for('listar_protocolos'))
        except Exception as e:
            conn.rollback()
            print(f"Erro ao editar protocolo: {e}")
            traceback.print_exc()
            cursor.execute("SELECT * FROM protocolos WHERE id = %s", (id,))
            protocolo = cursor.fetchone()
            return render_template('editar_protocolo.html', protocolo=protocolo, error="Erro ao editar protocolo.")
        finally:
            cursor.close()
            conn.close()
    else: # GET request
        cursor.execute("SELECT * FROM protocolos WHERE id = %s", (id,))
        protocolo = cursor.fetchone()
        cursor.close()
        conn.close()
        if not protocolo:
            return "Protocolo não encontrado.", 404
        return render_template('editar_protocolo.html', protocolo=protocolo)

@app.route('/protocolos/deletar/<int:id>', methods=['POST'])
def deletar_protocolo(id):
    conn = get_db_connection()
    if conn is None:
        return "Erro de conexão com o banco de dados.", 500
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM protocolos WHERE id = %s", (id,))
        conn.commit()
        return redirect(url_for('listar_protocolos'))
    except Exception as e:
        conn.rollback()
        print(f"Erro ao deletar protocolo: {e}")
        traceback.print_exc()
        return "Erro ao deletar protocolo.", 500
    finally:
        cursor.close()
        conn.close()

@app.route('/protocolos/detalhes/<int:id>')
def detalhes_protocolo(id):
    conn = get_db_connection()
    if conn is None:
        return "Erro de conexão com o banco de dados.", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM protocolos WHERE id = %s", (id,))
    protocolo = cursor.fetchone()
    cursor.close()
    conn.close()
    if not protocolo:
        return "Protocolo não encontrado.", 404
    return render_template('detalhes_protocolo.html', protocolo=protocolo)

@app.route('/relatorios')
def relatorios():
    conn = get_db_connection()
    if conn is None:
        return "Erro de conexão com o banco de dados.", 500
    cursor = conn.cursor()

    total = 0
    pendentes = 0
    recebidos = 0
    finalizados = 0
    tipos = []

    try:
        cursor.execute("SELECT COUNT(*) FROM protocolos")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM protocolos WHERE status = 'Pendente'")
        pendentes = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM protocolos WHERE status = 'Recebido'")
        recebidos = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM protocolos WHERE status = 'Finalizado'")
        finalizados = cursor.fetchone()[0]
        cursor.execute("SELECT tipo, COUNT(*) FROM protocolos GROUP BY tipo")
        tipos = cursor.fetchall()
    except Exception as e:
        print(f"Erro ao gerar relatórios: {e}")
        traceback.print_exc()
    finally:
        cursor.close()
        conn.close()

    return render_template('relatorios.html', 
                           total=total, 
                           pendentes=pendentes, 
                           recebidos=recebidos, 
                           finalizados=finalizados, 
                           tipos=tipos)

@app.route('/gerar_pdf')
def gerar_pdf():
    conn = get_db_connection()
    if conn is None:
        return "Erro de conexão com o banco de dados.", 500
    cursor = conn.cursor()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Relatório de Protocolos", ln=True, align='C')

    try:
        cursor.execute("SELECT numero, data, tipo, remetente, destinatario, status FROM protocolos")
        for row in cursor.fetchall():
            linha = f"Número: {row[0]}, Data: {row[1]}, Tipo: {row[2]}, Remetente: {row[3]}, Destinatário: {row[4]}, Status: {row[5]}"
            pdf.multi_cell(0, 10, linha)
        
        pdf_output_path = "relatorio_protocolos.pdf"
        pdf.output(pdf_output_path)
        return send_file(pdf_output_path, as_attachment=True, download_name="relatorio_protocolos.pdf")
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        traceback.print_exc()
        return "Erro ao gerar relatório PDF.", 500
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    from waitress import serve # Importe serve do waitress
    print("Iniciando o servidor Waitress...")
    serve(app, host="127.0.0.1", port=5000) # 'app' é a instância do seu aplicativo Flask