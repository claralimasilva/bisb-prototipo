from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from .info import get_topservice, get_amount, get_customersnum
from connection import get_db_connection
from .info import adm_check, get_saleschange

user_bp = Blueprint('user', __name__, template_folder='templates')

@user_bp.route('/customers')
def customers_page():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM salao.clientes
        ORDER BY id ASC;
    """)
    clientes = cur.fetchall()

    cur.close()
    conn.close()
    permission = adm_check()
    return render_template('customers.html', clientes=clientes, permission=permission)

@user_bp.route('/home')
def home_page():
    servico_mais_vendido = get_topservice()
    montante = get_amount()
    clientesnum = get_customersnum()
    salesChange = get_saleschange()
    permission = adm_check()
    return (render_template('home.html', servico_mais_vendido=servico_mais_vendido, montante=montante, 
                            clientesnum=clientesnum, salesChange=salesChange, permission=permission))

@user_bp.route('/services')
def services_page():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM salao.servicos
        ORDER BY id ASC;
    """)
    services = cur.fetchall()

    cur.close()
    conn.close()
    permission = adm_check()
    return render_template('services.html', services=services, permission=permission)

@user_bp.route('/sales')
def sales_page():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            v.id,
            v.id_cliente,
            v.id_servico,
            v.valor,
            v.forma_pagamento,
            v.data_venda,
            c.nome AS nome_cliente,
            s.nome_servico AS nome_servico
        FROM salao.vendas v
        JOIN salao.clientes c ON v.id_cliente = c.id
        JOIN salao.servicos s ON v.id_servico = s.id
        ORDER BY v.data_venda DESC;
    """)
    
    sales = cur.fetchall()

    cur.close()
    conn.close()
    permission = adm_check()
    return render_template('sales.html', sales=sales, permission=permission, path=request.path)

@user_bp.before_request
def check_authentication():
    flash('Você precisa estar logado')
    if 'token' not in session:
        return redirect(url_for('auth.login_page'))
