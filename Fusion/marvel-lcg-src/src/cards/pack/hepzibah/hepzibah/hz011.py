from . import *
# Vendetta (obligation d'Hepzibah, boost 2).
#
# Give to the Hepzibah player.
# You cannot flip to alter-ego while a minion is engaged with you.
# Forced Interrupt: When a minion enters play, engage it and flip to hero form.
# Action: Discard an ally you control -> remove this card from the game.
#
# Cartes de reference : hs092 (`PlayersCannotChangeForms(NonKeyword, "You", to_form=AlterEgo, conditions=[..])`), ma017
# (`PlayerActionToRemoveThisFromGame` + cout), tc001a (`CostFunc.Discard("YouControlCards", card_type=..)`), `Minion.EngagePlayer`.
def GetAbilities() -> Sequence['Ability']:
    def un_sbire_engage(effect: 'Effect', message: 'Message.WhenUnitWouldChangeForm') -> bool:
        # « engaged with YOU » : le joueur a qui l'obligation est donnee (l'initiateur d'une obligation est le mechant).
        joueur = JoueurDeLObligation(effect)
        return joueur is not None and message.trigger.GetControlByPlayer() == joueur and len(joueur.engaged_minions.Get(True)) > 0
    def vendetta(effect: 'Effect', message: 'Message.WhenCardEnterPlay') -> None:
        this = effect.this
        Unused(this)
        joueur = JoueurDeLObligation(effect)
        sbire = message.trigger
        if joueur is None:
            return
        if Minion.IsType(sbire):
            sbire.EngagePlayer(joueur, effect)
        identite = joueur.GetIdentity()
        if not Hero.IsType(identite):
            identite.ChangeToForm(Hero, effect)
    return [
        # ⚠ « AnyPlayer » + le joueur teste dans la condition : l'initiateur d'une obligation est le mechant, « You » ne designe donc
        # jamais le joueur qui la porte (le passage en alter ego n'etait pas bloque, vu au harnais le 26/10/2026).
        AbilityFactory.PlayersCannotChangeForms(
            AbilityType.NonKeyword,
            "AnyPlayer",
            to_form=AlterEgo,
            conditions=[un_sbire_engage],
        ),
        AbilityFactory.WhenCardEnterPlay(
            AbilityType.ForcedInterrupt,
            Minion,
            vendetta,
        ),
        AbilityFactory.PlayerActionToRemoveThisFromGame(
            AbilityType.Action,
        ).SetCostFunc(CostFunc.Discard("YouControlCards", card_type=Ally)),
    ]
