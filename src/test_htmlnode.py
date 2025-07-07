import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_init_with_all_args(self):
        """Correct initialization with all arguments."""
        children = [HTMLNode(tag="b", value="bold")]
        props = {"class": "header", "id": "title"}
        node = HTMLNode(tag="h1", value="Hello", children=children, props=props)
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_init_with_defaults(self):
        """Defaults are None if not provided."""
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_repr(self):
        """__repr__ outputs a string reflecting the constructor args."""
        node = HTMLNode("p", "Paragraph", [], {"style": "color:red;"})
        expected = "HTMLNode(p, Paragraph, [], {'style': 'color:red;'})"
        self.assertEqual(repr(node), expected)

    def test_props_to_html_basic(self):
        """props_to_html generates correct HTML from props."""
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        html = node.props_to_html()
        self.assertIn('href="https://example.com"', html)
        self.assertIn('target="_blank"', html)
        self.assertTrue(html.startswith(" "))
        self.assertEqual(html.count("="), 2)

    def test_props_to_html_empty(self):
        """props_to_html with empty dict returns just a space."""
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), " ")

    def test_props_to_html_none(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_to_html_not_implemented(self):
        """Calling to_html raises NotImplementedError."""
        node = HTMLNode("div", "Hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_strong(self):
        node = LeafNode("strong", "Important")
        self.assertEqual(node.to_html(), "<strong>Important</strong>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Link", props={"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Link</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_raises_on_none_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()


class TestParentNode(unittest.TestCase):
    def test_init_basic(self):
        """Stores constructor args verbatim."""
        kids = [LeafNode("b", "bold")]
        props = {"class": "box"}
        p = ParentNode("div", kids, props=props)
        self.assertEqual(p.tag, "div")
        self.assertEqual(p.children, kids)
        self.assertEqual(p.props, props)

    def test_init_defaults(self):
        """children and props default to None when not supplied."""
        p = ParentNode("ul", children=[LeafNode("li", "x")])
        self.assertIsNone(p.value)  # ParentNode never sets value
        self.assertIsNone(p.props)

    def test_to_html_simple(self):
        """Single child renders correctly inside wrapper tag."""
        p = ParentNode("p", [LeafNode(None, "hello")])
        self.assertEqual(p.to_html(), "<p>hello</p>")

    def test_to_html_multiple_children(self):
        """Concatenates multiple children in order."""
        p = ParentNode(
            "span",
            [
                LeafNode("b", "B"),
                LeafNode(None, "-"),
                LeafNode("i", "I"),
            ],
        )
        self.assertEqual(p.to_html(), "<span><b>B</b>-<i>I</i></span>")

    def test_to_html_nested_parent(self):
        """Works when children themselves are ParentNodes."""
        inner = ParentNode("em", [LeafNode(None, "inner")])
        outer = ParentNode("div", [LeafNode(None, "pre "), inner])
        self.assertEqual(
            outer.to_html(),
            "<div>pre <em>inner</em></div>",
        )

    def test_to_html_with_props(self):
        """Props are inserted on the opening tag."""
        p = ParentNode(
            "section",
            [LeafNode(None, "x")],
            props={"id": "s1", "class": "hero"},
        )
        html = p.to_html()
        self.assertTrue(html.startswith("<section "))
        self.assertIn('id="s1"', html)
        self.assertIn('class="hero"', html)
        self.assertTrue(html.endswith("</section>"))

    def test_to_html_no_tag_raises(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode(None, "x")]).to_html()

    def test_to_html_no_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_to_html_empty_children_list_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

    def test_child_without_to_html_raises(self):
        """Child that lacks .to_html() should surface AttributeError."""

        class Fake:  # intentionally missing to_html
            pass

        with self.assertRaises(AttributeError):
            ParentNode("div", [Fake()]).to_html()

    def test_children_order_preserved(self):
        """Order of children in output equals order in list."""
        kids = [
            LeafNode(None, "1"),
            LeafNode(None, "2"),
            LeafNode(None, "3"),
        ]
        html = ParentNode("div", kids).to_html()
        self.assertTrue(html.index("1") < html.index("2") < html.index("3"))

    def test_props_to_html_integration(self):
        """Changing props later affects rendered HTML."""
        p = ParentNode("a", [LeafNode(None, "click")])
        p.props = {"href": "https://example.com"}
        self.assertIn('href="https://example.com"', p.to_html())


if __name__ == "__main__":
    unittest.main()
