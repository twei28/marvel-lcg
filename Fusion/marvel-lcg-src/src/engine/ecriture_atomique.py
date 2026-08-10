"""Ecrire un JSON sans jamais laisser un fichier a moitie ecrit.

Pourquoi ce module existe : `open(chemin, 'w')` TRONQUE le fichier avant que
le premier octet du nouveau contenu ne soit ecrit. Entre les deux, le fichier
existe et il est vide. Une coupure de courant, un processus tue, une lecture
concurrente, et ce qu'on relit n'est plus du JSON.

Ce n'est pas un risque theorique. Le 10/8/2026, l'extinction du poste en pleine
partie a laisse `campagnes/Essai_RoleBuild.json` a 0 octet. `list_campagnes`
avale l'erreur de lecture et saute le fichier : la campagne avait purement
disparu de l'ecran, sans un mot.

Le remede tient en trois gestes : ecrire a cote, forcer sur le disque, puis
renommer. `os.replace` est atomique sur le meme systeme de fichiers — a tout
instant, le chemin final designe soit l'ANCIEN contenu complet, soit le
NOUVEAU complet, jamais un entre-deux.

Module volontairement sans dependance : rien que la bibliotheque standard. Il
s'importe donc seul, par chemin, ce qui le rend eprouvable sans amorcer le
moteur (voir tools/test_ecriture_atomique.py). Il est pose a la racine de
`engine` et non a cote du serveur des campagnes parce que trois ecritures s'en
servent, dont une qui vit dans `game/` : les campagnes, le carnet sortant et
les hauts faits.
"""
import json
import os
import tempfile


def ecrire_json(chemin, donnees, indent=1):
    """Ecrit `donnees` en JSON a `chemin`, tout ou rien.

    Si la serialisation echoue, le fichier d'origine reste tel quel et aucun
    temporaire ne survit : mieux vaut l'ancienne campagne que pas de campagne.
    """
    dossier = os.path.dirname(os.path.abspath(chemin)) or '.'
    os.makedirs(dossier, exist_ok=True)
    # Le temporaire est cree DANS le dossier de destination : os.replace n'est
    # atomique qu'a l'interieur d'un meme systeme de fichiers, et /tmp peut ne
    # pas en etre un.
    descripteur, temporaire = tempfile.mkstemp(
        dir=dossier, prefix=os.path.basename(chemin) + '.', suffix='.tmp')
    try:
        with os.fdopen(descripteur, 'w', encoding='utf-8') as f:
            json.dump(donnees, f, ensure_ascii=False, indent=indent)
            f.flush()
            # Sans fsync, le renommage peut atteindre le disque avant le
            # contenu : au retour de courant, le fichier existe et il est vide.
            os.fsync(f.fileno())
        os.replace(temporaire, chemin)
    except BaseException:
        try:
            os.remove(temporaire)
        except OSError:
            pass
        raise
