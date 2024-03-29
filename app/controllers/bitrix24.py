from app.exceptions.exceptions import TokenInvalido
import os, requests, urllib.parse


class Bitrix24 ():
    
    def __init__(self, aplication_token):
        if not self.auth(aplication_token):
            raise TokenInvalido('Token inválido!')
        self.__aplication_token = aplication_token
        
    
    def auth(self, aplication_token):
        return True if aplication_token ==  os.getenv('token_webhook') else False
    
    def get_lead(self, id):
        response = requests.get(f'{os.getenv("baseurl")}crm.lead.get.json?ID={id}')
        return response.json()['result']
        
        
    def list_leads(self, **kwargs):
        query_string = urllib.parse.urlencode(kwargs)
        url = f'{os.getenv("baseurl")}crm.lead.list.json?{query_string}'
        response = requests.get(f'{url}')
        result = response.json()['result']
        self.leads = []
        self.leads_id = []
        for lead_id in result:
            id = lead_id['ID']
            self.leads_id.append(id)
        return self.leads_id
    
    def merge(self):

        entity_ids_params = [f'params[entityIds][]={id}' for id in self.leads_id]

        response = requests.get(f'{os.getenv("baseurl")}crm.entity.mergeBatch.json?params[entityTypeId]=1&{"&".join(entity_ids_params)}')
        return response.json()
      

    def get_phone(self, lead): 
        if lead['HAS_PHONE'] == 'Y':
                return lead['PHONE']['VALUE']
        else:
            return False
