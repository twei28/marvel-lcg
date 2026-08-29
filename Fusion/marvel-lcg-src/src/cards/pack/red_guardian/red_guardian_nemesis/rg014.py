from . import *

# Envied Idol — manigance secondaire nemesis de Red Guardian
# The Red Guardian player cannot change to alter-ego form.
# When Revealed: The Red Guardian player changes to hero form.
#
# Menace de depart 3 par joueur, 2 boost et l'icone acceleration sont dans les
# DONNEES (`StartingThreat: "3*"`, `Boost`, `Acceleration`).
#
# « The Red Guardian player » et non « you » : la carte designe un joueur
# precis, pas celui qui la revele. Un set nemesis est melange a la pioche de
# rencontre une fois l'obligation resolue, donc n'importe quel joueur peut
# reveler cette manigance en multijoueur. Gabarit : Back to the Future
# (next_evol/cable_nemesis/40033), qui vise « the Cable player » via
# `PlayerFinder(name="Cable")`. `Player.IsName` teste les DEUX faces de la
# carte identite (`player.py:262`, `check_all_face=True`), donc le nom du
# heros suffit meme quand le joueur est en Alexei Shostakov.
#
# L'interdiction elle-meme suit Targeted for Elimination
# (mut_gen/sentinels/32107) : `PlayersCannotChangeForms(..., to_form=AlterEgo)`
# ne bloque QUE le sens hero -> alter-ego, ce qui laisse passer le passage en
# forme heros du « When Revealed » ci-dessous.


def GetAbilities() -> Sequence['Ability']:

    def envied_idol(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)

        joueur = Worlds.FindPlayer(PlayerFinder(name="Red Guardian"), effect)
        if joueur is None:
            return

        joueur.GetIdentity().ChangeToForm(Hero, effect)

    return [
        AbilityFactory.PlayersCannotChangeForms(
            AbilityType.NonKeyword,
            PlayerFinder(name="Red Guardian"),
            to_form=AlterEgo,
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            envied_idol,
        ),
    ]
