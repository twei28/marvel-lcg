from . import *
# Pym Particles — ressource, x2. Response : apres l'avoir depensee, redresse chaque Size Manipulation que tu
# controles et place EN TOUT 2 compteurs pym dessus. Si aucun n'a ete place, tu PEUX changer de forme.
def GetAbilities() -> Sequence['Ability']:
    def pym_particles(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(this)
        joueur = effect.GetInitiator()
        cartes = size_manipulations(joueur)
        Faces.ReadyAll(cartes, effect)
        places = 0
        for _ in range(2):
            if not cartes:
                break
            cible = cartes[0] if len(cartes) == 1 else joueur.AskChooseFace(cartes, effect)
            places += Faces.PlaceCountersOn([cible], 1, 'pym', effect) or 0
        if places == 0:
            joueur.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility("Change form", lambda cibles: changer_de_forme(effect)),
            )
    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.Response,
            pym_particles,
        ),
    ]
