from . import *

# Superhero Jailbreak (Civil War, 2B, Resistance 8/8, carte 202) — absent du moteur (audit du set Civil War, 22/10/2026), image hallofheroeslcg.com/civil-war/56202b.
# [star] Forced Response : After resolving step 1 of the villain phase, each player discards the top card of the encounter deck. Each player who discards a minion this way
#   puts it into play engaged with them.
# If this stage is completed, the players lose the game. (9 par joueur ; menace de depart 0 ; +1 par joueur.)
#
# Cartes de reference : gorr/gorr_the_god_butcher/gb005b (`AfterResolveVillainPhaseStep(ForcedResponse, 1, ...)`, meme etape 1), sm/shield_tech/27187a
# (`Worlds.DiscardEncounterTopCard(effect)`), punisher_mcdc_2026/capo_of_the_past/pu139 (`sbire.PutIntoPlay(joueur, effect)` = en jeu ENGAGE avec ce joueur).
# ⚠ Mots-pieges : « EACH player » (chacun defausse SA carte, l'une apres l'autre dans l'ordre des joueurs) ; « discards a MINION this way » (seulement si la carte defaussee
# est un sbire ; un traitrise, une annexe... restent defaussees) ; « engaged WITH THEM » = le joueur qui l'a defaussee ; « after resolving STEP 1 » (pas la phase entiere).


def GetAbilities() -> Sequence['Ability']:

    def evasion(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        def action(joueur: 'Player') -> None:
            face = Worlds.DiscardEncounterTopCard(effect)
            if face is not None and Minion.IsType(face):
                face.PutIntoPlay(joueur, effect)

        Players.ForEachPlayer(effect, action)

    return [
        AbilityFactory.AfterResolveVillainPhaseStep(AbilityType.ForcedResponse, 1, evasion),
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
