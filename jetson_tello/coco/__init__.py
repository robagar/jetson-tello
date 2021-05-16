from .classes import coco_classes_by_id

class InvalidCocoClassError(Exception):
    def __init__(self, id):
        super().__init__(f'invalid COCO class id: {id}')

def get_coco_class(id):
    try:
        return coco_classes_by_id[id]
    except IndexError:
        pass
    raise InvalidCocoClassError(id)