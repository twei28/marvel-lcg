from . import *

# Close Ranks
# Response: After a DORA MILAJE ally you control is defeated, place 1
#   phalanx counter here (to a maximum of 3).
# Resource: Exhaust Close Ranks and remove any number of phalanx counters
#   here -> generate that many [physical] resources.
#
# Declencheur : modele officiel classique `AbilityFactory.AfterUnitBeDefeated`,
# cible `("YouControl", CardFinder(card_type=Ally, trait="DORA MILAJE"))`
# (tuple deja utilise par le moteur pour restreindre "an ally YOU control").
#
# "remove any number of phalanx counters here -> generate that many
# resources" : PAS une conversion a montant fixe choisi une fois
# (`resources_fn` ne peut annoncer qu'un montant FIXE par source de paiement,
# verifie en lisant `resources.py:389-415 DoGenerateResources` -- sans
# `res_fn` explicite le moteur retombe sur `message.expected_res`, mais avec
# un `resources_fn` fixe le montant annonce EST le montant genere, aucun
# "clip" automatique au besoin reel). Modele retenu, prouve par deux cartes
# maison deja en jeu qui convertissent des compteurs en ressources choisies
# librement : spiderham/spider_ham/30001a.py (Spider-Ham, compteurs "toon")
# et falcon/falcon/53006.py (Falcon's Flock, compteurs "bird") -- toutes deux
# `CostFunc.Counter("This", 1, <nom>)` avec une valeur FIXE de 1 compteur
# pour 1 ressource, repete jusqu'a `SetToAvailableTimesFn` (le nombre de
# compteurs disponibles). Le paiement presente alors N choix identiques
# d'1 ressource chacun : en choisir K parmi N revient exactement a
# « retirer K compteurs sur un total disponible, K de 0 a N au choix du
# joueur » -- la traduction fidele de "any number" dans ce moteur.
#
# Le "Exhaust Close Ranks" du cout est ajoute par un DEUXIEME appel a
# `.SetCostFunc(...)` (chaque appel EMPILE dans `self.cost_funcs`, voir
# `Ability.SetCostFunc` : `+` entre deux `CostFunc.Base` n'existe pas, seul le
# chainage des appels fonctionne) : verifie a l'etape 7 (test_capacites,
# preuve par substitution) que la carte reste utilisable pour retirer
# plusieurs compteurs en une seule negociation de paiement malgre
# l'inclinaison.


def GetAbilities() -> Sequence['Ability']:

    def close_ranks_defeat(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)

        Faces.PlaceCountersOn([this], 1, 'phalanx', effect, maximum=3)

    def close_ranks_available(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> int:
        this = effect.this.CastTo(Support)
        Unused(message)

        return this.GetCounters('phalanx')

    return [
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.Response,
            ("YouControl", CardFinder(card_type=Ally, trait="DORA MILAJE")),
            close_ranks_defeat,
        ),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("R"),
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'phalanx'))
        .SetToAvailableTimesFn(close_ranks_available),
    ]
