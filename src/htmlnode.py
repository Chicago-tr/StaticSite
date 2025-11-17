class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if not self.props:
            return ""
        s = ""
        for key, value in self.props.items():
            a = str(key)
            b = str(value)
            c = " " + a + '="' + b + '"'
            s = s + c
        return s

    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self):
        return f"tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value)
        self.props = props

    # Alternative way to do above is: super().__init__(tag,value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("value cannot = None")
        if self.tag == None:
            return str(self.value)
        if self.props == None:
            o = f"<{self.tag}>"
            c = f"</{self.tag}>"

            return o + str(self.value) + c
        else:
            c = f"</{self.tag}>"

            p = self.props_to_html()
            o = f"<{self.tag}{p}>"
            return o + str(self.value) + c

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("No value given for children")

        htmls = f"<{self.tag}{self.props_to_html()}>"
        for obj in self.children:
            x = obj.to_html()
            htmls += x

        htmls = htmls + f"</{self.tag}>"
        return htmls

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
