import ast
import math
import itertools

class Node(object):
    parent = None

    def __init__(self, parent):
        self.parent = parent

    def set_parent(self, parent):
        self.parent = parent

    def leftmost_element(self):
        raise NotImplementedError

    def rightmost_element(self):
        raise NotImplementedError


class Inner(Node):
    left: Node = None
    right: Node = None

    def __init__(self, parent):
        assert isinstance(parent, Inner) or parent is None
        super().__init__(parent)

    def set_right(self, right: Node):
        assert isinstance(right, Node)
        self.right = right

    def set_left(self, left: Node):
        assert isinstance(left, Node)
        self.left = left

    def __repr__(self) -> str:
        return f"[{repr(self.left)},{repr(self.right)}]"


class Value(Node):
    value: int = -1

    def __init__(self, parent, value):
        assert isinstance(parent, Inner)

        super().__init__(parent)
        self.value = value

    def leftmost_element(self):
        return self.value

    def rightmost_element(self):
        return self.value

    def __repr__(self) -> str:
        return f"{self.value}"


def parse_elem_into_node(elem, parent: Inner) -> Node:
    assert isinstance(parent, Inner) or parent is None

    if isinstance(elem, ast.Constant):
        return Value(parent, elem.value)
    elif isinstance(elem, ast.List):
        elements = elem.elts
        assert len(elements) == 2

        parent = Inner(parent)

        left_elem = elements[0]
        left_node = parse_elem_into_node(left_elem, parent)
        parent.set_left(left_node)

        right_elem = elements[1]
        right_node = parse_elem_into_node(right_elem, parent)
        parent.set_right(right_node)

        return parent
    else:
        assert False


def parse_into_tree(source: str):
    tree = ast.parse(source)

    expr: ast.Expr = tree.body[0]
    assert isinstance(expr, ast.Expr)

    list: ast.List = expr.value
    assert isinstance(list, ast.List)

    return parse_elem_into_node(list, None)


def inorder_traversal(tree: Inner):
    if isinstance(tree, Inner):
        return inorder_traversal(tree.left) + inorder_traversal(tree.right)
    elif isinstance(tree, Value):
        return [tree]
    else:
        assert False


def explode_one(node: Node, root: Node, height: int):
    if isinstance(node, Inner):
        if height == 4:
            # print(f"\nExploding node {repr(node)}")

            inorder_values = inorder_traversal(root)
            for i in range(len(inorder_values)):
                if inorder_values[i] is node.left and i > 0:
                    inorder_values[i - 1].value += node.left.value
                if inorder_values[i] is node.right and i < len(inorder_values) - 1:
                    inorder_values[i + 1].value += node.right.value

            parent = node.parent
            if parent.left is node:
                parent.left = Value(parent, 0)
            if parent.right is node:
                parent.right = Value(parent, 0)

            return True
        else:
            return explode_one(node.left, root, height + 1) or explode_one(
                node.right, root, height + 1
            )


def reduce_one(node: Node):
    if isinstance(node, Value):
        if node.value >= 10:
            parent = node.parent

            # print(f"\nReducing node {repr(node)}")

            value = node.value
            new_node = Inner(parent)
            new_node.set_left(Value(new_node, math.floor(value / 2)))
            new_node.set_right(Value(new_node, math.ceil(value / 2)))

            if parent.left is node:
                parent.left = new_node
            elif parent.right is node:
                parent.right = new_node
            else:
                assert False

            return True
        else:
            return False
    else:
        return reduce_one(node.left) or reduce_one(node.right)


def reduce(root: Node):
    while True:
        if explode_one(root, root, 0) or reduce_one(root):
            # print("Result:")
            # print(repr(root))
            # print(inorder_traversal(root))
            # print()
            ...
        else:
            break


def test_explode(input: str, output: str):
    tree = parse_into_tree(input)
    explode_one(tree, tree, 0)
    assert repr(tree) == output


def test_split(input: str, output: str):
    tree = parse_into_tree(input)
    reduce_one(tree)
    assert repr(tree) == output


def add(first: Node, second: Node):
    tree = Inner(None)
    tree.set_left(first)
    tree.set_right(second)

    first.set_parent(tree)
    second.set_parent(tree)

    reduce(tree)
    return tree


def test_single_add():
    first = parse_into_tree("[[[[4,3],4],4],[7,[[8,4],9]]]")
    second = parse_into_tree("[1,1]")
    result = add(first, second)
    assert repr(result) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"


def test_multiple_add(inputs: list, output: str):
    tree = parse_into_tree(inputs[0])

    for i in inputs[1:]:
        second = parse_into_tree(i)
        tree = add(tree, second)

    assert repr(tree) == output


def add_file(filename: str):
    with open(filename) as f:
        data = f.read()
    lines = data.splitlines()

    tree = parse_into_tree(lines[0])

    for i in lines[1:]:
        second = parse_into_tree(i)
        tree = add(tree, second)

    return tree


def magnitude(node: Node):
    if isinstance(node, Value):
        return node.value
    elif isinstance(node, Inner):
        return 3 * magnitude(node.left) + 2 * magnitude(node.right)

def max_magnitude(filename: str):
    with open(filename) as f:
        data = f.read()
    lines = data.splitlines()

    max_magnitude = 0
    max_first = ""
    max_second = ""

    for x, y in itertools.product(lines, lines):
        first = parse_into_tree(x)
        second = parse_into_tree(y)
        result = add(first, second)

        current_magnitude = magnitude(result)

        if current_magnitude > max_magnitude:
            max_magnitude = current_magnitude
            max_first = x
            max_second = y

    print(max_first)
    print(max_second)
    return max_magnitude

def main():
    test_explode("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]")
    test_explode(
        "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
    )
    test_explode("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]")

    test_split("[10,1]", "[[5,5],1]")
    test_split("[1,11]", "[1,[5,6]]")

    test_single_add()

    test_multiple_add(
        ["[1,1]", "[2,2]", "[3,3]", "[4,4]"], "[[[[1,1],[2,2]],[3,3]],[4,4]]"
    )

    test_multiple_add(
        ["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]", "[6,6]"],
        "[[[[5,0],[7,4]],[5,5]],[6,6]]",
    )

    t = add_file("task18/example.txt")
    r = repr(t)
    m = magnitude(t)

    assert r == "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]"
    assert m == 4140

    # t = add_file("task18/input.txt")
    # r = repr(t)
    # m = magnitude(t)

    # print(r)
    # print(m)

    max = max_magnitude("task18/input.txt")
    print(max)

if __name__ == "__main__":
    main()
