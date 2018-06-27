#!/usr/bin/env python
from antlr4 import FileStream, CommonTokenStream
from generated.Python3Lexer import Python3Lexer
from generated.Python3Parser import Python3Parser
from generated.Python3Visitor import Python3Visitor

import json
import sys

def checkAncestorInstances(node, classType):
    while(node.parentCtx):
        if isinstance(node, classType):
            return node.getChild(1).getText()
        node = node.parentCtx
    return None

class Visitor(Python3Visitor):
    def visitFuncdef(self, ctx):
        className = checkAncestorInstances(ctx, Python3Parser.ClassdefContext)
        if className:
            if className not in self.fList:
                self.fList[className] = [ctx.getChild(1).getText()]
            else:
                self.fList[className].append(ctx.getChild(1).getText())
        return self.visitChildren(ctx)

def main(args):
    file = FileStream(args[1])
    lexer = Python3Lexer(file)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    tre = parser.file_input()
    if parser.getNumberOfSyntaxErrors()!=0:
        print("File contains {} "
              "syntax errors".format(parser.getNumberOfSyntaxErrors()))
        return

    visitor = Visitor()
    visitor.fList = {}
    visitor.visit(tre)
    print(json.dumps(visitor.fList, indent=2))

if __name__ == '__main__':
    main(sys.argv)
