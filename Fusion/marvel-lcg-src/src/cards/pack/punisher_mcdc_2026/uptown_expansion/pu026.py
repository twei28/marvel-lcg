from . import *

# West Side Warrior (U1) — PISTE Uptown. Response : While in Upper West Side, after you exactly defend an attack or exactly defeat an enemy or side scheme, add a
#   dojo counter here. Then, if there are 3 or more counters here, add this card to the victory display, reveal the top LEAD card, and draw 1 card.
#
# Cartes de reference : leads_the_big_apple/pu046 (`AfterUnitDefendAgainstAttack` + `CompteurPuisFin`), RECETTES-MOTEUR « EXACTLY defend » (`damage_before_defense ==
# defense_value`, up030), tmnt_aspect_aggression/ua019 (« exactly defeat » = `AfterUnitDefeatedUnit(..., has_excess_damage=False)`), pu041 (`AfterUnitDefeatedScheme`).
# ⚠ Mots-pieges :
#  - « exactly DEFEND an attack » : la valeur de l'attaque (boosts compris) est EGALE a la DEF du defenseur (parade pile) ; « you » = identite ou allie du joueur ;
#  - « exactly DEFEAT an enemy » : sans degats excedentaires (`has_excess_damage=False`), vilain ou sbire ; « exactly defeat a SIDE SCHEME » : menace enlevee
#    egale a la menace restante (AJOUT moteur : `AfterUnitDefeatedScheme.excess_thwart`) ; les TROIS declencheurs ajoutent chacun UN compteur ;
#  - « While in Upper West Side » : lu AU DECLENCHEMENT (`EnLieu`), les compteurs restent si on part ; seuil 3 ; « dojo counter » : jeton `dojo`.

def GetAbilities() -> Sequence['Ability']:

    def pile(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> bool:
        return message.damage_before_defense == message.defense_value

    def compter(effect: 'Effect', message: 'Message2') -> None:
        CompteurPuisFin(effect, Joueur(effect), 'dojo', 3)

    def ennemi_pile(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> bool:
        return message.excess_damage == 0

    def annexe_pile(effect: 'Effect', message: 'Message.AfterUnitDefeatedScheme') -> bool:
        return message.excess_thwart == 0

    return [
        AbilityFactory.AfterUnitDefendAgainstAttack(AbilityType.Response, "You", compter, conditions=[EnLieu(LIEU_U1), pile]),
        AbilityFactory.AfterUnitDefeatedUnit(AbilityType.Response, "You", Enemy, compter, has_excess_damage=False, conditions=[EnLieu(LIEU_U1)]),
        AbilityFactory.AfterUnitDefeatedScheme(AbilityType.Response, "You", SchemeSide2, compter, conditions=[EnLieu(LIEU_U1), annexe_pile]),
    ]
