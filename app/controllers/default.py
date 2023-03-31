from app import app
from app.controllers.bitrix24 import Bitrix24
from app.exceptions.exceptions import TokenInvalido
from flask import request, Response
import json


@app.route('/')
def index():
    return gera_response(401, 'return', {}, 'Não autorizado!')


@app.route('/controle_duplicatos_leads', methods=['POST'])
def controle_lead():
    data = request.form.to_dict()
    try:
        b24 = Bitrix24(data['auth[application_token]'])
    except TokenInvalido:
        return gera_response(401, 'return', {}, 'Não autorizado!')
    lead = b24.get_lead(data['data[FIELDS][ID]'])
    if lead['HAS_PHONE'] == 'Y':
        params = {
            'filter[PHONE]': lead['PHONE'][0]['VALUE'],
            'filter[OPENED]': 'Y',
            'select[]': 'ID',
            'order[ID]': 'DESC'
        }
    else:
        return gera_response(200, 'return', {}, 'Sem telefone')
    leads = b24.list_leads(**params)
    if(len(leads) <= 1):
        return gera_response(200, 'return', {}, 'Sem duplicatos')
    merge = b24.merge()
    if merge['result']['STATUS'] == 'SUCCESS':
        return gera_response(200, 'return', merge['result']['STATUS'], 'Sem duplicatos')
    elif merge['result']['STATUS'] == 'CONFLICT':
        comments = b24.comments(ENTITY_IDS=leads)
        print(comments)
        return gera_response(200, 'return', comments, 'Sem duplicatos')

def gera_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo
    if mensagem:
        body["msg"] = mensagem
    
    return Response(json.dumps(body), status, mimetype="application/json")