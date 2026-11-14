from . import *


def GetAbilities() -> Sequence['Ability']:
    def punisher_no_more(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()
        YouMayFlipToYourAlterEgoForm(joueur, effect)
        identite = joueur.GetIdentity()
        # « Discard 2 WEB-SHOOTER upgrades FROM PLAY » : pas de « you control » (arbitrage du 26/10/2026) : toute amelioration
        # WEB-SHOOTER en jeu, chez n'importe quel joueur ; c'est le joueur de l'obligation qui choisit lesquelles.
        armes: List['CardFace'] = []
        for p in Worlds.GetPlayers(effect):
            armes += [f for f in AmeliorationsDe(p) if f.HasTrait(WEB_SHOOTER) and f not in armes]

        def defausser_deux(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            restantes = list(armes)
            choisies: List['CardFace'] = []
            for _ in range(2):
                face = joueur.AskChooseFace(restantes, effect, prompt="Discard a Web-Shooter upgrade")
                restantes.remove(face)
                choisies.append(face)
            Faces.DiscardAll(choisies, effect)
            Faces.RemoveAllFromGame([this], effect)

        def epuiser_peter(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            if Faces.ExhaustAll([identite], effect):
                Faces.DiscardAll([this], effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard 2 Web-Shooter upgrades from play. Remove Punisher No More from the game",
                defausser_deux,
                condition=len(armes) >= 2,
            ),
            AbilityFactory.ForChoiceAbility(
                "Exhaust Peter Parker → discard this obligation",
                epuiser_peter,
                condition=AlterEgo.IsType(identite) and identite.CanExhaust(),
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            punisher_no_more,
        ),
    ]
