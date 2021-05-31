from .classes import coco_classes_by_id, coco_classes_by_name

class InvalidCocoClassError(Exception):
    def __init__(self, value):
        super().__init__(f'invalid COCO class: {value}')

def get_coco_class_by_id(id):
    try:
        return coco_classes_by_id[id]
    except IndexError:
        pass
    raise InvalidCocoClassError(id)

def get_coco_class_by_name(name):
    try:
        return coco_classes_by_name[name]
    except KeyError:
        pass
    raise InvalidCocoClassError(name)

def get_coco_class(value):

    if isinstance(value, int):
        return get_coco_class_by_id(value)

    if isinstance(value, str):
        return get_coco_class_by_name(value)

    try:
        return get_coco_class_by_id(value.ClassID)
    except AttributeError:
        pass

    raise InvalidCocoClassError(value)     
