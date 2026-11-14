from . import *

# * Terminal Spike : AMELIORATION (ITEM. TECH.), cout 2, [physical].
# Hero Action: Exhaust Terminal Spike → draw 1 card. Choose and discard 1 card from your hand. Deal damage to an enemy equal to the number of printed resources on the discarded card.
#
# CARTES DE REFERENCE
#  - `04011` Hawkeye : meme calcul (`FacesCounter.GetPrintedResourcesIcon`), mais la defausse y est un COUT ; ici elle suit la pioche, donc dans l'effet (`AskChooseFace` + `Faces.DiscardAll`).
#  - `web_bracelet` (27009) : `initiator.DrawUp(1, effect)` pour « draw 1 card ».
#
# TEXTE CONTRE CODE
#  « draw 1 card » PUIS « choose and discard 1 card from your hand » : la carte piochee peut etre celle qu'on defausse. « the number of PRINTED resources » -> les icones de
#  ressource imprimees sur la carte defaussee (une carte a deux icones donne 2), pas son cout. « an enemy » : la cible est choisie a l'activation.
#  Hero Action nue (pas d'attaque : aucun label), cout : s'incliner. Si la main est vide apres la pioche, rien n'est defausse et aucun degat n'est inflige.
#  Chiffres : cout 2, une carte piochee.


def GetAbilities() -> Sequence['Ability']:

    def terminal_spike(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        joueur = effect.GetInitiator()
        joueur.DrawUp(1, effect)
        main = list(joueur.hand_cards.Get())
        if not main:
            return
        carte = joueur.AskChooseFace(main, effect, forced=True, prompt="Terminal Spike : choose and discard 1 card")
        if carte is None:
            return
        degats = FacesCounter.GetPrintedResourcesIcon([carte], "Auto")
        Faces.DiscardAll([carte], effect)
        this.DealDamage(effect.targets, degats, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            terminal_spike,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Enemy),
    ]
