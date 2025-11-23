import re
from htmlnode import HTMLNode,LeafNode,ParentNode
from textnode import text_node_to_html_node,TextType,TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            new_text = node.text.split(delimiter)
            if len(new_text) % 2 == 0:
                raise Exception("invalid markdown syntax")
            for i in range(len(new_text)):
                if i % 2 == 0 and new_text[i] != '':
                    new_nodes.append(TextNode(new_text[i],TextType.TEXT))
                elif i % 2 == 1 and new_text[i] != '':
                    new_nodes.append(TextNode(new_text[i],text_type))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            matches = extract_markdown_images(node.text)
            if len(matches) == 0:
                new_nodes.append(node)
            else:
                current_text = node.text
                max_iter = len(matches)
                for match in matches:
                    max_iter -= 1
                    sections = current_text.split(f"![{match[0]}]({match[1]})", 1)
                    if sections[0] != '':
                        new_nodes.append(TextNode(sections[0],TextType.TEXT))
                    new_nodes.append(TextNode(match[0],TextType.IMAGE,match[1]))
                    if max_iter == 0 and sections[1] != '':
                        new_nodes.append(TextNode(sections[1],TextType.TEXT))
                    current_text = sections[1]
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            matches = extract_markdown_links(node.text)
            if len(matches) == 0:
                new_nodes.append(node)
            else:
                current_text = node.text
                max_iter = len(matches)
                for match in matches:
                    max_iter -= 1
                    sections = current_text.split(f"[{match[0]}]({match[1]})", 1)
                    if sections[0] != '':
                        new_nodes.append(TextNode(sections[0],TextType.TEXT))
                    new_nodes.append(TextNode(match[0],TextType.LINK,match[1]))
                    if max_iter == 0 and sections[1] != '':
                        new_nodes.append(TextNode(sections[1],TextType.TEXT))
                    current_text = sections[1]
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text,TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    output = []
    markdown = markdown.split("\n\n")
    for ele in markdown:
        output.append(ele.strip(" \n"))
    return output