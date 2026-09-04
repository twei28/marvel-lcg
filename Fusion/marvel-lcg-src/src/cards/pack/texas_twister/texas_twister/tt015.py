from . import *

# * Living Lightning (Miguel Santos) — ALLIE AGRESSIVITE, cout 3, PV 3,
#   CTR 1* / ATQ 1*. AERIAL. RANGER. [energy].
# [star] Interrupt: When Living Lightning attacks, deal 1 damage to each
#   character in play.
#
# CARTE DE REFERENCE
#  - `40049` Probability Field : `WhenUnitUseBasicPower` en Interruption,
#    filtre `powers=`.
#
# TEXTE CONTRE CODE
#  « EACH CHARACTER IN PLAY » -> TOUT LE MONDE, amis compris : les autres
#    allies, l'identite du joueur, et Living Lightning lui-meme. C'est une
#    carte a double tranchant, et en faire un « chaque ennemi » la
#    transformerait en carte de nettoyage sans risque. Mot-piege du set.
#  « When ... ATTACKS » -> une INTERRUPTION avant l'attaque : les degats
#    partent AVANT que l'attaque ne resolve, donc un sbire a 1 PV peut mourir
#    avant d'etre frappe, et l'attaque se retrouve sans cible.
#  ⚠ `Unit2` et non `Ally|Identity` : le type generique « personnage » du
#    moteur couvre les allies, les identites, les sbires et le vilain.


def GetAbilities() -> Sequence['Ability']:

    def foudre_vivante(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        personnages = list(Worlds.FindCardsOnField(effect, card_type=Unit2))
        if personnages:
            this.DealDamage(personnages, 1, effect)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.Interrupt,
            "This",
            foudre_vivante,
            powers=["ATK"],
        ),
    ]
