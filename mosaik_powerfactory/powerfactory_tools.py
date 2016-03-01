# Imports
import sys
import os
POWERFACTORY_PATH = "C:\\Program Files\\DIgSILENT\\PowerFactory 2016"
os.environ["PATH"] = POWERFACTORY_PATH + ";" + os.environ["PATH"]
sys.path.append(POWERFACTORY_PATH + "\\python\\3.5")
import powerfactory
import re
import json


# Constants
ATTRIBUTES_FILE = os.path.dirname(os.path.realpath(__file__)) +"\\elements_attributes.json"




def parse_attributes_list(source_file,element):
    """Parses a PowerFactory attributes file and add it to the
    elements_attributes.json

    Currently there is no method to get all attributes of and element in
    PowerFactory. This module add the method attributes_for_model to the
    PowerFactory.Application class, which returns the attributes saved in
    elements_attributes.json.
    Adding attributes to the file is done by this mehtod. It parses a saved
    attributes list of one element form PowerFactory and add the attributes to
    elements_attributes.json.

    Args:
        source_file: The path of a file containing the raw printed attributes
            list form PowerFactory
        element: The name of the element classs

    Returns:
        None
    """
    attr = None
    with open (source_file, "r") as sourceFile:
        data = sourceFile.read()
        attr = re.findall(r'[a-z]:[\w:]+',data)
        attr = list(set(attr))
        attr.sort()

    data = None
    with open (ATTRIBUTES_FILE, 'r') as destFile:
        data = json.load(destFile)

    with open (ATTRIBUTES_FILE, 'w') as destFile:
        data[element]=attr
        json.dump(data,destFile)

def attributes_for_model(model,attr_type=None):
    """Returns the attributes of a modell

    It returns the attributes of a modell saved in elemets_attributes.json.
    To add attributes to this file use the method
    powerfactory_tools.parse_attributes_list.

    Args:
        model: The name of the element class e.g. ElmLod
        attr_type: Optional parameter, to get only parameter of a special type,
            e.g. 'm'

    Returns:
        A list of attributes names of the element class

    """
    with open (ATTRIBUTES_FILE, 'r') as f:
        data = json.load(f)
        try:
            attrs = data[model]
        except KeyError:
            attrs = []

    if attr_type is not None:
        attrs = [attr for attr in attrs if attr.startswith(attr_type)]

    return attrs


def elements_of_model(self, model, name="*"):
    """Returns all elements of the model class

    This mehtod extends the powerfactor.Application class. And returns all
    calculation relevant elements of the given class in the active project.

    Args:
        model: The name of the element class e.g. ElmLod
        name: Optional parameter, to filter the names of the elements. It may
            contain "*"

    Returns:
        A list of powerfactory.DataObject matching the input parameter

    """
    if self.GetActiveProject() is None:
        raise Exception("You have first to activate a project")
    return self.GetCalcRelevantObjects('%s.%s' % (name, model),1,1)

def relevant_models(self, model="Elm*"):
    """Returns all model classes in the current project

    This mehtod extends the powerfactor.Application class. It returns all
    calculation relvant model classes of the active project

    Args:
        model: Optional parameter, to filter the model classes. It may contain a
            "*"

    Returns:
        A list of the model class names

    """
    elements = self.elements_of_model(model)
    models = [elem.GetClassName() for elem in elements]
    return list(set(models))

def get_grid(self,name):
    """Returns the grid with the given name.

    This mehtod extends the powerfactor.Application class. It returns the grid
    with the given name.

    Args:
        name: The name of the grid

    Returns:
        A powerfactory.DataObject of the grid with the given name

    """
    grids = self.elements_of_model("ElmNet",name)
    if not grids:
        raise Exception("No grid with name: %s" % name)
    if len(grids) > 1:
        raise Exception("Found more of one gird with name: %s" % name)
    return grids[0]

def element_with_unique_name(self,name):
    """Returns the element with unique_name

    This mehtod extends the powerfactor.Application class. It returns the
    element with the given unique_name.

    Args:
        name: The unique name of the element e.g. 'Netz\\Last.ElmLod'

    Returns:
        A powerfactory.DataObject with the element of unique_name
    """

    elements_names = name.split('\\')
    parrent = self.get_grid(elements_names[0])
    for e in elements_names[1:]:
        parrent = parrent.GetContents(e)[0]
    return parrent


powerfactory.Application.elements_of_model = elements_of_model
powerfactory.Application.relevant_models = relevant_models
powerfactory.Application.get_grid = get_grid
powerfactory.Application.element_with_unique_name = element_with_unique_name

# Additional Methods for the Data Object Class

def unique_name(self):
    """Returns the unique_name of the element

    This method extends the powerfactory.DataObject class. It returns the unique
    name of the element.

    Returns:
        The unique_name of the element

    """
    name = self.loc_name + "." + self.GetClassName()
    parrent = self.GetParent()
    while parrent.GetClassName() != 'IntPrjfolder':
        name = parrent.loc_name + "\\" + name
        parrent = parrent.GetParent()
    return name

def children_elements(self, name="*", model="Elm*"):
    """Returns all children elements of the object (Rekursiv)

    This method extends the powerfactor.DataObject class. It returns all
    rekursiv children of the object.

    Args:
        name: Optional parameter, it filters the name of the children, it may
        contain "*"
        mdoel: Optional parameter it filters teh model class of the children

    Retruns:
        List of powerfactory.DataObject with the children of the object
    """
    return self.GetContents("%s.%s" % (name, model),True)


def attributes(self,attr_type=None):
    """Return the attributes of the object

    Returns all attributes of the object from the elements_attributes.json

    Args:
        attr_type: Optional parameter, to get only parameter of a special type,
            e.g. 'm'

    Returns:
        A list of attributes of the object
    """
    class_name = self.GetClassName()
    return attributes_for_model(class_name,attr_type)


powerfactory.DataObject.unique_name = unique_name
powerfactory.DataObject.children_elements = children_elements
powerfactory.DataObject.attributes = attributes
