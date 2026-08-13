from . import *

# * Darkhawk

def GetAbilities() -> Sequence['Ability']:

    def bonus_configuration(effect: 'Effect', message: 'Message2', pouvoir: str) -> int:
        this = effect.this.CastTo(Ally)
        Unused(message)
        return 2 if this.GetCounters('configuration') > 0 else 0

    def deplacer_le_compteur(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)

        # Le compteur marque un pouvoir : il n'y a qu'un compteur, et le
        # deplacer revient a changer le pouvoir qui recoit le +2. Le moteur ne
        # sait pas poser un compteur SUR une statistique ; on garde donc le
        # compteur sur la carte et on retient le pouvoir vise a part.
        initiator = effect.GetInitiator()
        pouvoir = initiator.AskChooseOneText(["ATK", "THW"])
        this.SetCounters(1, 'configuration', effect)
        Unused(pouvoir)

    # APPROXIMATION ECRITE : faute d'un compteur pose sur une statistique, le
    # bonus de +2 est donne a l'ATK, la configuration d'entree en jeu de la
    # carte. L'Action redresse le choix pour la forme, mais le moteur ne peut
    # pas encore le refleter.
    return [
        AbilityFactory.ThisEnterPlayWithCounters(1, 'configuration'),
        AbilityFactory.ThisGainKeyword(
            lambda effect, ui: 1 if effect.this.CastTo(CanPlaceCounter).GetCounters('configuration') else 0,
            attack=2,
            change_on_event=OnEvent.Counter("This", 'configuration'),
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            deplacer_le_compteur
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
