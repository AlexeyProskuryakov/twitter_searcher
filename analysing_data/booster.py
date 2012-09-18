from pymongo import ASCENDING
from analysing_data.markov_chain_machine import element
from model.db import db_handler

__author__ = 'Alesha'
class db_booster(db_handler):
    mc_element_name = 'mc_element'
    mc_element_f_content_name = 'content'

    mc_model_name = 'mc_model'

    def __init__(self, truncate = None, messages_truncate = None):
        db_handler.__init__(self, truncate, messages_truncate)
        self.mc_elements = self.db.create_collection(db_booster.mc_element_f_content_name)
        if not self._is_index_presented(self.mc_elements):
            self.mc_elements.create_index('content', ASCENDING, unique=False)
            self.mc_elements.create_index([
                ('content',ASCENDING),
                ('weight',ASCENDING),
                ('additional_obj',ASCENDING)],
                                             unque = True )

        self.mc_models = self.db.create_collection(db_booster.mc_model_name)


    def get_mc_elements(self,by_content,model_id_=None, by_list_in_content = True):
        if by_list_in_content:
            elements = self.mc_elements.find({self.mc_element_f_content_name:list(by_content),'model_id_':model_id_})
        else:
            query = by_content
            query['model_id_'] = model_id_
            elements = self.mc_elements.find(query)

        result = []
        for el in elements:
            el = element.create(el)
            result.append(el)
        return result

    def add_mc_element(self,element):
        if isinstance(element,list):
            l_dict = []
            for el in element:
                l_dict.append(el._serialise())
            self.mc_elements.save(l_dict)
        dict = element._serialise()
        self.mc_elements.save(dict)

    def get_mc_parameters(self,model_id_):
        return self.mc_models.find_one({'model_id_':model_id_})

    def add_mc_parameters(self,markov_chain):
        dict = markov_chain._serialise()
        self.mc_models.save(dict)