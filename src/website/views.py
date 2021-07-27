from flask import Blueprint, render_template, request, flash, redirect, url_for
import json
import requests
import pandas as pd
import numpy as np

views = Blueprint('views', __name__)

## -- PÁGINA INICIAL --
@views.route('/')
def home():
    """
    Rota inicial.
    Não é necessário modificar nada nessa função
    """
    return render_template('home.html')


@views.route('/clientes')
def clientes():
    """
    Rota para aba de clientes. Mostra na tela uma representação do csv de clientes
    Não é necessário modificar nada nessa função
    """
    df = pd.read_csv('data/clientes.csv', dtype=object, sep=';')
    df = df.replace(np.nan, '', regex=True)
    return render_template('clientes.html', df=df, titles=df.columns.values)


## -- CADASTRO --
@views.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    """
    Função para cadastro de novos clientes. Deverá pegar as informações do forms e salvar numa nova linha no csv.
    Necessário também salvar as informações de endereço provindas da API de CEP
    """
    if request.method == 'POST':
        ## Pega as informacoes do forms
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        email = request.form['email']
        cep = request.form['cep']
        ## Busca as informações de endereço da API do ViaCEP (https://viacep.com.br/)
        url = f'https://viacep.com.br/ws/{cep}/json/'
        response = requests.request('GET', url)
        content = response.content.decode('utf-8')
        content_json = json.loads(content)
        logradouro = (u'%s' % content_json['logradouro'])
        complemento = (u'%s' % content_json['complemento'])
        bairro = (u'%s' % content_json['bairro'])
        localidade = (u'%s' % content_json['localidade'])
        uf = (u'%s' % content_json['uf'])
        ibge = (u'%s' % content_json['ibge'])
        gia = (u'%s' % content_json['gia'])
        ddd = (u'%s' % content_json['ddd'])
        siafi = (u'%s' % content_json['siafi'])
        response.close()
        ## Cria nova linha no arquivo csv
        clients = pd.DataFrame([[nome,sobrenome,email,cep,logradouro,complemento,bairro,localidade,uf,ibge,gia,ddd,siafi]])
        clients.to_csv('data/clientes.csv', index=False, sep=';', mode='a', header=False)
        return render_template('cadastro.html')
    else:
        return render_template('cadastro.html')

## -- CONSULTA CEP --
@views.route('/consulta-cep', methods=['GET', 'POST'])
def consulta_cep():
    if request.method == 'POST':
        ## Pega o CEP do forms
        cep = request.form['cep']
        ## Busca as informações de endereço da API do ViaCEP (https://viacep.com.br/)
        url = f'https://viacep.com.br/ws/{cep}/json/'
        response = requests.request('GET', url)
        content = response.content.decode('utf-8')
        content_json = json.loads(content)
        logradouro = (u'%s' % content_json['logradouro'])
        complemento = (u'%s' % content_json['complemento'])
        bairro = (u'%s' % content_json['bairro'])
        localidade = (u'%s' % content_json['localidade'])
        uf = (u'%s' % content_json['uf'])
        ibge = (u'%s' % content_json['ibge'])
        gia = (u'%s' % content_json['gia'])
        ddd = (u'%s' % content_json['ddd'])
        siafi = (u'%s' % content_json['siafi'])
        response.close()
        ## Mostra no html as informações obtidas
        return render_template('consulta_cep.html', cep=cep,logradouro=logradouro,complemento=complemento,bairro=bairro,localidade=localidade,uf=uf,ibge=ibge,gia=gia,ddd=ddd,siafi=siafi)
    else:
        return render_template('consulta_cep.html')

    