import re
import xml
import xml.etree.ElementTree as ET


class XMLExporter:
    """Exports all object information to a JSON file."""

    @staticmethod
    def to_xml(xml_string: str, export_path: str) -> None:
        """Clean mjcf changes on a given xml string and export it to an .xml file.
        The mjcf library creates a new asset for each object of type mesh that
        is attached and assigns an internal filename. This function bundles these
        assets to categories and removes duplicates. The names for meshes and
        materials in geoms are adapted accordingly.

        Parameters:
            xml_string (str): String representation of the environment mjcf model
            export_path (str): Path of the file to be exported
        """
        root = ET.fromstring(xml_string)
        asset = root.find("asset")

        if asset is not None:
            materials = asset.findall("material")
            textures = asset.findall("texture")
            meshes = asset.findall("mesh")

            material_names = set()
            texture_names = set()
            mesh_names = set()

            # Get clean names, remove ducplicate assets, fix file paths
            (
                material_names,
                mesh_names,
                root,
            ) = XMLExporter.remove_duplicate_assets_fix_paths(
                material_names,
                materials,
                mesh_names,
                meshes,
                root,
                texture_names,
                textures,
            )

            # Apply clean names to geoms
            XMLExporter.apply_new_names_to_geoms(material_names, mesh_names, root)

        # Serialize XML
        with open(export_path + ".xml", "w") as f:
            f.write(ET.tostring(root, encoding="unicode"))

    @staticmethod
    def remove_duplicate_assets_fix_paths(
        material_names: set,
        materials: list,
        mesh_names: set,
        meshes: list,
        root: xml.etree.ElementTree.Element,
        texture_names: set,
        textures: list,
    ) -> tuple[set, set, xml.etree.ElementTree.Element]:
        """Get clean names, remove duplicate assets, fix file paths.

        Parameters:
            material_names (set): Set of material names
            materials (list): List of materials
            mesh_names (set): Set of mesh names
            meshes (list): List of meshes
            root (xml.etree.ElementTree.Element): Root element of the xml tree
            texture_names (set): Set of texture names
            textures (list): List of textures

        Returns:
            tuple: Tuple containing the material names, mesh names and the root element of the xml tree
        """
        for texture in textures:
            name = texture.attrib["name"]

            match = re.match(
                r"\w+/(\w*)", name
            )  # extract e.g. the category "tree1" from "tree09/tree1"

            if match:
                category_name = match.group(1)
                texture.attrib["name"] = category_name

                if category_name in texture_names:
                    root.find("asset").remove(texture)  # remove duplicate textures
                else:
                    texture_names.add(category_name)  # unique texture
                    texture.attrib["file"] = (
                        "../examples/xml_objects/3D_Assets/" + category_name + ".png"
                    )
        for material in materials:
            name = material.attrib["name"]
            match = re.match(r"\w+/(\w*)", name)

            if match:
                category_name = match.group(1)
                material.attrib["name"] = category_name

                if category_name in material_names:
                    root.find("asset").remove(material)
                else:
                    material_names.add(category_name)

                    for tex_name in texture_names:
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

        return material_names, mesh_names, root

    @staticmethod
    def apply_new_names_to_geoms(
        material_names: set, mesh_names: set, root: xml.etree.ElementTree.Element
    ) -> xml.etree.ElementTree.Element:
        """Apply clean names to geoms.

        Parameters:
            material_names (set): Set of material names
            mesh_names (set): Set of mesh names
            root (xml.etree.ElementTree.Element): Root element of the xml tree

        Returns:
            xml.etree.ElementTree.Element: Root element of the xml tree with applied clean names to geoms
        """
        bodies = root.find("worldbody").findall("body")
        for body in bodies:
            geom = body.find("body").find("geom")

            if geom.attrib["type"] == "mesh":
                for material in material_names:
                    if material in geom.attrib["material"]:
                        geom.attrib["material"] = material

                for mesh in mesh_names:
                    if mesh in geom.attrib["mesh"]:
                        geom.attrib["mesh"] = mesh
        return root
