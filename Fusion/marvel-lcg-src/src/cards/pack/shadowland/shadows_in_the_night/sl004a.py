from . import *

# Position du heros, face a (The Streets Below). HERO POSITION.
# First Player Action : resoudre UN des effets ci-dessous, puis retourner cette carte :
#  • placer 3 menaces sur le complot principal et etourdir votre identite ;
#  • depenser [physical][physical] ;
#  • depenser 1 ressource de n'importe quel type et epuiser un personnage AERIAL que vous controlez.
# Cartes de reference : gmw/ship_command/16143 (First Player Action d'un environnement), fne/art_museum_heist/60127 (choix payant), mut_gen/sabretooth/32069 (3 menaces).
# ⚠ Le moteur reduit un choix PAYANT impayable au plus gros morceau payable (player_action.py:855) : on n'offre la branche que si elle est payable (PeutCouvrirLeCout, fne).
# ⚠ Mots-pieges : « one of the effects » = un seul, puis la carte se retourne ; chaque branche ne se retourne QUE si son effet a ete resolu ;
# « Spend [physical][physical] » = deux ressources physiques (Cost("RR")), « 1 resource of any type » = Cost("1").


def GetAbilities() -> Sequence['Ability']:

    def branches(effect: 'Effect', joueur: 'Player', retourner: Callable[[], None]) -> Sequence['Ability']:
        this = effect.this

        def menaces_et_etourdi(targets: Sequence['CardFace']) -> None:
            this.PlaceThreatOnSchemes("MainScheme", 3, effect)
            Faces.GiveStatus([joueur.GetIdentity()], "Stunned", effect)
            retourner()

        def deux_physiques(targets: Sequence['CardFace'], res: 'Resources') -> None:
            retourner()

        def une_ressource_et_aerial(targets: Sequence['CardFace'], res: 'Resources') -> None:
            Faces.ExhaustAll(targets, effect)
            retourner()

        return [
            AbilityFactory.ForChoiceAbility("Place 3 threat on the main scheme and stun your identity", menaces_et_etourdi),
            AbilityFactory.ForChoiceAbilityWithCost(Cost("RR"), "Spend [physical][physical] resources", deux_physiques,
                                                    conditions=[lambda e, m: PeutCouvrirLeCout(joueur, e, Cost("RR"))]),
            AbilityFactory.ForChoiceAbilityWithCost(Cost("1"), "Spend 1 resource of any type and exhaust an AERIAL character you control",
                                                    une_ressource_et_aerial,
                                                    conditions=[lambda e, m: PeutCouvrirLeCout(joueur, e, Cost("1"))]).SetTarget("YouControlUnit", trait="AERIAL", canbe_exhaust=True),
        ]

    return [ActionPositionHeros(branches)]
