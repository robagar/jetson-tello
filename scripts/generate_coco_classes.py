#!/usr/bin/env python3

# assumes https://github.com/dusty-nv/jetson-inference is checked out next to jetson-tello 
with open('../../jetson-inference/data/networks/ssd_coco_labels.txt', 'r') as f:
    labels = [l.rstrip() for l in f]


with open('../jetson_tello/coco/classes.py', 'w') as f:
    f.write('''from collections import namedtuple

CocoClass = namedtuple('CocoClass', 'id name')

coco_classes_by_id = [
''')
    n = len(labels)
    for i,l in enumerate(labels):
        f.write(f'    CocoClass({i}, "{l}")')
        if i < n-1:
            f.write(',')
        f.write('\n')
    f.write(']\n')

    f.write('''

coco_classes_by_name = {
''')
    n = len(labels)
    for i,l in enumerate(labels):
        f.write(f'    "{l}": coco_classes_by_id[{i}]')
        if i < n-1:
            f.write(',')
        f.write('\n')
    f.write('}\n')            