from cards.pack import *
from cards.pack.the_hunger_core.commun import *

# Helpers du set « The Hunger Core » (hg001-hg006 : le vilain 3 stades, la manigance principale 2 etapes,
# l'environnement Inside Galactus). Voir commun.py pour les helpers partages par tout le scenario.


################################################################################
# Le Coeur (hg001/hg002/hg003) : Shielded by the Horde + Just a Core X + Rupture X. Texte identique sur les
# trois stades hors PV/SCH et la valeur « Just a Core ».
def CapacitesDuCoeur(*, just_a_core: int, rupture_x: int = 1) -> List['Ability']:
    def bouclier(face: 'CardFace') -> bool:
        from game.effect.rule import GameRule
        return NbMetazombiesEnJeu(GameRule(face)) > 0

    def juste_un_coeur(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        joueur = message.against_player
        if Player.IsType(joueur) and joueur.IsHero():
            joueur.DealEncounterCards(just_a_core, effect)
            message.SetBeInstead(effect)
        # Contre un alter-ego : rien a faire, la regle de base du moteur manigance deja a la place d'attaquer.

    def rupture(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        coeur = effect.this.CastTo(Villain)
        if coeur.IsInPlay():
            coeur.DealDamage([coeur], rupture_x * NombreDeJoueurs(effect), effect)

    return [
        AbilityFactory.CannotBeAffectedByPlayerCards("This", while_fn=lambda face: bouclier(face)),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "This", juste_un_coeur),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.ForcedResponse, CardFinder(traits=["METAZOMBIE"], card_type=Villain), rupture),
    ]
