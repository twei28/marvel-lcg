from . import *

# Dweller Demon — SBIRE MYSTIC. PV 5, ATK 0, SCH 3, Boost 2, Surge 1, Teamwork (MYSTIC) (natifs).
# When Revealed : Place X threat on a scheme, where X is equal to the number of other MYSTIC minions in play.
# [star] Forced Response : After Dweller Demon attacks you, if there are no other minions engaged with you, deal yourself 1 facedown encounter card.
#
# Cartes de reference : `PlaceThreatOnSchemes`, `AfterUnitAttackYou` (do_attack.py), `Player.DealEncounterCards`.
# ⚠ Mots-pieges : « OTHER MYSTIC minions IN PLAY » (pas elle-meme, pas la defausse) ; « a scheme » : le joueur choisit (principale ou annexe) ; Forced Response : « if NO OTHER
# minions engaged with YOU » (engages avec le joueur attaque), la carte est distribuee FACE CACHEE a ce joueur.


def GetAbilities() -> Sequence['Ability']:
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetToPlayer()
        x = len(SbiresMystiquesEnJeu(effect, sauf=this))
        if x > 0:
            cibles = [s for s in Worlds.GetOnFieldSchemes(effect)]
            cible = joueur.AskChooseFace(cibles, effect) if len(cibles) > 1 else (cibles[0] if cibles else None)
            if cible is not None:
                this.PlaceThreatOnSchemes([cible], x, effect)

    def seul_engage(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
        joueur = message.GetAgainstPlayer()
        return joueur is not None and all(m.card is effect.this.card for m in joueur.engaged_minions.GetAll())

    def attaque(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        message.GetAgainstPlayer().DealEncounterCards(1, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.AfterUnitAttackYou(AbilityType.ForcedResponse, "This", attaque, conditions=[seul_engage]),
    ]
