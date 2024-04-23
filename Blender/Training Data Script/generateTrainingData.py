import bpy
import math
import os
import random
import mathutils
import time
import json
import bmesh
import xml.etree.ElementTree as ET
import bpy_extras
import bpy_extras.view3d_utils
import bpy_extras.object_utils

def read_config(config_path):
    with open(config_path, 'r') as config_file:
        return json.load(config_file)
    
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data.get('data', []) 

def create_annotation_xml(folder, filename, path, width, height, depth, xmin, ymin, xmax, ymax, object_name):
    annotation = ET.Element("annotation")
    ET.SubElement(annotation, "folder").text = folder
    ET.SubElement(annotation, "filename").text = filename
    ET.SubElement(annotation, "path").text = path

    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "database").text = "Unknown"

    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = str(depth)

    ET.SubElement(annotation, "segmented").text = "0"

    obj = ET.SubElement(annotation, "object")
    ET.SubElement(obj, "name").text = object_name
    ET.SubElement(obj, "pose").text = "Unspecified"
    ET.SubElement(obj, "truncated").text = "0"
    ET.SubElement(obj, "difficult").text = "0"

    bndbox = ET.SubElement(obj, "bndbox")
    ET.SubElement(bndbox, "xmin").text = str(xmin)
    ET.SubElement(bndbox, "ymin").text = str(ymin)
    ET.SubElement(bndbox, "xmax").text = str(xmax)
    ET.SubElement(bndbox, "ymax").text = str(ymax)

    tree = ET.ElementTree(annotation)
    tree.write(path.replace('.png', '.xml'))
    
def setup_materials():
    materials = []

    # Brown
    brown_mat = bpy.data.materials.new(name="BrownMaterial")
    brown_mat.use_nodes = True
    bsdf = brown_mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (0.065, 0.033, 0, 1)
    bsdf.inputs['Metallic'].default_value = 0
    bsdf.inputs['Roughness'].default_value = 1

    # Black
    black_mat = bpy.data.materials.new(name="BlackMaterial")
    black_mat.use_nodes = True
    bsdf = black_mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (0.0, 0.0, 0.0, 1)
    bsdf.inputs['Metallic'].default_value = 0
    bsdf.inputs['Roughness'].default_value = 1

    # Dark Gray
    dark_gray_mat = bpy.data.materials.new(name="DarkGrayMaterial")
    dark_gray_mat.use_nodes = True
    bsdf = dark_gray_mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (0.33, 0.33, 0.33, 1)
    bsdf.inputs['Metallic'].default_value = 0
    bsdf.inputs['Roughness'].default_value = 1
    
    # Light Gray
    light_gray_mat = bpy.data.materials.new(name="LightGrayMaterial")
    light_gray_mat.use_nodes = True
    bsdf = light_gray_mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (0.2, 0.2, 0.2, 1)
    bsdf.inputs['Metallic'].default_value = 0
    bsdf.inputs['Roughness'].default_value = 1
    
    # White
    white_mat = bpy.data.materials.new(name="WhiteMaterial")
    white_mat.use_nodes = True
    bsdf = white_mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1)
    bsdf.inputs['Metallic'].default_value = 0
    bsdf.inputs['Roughness'].default_value = 1
    
    # Brown Metallic
    brown_mat_metal = bpy.data.materials.new(name="BrownMaterial")
    brown_mat_metal.use_nodes = True
    bsdf = brown_mat_metal.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (0.065, 0.033, 0, 1)
    bsdf.inputs['Metallic'].default_value = 0.5
    bsdf.inputs['Roughness'].default_value = 0.2

    # Black Metallic
    black_mat_metal = bpy.data.materials.new(name="BlackMaterial")
    black_mat_metal.use_nodes = True
    bsdf = black_mat_metal.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (0.0, 0.0, 0.0, 1)
    bsdf.inputs['Metallic'].default_value = 0.5
    bsdf.inputs['Roughness'].default_value = 0.2

    # Dark Gray Metallic
    dark_gray_mat_metal = bpy.data.materials.new(name="DarkGrayMaterial")
    dark_gray_mat_metal.use_nodes = True
    bsdf = dark_gray_mat_metal.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (0.33, 0.33, 0.33, 1)
    bsdf.inputs['Metallic'].default_value = 0.5
    bsdf.inputs['Roughness'].default_value = 0.2
    
    # Light Gray Metallic
    light_gray_mat_metal = bpy.data.materials.new(name="LightGrayMaterial")
    light_gray_mat_metal.use_nodes = True
    bsdf = light_gray_mat_metal.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (0.2, 0.2, 0.2, 1)
    bsdf.inputs['Metallic'].default_value = 0.5
    bsdf.inputs['Roughness'].default_value = 0.2
    
    # White Metallic
    white_mat_metal = bpy.data.materials.new(name="WhiteMaterial")
    white_mat_metal.use_nodes = True
    bsdf = white_mat_metal.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1)
    bsdf.inputs['Metallic'].default_value = 0.5
    bsdf.inputs['Roughness'].default_value = 0.2

    materials.extend([brown_mat, black_mat, dark_gray_mat, light_gray_mat, white_mat, brown_mat_metal, black_mat_metal, dark_gray_mat_metal, light_gray_mat_metal, white_mat_metal])
    return materials

