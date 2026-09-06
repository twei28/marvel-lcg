from . import *

# Web Shot — EVENEMENT, cout 0, [energy]. SUPERPOWER. x2.
# Hero Interrupt: When a boost card is turned faceup during an enemy
#   activation, discard it instead and tuck it under Spider-Man Noir
#   (to a maximum of 3).
#
# ---------------------------------------------------------------------------
# ⚠⚠ CARTE A BOUCLE INFINIE SI ON LA CODE DE TRAVERS. A LIRE AVANT DE TOUCHER.
#
# `CanBoost.ResolveBoostCards` (can_boost.py:51-62) tourne ainsi :
#
#     while <paquet de boost non vide>:
#         face = <carte du dessus>
#         would = WhenBoostCardWouldTurnedFaceUp(face, ...)
#         would.Send()
#         if would.is_be_instead:
#             continue          # <-- ON REPART SUR LA MEME CARTE
#         Faces.MoveAllTo([face], area_boosting, ...)
#         ...
#
# Le `continue` ne retire PAS la carte du paquet. Poser `SetBeInstead` sans
# faire QUITTER la carte, c'est donc une boucle infinie : le moteur relit
# eternellement la meme carte du dessus, la partie se fige, et aucun outil ne
# le voit — `test_capacites` rendrait juste un cas en timeout.
#
# CONSEQUENCE, et c'est ce que dit le texte imprime : la carte part TOUJOURS.
# « discard it instead » est inconditionnel ; « and tuck it » est ce qui lui
# arrive ENSUITE, et seulement s'il reste de la place. Les deux branches du
# code sortent donc la carte du paquet de boost.
# ---------------------------------------------------------------------------
#
# CARTES DE REFERENCE
#  - `sd020` Inspirational Art (pack speed) : l'endroit du depot ou le
#    pipeline complet des cartes de boost est deroule etape par etape, avec
#    la raison pour laquelle il ne faut PAS s'accrocher au message « would »
#    quand on veut modifier des icones. Ici c'est l'inverse : on veut
#    justement empecher le retournement, donc c'est bien « would » qu'il faut.
#  - `aa010` / `ag012` / `av002` / `tg016` : `message.SetBeInstead(effect)`.
#  - `10003` Hulk Smash : l'evenement joue en « Hero Interrupt » -> `.SetPlay()`.
#
# TEXTE CONTRE CODE
#  « during an ENEMY activation » -> vilain OU sbire. On ne passe donc PAS
#    `boost_for_card=Villain` (ce que fait `sd020`, qui dit « villain »).
#  « discard it INSTEAD » -> le mot « instead » du moteur, `SetBeInstead` : la
#    carte n'est pas retournee, ses icones ne comptent pas, sa capacite Boost
#    ne se resout pas. C'est tout l'interet de la carte.
#  « tuck it under SPIDER-MAN NOIR » -> la pile de l'identite. ⚠ Le nom n'est
#    PAS utilise pour la retrouver : deux ALLIES du depot s'appellent ainsi.
#  « (to a maximum of 3) » -> si la pile est pleine, la carte est simplement
#    defaussee. Le texte ne prevoit pas de repli, et le moteur EXIGE qu'elle
#    parte (voir l'encadre).


def GetAbilities() -> Sequence['Ability']:

    def tir_de_toile(effect: 'Effect', message: 'Message.WhenBoostCardWouldTurnedFaceUp') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        carte = message.trigger
        message.SetBeInstead(effect)

        # ⚠ LA CARTE DOIT QUITTER LE PAQUET DE BOOST DANS TOUS LES CAS, sans
        # quoi `ResolveBoostCards` boucle a l'infini (voir l'encadre en tete).
        glissees = GlisserSousIdentite(effect, [carte], JoueurDeCetteCarte(effect))
        if not glissees:
            Faces.DiscardAll([carte], effect)

    return [
        AbilityFactory.WhenBoostCardWouldTurnedFaceUp(
            AbilityType.HeroInterrupt,
            tir_de_toile,
        ).SetPlay(),
    ]
