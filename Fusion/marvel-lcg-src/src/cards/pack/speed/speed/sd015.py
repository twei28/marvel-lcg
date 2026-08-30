from . import *

# Never Ending Spark — AMELIORATION signature, custom « CptScorp »
# Cout 3, [energy], classe Hero, trait SUPERPOWER.
# Hero Response: After an explosive counter is placed on an enemy or scheme,
#   ready this card.
# Resource: Exhaust Never Ending Spark -> generate a [energy] resource.
#
# DEUX capacites imprimees, deux blocs distincts. Chacune a son cas de test.
#
# ---------------------------------------------------------------------------
# BLOC 1, la Response -> `AbilityFactory.AfterCounterPlacedOn(AbilityType
# .HeroResponse, None, COMPTEUR_EXPLOSIF, ...)` (factory/counter.py:97).
#
# `which_card=None` : « on AN ENEMY OR SCHEME », n'importe laquelle — et
# `Condition.CheckWhichCard(None, ...)` rend toujours vrai
# (condition/card_type.py:98). On ne filtre donc que sur le NOM du compteur.
# Le declencheur est le message d'une AUTRE carte (l'ennemi ou la manigance
# marquee), mais aucune cible n'est a designer : l'effet porte sur « THIS
# CARD ». Pas de `.SetTarget('Trigger')` a poser, l'effet ne cible rien.
#
# `Faces.ReadyAll([this], effect)` tolere une carte DEJA REDRESSEE : `Ready`
# ne fait alors rien, sans erreur. C'est le cas nominal quand un compteur est
# pose alors que la Spark n'a pas encore servi.
#
# ⚠ LA BOUCLE EST VOULUE ET FINIE : Spark -> energie -> evenement paye en
# energie -> Hyperkinetic Fuel pose un compteur -> Spark redressee. Elle ne
# s'emballe pas, parce que chaque tour de boucle exige de PAYER un evenement
# a son cout plein : la Spark ne fournit qu'UNE ressource par redressement, et
# le plafond de 1 compteur par carte limite les cibles utiles. Le compteur peut
# aussi etre pose EN PLEIN PAIEMENT (Hyperkinetic Fuel est un Interrupt sur
# `WhenPlayerWouldPlayCard`, donc apres `ProcessSelfCost`) : la Spark est alors
# redressee juste apres avoir ete depensee, ce qui est exactement l'intention
# de l'auteur.
#
# ---------------------------------------------------------------------------
# BLOC 2, la ressource -> `AbilityFactory.CanGenerateResources(AbilityType
# .Resource, Resources("Y")).SetCostFunc(CostFunc.Exhaust("This"))`. Modele
# exact : `48005` Prehensile Tail et `54002` Cybernetic Arm, meme forme au mot
# pres (celles-la restreignent la carte financee, pas Never Ending Spark : le
# texte imprime ne dit rien de tel, donc pas de `for_card=`).
#
# ⚠ UNE SEULE `CanGenerateResources` par carte : `ClassCard.GetAbilities`
# (card_player.py:83-84) leve un assert au-dela. Ne jamais ajouter de seconde
# capacite ressource ici.
#
# `AbilityType.Resource` (et non `HeroResource`) : le texte imprime dit
# « Resource: », sans restriction de forme.


def GetAbilities() -> Sequence['Ability']:

    def never_ending_spark(effect: 'Effect', message: 'Message.AfterCardPlacedCounter') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        Faces.ReadyAll([this], effect)

    return [
        AbilityFactory.AfterCounterPlacedOn(
            AbilityType.HeroResponse,
            None,
            COMPTEUR_EXPLOSIF,
            never_ending_spark,
        ),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("Y"),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