def apply_material_and_color(obj, material_name, color):
    # Ensure the object has a material slot
    if not obj.data.materials:
        obj.data.materials.append(None)
    
    # Get or create the material
    material = bpy.data.materials.get(material_name)
    if material is None:
        material = bpy.data.materials.new(name=material_name)
        material.use_nodes = True
    
    # Assign the material to the first material slot
    obj.data.materials[0] = material

    # Get the nodes in the material
    nodes = material.node_tree.nodes

    # Attempt to find the Principled BSDF and Refraction BSDF
    principled_bsdf = nodes.get('Principled BSDF')
    refraction_bsdf = nodes.get('Refraction BSDF')

    # Set the color based on the shader type
    if principled_bsdf:
        principled_bsdf.inputs['Base Color'].default_value = (color[0], color[1], color[2], color[3])
    elif refraction_bsdf:
        refraction_bsdf.inputs['Color'].default_value = (color[0], color[1], color[2], 1)  # Refraction might not use alpha
    else:
        print("Supported shader not found. Material might need manual adjustment.")

def export_fbx(export_path, selected_objects=True, apply_transform=True):
    """
    Exports selected objects to an FBX file.
    Args:
    - export_path: The path where the FBX file will be saved.
    - selected_objects: If True, only exports selected objects. If False, exports all objects.
    - apply_transform: Apply transformation to exported data (scale, rotation).
    """
    
    export_dir = os.path.dirname(export_path)
    
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
        print(f"Created directory: {export_dir}")
        
    bpy.ops.export_scene.fbx(
        filepath=export_path,
        use_selection=selected_objects,
        apply_scale_options='FBX_SCALE_ALL',
        apply_unit_scale=apply_transform,
        global_scale=1.0,
        axis_forward='-Z',
        axis_up='Y'
    )

# Configure render settings
bpy.context.scene.render.resolution_x = 512
bpy.context.scene.render.resolution_y = 512
bpy.context.scene.render.resolution_percentage = 100 # render quality
bpy.context.scene.render.image_settings.file_format = 'PNG'    
bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'OPTIX'
bpy.context.scene.cycles.device = 'GPU'    

# Clear existing objects in the default scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Determine the directory of the current script
script_directory = bpy.path.abspath("//")
config_path = os.path.join(script_directory, "config.json")
config = read_config(config_path)

# Object data from JSON file
object_data_path = os.path.join(script_directory, "FBX Model/exportedObject.json")
object_data_list = read_json_file(object_data_path)

# Path to model
model_file_path = os.path.normpath(os.path.join(script_directory, config['model_file_path']))

# Path to render output
render_output_path = os.path.normpath(os.path.join(script_directory, config['render_output_directory']))
render_name = config['render_name']

if not os.path.exists(render_output_path):
    os.makedirs(render_output_path)

# File format of model (.obj)
file_format = config['file_format']

# Number of renders for main process loop
NUM_RENDERS = config['num_renders']

# Data augmentation to manipulate dataset
percent_objects_placed_flat = config['percent_objects_placed_flat']
num_flat_rotations = int(NUM_RENDERS * (percent_objects_placed_flat / 100.0))
percent_planes_added = config['percent_planes_added']
num_planes_added = int(NUM_RENDERS * (percent_planes_added / 100.0))

# Get materials for plane
plane_materials = setup_materials()

# Create a plane outside the loop, to be potentially reused
bpy.ops.mesh.primitive_plane_add(size=1000, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(100.0, 100.0, 0.0))
plane = bpy.context.active_object
plane.hide_viewport = True
plane_created = True
    
# Create a collection for original imported objects
collection_name = "ModelCollection"
if collection_name not in bpy.data.collections:
    model_collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(model_collection)
else:
    model_collection = bpy.data.collections[collection_name]
    
# Import the object file once
if file_format.lower() == 'fbx':
    bpy.ops.import_scene.fbx(filepath=model_file_path)

