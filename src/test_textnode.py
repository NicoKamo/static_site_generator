import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

class TestSplitNodeDelimiter(unittest.TestCase):
    def test_delimiter(self):
        node = TextNode("This is **a** text node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],"**",TextType.CODE)
        self.assertEqual(new_nodes,
                         [
        TextNode("This is ", TextType.TEXT),
        TextNode("a", TextType.CODE),
        TextNode(" text node", TextType.TEXT),
                        ]
                        )
        
    #def test_exception(self):
        #node = TextNode("This should $ not work.", TextType.TEXT)
        #self.assertRaises(Exception("invalid markdown syntax"),split_nodes_delimiter([node],"$",TextType.ITALIC),
        #                  )
        
    def test_delimiter_left(self):
        node1 = TextNode("This is -a- text node", TextType.TEXT)
        node2 = TextNode("This is a -second- text node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1,node2],"-",TextType.BOLD)
        self.assertEqual(new_nodes,
                         [
        TextNode("This is ", TextType.TEXT),
        TextNode("a", TextType.BOLD),
        TextNode(" text node", TextType.TEXT),
        TextNode("This is a ", TextType.TEXT),
        TextNode("second", TextType.BOLD),
        TextNode(" text node", TextType.TEXT),
                        ])


if __name__ == "__main__":
    unittest.main()
