"""Les routes se comparent au CHEMIN, jamais a `self.path`.

    python3 site/test_routes_chemin.py

⚠ POURQUOI. `self.path` contient la chaine de requete. Un formulaire
`<form method="get" action="/reprendre">` sans champ envoie « /reprendre? »,
avec le point d'interrogation : compare a « /reprendre », l'egalite est fausse
et le site repond « Introuvable ».

⚠ ET RIEN NE LE SIGNALE. Une route qui ne correspond a rien tombe dans le
`else` final : pas d'exception, pas de trace, juste une page morte. Constate EN
PRODUCTION le 14/09/2026 sur le bouton « Reprendre », qui n'avait jamais pu
marcher depuis sa livraison la veille. Les 33 comparaisons du fichier portaient
toutes sur `self.path`.

⚠ LE CAS QUI COMPTE LE PLUS est `aucune route ne compare self.path` : c'est lui
qui empeche la faute de revenir. Les autres verifient que la propriete fait bien
ce qu'elle promet.
"""

import ast
import io
import os
import sys
import urllib.parse

ICI = os.path.dirname(os.path.abspath(__file__))
FICHIER = os.path.join(ICI, 'orchestrateur.py')

echecs = []


def verifier(nom, obtenu, attendu):
    if obtenu == attendu:
        print(f"  ok   {nom}")
    else:
        print(f"  ECHEC {nom} : obtenu {obtenu!r}, attendu {attendu!r}")
        echecs.append(nom)


def comparaisons_sur_path():
    """Les lignes qui comparent `self.path` au lieu de `self.chemin`."""
    arbre = ast.parse(io.open(FICHIER, encoding='utf-8').read())

    def est_self_path(noeud):
        return (isinstance(noeud, ast.Attribute) and noeud.attr == 'path'
                and isinstance(noeud.value, ast.Name) and noeud.value.id == 'self')

    fautives = []
    for noeud in ast.walk(arbre):
        # `self.path == "..."`, `self.path in (...)`
        if isinstance(noeud, ast.Compare) and est_self_path(noeud.left):
            fautives.append(noeud.lineno)
        # `self.path.startswith(...)`
        if (isinstance(noeud, ast.Call) and isinstance(noeud.func, ast.Attribute)
                and noeud.func.attr == 'startswith' and est_self_path(noeud.func.value)):
            fautives.append(noeud.lineno)
        # `self.path[1:]` : un chemin decoupe, donc traite comme un chemin
        if isinstance(noeud, ast.Subscript) and est_self_path(noeud.value):
            fautives.append(noeud.lineno)
    return sorted(set(fautives))


def main():
    sys.path.insert(0, ICI)
    import orchestrateur as o  # noqa: E402

    print("La propriete rend bien le chemin seul")

    class FauxHandler:
        chemin = o.Handler.chemin

        def __init__(self, path):
            self.path = path

    for brut, attendu in (
        ('/reprendre?', '/reprendre'),          # le cas reel : formulaire GET sans champ
        ('/reprendre', '/reprendre'),
        ('/entrer?x=1&y=2', '/entrer'),
        ('/inscription?i=abc', '/inscription'),
        ('/', '/'),
        ('/favicon.ico', '/favicon.ico'),
    ):
        verifier(f"{brut!r} -> {attendu!r}", FauxHandler(brut).chemin, attendu)

    print("\naucune route ne compare self.path")
    # ⚠ C'EST CE CAS QUI EMPECHE LA FAUTE DE REVENIR. Sans lui, la prochaine
    # route ecrite avec `self.path ==` retomberait dans le meme piege, et
    # personne ne le verrait avant qu'un joueur bute dessus.
    fautives = comparaisons_sur_path()
    verifier("aucune comparaison sur self.path", fautives, [])

    print("\nla route de reprise repond bien aux deux formes")
    # Les deux chemins que le navigateur peut produire pour le meme bouton.
    routes = ("/entrer", "/reprendre", "/nouvelle-partie")
    for brut in ("/reprendre", "/reprendre?"):
        verifier(f"{brut!r} est reconnue", FauxHandler(brut).chemin in routes, True)

    print()
    if echecs:
        print(f"{len(echecs)} ECHEC(S) : " + ', '.join(echecs))
        return 1
    print("tout est vert")
    return 0


if __name__ == '__main__':
    sys.exit(main())