# Store the imported objects
imported_objs = [obj for obj in bpy.context.selected_objects]

# Move imported objects to the model collection and hide them
for obj in imported_objs:
    # Check if the object is actually in the current scene collection before unlinking
    if obj.name in bpy.context.scene.collection.objects:
        bpy.context.scene.collection.objects.unlink(obj)
        model_collection.objects.link(obj)
    else:
        # If the object is not in the scene collection, find the correct collection
        found = False
        for coll in bpy.data.collections:
            if obj.name in coll.objects:
                coll.objects.unlink(obj)
                model_collection.objects.link(obj)
                found = True
                break
        if not found:
            print(f"Warning: Object '{obj.name}' was not found in any collection and cannot be moved.")
    
# Iterate over imported objects and apply JSON data
for obj_data in object_data_list:
    # Search for the corresponding object in Blender
    obj = next((o for o in model_collection.objects if o.name == obj_data['originalName']), None)
    if obj:
        color = [float(c) for c in obj_data['color']]  # Ensure this is properly formatted in your JSON
        apply_material_and_color(obj, obj_data['materialName'], color)
        obj.name = obj_data['name']
    else:
        continue

export_file_path = config['export_object_path']
for obj in model_collection.objects:
    obj.select_set(True)
    
export_fbx(export_file_path, selected_objects=True, apply_transform=False)

