from cards.pack import *

# ===========================================================================
# MUSE (Rainy, set 174, prefixe `mu`) — helpers partages du SET MODULAIRE.
#
# Ce n'est ni un heros ni un vilain : c'est un set modulaire, celui qu'on
# ajoute a n'importe quel scenario (modele `necroverse`, `intergalactic_hazards`).
# Six cartes distinctes, sept exemplaires (Obsession en double).
#
# ⚠ L'ARBITRAGE QUI TIENT TOUT LE SET, decision utilisateur du 13/09/2026.
#
# QUATRE cartes sur six parlent d'« une carte avec l'image de votre identite
# dessus » (mu001, mu003, mu004, mu006). Le moteur ne sait rien de ce que
# montre une illustration. On rend cela par les CARTES SIGNATURE, celles que
# le moteur marque `card_class="IdentitySpecific"`.
#
# Ce n'est pas un pis-aller : c'est le vocabulaire de l'AUTEUR LUI-MEME, qui
# ecrit noir sur blanc « an identity-specific card » sur `mu005` Grim
# Inspiration. Les deux autres lectures ont ete ecartees devant l'utilisateur :
# « les cartes qui portent ton nom » attraperait des allies homonymes d'un
# autre aspect, imprevisible ; « vraiment l'illustration » demanderait de
# relever a l'oeil des milliers d'images, liste fausse des le premier oubli.
#
# ⚠ Ce que cette lecture ne couvre pas, et c'est assume : une carte d'aspect
# qui REPRESENTE le heros (il y en a beaucoup) ne compte pas. Muse ne se
# reveille que sur le kit signature.
# ===========================================================================

NOM_MUSE = "Muse"


def EstUneCarteSignature(face: 'CardFace|None') -> bool:
    """« Une carte avec l'image de votre identite dessus » : une carte signature.

    ⚠ Le test porte sur la CLASSE de la carte, pas sur son proprietaire. Une
    carte signature l'est pour un heros donne, mais un joueur n'a que celles de
    SON heros dans son deck : en pratique les deux se confondent. Le jour ou
    une carte fera changer de deck une signature d'un autre heros, elle
    comptera quand meme — et c'est le comportement le plus simple a expliquer.
    """
    if face is None:
        return False
    classe = face.CastTo(ClassCard)
    if classe is None:
        return False
    return classe.IsClass("IdentitySpecific")


def CartesSignatureDe(faces: Sequence['CardFace']) -> List['CardFace']:
    return [f for f in faces if EstUneCarteSignature(f)]


def TrouverMuse(effect: 'Effect') -> 'CardFace|None':
    """Muse EN JEU, s'il y est. Rien d'autre : les cartes qui veulent le faire
    venir cherchent ensuite dans le deck de rencontre."""
    return Worlds.FindCardOnField(effect, name=NOM_MUSE, card_type=Minion)
