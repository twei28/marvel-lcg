"""Repare les artefacts systematiques de pycdc dans le code decompile."""
import ast, re, sys

class Fixer(ast.NodeTransformer):
    def __init__(self): self.kw=0; self.lst=0
    def visit_Call(self, node):
        self.generic_visit(node)
        # f(a,b, **('x','y'))  ->  f(x=a, y=b)
        newkw=[]
        for k in node.keywords:
            if k.arg is None and isinstance(k.value, ast.Tuple) and \
               all(isinstance(e, ast.Constant) and isinstance(e.value,str) for e in k.value.elts):
                names=[e.value for e in k.value.elts]
                if len(names)<=len(node.args):
                    take=node.args[len(node.args)-len(names):]
                    node.args=node.args[:len(node.args)-len(names)]
                    for n,v in zip(names,take):
                        newkw.append(ast.keyword(arg=n, value=v))
                    self.kw+=1
                    continue
            newkw.append(k)
        node.keywords=newkw
        return node
    def visit_Subscript(self, node):
        self.generic_visit(node)
        sl=node.slice
        elts = list(sl.elts) if isinstance(sl, ast.Tuple) else [sl]
        # None[X] -> [X]
        if isinstance(node.value, ast.Constant) and node.value.value is None:
            self.lst+=1
            return ast.List(elts=elts, ctx=ast.Load())
        # [A][B] (chaine issue de None[A][B]) -> [A, B]
        if isinstance(node.value, ast.List):
            self.lst+=1
            return ast.List(elts=node.value.elts+elts, ctx=ast.Load())
        return node

def chain_lists(tree):
    """None[A][B] devient List([B]) imbrique -> aplatir en [A, B]"""
    class Flat(ast.NodeTransformer):
        def visit_List(self, node):
            self.generic_visit(node)
            out=[]
            for e in node.elts:
                out.append(e)
            return ast.List(elts=out, ctx=ast.Load())
    return Flat().visit(tree)

def fix_source(src):
    src = re.sub(r'^from\s+import\s+\*', 'from cards.pack import *', src, flags=re.M)
    try: tree=ast.parse(src)
    except SyntaxError: return None,0,0
    f=Fixer(); tree=f.visit(tree); ast.fix_missing_locations(tree)
    try: out=ast.unparse(tree)
    except Exception: return None,0,0
    return out, f.kw, f.lst

if __name__=='__main__':
    s=open(sys.argv[1]).read()
    o,a,b=fix_source(s)
    print(o if o else "ECHEC")
