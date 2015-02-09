
import mosaik.scenario


def child_with_eid(self,eid):
    """Returns the child with the given eid

    This method extends the mosaik.scenario.Entity class. It returns the a child
    of the entity with the given eid

    Args:
        eid: The eid for the child

    Returns:
        The child entity

    """
    children = self.children
    child = [e for e in children if e.eid == eid]
    return child[0]

def children_of_model(self,model):
    """Returns all children of the given model

    This method extends the mosaik.scenario.Entity class. It returns all children
    of the given model of the entity.

    Args:
        model: The model of the children

    Returns:
        A list of entities.

    """
    children = self.children
    children = [e for e in children if e.type == model]
    return children


mosaik.scenario.Entity.child_with_eid = child_with_eid
mosaik.scenario.Entity.children_of_model = children_of_model
