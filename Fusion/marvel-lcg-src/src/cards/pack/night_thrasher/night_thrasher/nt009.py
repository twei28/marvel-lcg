from . import *

# * Escrima Sticks — amelioration signature, x1 (n/16 = 14). WEAPON.
# Cout 3, ressource [energy].
# While the Battle Board upgrade has the [[VEHICLE]] trait, your attacks gain
#   piercing and overkill.
# Hero Action (attack): Deal 6 damage to an enemy. Shuffle this card into your
#   deck.
#
# Cartes de reference :
#  - **`27078`** / `ho016` / `40122a` pour `UnitAttackGainKeyword(<qui>,
#    piercing=True, overkill=True)`, avec `conditions=[...]` pour la
#    condition continue.
#  - **`50093`** Embassy Guard / Alert Level pour le motif « tant que TELLE
#    carte recto-verso est sur TELLE face », deja employe sur `as012`.
#  - `32177` Swagger / `Faces.ShuffleAllTo` pour « Shuffle this card into your
#    deck » (`bt006`).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **your** attacks » : les attaques du HEROS, pas celles des allies. Le
#    filtre nomme la face heros, comme les bonus continus du pack.
#  - « piercing **and** overkill » : les deux, et rien d'autre — pas de
#    portee.
#  - « While the Battle Board upgrade has the **[[VEHICLE]]** trait » : le
#    bonus tombe cote ARME. C'est contre-intuitif — l'arme, c'est la planche
#    elle-meme — mais c'est imprime, et ca fait sens : la planche sous les
#    pieds libere les mains pour les batons.
#  - « **Shuffle** this card into your deck » : dans le DECK, pas dans la
#    defausse, et la carte revient donc. C'est une amelioration a usage
#    unique qui se recycle, pas une carte perdue.
#  - « Deal 6 damage » : l'Action se paie par le retrait de la carte du
#    terrain, il n'y a AUCUN autre cout.
#  - « **(attack)** » : un seul `SetLabel`.


def GetAbilities() -> Sequence['Ability']:

    def planche_en_vehicule(effect: 'Effect', message: 'Message2') -> bool:
        Unused(message)
        return PlancheEstVehicule(effect)

    def escrima_sticks(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        this.DealDamage(effect.targets, 6, effect)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None:
            Faces.ShuffleAllTo([this], joueur.player_deck, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.UnitAttackGainKeyword(
            CardFinder(name="Night Thrasher"),
            piercing=True,
            overkill=True,
            conditions=[planche_en_vehicule],
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            escrima_sticks,
        ).SetLabel('attack')
        .SetTarget(Enemy),
    ]
