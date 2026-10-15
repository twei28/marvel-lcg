from . import *

# * Baxter Building — SOUTIEN BASIC, cout 4 [mental]. FANTASTIC FOUR. LOCATION.
# Reduce the cost to play this card by 1 if you control a FANTASTIC FOUR character.
# Resource: Exhaust Baxter Building → generate a [wild] resource for any player.
#
# Cartes de reference :
#  - **`27041`** / **`nt005`** : `ReduceCostToPlayThis(1, conditions=[...])` pour une
#    reduction conditionnelle de CE soutien.
#  - **`22033`** / **`mf005`** : `CanPlayThisSupportCard(under_any_players_control=True)`
#    pour un soutien qui sert a tous ; **`16142`** : `.AnyPlayerCanDoThis()`, la
#    capacite peut etre declenchee par n'importe quel joueur.
#  - **`sk013`** Excelsior : `CanGenerateResources(Resource, Resources("G"))
#    .SetCostFunc(CostFunc.Exhaust("This"))`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « IF YOU control a FANTASTIC FOUR CHARACTER » : un PERSONNAGE (identite ou allie)
#    sous VOTRE controle, pas un soutien ni une amelioration FF (Baxter Building lui-meme
#    est FF mais n'est pas un personnage).
#  - « Reduce by 1 » : cout 4 -> 3 ; seulement si la condition tient.
#  - « for ANY player » : `AnyPlayerCanDoThis()` ; la ressource est [wild] (Resources("G")).
#  - Resource (pas Hero Resource) : les deux formes.


def GetAbilities() -> Sequence['Ability']:

    def controle_un_personnage_ff(effect: 'Effect', message: 'Message2') -> bool:
        Unused(message)
        joueur = effect.GetInitiator()
        return any(c.HasTrait("FANTASTIC FOUR") for c in joueur.GetControlCharacters())

    return [
        AbilityFactory.CanPlayThisSupportCard(under_any_players_control=True),
        AbilityFactory.ReduceCostToPlayThis(1, conditions=[controle_un_personnage_ff]),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .AnyPlayerCanDoThis(),
    ]
