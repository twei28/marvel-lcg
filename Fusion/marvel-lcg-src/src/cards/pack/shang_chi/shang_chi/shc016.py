from . import *

# Metal Bracers — AMELIORATION, cout 3, [physical]. ARMOR. (card_id shc016, 14/15)
# Shang-Chi gets +1 DEF. Enters play with 2 reflection counters on it.
# Hero Action: Exhaust Metal Bracers and remove 2 reflection counters from it → give Shang-Chi a tough status card.
# (Le fichier du zip s'appelle « Golden Bracers » : la carte imprimee est Metal Bracers.)
#
# Cartes de reference :
#  - `60038` : `*AbilityFactory.GiveKeywordToAttached(Hero, defense=1)` (+1 DEF au heros porteur).
#  - `dz002` : `ThisEnterPlayWithCounters` ; `shc015` (meme pack) : cout double incline + compteurs.
#  - `ra006` / `90123` : `Faces.GiveStatus([identite], "Tough", effect)`.
#
# ⚠ Mots-pieges :
#  - « Shang-Chi gets +1 DEF » : la face HEROS (l'alter-ego n'a pas de DEF) : `Hero`, pas l'identite quelle qu'elle soit.
#  - « remove 2 reflection counters » : DEUX ; condition de paiement posee a la main (RECETTES §5).
#  - « give SHANG-CHI a tough status card » : la carte de statut va au HEROS du joueur (pas a un allie) ; un heros deja
#    robuste n'en recoit pas une seconde (le moteur refuse un 2e statut identique).
#  - « Hero Action » : forme heros seulement.


def GetAbilities() -> Sequence['Ability']:

    def deux_compteurs(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        return effect.this.GetCounters('reflection') >= 2

    def bracers(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            Faces.GiveStatus([identite], "Tough", effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(Hero, defense=1),
        AbilityFactory.ThisEnterPlayWithCounters(2, 'reflection'),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            bracers,
            conditions=[deux_compteurs],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 2, 'reflection')),
    ]
