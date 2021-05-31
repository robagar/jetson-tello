from .classes import coco_classes_by_id, coco_classes_by_name

class InvalidCocoClassError(Exception):
    '''
    Exception raised if a COCO class could not identified from the given value. 
    '''
    def __init__(self, value):
        super().__init__(f'invalid COCO class: {value}')

def get_coco_class_by_id(id):
    '''
    COCO class from a class ID.

    :param id: The class ID
    :type id: int
    :rtype: :class:`jetson_tello.coco.classes.CocoClass`
    :throws: :class:`jetson_tello.coco.functions.InvalidCocoClassError`
    '''
    try:
        return coco_classes_by_id[id]
    except IndexError:
        pass
    raise InvalidCocoClassError(id)

def get_coco_class_by_name(name):
    '''
    COCO class from a class name.
    
    :param name: The class name
    :type name: string
    :rtype: :class:`jetson_tello.coco.classes.CocoClass`
    :throws: :class:`jetson_tello.coco.functions.InvalidCocoClassError`
    '''
    try:
        return coco_classes_by_name[name]
    except KeyError:
        pass
    raise InvalidCocoClassError(name)

def get_coco_class(value):
    '''
    COCO class from a class ID, name or object detection object.

    :param value: The class ID, name or object detection
    :type id: int, str or :class:`detectNet.Detection`
    :rtype: :class:`jetson_tello.coco.classes.CocoClass`
    :throws: :class:`jetson_tello.coco.functions.InvalidCocoClassError`
    '''

    if isinstance(value, int):
        return get_coco_class_by_id(value)

    if isinstance(value, str):
        return get_coco_class_by_name(value)

    try:
        return get_coco_class_by_id(value.ClassID)
    except AttributeError:
        pass

    raise InvalidCocoClassError(value)     
