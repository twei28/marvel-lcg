from . import *

# Gang War (1B) — MANIGANCE PRINCIPALE. Menace 9 par joueur, depart 1 par joueur, acceleration +1 par joueur.
# Forced Interrupt : When a villain would be defeated, instead reset their hit points and remove 5 threat from here.
# Forced Response : After a LEAD card is added to the victory display, if there are 2[per hero] LEAD cards there, advance to stage 2A
#   (the players win by advancing).
# If this scheme is completed, the players lose the game.
#
# Cartes de reference : fne/typhoid_mary/__init__.py (`WhenUnitWouldBeDefeated` + `SetBeInstead` + `ResetHealth`), gmw/collector_1/16073b.py
# (`AfterCardsMoved` sur une pile, `IfThisSchemeStageIsCompletedPlayersLoseTheGame`), `MainScheme.Advance`.
# ⚠ « a villain » : N'IMPORTE QUEL des CAPO en jeu (pas seulement « le mechant ») ; « their hit points » = ses PV de depart (maximum) ;
# « remove 5 threat » : 5 menaces fixes (pas par joueur), sans descendre sous 0 ; « 2[per hero] » : 2 x joueurs.

def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(MainScheme)
        message.SetBeInstead(effect)
        message.trigger.ResetHealth(effect)
        message.trigger.RemoveThreatFromSchemes([this], 5, effect)

    def une_piste_en_victoire(effect: 'Effect', message: 'Message.AfterCardsMoved') -> bool:
        pile = Worlds.VictoryDisplay(effect)
        return pile in message.into_areas and any(f.HasTrait("LEAD") for f in message.faces)

    def deux_par_joueur(effect: 'Effect', message: 'Message.AfterCardsMoved') -> bool:
        return len(PistesEnVictoire(effect)) >= Worlds.ConvertPerPlayerIconToInt("2*", effect)

    def avancer(effect: 'Effect', message: 'Message.AfterCardsMoved') -> None:
        effect.this.CastTo(MainScheme).Advance(None, effect)

    return [
        AbilityFactory.WhenUnitWouldBeDefeated(AbilityType.ForcedInterrupt, Villain, vaincu),
        AbilityFactory.AfterCardsMoved(AbilityType.ForcedResponse, None, avancer, conditions=[une_piste_en_victoire, deux_par_joueur]),
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
