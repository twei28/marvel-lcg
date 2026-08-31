from . import *

# Chaotic Forces — obligation. Boost 1. GiveTo: Agatha Harkness.
# Give to the Agatha Harkness player.
# You may flip to alter-ego form. Choose:
#  • Search the victory display for Agatha All Along and put it into play ->
#    remove Chaotic Forces from the game.
#  • Discard this card and the top card of the encounter deck. For each
#    boost icon discarded this way, take 1 indirect damage.
#
# Cartes de reference (RECETTES) :
#  - squelette : an010 Banished from Asgard (`WhenThisObligationGiveToYou` +
#    `YouMayFlipToYourAlterEgoForm` + `ChooseAbilities` a deux puces) ;
#  - le tableau des victoires : `from_where=["VictoryDisplay"]` n'est utile
#    qu'aux selecteurs — ici on cherche aa008 directement dans
#    `Worlds.VictoryDisplay` (player.py:201 l'interroge pareil) et on la
#    remet en jeu par `face.PutIntoPlay(player, effect)` (aa001b) ;
#  - l'indirect : kb019 Golden Shot, `identity.TakeIndirectDamage(this, n,
#    effect)` ; les icones : `CountTotalBoostIcons` (15004).
#
# ⚠ La premiere puce n'est proposable que si aa008 EST au tableau des
# victoires (condition du choix, comme an010 conditionne sa puce a la forme).

def GetAbilities() -> Sequence['Ability']:

    def chaotic_forces(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()
        if player is None:
            return

        YouMayFlipToYourAlterEgoForm(player, effect)

        def au_tableau(rule: 'Effect') -> 'CardFace|None':
            return Worlds.VictoryDisplay(rule).FindCard(card_ids=["aa008"])

        def ramener(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            face = au_tableau(effect)
            if face is not None:
                face.PutIntoPlay(player, effect)
            Faces.RemoveAllFromGame([this], effect)

        def subir(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            defaussees = Worlds.DiscardEncounterCards(1, effect)
            icones = FacesCounter.CountTotalBoostIcons(defaussees)
            identite = player.GetIdentity()
            if icones > 0 and identite is not None:
                identite.TakeIndirectDamage(this, icones, effect)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Search the victory display for Agatha All Along and put it "
                "into play → remove Chaotic Forces from the game",
                ramener,
                condition=au_tableau(effect) is not None,
            ),
            AbilityFactory.ForChoiceAbility(
                "Discard this card and the top card of the encounter deck. "
                "For each boost icon discarded this way, take 1 indirect damage",
                subir,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            chaotic_forces
        ),
    ]
