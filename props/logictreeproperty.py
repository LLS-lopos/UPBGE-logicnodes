from bpy.props import StringProperty
from bpy.props import BoolProperty
from bpy.props import EnumProperty

from .property import propgroup
from .property import check_double_name
from bpy.types import PropertyGroup

import bpy


def _deferred_reload_components():
    try:
        bpy.ops.logic_nodes.reload_components()
    except Exception as e:
        print(f'[Logic Nodes] Could not reload components from property update: {e}')
    return None


_value_types = [
    ('0', 'Float', ''),
    ('1', 'String', ''),
    ('2', 'Integer', ''),
    ('3', 'Boolean', ''),
    None,
    ('4', 'Vector', ''),
    ('5', 'Color', ''),
    ('6', 'Color Alpha', ''),
    None,
    ('7', 'Object', ''),
    ('8', 'Collection', ''),
    ('9', 'Material', ''),
    ('10', 'Mesh', ''),
    ('11', 'Node Tree', ''),
    ('12', 'Action', ''),
    None,
    ('13', 'Text', ''),
    ('14', 'Sound', ''),
    ('15', 'Image', ''),
    ('16', 'Font', ''),
    None,
    ('17', 'List', '')
]


def check_double_prop(self, context):
    tree = getattr(context.space_data, 'edit_tree', None)
    if tree:
        # for node in tree.nodes:
        #     if node.bl_idname == 'LogicNodeGetLogicTreeProperty':
        #         if node.inputs[0].default_value == 
        tree.changes_staged = True
        check_double_name(self, tree.properties)
        bpy.app.timers.register(_deferred_reload_components)
    else:
        print('No Tree Found')


def update_tree(self, context):
    if context is None:
        print('No Context Found')
        return
    tree = getattr(context.space_data, 'edit_tree', None)
    if tree:
        tree.update_draw(context)
        tree.changes_staged = True
        bpy.app.timers.register(_deferred_reload_components)
    else:
        print('No Tree Found')


@propgroup
class LogicNodesLogicTreeProperty(PropertyGroup):
    value_type: EnumProperty(items=_value_types, name='Value Types', update=update_tree)
    name: StringProperty(default='Property', update=check_double_prop)
    show_prop: BoolProperty(
        default=True,
        name='Show Default',
        description='Show the default value for this property'
    )
    value: StringProperty(
        default='',
        name='List Items',
        description='Comma separated list of options, used when the value type is set to List',
        update=update_tree
    )