render_count = 0
#    
while render_count < NUM_RENDERS:
    # Randomly choose a material for plane
    random_plane_material = random.choice(plane_materials)
    
    # Hide or show the plane randomly based on percentage
    show_plane = random.random() < (percent_planes_added / 100.0)
    
    if show_plane:
        plane.hide_viewport = False  # Make sure the plane is visible
        plane.hide_render = False
        if plane.data.materials:
            plane.data.materials[0] = random_plane_material
        else:
            plane.data.materials.append(random_plane_material)
    else:
        plane.hide_viewport = True  # Hide the plane if it's not supposed to be in the scene
        plane.hide_render = True
        
    
    # Reset transformation each iteration
    for obj in model_collection.objects:
        obj.rotation_euler = (0, 0, 0)  # Reset rotation
        obj.location = (0, 0, 0)  # Reset location
  
    # Determine the transformation for this iteration
    model_location = (0, 0, 0)  # Adjust as needed
    rotation = (0, 0, math.radians(random.uniform(0, 360)))
    if not show_plane:
        rotation = (math.radians(random.uniform(0, 360)),
                    math.radians(random.uniform(0, 360)),
                    math.radians(random.uniform(0, 360)))
    if render_count < num_flat_rotations:
        rotation = (0,
                    0,
                    rotation[2])
        print('flat rotation: ' + str(rotation))
    
    # Apply the same transformation to all objects in the collection
    for obj in model_collection.objects:
        obj.location = model_location
        obj.rotation_euler = rotation

    # Now, calculate the lowest Z after transformations
    lowest_z = None
    
    for obj in model_collection.objects:
        if obj.type == 'MESH':
            obj.update_from_editmode()  # Update mesh data if in edit mode
            bpy.context.view_layer.update()  # Update the scene to apply transformation
            vertices_global = [obj.matrix_world @ v.co for v in obj.data.vertices]
            min_z = min(v.z for v in vertices_global)
            if lowest_z is None or min_z < lowest_z:
                lowest_z = min_z

    # Adjust the position to make the lowest point flush with the plane
    if lowest_z is not None:
        z_offset = -lowest_z
        for obj in model_collection.objects:
            if obj.type == 'MESH':
                obj.location.z += z_offset

    # Add all HDRI's into a list
    hdri_folder = os.path.normpath(os.path.join(script_directory, config['hdri_folder']))
    hdri_files = [os.path.join(hdri_folder, f) for f in os.listdir(hdri_folder) if f.endswith('exr') or f.endswith('hdr')]

    # HDRI settings and loading
    bpy.context.scene.render.engine= 'CYCLES'
    hdri_path = random.choice(hdri_files)
    world = bpy.context.scene.world
    world.use_nodes = True
    nodes = world.node_tree.nodes

    # Clear existing nodes
    nodes.clear()

    # Add environment texture and background nodes
    env_texture_node = nodes.new('ShaderNodeTexEnvironment')
    env_texture_node.image = bpy.data.images.load(hdri_path)
    background_node = nodes.new('ShaderNodeBackground')
    world_output_node = nodes.new('ShaderNodeOutputWorld')

    # Link nodes
    links = world.node_tree.links
    links.new(env_texture_node.outputs['Color'], background_node.inputs['Color'])
    links.new(background_node.outputs['Background'], world_output_node.inputs['Surface'])

    # Hemisphere parameters
    min_radius = 50  # min distance from the model
    max_radius = 100  # max distrance from the model
    min_height = 5  # min height from the plane
    max_height = 500  # max height from the plane

    # Generate random spherical coordinates
    #radius = random.uniform(min_radius, max_radius)
    radius = 100
    theta = math.radians(random.uniform(0, 90))  # Latitude angle in radians
    phi = math.radians(random.uniform(0, 360))  # Longitude angle in radians

    # Convert spherical coordinates to Cartesian coordinates for the camera
    camera_x = radius * math.sin(theta) * math.cos(phi)
    camera_y = radius * math.sin(theta) * math.sin(phi)
    camera_z = random.uniform(min_height, max_height) # Height is directly used as the Z coordinate

    camera_location = (camera_x, camera_y, camera_z)

    # Create camera directly without using ops
    cam_data = bpy.data.cameras.new(name=f"Camera_{render_count}")
    camera = bpy.data.objects.new(name=f"Camera_{render_count}", object_data=cam_data)
    bpy.context.scene.collection.objects.link(camera)
    camera.location = camera_location

    # Create an empty object at the center of the model collection
    empty = bpy.data.objects.new("Empty", None)
    empty.location = model_location  # or any other location you want to focus on
    bpy.context.scene.collection.objects.link(empty)

    # Aim the camera at the empty using a 'Track To' constraint
    track_to = camera.constraints.new(type='TRACK_TO')
    track_to.target = empty
    track_to.up_axis = 'UP_Y'
    track_to.track_axis = 'TRACK_NEGATIVE_Z'
    
    # Set to active camera
    bpy.context.scene.camera = camera
    
    # Update scene before rendering
    bpy.context.view_layer.update()
    
    # Calculate the 2D bounding box from the camera's perspective
    scene = bpy.context.scene
    cam = bpy.context.scene.camera
    render_scale = scene.render.resolution_percentage / 100
    render_size = (
        int(scene.render.resolution_x * render_scale),
        int(scene.render.resolution_y * render_scale),
    )

    # Initialize min and max with opposite values
    min_x, min_y = 1.0, 1.0
    max_x, max_y = 0.0, 0.0

    skip_render = False
    
    for obj in model_collection.objects:
        if obj.type == 'MESH':
            for corner in obj.bound_box:
                world_corner = obj.matrix_world @ mathutils.Vector(corner)
                camera_coord = bpy_extras.object_utils.world_to_camera_view(scene, cam, world_corner)

                # Update min and max values
                min_x = min(min_x, camera_coord.x)
                min_y = min(min_y, camera_coord.y)
                max_x = max(max_x, camera_coord.x)
                max_y = max(max_y, camera_coord.y)
                
                # Check if the object is within the camera frame
                if min_x < 0 or max_x > 1 or min_y < 0 or max_y > 1:
                    skip_render = True
                    break
                
            if skip_render:
               break
       
    if skip_render:
        print("Skipping render because the object is out of the frame")
    else:
        # Render the scene
        render_file_path = os.path.join(render_output_path, f"{render_name}_{render_count}.png")
        bpy.context.scene.render.filepath = render_file_path
        bpy.ops.render.render(write_still=True)

        # Calculate pixel values for the bounding box
        min_x = int(min_x * render_size[0])
        min_y = int((1.0 - min_y) * render_size[1])  # Flip y
        max_x = int(max_x * render_size[0])
        max_y = int((1.0 - max_y) * render_size[1])  # Flip y

        # Output the bounding box
        print(f"Bounding box: {(min_x, min_y, max_x, max_y)}")
        create_annotation_xml(
            config['render_folder_name'],
            f"{render_name}_{render_count}.png",
            render_file_path,
            render_size[0],
            render_size[1],
            3,  # Assuming RGB images
            min_x, min_y, max_x, max_y,
            config['render_name']
        )
        render_count += 1
                                                               
    # Remove camera for this iteration
    bpy.data.objects.remove(camera, do_unlink=True)                                                                                                                                                                                                                          

# Cleanup after all iterations: remove model and remove the plane if it was created
if collection_name in bpy.data.collections:
    collection = bpy.data.collections[collection_name]
    bpy.ops.object.select_all(action='DESELECT')
    for obj in collection.objects:
        obj.select_set(True)
    bpy.ops.object.delete()
    bpy.data.collections.remove(collection)
    
if plane_created:
    bpy.data.objects.remove(plane, do_unlink=True)

print("Processing Complete")
        