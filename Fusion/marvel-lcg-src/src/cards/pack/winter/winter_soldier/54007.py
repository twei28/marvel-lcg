from . import *

# * Safe House #30

def GetAbilities() -> Sequence['Ability']:

    def safe_house_30(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()
        face = Search.EncounterCard(
            effect,
            initiator,
            include_discard_pile=False,
            card_type=Minion,
        )
        if face:
            face.PutIntoPlay(initiator, effect)
            # « Then, draw 1 card » : RR « Then » : la suite ne se resout que si la partie avant « Then » s'est resolue entierement
            # (decision de l'utilisateur du 26/10/2026, carte montree).
            initiator.DrawUp(1, effect)
        else:
            # Pas de sbire a mettre en jeu : pas de pioche, MAIS le joueur doit le savoir (Safe House ne piochait pas, sans rien dire).
            initiator.NotifyNoResult(effect.this, "No minion in the encounter deck: no card is drawn.")


    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            safe_house_30
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]

