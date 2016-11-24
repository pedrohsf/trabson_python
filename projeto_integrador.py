#coding: utf-8


import sys
from wit import Wit
import json
import ast
import random

if len(sys.argv) != 2:
    print('usage: python ' + sys.argv[0] + ' <wit-token>')
    exit(1)
access_token = sys.argv[1]

# Quickstart example
# See https://wit.ai/ar7hur/Quickstart

def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def send(request, response):
    print(response['text'])

def get_forecast(request):
    context = request['context']
    entities = request['entities']

    loc = first_entity_value(entities, 'location')
    if loc:
        context['forecast'] = 'sunny'
        if context.get('missingLocation') is not None:
            del context['missingLocation']
    else:
        context['missingLocation'] = True
        if context.get('forecast') is not None:
            del context['forecast']

    return context









#TRANSFORMA EM DICIONARIO A REQUEST / MANIPULAR MAIS FACIL
def request_to_dict(transform):
	new_dict = ast.literal_eval(      json.dumps(transform)    )
	return new_dict
	

	
#NOTAS
def saberNotas(recived):
	context = {} 
	retorno = request_to_dict( recived['entities'] )	
	context['nota'] = notas( retorno['nome'][0]['value'] )
	context['nome'] = retorno['nome'][0]['value']
	return context

def notas(nome):
	if nome == 'pedro':
		return 10
	if nome == 'dillei':
		return 0
#FIM NOTAS



		
		
#FINANCEIRO
def financeiro(recived):
	context = {} 
	retorno = request_to_dict( recived['entities'] )	
	context['meu_financeiro'] = meu_financeiro( retorno['nome'][0]['value'] )
	context['nome'] = retorno['nome'][0]['value']
	return context

def meu_financeiro(nome):
	if nome == 'pedro':
		return 'você não deve nada para a faculdade'
	elif nome == 'dillei':
		return 'você está devendo boleta desse mes' 
	else:
		return 'você não está cadastrado no nosso sistema'
#FIM FINANCEIRO
	
	
#RESOLVE INTENÇÂO
def resolve_intent(recived):
	context = {} 
	
	try:
		retorno = request_to_dict( recived['entities'] )	
		context[ possiveis_intents( retorno['intent'][0]['value'] ) ] = possiveis_intents( retorno['intent'][0]['value'] )
	except:
		context['idk'] = True
	return context


def possiveis_intents(possiveis):
	if possiveis == 'nota':
		return 'nota'
	elif possiveis == 'financeiro':
		return 'financeiro'
	elif possiveis == 'atividade':
		return 'atividade'
	elif possiveis == 'falta':
		return 'falta'
	else:
		return 'idk'
#FIM RESOLVE INTENÇÂO


#CRIA IDK PARA RESETAR A CONVERSA
def sair_fora(recived):
	context = {}
	context['idk'] = True
	return context



#FALTAS
def saber_faltas(recived):
	context = {} 
	retorno = request_to_dict( recived['entities'] )	
	context['falta'] = minhas_faltas( retorno['nome'][0]['value'] )
	return context

def minhas_faltas(nome):
		return nome +' você tem ' + str( int(random.random() *10) ) + ' faltas'
#FIM FALTAS


#ATIVIDADES
def saber_atividade(recived):
	context = {} 
	retorno = request_to_dict( recived['entities'] )	
	
	context['nome'] = retorno['nome'][0]['value']
	context['date_time'] = retorno['datetime'][0]['value'] 
	context['num_atividades'] = random_atividades() 
	
	print(context)
	
	return context
	
def random_atividades():
	return str ( int(random.random() * (random.random() * 10) ) ) + ' atividades'
	
#FIM ATIVIDADES
	
	
	
actions = {
	'send': send,
	'getForecast': get_forecast,
	'saberNotas': saberNotas,
	'saberFinanceiro' : financeiro,
	'resolve_intent' : resolve_intent,
	'sair_da_nota': sair_fora,
	'saberFaltas': saber_faltas,
	'saberAtividade': saber_atividade
}




client = Wit(access_token=access_token, actions=actions)
client.interactive()
