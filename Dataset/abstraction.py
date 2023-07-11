import ast
import astunparse

import os
import tokenize
from io import BytesIO


class ASTNodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.ARG_COUNT = 2147483647  # Number of arguments to be used in the function
        self.TOKEN_LIMIT = (
            2147483647  # Number of tokens to be used in the python program
        )

        # Counter for the number of tokens
        self.counter = {
            "variableCount": 1,
            "methodCount": 1,
            "attributeCount": 1,
            "exceptionCount": 1,
            "annotationCount": 1,
            "keywordCount": 1,
            "stringCount": 1,
            "integerCount": 1,
            "floatCount": 1,
            "bytesCount": 1,
            "iterableCount": 1,
            "moduleCount": 1,
            "aliasCount": 1,
            "formatCount": 1,
        }

        # Tokens to be used in the python program
        self.tokens = {
            "variableTokens": {},
            "methodTokens": {},
            "attributeTokens": {},
            "exceptionTokens": {},
            "annotationTokens": {},
            "keywordTokens": {},
            "stringTokens": {},
            "integerTokens": {},
            "floatTokens": {},
            "bytesTokens": {},
            "iterableTokens": {},
            "moduleTokens": {},
            "aliasTokens": {},
            "formatTokens": {},
        }

        # Flags to be used in the python program
        self.flag = {
            "callFlaginName": 0,
            "callFlaginAttribute": 0,
            "exceptionFlaginExceptHandler": 0,
            "annotationFlaginArg": 0,
            "iterableFlaginSubscript": 0,
            "formattedValueinConstant": 0,
            "UAddFlaginConstant": 0,
            "USubFlaginConstant": 0,
            "InvertFlaginConstant": 0,
            "annotationFlaginAnnAssign": 0,
        }

        # Idioms to be used in the python program
        self.idiom_list = list(set(open("new_idioms.txt", "r").read().splitlines()))
        for i in [
            8,
            100,
            0.5,
            1,
            0,
            0.0,
            4,
            -1,
            200,
            6,
            2,
            3,
            1.0,
            10,
            5,
            "-inf",
            "inf",
            "nan",
            True,
            False,
            None,
        ]:
            self.idiom_list.append(i)

    def checkTokenKey(self, token_type, key):
        """Check if the token key is present in the token dictionary

        Args:
            token_type: Type of the token
            key: Key of the token

        Returns:
            True: If the token key is present in the token dictionary
            False: If the token key is not present in the token dictionary
        """
        for k, _ in self.tokens[token_type].items():
            if k == key:
                return True
        return False

    def checkTokenValue(self, token_type, value):
        """Check if the token value is present in the token dictionary

        Args:
            token_type: Type of the token
            value: Value of the token

        Returns:
            True: If the token value is present in the token dictionary
            False: If the token value is not present in the token dictionary
        """
        for _, v in self.tokens[token_type].items():
            if v == value:
                return True
        return False

    def getTokenKey(self, token_type, value):
        """Get the token key from the token dictionary

        Args:
            token_type: Type of the token
            value: Value of the token

        Returns:
            k: Key of the token
            None: If the token value is not present in the token dictionary
        """
        for k, v in self.tokens[token_type].items():
            if v == value:
                return k
        return None

    def getTokensValue(self, token_type, key):
        """Get the token value from the token dictionary

        Args:
            token_type: Type of the token
            key: Key of the token

        Returns:
            v: Value of the token
            None: If the token key is not present in the token dictionary
        """
        for k, v in self.tokens[token_type].items():
            if k == key:
                return v
        return None

    def setToken(self, token_type, key, value):
        """Set the token in the token dictionary

        Args:
            token_type: Type of the token
            key: Key of the token
            value: Value of the token
        """
        self.tokens[token_type][key] = value

    def clearToken(self):
        """Clear the token dictionary"""
        for value in self.tokens.values():
            value.clear()
        for key, value in self.counter.items():
            self.counter[key] = 1

    def visit_FunctionDef(self, node: ast.AST):
        """ast.FunctionDef node of ast.NodeVisitor."""
        if node.decorator_list:
            raise "Raised when a decorator can be found"
        else:
            if self.counter["methodCount"] >= self.TOKEN_LIMIT:
                raise "Allowed number of token limit exceeded"
            if node.name not in self.idiom_list:
                if self.checkTokenValue(token_type="methodTokens", value=node.name):
                    node.name = self.getTokenKey(
                        token_type="methodTokens", value=node.name
                    )
                else:
                    key = "METHOD_" + str(self.counter["methodCount"])
                    self.setToken(token_type="methodTokens", key=key, value=node.name)
                    node.name = key
                    self.counter["methodCount"] += 1
        print(
            "Node type: FunctionDef and fields: ",
            node._fields,
            node.name,
            node.args,
            node.body,
            node.decorator_list,
            node.returns,
            node.type_comment,
        )
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AST):
        """ast.AsyncFunctionDef node of ast.NodeVisitor."""
        if node.decorator_list:
            raise "Raised when a decorator can be found"
        else:
            if self.counter["methodCount"] >= self.TOKEN_LIMIT:
                raise "Allowed number of token limit exceeded"
            if node.name not in self.idiom_list:
                if self.checkTokenValue(token_type="methodTokens", value=node.name):
                    node.name = self.getTokenKey(
                        token_type="methodTokens", value=node.name
                    )
                else:
                    key = "METHOD_" + str(self.counter["methodCount"])
                    self.setToken(token_type="methodTokens", key=key, value=node.name)
                    node.name = key
                    self.counter["methodCount"] += 1
        print(
            "Node type: AsyncFunctionDef and fields: ",
            node._fields,
            node.name,
            node.args,
            node.body,
            node.decorator_list,
            node.returns,
            node.type_comment,
        )
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.AST):
        """ast.ClassDef node of ast.NodeVisitor."""
        raise "Raised when a class can be found"

    def visit_Return(self, node: ast.AST):
        """ast.Return node of ast.NodeVisitor."""
        print("Node type: Return and fields: ", node._fields, node.value)
        self.generic_visit(node)

    def visit_Delete(self, node: ast.AST):
        """ast.Delete node of ast.NodeVisitor."""
        print("Node type: Delete and fields: ", node._fields, node.targets)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.AST):
        """ast.Assign node of ast.NodeVisitor."""
        print(
            "Node type: Assign and fields: ",
            node._fields,
            node.targets,
            node.value,
            node.type_comment,
        )
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AST):
        """ast.AugAssign node of ast.NodeVisitor."""
        print(
            "Node type: AugAssign and fields: ",
            node._fields,
            node.target,
            node.op,
            node.value,
        )
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AST):
        """ast.AnnAssign node of ast.NodeVisitor."""
        print(
            "Node type: AnnAssign and fields: ",
            node._fields,
            node.target,
            node.annotation,
            node.value,
            node.simple,
        )
        self.generic_visit(node)

    def visit_For(self, node: ast.AST):
        """ast.For node of ast.NodeVisitor."""
        print(
            "Node type: For and fields: ",
            node._fields,
            node.target,
            node.iter,
            node.body,
            node.orelse,
            node.type_comment,
        )
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AST):
        """ast.AsyncFor node of ast.NodeVisitor."""
        print(
            "Node type: AsyncFor and fields: ",
            node._fields,
            node.target,
            node.iter,
            node.body,
            node.orelse,
            node.type_comment,
        )
        self.generic_visit(node)

    def visit_While(self, node: ast.AST):
        """ast.While node of ast.NodeVisitor."""
        print(
            "Node type: While and fields: ",
            node._fields,
            node.test,
            node.body,
            node.orelse,
        )
        self.generic_visit(node)

    def visit_If(self, node: ast.AST):
        """ast.If node of ast.NodeVisitor."""
        print(
            "Node type: If and fields: ",
            node._fields,
            node.test,
            node.body,
            node.orelse,
        )
        self.generic_visit(node)

    def visit_With(self, node: ast.AST):
        """ast.With node of ast.NodeVisitor."""
        print(
            "Node type: With and fields: ",
            node._fields,
            node.items,
            node.body,
            node.type_comment,
        )
        self.generic_visit(node)

    def visit_AsyncWith(self, node: ast.AST):
        """ast.AsyncWith node of ast.NodeVisitor."""
        print(
            "Node type: AsyncWith and fields: ",
            node._fields,
            node.items,
            node.body,
            node.type_comment,
        )
        self.generic_visit(node)

    def visit_Raise(self, node: ast.AST):
        """ast.Raise node of ast.NodeVisitor."""
        print("Node type: Raise and fields: ", node._fields, node.exc, node.cause)
        self.generic_visit(node)

    def visit_Try(self, node: ast.AST):
        """ast.Try node of ast.NodeVisitor."""
        print(
            "Node type: Try and fields: ",
            node._fields,
            node.body,
            node.handlers,
            node.orelse,
            node.finalbody,
        )
        self.generic_visit(node)

    def visit_Assert(self, node: ast.AST):
        """ast.Assert node of ast.NodeVisitor."""
        print("Node type: Assert and fields: ", node._fields, node.test, node.msg)
        self.generic_visit(node)

    def visit_Import(self, node: ast.AST):
        """ast.Import node of ast.NodeVisitor."""
        print("Node type: Import and fields: ", node._fields, node.names)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.AST):
        """ast.ImportFrom node of ast.NodeVisitor."""
        if self.counter["moduleCount"] >= self.TOKEN_LIMIT:
            raise "Allowed number of token limit exceeded"
        if node.module not in self.idiom_list:
            if self.checkTokenValue(token_type="moduleTokens", value=node.module):
                node.module = self.getTokenKey(
                    token_type="moduleTokens", value=node.module
                )
            else:
                key = "MODULE_" + str(self.counter["moduleCount"])
                self.setToken(token_type="moduleTokens", key=key, value=node.module)
                node.module = key
                self.counter["moduleCount"] += 1
        print(
            "Node type: ImportFrom and fields: ",
            node._fields,
            node.module,
            node.names,
            node.level,
        )
        self.generic_visit(node)

    def visit_Global(self, node: ast.AST):
        """ast.Global node of ast.NodeVisitor."""
        if self.counter["variableCount"] >= self.TOKEN_LIMIT:
            raise "Allowed number of token limit exceeded"
        for idx, _ in enumerate(node.names):
            if node.names[idx] not in self.idiom_list:
                if self.checkTokenValue(
                    token_type="variableTokens", value=node.names[idx]
                ):
                    node.names[idx] = self.getTokenKey(
                        token_type="variableTokens", value=node.names[idx]
                    )
                else:
                    key = "VAR_" + str(self.counter["variableCount"])
                    self.setToken(
                        token_type="variableTokens", key=key, value=node.names[idx]
                    )
                    node.names[idx] = key
                    self.counter["variableCount"] += 1
        print("Node type: Global and fields: ", node._fields, node.names)
        self.generic_visit(node)

    def visit_Nonlocal(self, node: ast.AST):
        """ast.Nonlocal node of ast.NodeVisitor."""
        if self.counter["variableCount"] >= self.TOKEN_LIMIT:
            raise "Allowed number of token limit exceeded"
        for idx, _ in enumerate(node.names):
            if node.names[idx] not in self.idiom_list:
                if self.checkTokenValue(
                    token_type="variableTokens", value=node.names[idx]
                ):
                    node.names[idx] = self.getTokenKey(
                        token_type="variableTokens", value=node.names[idx]
                    )
                else:
                    key = "VAR_" + str(self.counter["variableCount"])
                    self.setToken(
                        token_type="variableTokens", key=key, value=node.names[idx]
                    )
                    node.names[idx] = key
                    self.counter["variableCount"] += 1
        print("Node type: Nonlocal and fields: ", node._fields, node.names)
        self.generic_visit(node)

    def visit_Expr(self, node: ast.AST):
        """ast.Expr node of ast.NodeVisitor."""
        print("Node type: Expr and fields: ", node._fields, node.value)
        self.generic_visit(node)

    def visit_Pass(self, node: ast.AST):
        """ast.Pass node of ast.NodeVisitor."""
        print("Node type: Pass and fields: ", node._fields)
        self.generic_visit(node)

    def visit_Break(self, node: ast.AST):
        """ast.Break node of ast.NodeVisitor."""
        print("Node type: Break and fields: ", node._fields)
        self.generic_visit(node)

    def visit_Continue(self, node: ast.AST):
        """ast.Continue node of ast.NodeVisitor."""
        print("Node type: Continue and fields: ", node._fields)
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.AST):
        """ast.BoolOp node of ast.NodeVisitor."""
        print("Node type: BoolOp and fields: ", node._fields, node.op, node.values)
        self.generic_visit(node)

    def visit_NamedExpr(self, node: ast.AST):
        """ast.NamedExpr node of ast.NodeVisitor."""
        print(
            "Node type: NamedExpr and fields: ", node._fields, node.target, node.value
        )
        self.generic_visit(node)

    def visit_BinOp(self, node: ast.AST):
        """ast.BinOp node of ast.NodeVisitor."""
        print(
            "Node type: BinOp and fields: ",
            node._fields,
            node.left,
            node.op,
            node.right,
        )
        self.generic_visit(node)

    def visit_UnaryOp(self, node: ast.AST):
        """ast.UnaryOp node of ast.NodeVisitor."""
        print("Node type: UnaryOp and fields: ", node._fields, node.op, node.operand)
        self.generic_visit(node)

    def visit_Lambda(self, node: ast.AST):
        """ast.Lambda node of ast.NodeVisitor."""
        print("Node type: Lambda and fields: ", node._fields, node.args, node.body)
        self.generic_visit(node)

    def visit_IfExp(self, node: ast.AST):
        """ast.IfExp node of ast.NodeVisitor."""
        print(
            "Node type: IfExp and fields: ",
            node._fields,
            node.test,
            node.body,
            node.orelse,
        )
        self.generic_visit(node)

    def visit_Dict(self, node: ast.AST):
        """ast.Dict node of ast.NodeVisitor."""
        print("Node type: Dict and fields: ", node._fields, node.keys, node.values)
        self.generic_visit(node)

    def visit_Set(self, node: ast.AST):
        """ast.Set node of ast.NodeVisitor."""
        print("Node type: Set and fields: ", node._fields, node.elts)
        self.generic_visit(node)

    def visit_ListComp(self, node: ast.AST):
        """ast.ListComp node of ast.NodeVisitor."""
        print(
            "Node type: ListComp and fields: ", node._fields, node.elt, node.generators
        )
        self.generic_visit(node)

    def visit_SetComp(self, node: ast.AST):
        """ast.SetComp node of ast.NodeVisitor."""
        print(
            "Node type: SetComp and fields: ", node._fields, node.elt, node.generators
        )
        self.generic_visit(node)

    def visit_DictComp(self, node: ast.AST):
        """ast.DictComp node of ast.NodeVisitor."""
        print(
            "Node type: DictComp and fields: ",
            node._fields,
            node.key,
            node.value,
            node.generators,
        )
        self.generic_visit(node)

    def visit_GeneratorExp(self, node: ast.AST):
        """ast.GeneratorExp node of ast.NodeVisitor."""
        print(
            "Node type: GeneratorExp and fields: ",
            node._fields,
            node.elt,
            node.generators,
        )
        self.generic_visit(node)

    def visit_Await(self, node: ast.AST):
        """ast.Await node of ast.NodeVisitor."""
        print("Node type: Await and fields: ", node._fields, node.value)
        self.generic_visit(node)

    def visit_Yield(self, node: ast.AST):
        """ast.Yield node of ast.NodeVisitor."""
        print("Node type: Yield and fields: ", node._fields, node.value)
        self.generic_visit(node)

    def visit_YieldFrom(self, node: ast.AST):
        """ast.YieldFrom node of ast.NodeVisitor."""
        print("Node type: YieldFrom and fields: ", node._fields, node.value)
        self.generic_visit(node)

    def visit_Compare(self, node: ast.AST):
        """ast.Compare node of ast.NodeVisitor."""
        print(
            "Node type: Compare and fields: ",
            node._fields,
            node.left,
            node.ops,
            node.comparators,
        )
        self.generic_visit(node)

    def visit_Call(self, node: ast.AST):
        """ast.Call node of ast.NodeVisitor."""
        self.flag["callFlaginName"] = 1
        self.flag["callFlaginAttribute"] = 1
        print("Node type: Call and fields: ", node._fields, node.func)
        self.generic_visit(node)

    def visit_FormattedValue(self, node: ast.AST):
        """ast.FormattedValue node of ast.NodeVisitor."""
        if node.format_spec:
            self.flag["formattedValueinConstant"] = 1
        print(
            "Node type: FormattedValue and fields: ",
            node._fields,
            node.value,
            node.conversion,
            node.format_spec,
        )
        self.generic_visit(node)

    def visit_JoinedStr(self, node: ast.AST):
        """ast.JoinedStr node of ast.NodeVisitor."""
        print("Node type: JoinedStr and fields: ", node._fields, node.values)
        self.generic_visit(node)

    def visit_Constant(self, node: ast.AST):
        """ast.Constant node of ast.NodeVisitor."""
        if (
            self.counter["stringCount"] >= self.TOKEN_LIMIT
            or self.counter["formatCount"] >= self.TOKEN_LIMIT
            or self.counter["integerCount"] >= self.TOKEN_LIMIT
            or self.counter["floatCount"] >= self.TOKEN_LIMIT
            or self.counter["bytesCount"] >= self.TOKEN_LIMIT
        ):
            raise "Allowed number of token limit exceeded"
        if node.value not in self.idiom_list:
            if isinstance(node.value, str):
                if self.flag["formattedValueinConstant"] == 0:
                    if self.checkTokenValue(
                        token_type="stringTokens", value=node.value
                    ):
                        node.value = self.getTokenKey(
                            token_type="stringTokens", value=node.value
                        )
                    else:
                        key = "STR_" + str(self.counter["stringCount"])
                        self.setToken(
                            token_type="stringTokens", key=key, value=node.value
                        )
                        node.value = key
                        self.counter["stringCount"] += 1
                else:
                    if self.checkTokenValue(
                        token_type="formatTokens", value=node.value
                    ):
                        node.value = self.getTokenKey(
                            token_type="formatTokens", value=node.value
                        )
                    else:
                        key = "FORMAT_" + str(self.counter["formatCount"])
                        self.setToken(
                            token_type="formatTokens", key=key, value=node.value
                        )
                        node.value = key
                        self.counter["formatCount"] += 1
                    self.flag["formattedValueinConstant"] = 0
            elif isinstance(node.value, int):
                if self.flag["UAddFlaginConstant"] == 1:
                    if self.checkTokenValue(
                        token_type="integerTokens", value=+node.value
                    ):
                        node.value = self.getTokenKey(
                            token_type="integerTokens", value=+node.value
                        )
                    else:
                        node.value = +node.value
                        key = "INT_" + str(self.counter["integerCount"])
                        self.setToken(
                            token_type="integerTokens", key=key, value=node.value
                        )
                        node.value = key
                        print(node.value)
                        self.counter["integerCount"] += 1
                    self.flag["UAddFlaginConstant"] = 0
                elif self.flag["USubFlaginConstant"] == 1:
                    if self.checkTokenValue(
                        token_type="integerTokens", value=-node.value
                    ):
                        node.value = self.getTokenKey(
                            token_type="integerTokens", value=-node.value
                        )
                    else:
                        node.value = -node.value
                        key = "INT_" + str(self.counter["integerCount"])
                        self.setToken(
                            token_type="integerTokens", key=key, value=node.value
                        )
                        node.value = key
                        self.counter["integerCount"] += 1
                    self.flag["USubFlaginConstant"] = 0
                elif self.flag["InvertFlaginConstant"] == 1:
                    if self.checkTokenValue(
                        token_type="integerTokens", value=~node.value
                    ):
                        node.value = self.getTokenKey(
                            token_type="integerTokens", value=~node.value
                        )
                    else:
                        node.value = ~node.value
                        key = "INT_" + str(self.counter["integerCount"])
                        self.setToken(
                            token_type="integerTokens", key=key, value=node.value
                        )
                        node.value = key
                        self.counter["integerCount"] += 1
                        self.flag["InvertFlaginConstant"] = 0
                else:
                    if self.checkTokenValue(
                        token_type="integerTokens", value=node.value
                    ):
                        node.value = self.getTokenKey(
                            token_type="integerTokens", value=node.value
                        )
                    else:
                        key = "INT_" + str(self.counter["integerCount"])
                        self.setToken(
                            token_type="integerTokens", key=key, value=node.value
                        )
                        node.value = key
                        self.counter["integerCount"] += 1
            elif isinstance(node.value, float):
                if self.flag["UAddFlaginConstant"] == 1:
                    if self.checkTokenValue(
                        token_type="floatTokens", value=+node.value
                    ):
                        node.value = self.getTokenKey(
                            token_type="floatTokens", value=+node.value
                        )
                    else:
                        node.value = +node.value
                        key = "FLOAT_" + str(self.counter["floatCount"])
                        self.setToken(
                            token_type="floatTokens", key=key, value=node.value
                        )
                        node.value = key
                        self.counter["floatCount"] += 1
                    self.flag["UAddFlaginConstant"] = 0
                elif self.flag["USubFlaginConstant"] == 1:
                    if self.checkTokenValue(
                        token_type="floatTokens", value=-node.value
                    ):
                        node.value = self.getTokenKey(
                            token_type="floatTokens", value=-node.value
                        )
                    else:
                        node.value = -node.value
                        key = "FLOAT_" + str(self.counter["floatCount"])
                        self.setToken(
                            token_type="floatTokens", key=key, value=node.value
                        )
                        node.value = key
                        self.counter["floatCount"] += 1
                    self.flag["USubFlaginConstant"] = 0
                else:
                    if self.checkTokenValue(token_type="floatTokens", value=node.value):
                        node.value = self.getTokenKey(
                            token_type="floatTokens", value=node.value
                        )
                    else:
                        key = "FLOAT_" + str(self.counter["floatCount"])
                        self.setToken(
                            token_type="floatTokens", key=key, value=node.value
                        )
                        node.value = key
                        self.counter["floatCount"] += 1
            elif isinstance(node.value, bytes):
                if self.checkTokenValue(token_type="bytesTokens", value=node.value):
                    node.value = self.getTokenKey(
                        token_type="bytesTokens", value=node.value
                    )
                else:
                    key = "BYTES_" + str(self.counter["bytesCount"])
                    self.setToken(token_type="bytesTokens", key=key, value=node.value)
                    node.value = key
                    self.counter["bytesCount"] += 1
        print("Node type: Constant and fields: ", node._fields, node.value)
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.AST):
        """ast.Attribute node of ast.NodeVisitor."""
        if (
            self.counter["attributeCount"] >= self.TOKEN_LIMIT
            or self.counter["methodCount"] >= self.TOKEN_LIMIT
        ):
            raise "Allowed number of token limit exceeded"
        if node.attr not in self.idiom_list:
            if self.flag["callFlaginAttribute"] == 0:  # For Attribute
                if self.checkTokenValue(token_type="attributeTokens", value=node.attr):
                    node.attr = self.getTokenKey(
                        token_type="attributeTokens", value=node.attr
                    )
                else:
                    key = "ATTRIBUTE_" + str(self.counter["attributeCount"])
                    self.setToken(
                        token_type="attributeTokens", key=key, value=node.attr
                    )
                    node.attr = key
                    self.counter["attributeCount"] += 1
                print("Node type: Name and fields ATTRIBUTE: ", node._fields, node.attr)
            elif self.flag["callFlaginAttribute"] == 1:  # For Method
                if self.checkTokenValue(token_type="methodTokens", value=node.attr):
                    node.attr = self.getTokenKey(
                        token_type="methodTokens", value=node.attr
                    )
                else:
                    key = "METHOD_" + str(self.counter["methodCount"])
                    self.setToken(token_type="methodTokens", key=key, value=node.attr)
                    node.attr = key
                    self.counter["methodCount"] += 1
                print("Node type: Name and fields METHOD: ", node._fields, node.attr)

        self.flag["callFlaginAttribute"] = 0
        self.flag["callFlaginName"] = 0
        self.generic_visit(node)

    def visit_Subscript(self, node: ast.AST):
        """ast.Subscript node of ast.NodeVisitor."""
        if node.value:
            self.flag["iterableFlaginSubscript"] = 1
        else:
            self.flag["iterableFlaginSubscript"] = 0

        print("Node type: Subscript and fields: ", node._fields, node.value, node.ctx)
        self.generic_visit(node)

    def visit_Starred(self, node: ast.AST):
        """ast.Starred node of ast.NodeVisitor."""
        print("Node type: Starred and fields: ", node._fields, node.value, node.ctx)
        self.generic_visit(node)

    def visit_Name(self, node: ast.AST):
        if (
            self.counter["exceptionCount"] >= self.TOKEN_LIMIT
            or self.counter["annotationCount"] >= self.TOKEN_LIMIT
            or self.counter["iterableCount"] >= self.TOKEN_LIMIT
            or self.counter["variableCount"] >= self.TOKEN_LIMIT
            or self.counter["methodCount"] >= self.TOKEN_LIMIT
        ):
            raise "Allowed number of token limit exceeded"
        if node.id not in self.idiom_list:
            if self.checkTokenValue(token_type="aliasTokens", value=node.id):
                node.id = self.getTokenKey(token_type="aliasTokens", value=node.id)
            else:
                if self.flag["exceptionFlaginExceptHandler"] == 1:
                    if self.checkTokenValue(
                        token_type="exceptionTokens", value=node.id
                    ):
                        node.id = self.getTokenKey(
                            token_type="exceptionTokens", value=node.id
                        )
                    else:
                        key = "EXCEPTION_" + str(self.counter["exceptionCount"])
                        self.setToken(
                            token_type="exceptionTokens", key=key, value=node.id
                        )
                        node.id = key
                        self.counter["exceptionCount"] += 1
                elif self.flag["annotationFlaginArg"] == 1:
                    if self.checkTokenValue(
                        token_type="annotationTokens", value=node.id
                    ):
                        node.id = self.getTokenKey(
                            token_type="annotationTokens", value=node.id
                        )
                    else:
                        key = "ANNOTATION_" + str(self.counter["annotationCount"])
                        self.setToken(
                            token_type="annotationTokens", key=key, value=node.id
                        )
                        node.id = key
                        self.counter["annotationCount"] += 1
                    self.flag["annotationFlaginArg"] = 0
                elif self.flag["iterableFlaginSubscript"] == 1:
                    if self.checkTokenValue(token_type="iterableTokens", value=node.id):
                        node.id = self.getTokenKey(
                            token_type="iterableTokens", value=node.id
                        )
                    else:
                        key = "ITERABLE_" + str(self.counter["iterableCount"])
                        self.setToken(
                            token_type="iterableTokens", key=key, value=node.id
                        )
                        node.id = key
                        self.counter["iterableCount"] += 1
                elif self.flag["callFlaginName"] == 0:  # For Variable - Default
                    if self.checkTokenValue(token_type="variableTokens", value=node.id):
                        node.id = self.getTokenKey(
                            token_type="variableTokens", value=node.id
                        )
                    else:
                        key = "VAR_" + str(self.counter["variableCount"])
                        self.setToken(
                            token_type="variableTokens", key=key, value=node.id
                        )
                        node.id = key
                        self.counter["variableCount"] += 1
                elif self.flag["callFlaginName"] == 1:  # For Method
                    if self.checkTokenValue(token_type="methodTokens", value=node.id):
                        node.id = self.getTokenKey(
                            token_type="methodTokens", value=node.id
                        )
                    else:
                        key = "METHOD_" + str(self.counter["methodCount"])
                        self.setToken(token_type="methodTokens", key=key, value=node.id)
                        node.id = key
                        self.counter["methodCount"] += 1

        self.flag["callFlaginName"] = 0
        self.flag["callFlaginAttribute"] = 0
        self.flag["exceptionFlaginExceptHandler"] = 0
        self.flag["annotationFlaginArg"] = 0
        self.flag["iterableFlaginSubscript"] = 0
        self.generic_visit(node)

    def visit_List(self, node: ast.AST):
        """ast.List node of ast.NodeVisitor."""
        print("Node type: List and fields: ", node._fields, node.elts, node.ctx)
        self.generic_visit(node)

    def visit_Tuple(self, node: ast.AST):
        """ast.Tuple node of ast.NodeVisitor."""
        print("Node type: Tuple and fields: ", node._fields, node.elts, node.ctx)
        self.generic_visit(node)

    def visit_Slice(self, node: ast.AST):
        """ast.Slice node of ast.NodeVisitor."""
        print(
            "Node type: Slice and fields: ",
            node._fields,
            node.lower,
            node.upper,
            node.step,
        )
        self.generic_visit(node)

    def visit_Load(self, node: ast.AST):
        """ast.Load node of ast.NodeVisitor."""
        print("Node type: Load and fields: ", node._fields)
        self.generic_visit(node)

    def visit_Store(self, node: ast.AST):
        """ast.Store node of ast.NodeVisitor."""
        print("Node type: Store and fields: ", node._fields)
        self.generic_visit(node)

    def visit_Del(self, node: ast.AST):
        """ast.Del node of ast.NodeVisitor."""
        print("Node type: Del and fields: ", node._fields)
        self.generic_visit(node)

    def visit_And(self, node: ast.AST):
        """ast.And node of ast.NodeVisitor."""
        print("Node type: And and fields: ", node._fields)
        self.generic_visit(node)

    def visit_Or(self, node: ast.AST):
        """ast.Or node of ast.NodeVisitor."""
        print("Node type: Or and fields: ", node._fields)
        self.generic_visit(node)

    def visit_Add(self, node: ast.AST):
        """ast.Add node of ast.NodeVisitor."""
        print("Node type: Add and fields: ", node._fields)
        self.generic_visit(node)

    def visit_Sub(self, node: ast.AST):
        """ast.Sub node of ast.NodeVisitor."""
        print("Node type: Sub and fields: ", node._fields)
        self.generic_visit(node)

    def visit_Mult(self, node: ast.AST):
        """ast.Mult node of ast.NodeVisitor."""
        print("Node type: Mult and fields: ", node._fields)
        self.generic_visit(node)

    def visit_MatMult(self, node: ast.AST):
        """ast.MatMult node of ast.NodeVisitor."""
        print("Node type: MatMult and fields: ", node._fields)
        self.generic_visit(node)

    def visit_Div(self, node: ast.AST):
        """ast.Div node of ast.NodeVisitor."""
        print("Node type: Div and fields: ", node._fields)
        self.generic_visit(node)

    def visit_Mod(self, node: ast.AST):
        """ast.Mod node of ast.NodeVisitor."""
        print("Node type: Mod and fields: ", node._fields)
        self.generic_visit(node)

    def visit_Pow(self, node: ast.AST):
        """ast.Pow node of ast.NodeVisitor."""
        print("Node type: Pow and fields: ", node._fields)
        self.generic_visit(node)

    def visit_LShift(self, node: ast.AST):
        """ast.LShift node of ast.NodeVisitor."""
        print("Node type: LShift and fields: ", node._fields)
        self.generic_visit(node)

    def visit_RShift(self, node: ast.AST):
        """ast.RShift node of ast.NodeVisitor."""
        print("Node type: RShift and fields: ", node._fields)
        self.generic_visit(node)

    def visit_BitOr(self, node: ast.AST):
        """ast.BitOr node of ast.NodeVisitor."""
        print("Node type: BitOr and fields: ", node._fields)
        self.generic_visit(node)

    def visit_BitXor(self, node: ast.AST):
        """ast.BitXor node of ast.NodeVisitor."""
        print("Node type: BitXor and fields: ", node._fields)
        self.generic_visit(node)

    def visit_BitAnd(self, node: ast.AST):
        """ast.BitAnd node of ast.NodeVisitor."""
        print("Node type: BitAnd and fields: ", node._fields)
        self.generic_visit(node)

    def visit_FloorDiv(self, node: ast.AST):
        """ast.FloorDiv node of ast.NodeVisitor."""
        print("Node type: FloorDiv and fields: ", node._fields)
        self.generic_visit(node)

    def visit_Invert(self, node: ast.AST):
        """ast.Invert node of ast.NodeVisitor."""
        self.flag["InvertFlaginConstant"] = 1
        print("Node type: Invert and fields: ", node._fields)
        self.generic_visit(node)

    def visit_Not(self, node: ast.AST):
        """ast.Not node of ast.NodeVisitor."""
        print("Node type: Not and fields: ", node._fields)
        self.generic_visit(node)

    def visit_UAdd(self, node: ast.AST):
        """ast.UAdd node of ast.NodeVisitor."""
        self.flag["UAddFlaginConstant"] = 1
        print("Node type: UAdd and fields: ", node._fields)
        self.generic_visit(node)

    def visit_USub(self, node: ast.AST):
        """ast.USub node of ast.NodeVisitor."""
        self.flag["USubFlaginConstant"] = 1
        print("Node type: USub and fields: ", node._fields)
        self.generic_visit(node)

    def visit_Eq(self, node: ast.AST):
        """ast.Eq node of ast.NodeVisitor."""
        print("Node type: Eq and fields: ", node._fields)
        self.generic_visit(node)

    def visit_NotEq(self, node: ast.AST):
        """ast.NotEq node of ast.NodeVisitor."""
        print("Node type: NotEq and fields: ", node._fields)
        self.generic_visit(node)

    def visit_Lt(self, node: ast.AST):
        """ast.Lt node of ast.NodeVisitor."""
        print("Node type: Lt and fields: ", node._fields)
        self.generic_visit(node)

    def visit_LtE(self, node: ast.AST):
        """ast.LtE node of ast.NodeVisitor."""
        print("Node type: LtE and fields: ", node._fields)
        self.generic_visit(node)

    def visit_Gt(self, node: ast.AST):
        """ast.Gt node of ast.NodeVisitor."""
        print("Node type: Gt and fields: ", node._fields)
        self.generic_visit(node)

    def visit_GtE(self, node: ast.AST):
        """ast.GtE node of ast.NodeVisitor."""
        print("Node type: GtE and fields: ", node._fields)
        self.generic_visit(node)

    def visit_Is(self, node: ast.AST):
        """ast.Is node of ast.NodeVisitor."""
        print("Node type: Is and fields: ", node._fields)
        self.generic_visit(node)

    def visit_IsNot(self, node: ast.AST):
        """ast.IsNot node of ast.NodeVisitor."""
        print("Node type: IsNot and fields: ", node._fields)
        self.generic_visit(node)

    def visit_In(self, node: ast.AST):
        """ast.In node of ast.NodeVisitor."""
        print("Node type: In and fields: ", node._fields)
        self.generic_visit(node)

    def visit_NotIn(self, node: ast.AST):
        """ast.NotIn node of ast.NodeVisitor."""
        print("Node type: NotIn and fields: ", node._fields)
        self.generic_visit(node)

    def visit_comprehension(self, node: ast.AST):
        """ast.comprehension node of ast.NodeVisitor."""
        print(
            "Node type: comprehension and fields: ",
            node._fields,
            node.target,
            node.iter,
            node.ifs,
            node.is_async,
        )
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.AST):
        """ast.ExceptHandler node of ast.NodeVisitor."""
        if self.counter["variableCount"] >= self.TOKEN_LIMIT:
            raise "Allowed number of token limit exceeded"

        if node.type:
            self.flag["exceptionFlaginExceptHandler"] = 1
        else:
            self.flag["exceptionFlaginExceptHandler"] = 0

        if node.name not in self.idiom_list:
            if node.name is not None:
                if self.checkTokenValue(token_type="variableTokens", value=node.name):
                    node.name = self.getTokenKey(
                        token_type="variableTokens", value=node.name
                    )
                else:
                    key = "VAR_" + str(self.counter["variableCount"])
                    self.setToken(token_type="variableTokens", key=key, value=node.name)
                    node.name = key
                    self.counter["variableCount"] += 1

        print(
            "Node type: ExceptHandler and fields: ",
            node._fields,
            node.type,
            node.name,
            node.body,
        )
        self.generic_visit(node)

    def visit_arguments(self, node: ast.AST):
        """ast.arguments node of ast.NodeVisitor."""
        print(
            "Node type: arg and fields: ",
            node._fields,
            node.posonlyargs,
            node.args,
            node.vararg,
            node.kwonlyargs,
            node.kw_defaults,
            node.kwarg,
            node.defaults,
        )
        self.generic_visit(node)

    def visit_arg(self, node: ast.AST):
        """ast.arg node of ast.NodeVisitor."""
        if self.counter["variableCount"] >= self.ARG_COUNT:
            raise "Allowed number of token limit exceeded"
        if node.arg not in self.idiom_list:
            if self.checkTokenValue(token_type="variableTokens", value=node.arg):
                node.arg = self.getTokenKey(token_type="variableTokens", value=node.arg)
            else:
                key = "VAR_" + str(self.counter["variableCount"])
                self.setToken(token_type="variableTokens", key=key, value=node.arg)
                node.arg = key
                self.counter["variableCount"] += 1
        print(
            "Node type: arg and fields: ",
            node._fields,
            node.arg,
            node.annotation,
            node.type_comment,
        )

        if node.annotation:
            self.flag["annotationFlaginArg"] = 1
        self.generic_visit(node)

    def visit_keyword(self, node: ast.AST):
        """ast.keyword node of ast.NodeVisitor."""
        if self.counter["keywordCount"] >= self.TOKEN_LIMIT:
            raise "Allowed number of token limit exceeded"
        if node.arg is not None:
            if node.arg not in self.idiom_list:
                if self.checkTokenValue(token_type="keywordTokens", value=node.arg):
                    node.arg = self.getTokenKey(
                        token_type="keywordTokens", value=node.arg
                    )
                else:
                    key = "KEYWORD_" + str(self.counter["keywordCount"])
                    self.setToken(token_type="keywordTokens", key=key, value=node.arg)
                    node.arg = key
                    self.counter["keywordCount"] += 1
        print("Node type: keyword and fields: ", node._fields, node.arg, node.value)
        self.generic_visit(node)

    def visit_alias(self, node: ast.AST):
        if self.counter["aliasCount"] >= self.TOKEN_LIMIT:
            raise "Allowed number of token limit exceeded"
        if node.name not in self.idiom_list:
            if node.name == node.asname:
                if self.checkTokenValue(token_type="aliasTokens", value=node.name):
                    node.name = self.getTokenKey(
                        token_type="aliasTokens", value=node.name
                    )
                    node.asname = self.getTokenKey(
                        token_type="aliasTokens", value=node.asname
                    )
                else:
                    key = "ALIAS_" + str(self.counter["aliasCount"])
                    self.setToken(token_type="aliasTokens", key=key, value=node.name)
                    node.name = key
                    node.asname = key
                    self.counter["aliasCount"] += 1
            else:
                if self.checkTokenValue(token_type="aliasTokens", value=node.name):
                    node.name = self.getTokenKey(
                        token_type="aliasTokens", value=node.name
                    )
                else:
                    key = "ALIAS_" + str(self.counter["aliasCount"])
                    self.setToken(token_type="aliasTokens", key=key, value=node.name)
                    node.name = key
                    self.counter["aliasCount"] += 1
                if node.asname is not None:
                    if self.checkTokenValue(
                        token_type="aliasTokens", value=node.asname
                    ):
                        node.asname = self.getTokenKey(
                            token_type="aliasTokens", value=node.asname
                        )
                    else:
                        key = "ALIAS_" + str(self.counter["aliasCount"])
                        self.setToken(
                            token_type="aliasTokens", key=key, value=node.asname
                        )
                        node.asname = key
                        self.counter["aliasCount"] += 1
        self.generic_visit(node)

    def visit_withitem(self, node: ast.AST):
        """ast.withitem node of ast.NodeVisitor."""
        print(
            "Node type: withitem and fields: ",
            node._fields,
            node.context_expr,
            node.optional_vars,
        )
        self.generic_visit(node)


