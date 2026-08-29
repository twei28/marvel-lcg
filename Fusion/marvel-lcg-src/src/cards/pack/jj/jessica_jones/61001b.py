from . import *
def GetAbilities() -> Sequence['Ability']:
    def incognito_mode(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)
        player = effect.GetInitiator()
        player.GetIdentity().ChangeToForm(Hero, effect)
        # « You cannot change back to alter-ego form this phase. »
        this.effect.RegisterTemp(
            AbilityFactory.PlayersCannotChangeForms(
                AbilityType.NonKeyword, "You", to_form=AlterEgo),
            unregister_after_exec=False,
            until_phase_end=True,
        )
    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, incognito_mode).SetName("Incognito Mode"),
        # « Setup: Put the Alias Investigations support into play. »
        # Le moteur a une fabrique dediee (cf. Logan 35001b, Monica Rambeau
        # 21001b) : elle instancie la carte mise de cote et la met en jeu sous
        # le controle du joueur. L'ancienne version passait par une recherche
        # generique qui ne trouvait rien, et la capacite restait sans effet.
        AbilityFactory.SetupPutIntoPlay(["61002"]),
    ]
