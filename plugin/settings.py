import json
import bpy

from bpy_types import (PropertyGroup)
from bpy.props import (BoolProperty, StringProperty, PointerProperty, EnumProperty)

def update_scene_lists(self, context):                
    print("updating scene lists")
    # blenvy = self# context.window_manager.blenvy
    # blenvy.main_scene_names = [scene.name for scene in blenvy.main_scenes] # FIXME: unsure
    # blenvy.library_scene_names = [scene.name for scene in blenvy.library_scenes] # FIXME: unsure
    # upsert_settings(blenvy.settings_save_path, {"common_main_scene_names": [scene.name for scene in blenvy.main_scenes]})
    # upsert_settings(blenvy.settings_save_path, {"common_library_scene_names": [scene.name for scene in blenvy.library_scenes]})

def update_asset_folders(self, context):
    print("updating asset folders")
    # blenvy = context.window_manager.blenvy
    # asset_path_names = ['project_root_path', 'assets_path', 'blueprints_path', 'levels_path', 'materials_path']
    # for asset_path_name in asset_path_names:
    #     upsert_settings(blenvy.settings_save_path, {asset_path_name: getattr(blenvy, asset_path_name)})

def update_mode(self, context):
    print("updating mode")
    # blenvy = self # context.window_manager.blenvy
    # upsert_settings(blenvy.settings_save_path, {"mode": blenvy.mode })

