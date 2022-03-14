# "NodeTexture Viewer" Blender Addon.
# Copyright (C) 2021, Rodrigo Gama, Kuimi 3D
#
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    "name": "NodeTexture Viewer",
    "author": "Rodrigo Gama, Kuimi3D",
    "version": (1, 0, 0),
    "blender": (2, 92, 0),
    "location": "Image Editor Header",
    "description": "Simply Opens Selected Texture in Image Editor",
    "wiki_url": "https://help.kuimi3d.com/docs/nodetexture-viewer/",
    "tracker_url": "https://help.kuimi3d.com/bug-report/",
    "category": "Interface"}

import bpy

def find_in_group(n):
    for i in n.node_tree.nodes:
        if i.select:
            if i.type != 'GROUP' and i.type == 'TEX_IMAGE':
                return i
            if i.type == 'GROUP':
                return find_in_group(i)

class Open_Selected_Node(bpy.types.Operator):
    bl_idname = "sa.openimage"
    bl_label = "Open Selected Texture"
    bl_description = "Open Texture of selected texture node"
    bl_options = {"REGISTER"}

    def execute(self, context):
        
        img_found = '0'           
        ob = context.active_object
        
        if ob:
            ob = context.active_object
            if ob.active_material:
                mat = ob.active_material
                if mat.node_tree:
                    text_node = find_in_group(mat)                  
                    if text_node:  
                        if text_node.image:
                            if text_node.image.size[1] > 0:
                                try:
                                    img = bpy.data.images.get(text_node.image.name)
                                    img_found = '1'
                                except:
                                    img_found = '2' 
                            else:
                                img_found = '2'
                                                                                            
        if img_found == '1':                        
            bpy.context.area.spaces.active.image = img
            
        if img_found == '2': 
            self.report({'ERROR'},
                                    "Could not load this texture")
            return {'CANCELLED'} 
        
        if img_found == '0': 
            self.report({'ERROR'},
                                    "No Texture Selected")
            return {'CANCELLED'} 
        
        return {"FINISHED"}


def draw(self, context):
    self.layout.separator()
    self.layout.operator(Open_Selected_Node.bl_idname,text='Selected Node',icon='NODE_TEXTURE')

classes = (Open_Selected_Node,)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.IMAGE_MT_editor_menus.append(draw)

def unregister():
    bpy.types.IMAGE_MT_editor_menus.remove(draw)
    
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()