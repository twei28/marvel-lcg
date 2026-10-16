from . import *

# Manipulated — OBLIGATION (Boost 2, Acceleration 2), donnee au joueur Alopex.
# Give to the Alopex player.
# Action: Exhaust Alopex and deal 1 damage to each character you control ->
#   discard Manipulated.
#
# Cartes de reference :
#  - squelette obligation + sortie : `harry_osborn/ho013` /
#    `PlayerActionToDiscardThis(...).SetCostFunc(CostFunc.Exhaust("YourIdentity"))` ;
#  - `leonardo/tl013` (meme equipe) pour la structure et le cout a deux parties ;
#  - degats en COUT sur plusieurs personnages : `CostFunc.Custom(None, fn)`
#    (`27150`, `im007`) avec `joueur.GetControlCharacters()` (identite + allies
#    controles) ; `effect.this.DealDamage(...)` : la carte inflige (≠ « take »).
#
# ⚠ BASES AUTOMATIQUES (desc, aucun script) : `Boost 2` (deux icones « Y »),
# `Acceleration 2` (deux icones « + barre » : verifie par comparaison au glyphe
# `A` de ChampionsIcons.ttf, fiche acceleration.md), `GiveTo` = « Alopex » (le
# nom des DEUX faces d'identite).
#
# Mots-pieges :
#  - « Action » NUE : jouable en forme heros comme en alter-ego (pas un
#    `Alter-Ego Action`) ;
#  - « Exhaust ALOPEX AND deal 1 damage ... -> » : DEUX parties de cout ; si
#    l'identite est deja inclinee le cout est impayable, l'obligation reste ;
#  - « EACH CHARACTER YOU CONTROL » : l'identite ET chaque allie du joueur
#    (pas ceux des autres joueurs) ;
#  - « deal 1 damage » : la carte INFLIGE (cout paye meme si prevenu), le texte
#    imprime « charcter » (typo du scan) est corrige dans cards.json.


def GetAbilities() -> Sequence['Ability']:

    def un_degat_a_chacun(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(targets)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return False
        personnages = list(joueur.GetControlCharacters())
        if not personnages:
            return False
        effect.this.DealDamage(personnages, 1, effect)
        return True

    return [
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.Action,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity"))
        .SetCostFunc(CostFunc.Custom(None, un_degat_a_chacun)),
    ]
