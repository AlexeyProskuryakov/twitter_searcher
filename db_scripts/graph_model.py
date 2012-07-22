__author__ = 'Alesha'
class node(object):
    def __init__(self, content):
        self.information_element = create_information_element(content)
        self.index = get_node_index()


class vertex(object):
    def __init__(self):
        self.index = gt_vertex_index()


class information_stream(object):
    def __init__(self):
        self.vertices = []
        self.nodes = []

    def get_n_I(self):
        return len(self.nodes)

    def get_n_R(self):
        return len(self.vertices)