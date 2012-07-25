__author__ = '4ikist'

def __get_count(input,x):
        return input.count(x)

def create_set_with_counts(input):
    return set(zip(input,[__get_count(input,x) for x in input]))

def flush(data, by_what=lambda x:x.screen_name):
       """
       returning list of parameters which retrieving used lambda name
       """
       return [by_what(element) for element in data]

def get_by_name(from_,what, by_what=lambda x:x.screen_name):
       users = [e for e in from_ if what == by_what(e)]
       if len(users):
           return users[0]
       return None

def print_model_serializable(m_user):
    d = m_user.serialise()
    for el in d.items():
        print el[0],':',el[1]

if __name__ =='__main__':
    print create_set_with_counts([1,1,3,4,5,6,6,6,7])

