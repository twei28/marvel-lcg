"""Fusionne les corrections de couleurs du poste et celles du serveur.

    python3 outils/fusionner-palettes.py <base> <local> <serveur> <sortie>

Les corrections de couleurs (`data/palettes-heros-corrections.json`) se font
aux DEUX endroits : dans l'editeur local, et dans l'editeur en ligne. Un
fichier qui ne va que dans un sens perdait l'un des deux (le deploiement
excluait ce fichier : tes corrections locales n'arrivaient jamais en ligne).

Fusion A TROIS (comme git), carte par carte :
  - `base`    : la version commune a la derniere synchronisation ;
  - `local`   : le fichier du depot, corrige a la main ici ;
  - `serveur` : le fichier du serveur, corrige a la main en ligne.
Une carte changee d'un seul cote prend ce cote. Changee des DEUX cotes
differemment : le LOCAL gagne (decision de l'utilisateur, 21/10/2026 : « si je
le fais en local, je veux que ca passe en ligne »), et le conflit est dit.

Sans `base` (premiere synchronisation) : union des deux, le local gagnant les
conflits, et RIEN n'est supprime, faute de savoir qui a retire quoi.

Fichier absent ou vide = aucune correction. Code de sortie : 0.
"""
import json
import os
import sys


def lire(chemin):
    """Le dictionnaire `palettes` d'un fichier de corrections, ou None s'il manque."""
    if not chemin or not os.path.exists(chemin) or os.path.getsize(chemin) == 0:
        return None, {}
    with open(chemin, encoding='utf-8') as f:
        brut = json.load(f)
    return brut, dict(brut.get('palettes', {}))


def fusionner(base, local, serveur):
    """(fusion, conflits) ; `base` est None a la premiere synchronisation."""
    fusion, conflits = {}, []
    for carte in sorted(set(local) | set(serveur) | set(base or {})):
        l, s = local.get(carte), serveur.get(carte)
        if base is None:
            valeur = l if l is not None else s
            if l is not None and s is not None and l != s:
                conflits.append(carte)
        else:
            b = base.get(carte)
            l_change, s_change = l != b, s != b
            if l_change and s_change and l != s:
                conflits.append(carte)
                valeur = l
            elif l_change:
                valeur = l
            elif s_change:
                valeur = s
            else:
                valeur = b
        if valeur is not None:
            fusion[carte] = valeur
    return fusion, conflits


def main(argv):
    if len(argv) != 5:
        print(__doc__)
        return 2
    chemin_base, chemin_local, chemin_serveur, sortie = argv[1:]
    brut_base, base = lire(chemin_base)
    brut_local, local = lire(chemin_local)
    _, serveur = lire(chemin_serveur)
    fusion, conflits = fusionner(base if brut_base is not None else None, local, serveur)

    modele = brut_local or {'_lisez_moi': '', 'version': 1}
    resultat = {k: v for k, v in modele.items() if k != 'palettes'}
    resultat['palettes'] = fusion
    with open(sortie, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(resultat, f, ensure_ascii=False, indent=1, sort_keys=True)

    print('%d corrections : %d du poste, %d du serveur, %d ensemble' % (
        len(fusion), len(set(local) - set(serveur)), len(set(serveur) - set(local)),
        len(set(local) & set(serveur))))
    if conflits:
        print('%d conflit(s), le poste gagne : %s' % (len(conflits), ', '.join(conflits[:20])))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
