#!/usr/bin/env python3

"""abstraction.py"""

# This file is part of pythonparser.

# pythonparser is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pythonparser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pythonparser.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2020-2021 Jean-Rémy Falleri <jr.falleri@gmail.com>

from xml.dom import minidom
import sys
import parso


doc = minidom.Document()
positions = [0]


def main(file):
    """main"""
    document = minidom.Document()
    parso_ast = parso.parse(read_file(file))
    gumtree_ast = to_gumtree_node(parso_ast)
    document.appendChild(gumtree_ast)
    process_node(parso_ast, gumtree_ast)
    xml = document.toprettyxml()
    return xml


def process_node(parso_node, gumtree_node):
    """process node"""
    if parso_node.type == "error_node":
        sys.exit(parso_node)

    for parso_child in parso_node.children:
        gumtree_child = to_gumtree_node(parso_child)
        if gumtree_child is not None:
            gumtree_node.appendChild(gumtree_child)
            if hasattr(parso_child, "children"):
                process_node(parso_child, gumtree_child)


def to_gumtree_node(parso_node):
    """to_gumtree_node"""
    if parso_node.type in ["keyword", "newline", "endmarker"]:
        return
    if parso_node.type == "operator" and parso_node.value in [
        ".",
        "(",
        ")",
        "[",
        "]",
        ":",
        ";",
    ]:
        return
    gumtree_node = doc.createElement(parso_node.type)
    # start_position = positions[parso_node.start_pos[0] -
    #                            1] + parso_node.start_pos[1]
    # end_position = positions[parso_node.end_pos[0] - 1] + parso_node.end_pos[1]
    # length = end_position - start_position
    if (not hasattr(parso_node, "children")) or len(parso_node.children) == 0:
        gumtree_node.setAttribute("label", parso_node.value)
    return gumtree_node


def read_file(file):
    """read file"""
    with open(file, mode="r", encoding="utf-8") as reading_file:
        data = reading_file.read()
    index = 0
    for char in data:
        index += 1
        if char == "\n":
            positions.append(index)
    return data


if __name__ == "__main__":
    main(sys.argv[1])