def remove_docstring(source_path: str):
    with open(source_path, "r") as source:
        source_ast = ast.parse(source.read())

        for node in ast.walk(source_ast):
            if not isinstance(
                node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef, ast.Module)
            ):
                continue
            if not len(node.body):
                continue
            if not isinstance(node.body[0], ast.Expr):
                continue
            if not hasattr(node.body[0], "value") or not isinstance(
                node.body[0].value, ast.Str
            ):
                continue

            node.body = node.body[1:]

    return source_ast


def inline_code(source: str):
    tokens = tokenize.tokenize(BytesIO(source.encode("utf-8")).readline)

    token_list = []
    for token in tokens:
        if (
            token.type == tokenize.NEWLINE
            or token.type == tokenize.NL
            or token.string == "\n"
        ):
            token_list.append("NEWLINE")
            # print("NEWLINE")
        elif token.type == tokenize.INDENT:
            token_list.append("INDENT")
            # print("INDENT")
        elif token.type == tokenize.DEDENT:
            token_list.append("DEDENT")
            # print("DEDENT")
        else:
            token_list.append(token.string)
            # print(token.string)

    return " ".join(token_list[3:])


def main():
    source_ast = remove_docstring("test.py")
    ast_visitor = ASTNodeVisitor()
    ast_visitor.visit(
        source_ast
    )  # With visit function, walking through AST nodes starts
    source = astunparse.unparse(
        source_ast
    )  # Abstracted AST is converted back to source code.
    print(source)

    print(inline_code(source))


if __name__ == "__main__":
    main()
