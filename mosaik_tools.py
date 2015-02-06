
import mosaik.scenario


def child_with_eid(self,eid):
    children = self.children
    child = [e for e in children if e.eid == eid]
    return child[0]

def children_of_model(self,model):
    children = self.children
    children = [e for e in children if e.type == model]
    return children


mosaik.scenario.Entity.child_with_eid = child_with_eid
mosaik.scenario.Entity.children_of_model = children_of_model
