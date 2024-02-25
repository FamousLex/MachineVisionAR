import xml.etree.ElementTree as ET
import os

def convert_xml_to_yolo(xml_file_path, output_dir, class_names):
    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Extract the filename without extension and image size
    file_name = root.find('filename').text.replace('.png', '')
    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)

    # Open a text file for writing YOLO formatted annotations
    with open(os.path.join(output_dir, f"{file_name}.txt"), 'w') as file:
        # Iterate through all object in the XML file
        for obj in root.iter('object'):
            # Extract class name and bounding box coordinates
            class_name = obj.find('name').text
            if class_name not in class_names:
                continue # Skip classes not in our list
            class_id = class_names.index(class_name)
            xmlbox = obj.find('bndbox')
            xmin = int(xmlbox.find('xmin').text)
            ymin = int(xmlbox.find('ymin').text)
            xmax = int(xmlbox.find('xmax').text)
            ymax = int(xmlbox.find('ymax').text)

            # Convert to YOLO format
            x_center = ((xmin + xmax) / 2) / width
            y_center = ((ymin + ymax) / 2) / height
            bbox_width = (xmax - xmin) / width
            bbox_height = (ymax - ymin) / height

            # Write to .txt file
            file.write(f"{class_id} {x_center} {y_center} {bbox_width} {bbox_height}\n")

# Define classes here
class_names = ['ESP32']

# Specify input and output directories
input_dir = 'D:\Alex\MachineVisionAR\Renders\ESP32 Images 2000 Labeled\\'
output_dir = 'D:\Alex\MachineVisionAR\Renders\ESP32 Images 2000 Labeled\\'

# Convert all XML files in the input directory
for xml_file in os.listdir(input_dir):
    if xml_file.endswith('.xml'):
        convert_xml_to_yolo(os.path.join(input_dir, xml_file), output_dir, class_names)