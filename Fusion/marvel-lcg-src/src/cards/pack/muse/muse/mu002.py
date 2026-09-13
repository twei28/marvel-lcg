from . import *

# Supply Run — MANIGANCE ANNEXE. 3[per_hero] menaces, 2 icones de boost.
# <i>Muse is draining the blood of innocent bystanders for his next
# 'masterpiece'.</i>
# Forced Interrupt: When a unique ([star]) enemy activates, discard the top
#   card of the encounter deck. If the discarded card has a picture of that
#   enemy on it, give it to them as a facedown boost card.
#
# CARTES DE REFERENCE
#  - `15025` * Luminous : « after X activates against you, discard the top card
#    of the encounter deck », la meme lecture du dessus du deck rencontre.
#  - `02007` Hired Gun pour la famille, MAIS PAS SA PRIMITIVE :
#    `Faces.GiveFacedownBoostCards(n)` PIOCHE n NOUVELLES cartes du deck
#    rencontre. Ici le texte dit « give IT to them » — c'est LA CARTE QU'ON
#    VIENT DE DEFAUSSER qui devient la carte de boost, pas une autre. D'ou
#    `CanBoost.GiveBoostCard(face, effect)` (can_boost.py:34), qui prend une
#    carte PRECISE. Se tromper de primitive aurait defausse une carte ET
#    pioche une seconde : deux cartes perdues au lieu d'une.
#  - `04078` * Absorbing Man pour la fenetre d'activation d'un ennemi.
#
# ⚠ ARBITRAGE, decision utilisateur du 13/09/2026. « Si elle porte une image de
# cet ennemi » : le moteur ne lit pas les illustrations. On retient une carte
# rencontre DU MEME SET que l'ennemi (une carte Muse pour Muse, une carte Rhino
# pour Rhino). Le vilain se renforce de ses propres cartes, ce que raconte
# l'illustration, et le joueur peut le prevoir. Les deux autres lectures
# ecartees : « une carte qui porte son nom » ne se declencherait presque
# jamais ; « toujours, sans condition » rendait le set nettement plus dur.
#
# TEXTE CONTRE CODE
#  ⚠ « a UNIQUE ([star]) enemy » : le vilain, ou un sbire unique comme Muse
#    lui-meme. Pas un sbire ordinaire. C'est `is_unique` sur la face.
#  ⚠ « WHEN ... activates » : une INTERRUPTION, donc AVANT l'activation — la
#    carte de boost arrive a temps pour compter dans cette activation-la.
#  ⚠ « give it TO THEM » : a l'ennemi qui s'active, pas au vilain par defaut.
#  ⚠ La carte du dessus est defaussee DANS TOUS LES CAS ; seule sa
#    transformation en carte de boost depend du set.


def GetAbilities() -> Sequence['Ability']:

    def supply_run(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)

        ennemi = message.trigger
        if ennemi is None:
            return

        defaussee = Worlds.DiscardEncounterTopCard(effect)
        if defaussee is None:
            return

        # « une image de cet ennemi » -> une carte du MEME SET que lui.
        set_ennemi = getattr(ennemi.paper, "set_name", None)
        if not set_ennemi:
            return
        if getattr(defaussee.paper, "set_name", None) != set_ennemi:
            return

        ennemi.CastTo(CanBoost).GiveBoostCard(defaussee, effect)

    return [
        AbilityFactory.WhenEnemyWouldActivate(
            AbilityType.ForcedInterrupt,
            CardFinder(is_unique=True),
            supply_run,
        ),
    ]
