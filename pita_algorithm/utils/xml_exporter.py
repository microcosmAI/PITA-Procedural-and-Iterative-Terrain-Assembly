import re
import xml.etree.ElementTree as ET


class XMLExporter:
    """Exports all object information to a JSON file."""

    @staticmethod
    def to_xml(xml_string, export_path):
        """
        Clean mjcf changes on a given xml string and export it to an .xml file.
        The mjcf library creates a new asset for each object of type mesh that
        is attached and assigns an internal filename. This function bundles these
        assets to categories and removes duplicates. The names for meshes and
        materials in geoms are adapted accordingly.

        Parameters:
            xml_string (str): String representation of the environment mjcf model
            export_path (str): Path of the file to be exported
        """
        root = ET.fromstring(xml_string)

        materials = root.find("asset").findall("material")
        textures = root.find("asset").findall("texture")
        meshes = root.find("asset").findall("mesh")

        mat_names = set()
        tex_names = set()
        mesh_names = set()

        """
        get clean names, remove ducplicate assets, fix file paths
        """
        for texture in textures:
            name = texture.attrib["name"]

            match = re.match(
                r"\w+/(\w*)", name
            )  # extract e.g. the category "tree1" from "tree09/tree1"

            if match:
                category_name = match.group(1)
                texture.attrib["name"] = category_name

                if category_name in tex_names:
                    root.find("asset").remove(texture)  # remove duplicate textures
                else:
                    tex_names.add(category_name)  # unique texture
                    texture.attrib["file"] = (
                        "../examples/xml_objects/3D_Assets/" + category_name + ".png"
                    )

        for material in materials:
            name = material.attrib["name"]
            match = re.match(r"\w+/(\w*)", name)

            if match:
                category_name = match.group(1)
                material.attrib["name"] = category_name

                if category_name in mat_names:
                    root.find("asset").remove(material)
                else:
                    mat_names.add(category_name)

                    for tex_name in tex_names:
                        if tex_name in material.attrib["texture"]:
                            material.attrib["texture"] = tex_name

        for mesh in meshes:
            name = mesh.attrib["name"]

            match = re.match(r"\w+/(\w*)", name)

            if match:
                category_name = match.group(1)
                mesh.attrib["name"] = category_name
                if category_name in mesh_names:
                    root.find("asset").remove(mesh)
                else:
                    mesh_names.add(category_name)
                    mesh.attrib["file"] = (
                        "../examples/xml_objects/3D_Assets/" + category_name + ".obj"
                    )

        """
        apply clean names to geoms
        """
        bodies = root.find("worldbody").findall("body")

        for body in bodies:
            geom = body.find("body").find("geom")

            if geom.attrib["type"] == "mesh":
                for material in mat_names:
                    if material in geom.attrib["material"]:
                        geom.attrib["material"] = material

                for mesh in mesh_names:
                    if mesh in geom.attrib["mesh"]:
                        geom.attrib["mesh"] = mesh

        """
        serialize xml
        """
        with open(export_path + ".xml", "w") as f:
            f.write(ET.tostring(root, encoding="unicode"))
