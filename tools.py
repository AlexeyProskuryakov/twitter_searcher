__author__ = '4ikist'
def __get_count(input,x):
        return input.count(x)
def create_set_with_counts(input):
    return set(zip(input,[__get_count(input,x) for x in input]))

if __name__ =='__main__':
    print create_set_with_counts([1,1,3,4,5,6,6,6,7])
    
  