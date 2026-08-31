from . import *

# Witchcraft — evenement. ATTACK. SPELL. Cout 2. x3
# Hero Action (attack): Deal 1 damage to an enemy. Discard the top 3 cards
#   of the encounter deck. For each boost icon discarded this way, deal 1
#   additional damage to that enemy. For each card discarded this way that
#   has boost icons equal to 0, stun or confuse an enemy.
#
# Cartes de reference (RECETTES §2) : 15004 Hex Bolt, jumeau structurel —
# `Worlds.DiscardEncounterCards(3, effect)` + `CountTotalBoostIcons`. Le
# « stun or confuse » est un choix par carte a 0 icone (`ChooseAbilities`).
#
# ⚠ Mots-pieges :
#  - « to THAT enemy » : le 1 de base ET les bonus d'icones vont au MEME
#    ennemi (la cible de l'evenement) ;
#  - « stun or confuse AN enemy » : la CIBLE du statut est libre, pas
#    forcement l'ennemi frappe ;
#  - les degats partent en DEUX temps fideles au texte : 1 d'abord, puis le
#    total des icones — une carte robuste absorbe donc au plus une fois
#    chaque paquet.

def GetAbilities() -> Sequence['Ability']:

    def witchcraft(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        cibles = [t for t in effect.targets if t is not None]
        this.DealDamage(cibles, 1, effect)

        defaussees = Worlds.DiscardEncounterCards(3, effect)
        icones = FacesCounter.CountTotalBoostIcons(defaussees)
        vivantes = [t for t in cibles if t.IsInPlay()]
        if icones > 0 and vivantes:
            this.DealDamage(vivantes, icones, effect)

        sans_icone = sum(
            1 for f in defaussees if FacesCounter.CountTotalBoostIcons([f]) == 0)

        def sonner(c: Sequence['CardFace']) -> None:
            Faces.GiveStatus(list(c), "Stunned", effect)

        def desorienter(c: Sequence['CardFace']) -> None:
            Faces.GiveStatus(list(c), "Confused", effect)

        for _ in range(sans_icone):
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Stun an enemy", sonner,
                ).SetTarget(Enemy, canbe_stunned=True),
                AbilityFactory.ForChoiceAbility(
                    "Confuse an enemy", desorienter,
                ).SetTarget(Enemy, canbe_confused=True),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            witchcraft
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
