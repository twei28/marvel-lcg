from . import *

# * Klyntar Bond : AMELIORATION (CONDITION. SYMBIOTE.), cout 3, [physical]. Classe Hero.
# Hero Interrupt: When Carnage uses a basic power, you may give him a boost card.
# Resource: Exhaust this card -> generate a [wild] resource for a Carnage event.
#
# CARTES DE REFERENCE
#  - « When X uses a basic power » : `32177` (Swagger) : `WhenUnitUseBasicPower(HeroInterrupt, 'YourHero', op)`.
#  - « give him a boost card » : CORRECTIF (04/11/2026, signale en partie reelle : « donne une carte boost mais
#    n'utilise pas la carte »). `Faces.GiveFacedownBoostCards` (ancien code) alimente la pile de boost facon
#    ENNEMI (`CanBoost`/`HasVillainous`) : la carte est POSEE mais JAMAIS RESOLUE pour un pouvoir de base d'un
#    HEROS (`ResolveBoostCards`, can_boost.py, ne tourne que sur `WhenUnitBeingAttack`/`WhenSchemeBeingScheme`,
#    une activation d'ENNEMI). Gap DEJA DOCUMENTE dans `dd001a.py` (Doctor Doom, qui l'ignore sciemment : son texte
#    dit « Ignore any boost effects on boost cards dealt to you »). Klyntar Bond veut l'effet reel : modele deja
#    etabli dans le depot pour ce cas, `bc002` (Black Cat) et `14002` (Scarlet Witch) : `Worlds.
#    DiscardEncounterTopCard` + `FacesCounter.CountTotalBoostIcons` + `message.GainValue(valeur, effect)`, la
#    primitive qui aiguille seule vers `GainATKForThisAttack` / `GainTHWForThisThwart` / `GainDEFForThisAttack`
#    selon le pouvoir en cours (`sender_unit.py:21`).
#  - « Resource: Exhaust → generate a [wild] resource » : `im005` (Stark Tower) : `CanGenerateResources(AbilityType.Resource, Resources("G"))` + `CostFunc.Exhaust("This")` ; restriction « for a Carnage event » : parametre `for_card=CardFinder(..)` de la fabrique (resources.py:341).
#
# TEXTE CONTRE CODE
#  « Hero Interrupt: When CARNAGE uses a basic power » : `YourHero` (face heros seule), pouvoirs de base ATK / THW / DEF ; « you MAY give him a boost card » : Interruption facultative (le joueur la prend ou non) ; UNE carte du DESSUS du deck de rencontre, defaussee, dont les icones de boost imprimees (chiffrees seules, pas l'etoile : aucune carte heros du depot ne resout un [star] Boost) s'ajoutent AU POUVOIR EN COURS pour cet usage.
#  « Resource » NU : se genere dans les deux formes. « generate a [WILD] resource » : DECISION UTILISATEUR du 03/11 : ressource WILD (comme ecrit dans `cards.json`), PAS une ressource maison ★. « FOR A CARNAGE EVENT » : ne paie qu'un EVENEMENT du set « Carnage » (ca010 a ca013), jamais une amelioration ni une carte d'un autre set.
#  Chiffres : cout 3, 1 carte de boost, 1 ressource wild.


def GetAbilities() -> Sequence['Ability']:

    def klyntar_bond(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        # CORRECTIF (04/11/2026) : voir l'encart de tete. `Faces.
        # GiveFacedownBoostCards` alimentait la pile de boost facon ENNEMI
        # (`CanBoost`), jamais resolue pour un pouvoir de base d'un HEROS.
        # Modele bc002 / 14002 : on defausse le dessus du deck de rencontre et
        # on applique ses icones directement au pouvoir en cours.
        face = Worlds.DiscardEncounterTopCard(effect)
        if face is None:
            return
        valeur = FacesCounter.CountTotalBoostIcons([face])
        if valeur > 0:
            message.GainValue(valeur, effect)

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
