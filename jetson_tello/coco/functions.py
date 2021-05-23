from .classes import coco_classes_by_id, coco_classes_by_name

class InvalidCocoClassError(Exception):
    def __init__(self, id_or_name):
        super().__init__(f'invalid COCO class: {id_or_name}')

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

def get_coco_class(id_or_name):
    if isinstance(id_or_name, str):
        return get_coco_class_by_name(id_or_name)
    else:
        return get_coco_class_by_id(id_or_name)
