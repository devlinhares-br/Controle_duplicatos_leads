from app.exceptions.exceptions import TokenInvalido
from datetime import datetime
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
      
    def activit(self, ENTITY_IDS, ENTITY_TYPE_ID=1, TYPE_ID=5):
        ids = ','.join(ENTITY_IDS)
        link = f"{os.getenv('domain')}crm/lead/merge/?id={ids}"
        now = datetime.now()
        r = []
        for ENTITY_ID in ENTITY_IDS:
            fields = { 
                        "COMMUNICATIONS": [{'VALUE': "Conflito ao tentar mesclar Leads", 'ENTITY_ID': ENTITY_ID, "ENTITY_TYPE_ID": ENTITY_TYPE_ID}],
                        "TYPE_ID": TYPE_ID,
                        "SUBJECT": "Confilto ao mesclar Leads",
                        "START_TIME": now.strftime('%Y-%m-%dT%H:%M:%S+00:00'),
                        "COMPLETED": "N",
                        "PRIORITY": 3,
                        "RESPONSIBLE_ID": 1,
                        "DESCRIPTION": f"<a href='{link}'>Leads para mesclar</a>",
                        "DESCRIPTION_TYPE": 3
                    }
            field_strings = []
            for k, v in fields.items():
                if k == "COMMUNICATIONS":
                    for i, comm in enumerate(v):
                        for k2, v2 in comm.items():
                            field_strings.append(f"fields[{k}][{i}][{k2}]={v2}")
                else:
                    field_strings.append(f"fields[{k}]={v}")

            # Join the list of formatted strings with the "&" character to create the URL string
            query_string = "&".join(field_strings)
            print(query_string)
            response = requests.get(f'{os.getenv("baseurl")}crm.activity.add.json?{query_string}')
            r.append(response.json())
        return {'results': r}
            