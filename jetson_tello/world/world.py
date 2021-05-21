from .thing import Thing

class WorldObserver:
    async def on_thing_detected(self, thing, is_new_thing):
        pass

class World:
    def __init__(self, observer = None):
        self._observer = observer
        self._things_by_coco_class_id = {}

    async def update_things(self, detected_objects):
        # for now there can only be one thing of a given class in the world
        for d in detected_objects:
            cid = d.ClassID
            m = self._things_by_coco_class_id
            try:
                thing = m[cid]
                thing.link_detected_object(d)
                is_new_thing = False
            except KeyError:
                thing = Thing(d)
                m[cid] = thing
                is_new_thing = True
            if self._observer:
                await self._observer.on_thing_detected(thing, is_new_thing)

    @property
    def things(self):
        return self._things_by_coco_class_id.values()

    def get_thing_of_class(id):
        return self._things_by_coco_class_id.get(id)
