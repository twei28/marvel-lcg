from . import *

# * Klyntar Bond : AMELIORATION (CONDITION. SYMBIOTE.), cout 3, [physical]. Classe Hero.
# Hero Interrupt: When Carnage uses a basic power, you may give him a boost card.
# Resource: Exhaust this card -> generate a [wild] resource for a Carnage event.
#
# CARTES DE REFERENCE
#  - « When X uses a basic power » : `32177` (Swagger) : `WhenUnitUseBasicPower(HeroInterrupt, 'YourHero', op)` ; carte de boost donnee a un HEROS : `Faces.GiveFacedownBoostCards([identite], 1, effect)` (`sf011`, `dd001a`).
#  - « Resource: Exhaust → generate a [wild] resource » : `im005` (Stark Tower) : `CanGenerateResources(AbilityType.Resource, Resources("G"))` + `CostFunc.Exhaust("This")` ; restriction « for a Carnage event » : parametre `for_card=CardFinder(..)` de la fabrique (resources.py:341).
#
# TEXTE CONTRE CODE
#  « Hero Interrupt: When CARNAGE uses a basic power » : `YourHero` (face heros seule), pouvoirs de base ATK / THW / DEF ; « you MAY give him a boost card » : Interruption facultative (le joueur la prend ou non) ; UNE carte de boost, face cachee, au heros.
#  « Resource » NU : se genere dans les deux formes. « generate a [WILD] resource » : DECISION UTILISATEUR du 03/11 : ressource WILD (comme ecrit dans `cards.json`), PAS une ressource maison ★. « FOR A CARNAGE EVENT » : ne paie qu'un EVENEMENT du set « Carnage » (ca010 a ca013), jamais une amelioration ni une carte d'un autre set.
#  Chiffres : cout 3, 1 carte de boost, 1 ressource wild.


def GetAbilities() -> Sequence['Ability']:

    def klyntar_bond(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        Faces.GiveFacedownBoostCards([joueur.GetIdentity()], 1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.HeroInterrupt,
            'YourHero',
            klyntar_bond,
        ),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
            CardFinder(set_name=NOM_CARNAGE, card_type=Event),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
