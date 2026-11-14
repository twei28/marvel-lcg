from . import *
# Shi'ar Battle Cruiser. Environnement SHI'AR VEHICLE, Alliance (cle `desc`), boost 1.
#
# Alliance.
# Forced Interrupt: When the villain phase ends, deal 1 indirect damage to each player.
# Hero Action: Exhaust your identity and spend [energy][energy] resources → discard this card.
#
# Cartes de reference : gb018 Forgotten Gods (`WhenVillainPhaseEnd` + `Players.ForEachPlayer` +
# `identite.TakeIndirectDamage(this, 1, effect)`), 60122 (Hero Action d'une carte de rencontre : `SetCost` + `Exhaust`).
# « Hero Action » : jouable en forme heros seulement. `Cost("YY")` = deux ressources energie (Y).
def GetAbilities() -> Sequence['Ability']:
    def bombarder(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        this = effect.this
        Unused(message)
        def frapper(joueur: 'Player') -> None:
            identite = joueur.GetIdentity()
            if identite is not None:
                identite.TakeIndirectDamage(this, 1, effect)
        Players.ForEachPlayer(effect, frapper)
    def repousser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Faces.DiscardAll([effect.this], effect)
    # CORRECTIF (26/10/2026) : « Alliance » est imprime sur un ENVIRONNEMENT, or `HasAlliance` est reserve aux evenements. RR
    # « Alliance » : « While paying costs for this card, any player may contribute to paying those costs » : la capacite de
    # jeu est donc marquee `cout_en_groupe` (meme marque que sk280 Princess Anelle), lue par `CheckAnyPlayerMayHelpPay`.
    # Seule l'inclinaison de l'identite reste au joueur actif.
    repousser_ability = (
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, repousser)
        .SetCostFunc(CostFunc.Exhaust("YourIdentity"))
        .SetCost(Cost("YY"))
    )
    repousser_ability.cout_en_groupe = True
    return [
        AbilityFactory.WhenVillainPhaseEnd(AbilityType.ForcedInterrupt, bombarder),
        repousser_ability,
    ]
