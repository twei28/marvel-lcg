from . import *

# Swoop Down
# When Revealed (Alter-Ego): The villain and each minion engaged with you
#   schemes. Each AERIAL enemy gets +2 SCH for its activation.
# When Revealed (Hero): The villain and each minion engaged with you attacks
#   you. Each AERIAL enemy gets +2 ATK for its activation.
#
# Modeles : 32117 Master Mold's Children (vilain puis sbires engages), 04086
# Swinging Stone (additional_value dans la propriete). On deroule a la main
# plutot que par Worlds.Enemies.* pour porter le +2 propre a chaque ennemi.

def GetAbilities() -> Sequence['Ability']:

    def ennemis(effect: 'Effect', joueur: 'Player') -> List['Enemy']:
        liste: List['Enemy'] = []
        vilain = Worlds.FindVillain(effect)
        if vilain:
            liste.append(vilain)
        liste.extend(list(joueur.GetEngagedMinions()))
        return liste

    def bonus(ennemi: 'Enemy') -> int:
        return 2 if ennemi.HasTrait("AERIAL") else 0

    def alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        for ennemi in ennemis(effect, joueur):
            if ennemi.IsInPlay():
                ennemi.DoSchemes(joueur, effect, property=SchemeProperty(additional_value=bonus(ennemi)))

    def heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        for ennemi in ennemis(effect, joueur):
            if ennemi.IsInPlay():
                ennemi.DoAttackYou(joueur, effect, property=AttackProperty(additional_value=bonus(ennemi)))

    return [
        AbilityFactory.WhenThisRevealed("Alter-Ego", alter_ego),
        AbilityFactory.WhenThisRevealed("Hero", heros),
    ]