class BevySettings(PropertyGroup):
    settings_save_path = ".bevy_settings" # where to store data in bpy.texts
    mode: EnumProperty(
        items=(
                ('COMPONENTS', "Components", ""),
                ('BLUEPRINTS', "Blueprints", ""),
                ('ASSETS', "Assets", ""),
                ('SETTINGS', "Settings", ""),
                ('TOOLS', "Tools", ""),
        ),
        update=update_mode
    ) # type: ignore    
    project_root_path: StringProperty(
        name = "Project Root Path",
        description="The root folder of your (Bevy) project (not assets!)",
        default='../',
        update= update_asset_folders
    ) # type: ignore

    assets_path: StringProperty(
        name='Export folder',
        description='The root folder for all exports(relative to the root folder/path) Defaults to "assets" ',
        default='./assets',
        options={'HIDDEN'},
        update= update_asset_folders
    ) # type: ignore

    blueprints_path: StringProperty(
        name='Blueprints path',
        description='path to export the blueprints to (relative to the assets folder)',
        default='blueprints',
        update= update_asset_folders
    ) # type: ignore

    levels_path: StringProperty(
        name='Levels path',
        description='path to export the levels (main scenes) to (relative to the assets folder)',
        default='levels',
        update= update_asset_folders
    ) # type: ignore

    materials_path: StringProperty(
        name='Materials path',
        description='path to export the materials libraries to (relative to the assets folder)',
        default='materials',
        update= update_asset_folders
    ) # type: ignore

    #main_scenes: CollectionProperty(name="main scenes", type=SceneSelector) # type: ignore
    #main_scenes_index: IntProperty(name = "Index for main scenes list", default = 0, update=update_scene_lists) # type: ignore
    #main_scene_names = [] # FIXME: unsure

    #library_scenes: CollectionProperty(name="library scenes", type=SceneSelector) # type: ignore
    #library_scenes_index: IntProperty(name = "Index for library scenes list", default = 0, update=update_scene_lists) # type: ignore
    #library_scene_names = [] # FIXME: unsure

    # sub ones
    #auto_export: PointerProperty(type=auto_export_settings.AutoExportSettings) # type: ignore
    #components: PointerProperty(type=bevy_component_settings.ComponentSettings) # type: ignore

    def is_scene_ok(self, scene):
        try:
            operator = bpy.context.space_data.active_operator
            return scene.name not in operator.main_scenes and scene.name not in operator.library_scenes
        except:
            return True
        
    @classmethod
    def register(cls):
        #bpy.types.WindowManager.main_scene = bpy.props.PointerProperty(type=bpy.types.Scene, name="main scene", description="main_scene_picker", poll=cls.is_scene_ok)
        #bpy.types.WindowManager.library_scene = bpy.props.PointerProperty(type=bpy.types.Scene, name="library scene", description="library_scene_picker", poll=cls.is_scene_ok)
        bpy.types.WindowManager.bevy = PointerProperty(type=BevySettings)

    @classmethod
    def unregister(cls):
        #del bpy.types.WindowManager.main_scene
        #del bpy.types.WindowManager.library_scene
        del bpy.types.WindowManager.bevy

    def load_settings(self):
        settings = load_settings(self.settings_save_path)
        if settings is not None:
            if "mode" in settings:
                self.mode = settings["mode"]
            if "common_main_scene_names" in settings:
                for main_scene_name in settings["common_main_scene_names"]:
                    added = self.main_scenes.add()
                    added.name = main_scene_name
            if "common_library_scene_names" in settings:
                for main_scene_name in settings["common_library_scene_names"]:
                    added = self.library_scenes.add()
                    added.name = main_scene_name

            asset_path_names = ['project_root_path', 'assets_path', 'blueprints_path', 'levels_path', 'materials_path']
            for asset_path_name in asset_path_names:
                if asset_path_name in settings:
                    setattr(self, asset_path_name, settings[asset_path_name])
        settings
        

        # target = row.box() if context.mode == 'COMPONENTS' else row
        # tool_switch_components = target.operator(operator="bevy.tooling_switch", text="", icon="PROPERTIES")
        # tool_switch_components.tool = "COMPONENTS"

        # target = row.box() if self.mode  == 'BLUEPRINTS' else row
        # tool_switch_components = target.operator(operator="bevy.tooling_switch", text="", icon="PACKAGE")
        # tool_switch_components.tool = "BLUEPRINTS"

        # target = row.box() if self.mode  == 'ASSETS' else row
        # tool_switch_components = target.operator(operator="bevy.tooling_switch", text="", icon="ASSET_MANAGER")
        # tool_switch_components.tool = "ASSETS"

        # target = row.box() if self.mode  == 'SETTINGS' else row
        # tool_switch_components = target.operator(operator="bevy.tooling_switch", text="", icon="SETTINGS")
        # tool_switch_components.tool = "SETTINGS"

        # target = row.box() if self.mode  == 'TOOLS' else row
        # tool_switch_components = target.operator(operator="bevy.tooling_switch", text="", icon="TOOL_SETTINGS")
        # tool_switch_components.tool = "TOOLS"

        # if self.mode == "SETTINGS": 
        #     row.label(text="main scenes")
            
            # header, panel = layout.panel("common", default_closed=False)
            # header.label(text="Common")
            # if panel:
            #     row = panel.row()
            #     draw_folder_browser(layout=row, label="Root Folder", prop_origin=blenvy, target_property="project_root_path")
            #     row = panel.row()
            #     draw_folder_browser(layout=row, label="Assets Folder", prop_origin=blenvy, target_property="assets_path")
            #     row = panel.row()
            #     draw_folder_browser(layout=row, label="Blueprints Folder", prop_origin=blenvy, target_property="blueprints_path")
            #     row = panel.row()
            #     draw_folder_browser(layout=row, label="Levels Folder", prop_origin=blenvy, target_property="levels_path")
            #     row = panel.row()
            #     draw_folder_browser(layout=row, label="Materials Folder", prop_origin=blenvy, target_property="materials_path")

            #     panel.separator()


            #     # scenes selection
            #     if len(blenvy.main_scenes) == 0 and len(blenvy.library_scenes) == 0:
            #         row = panel.row()
            #         row.alert = True
            #         panel.alert = True
            #         row.label(text="NO library or main scenes specified! at least one main scene or library scene is required!")
            #         row = panel.row()
            #         row.label(text="Please select and add one using the UI below")


            #     section = panel
            #     rows = 2
            #     row = section.row()
            #     row.label(text="main scenes")
            #     row.prop(context.window_manager, "main_scene", text='')

            #     row = section.row()
            #     row.template_list("SCENE_UL_Blenvy", "level scenes", blenvy, "main_scenes", blenvy, "main_scenes_index", rows=rows)

            #     col = row.column(align=True)
            #     sub_row = col.row()
            #     add_operator = sub_row.operator("scene_list.list_action", icon='ADD', text="")
            #     add_operator.action = 'ADD'
            #     add_operator.scene_type = 'LEVEL'
            #     #add_operator.operator = operator
            #     sub_row.enabled = context.window_manager.main_scene is not None

            #     sub_row = col.row()
            #     remove_operator = sub_row.operator("scene_list.list_action", icon='REMOVE', text="")
            #     remove_operator.action = 'REMOVE'
            #     remove_operator.scene_type = 'LEVEL'
            #     col.separator()

            #     # library scenes
            #     row = section.row()
            #     row.label(text="library scenes")
            #     row.prop(context.window_manager, "library_scene", text='')

            #     row = section.row()
            #     row.template_list("SCENE_UL_Blenvy", "library scenes", blenvy, "library_scenes", blenvy, "library_scenes_index", rows=rows)

            #     col = row.column(align=True)
            #     sub_row = col.row()
            #     add_operator = sub_row.operator("scene_list.list_action", icon='ADD', text="")
            #     add_operator.action = 'ADD'
            #     add_operator.scene_type = 'LIBRARY'
            #     sub_row.enabled = context.window_manager.library_scene is not None


            #     sub_row = col.row()
            #     remove_operator = sub_row.operator("scene_list.list_action", icon='REMOVE', text="")
            #     remove_operator.action = 'REMOVE'
            #     remove_operator.scene_type = 'LIBRARY'
            #     col.separator()
            
            # header, panel = layout.panel("components", default_closed=False)
            # header.label(text="Components")
            # if panel:
            #     components_ui.draw_settings_ui(panel, context.window_manager.components_registry)

            # header, panel = layout.panel("auto_export", default_closed=False)
            # header.label(text="Auto Export")
            # if panel:
            #     auto_export_ui.draw_settings_ui(panel, blenvy.auto_export)



def upsert_settings(name, data):
    stored_settings = bpy.data.texts[name] if name in bpy.data.texts else None#bpy.data.texts.new(name)
    if stored_settings is None:
        stored_settings = bpy.data.texts.new(name)
        stored_settings.write(json.dumps(data))
    else:
        current_settings = json.loads(stored_settings.as_string())
        current_settings = {**current_settings, **data}
        stored_settings.clear()
        stored_settings.write(json.dumps(current_settings))

def load_settings(name):
    print("loading settings", name)
    stored_settings = bpy.data.texts[name] if name in bpy.data.texts else None
    if stored_settings != None:
        return json.loads(stored_settings.as_string())
    return None

# checks if old & new settings (dicts really) are identical
def are_settings_identical(old, new, white_list=None):
    if old is None and new is None:
        return True
    if old is None and new is not None:
        return False
    if old is not None and new is None:
        return False
    
    old_items = sorted(old.items())
    new_items = sorted(new.items())
    if white_list is not None:
        old_items_override = {}
        new_items_override = {}
        for key in white_list:
            if key in old_items:
                old_items_override[key] = old_items[key]
            if key in new_items:
                new_items_override[key] = new_items[key]
        old_items = old_items_override
        new_items = new_items_override
            
    return old_items != new_items if new is not None else False