from . import *

# * Pool-O-Vision (titre d'origine « Point of View ») — SOUTIEN de campagne ('Pool / Campaign, n° 279). Cout 0.
# METAGAME.
# Hero Response: After a SKRULL minion is defeated, exhaust Pool-O-Vision -> draw 1 card (to a maximum of 3)
#   for each [crisis], [acceleration], [amplify], and [hazard] in play.
# (Les quatre icones : Crisis, Acceleration, Amplify, Hazard : decision utilisateur du 14/10, corrigee le 15/10.)
#
# Cartes de reference :
#  - **`04047`** Skilled Investigator : « Hero Response: After X is defeated, exhaust -> draw 1 card » =
#    `AfterSchemeBeDefeated(HeroResponse, ...).SetCostFunc(CostFunc.Exhaust("This"))` ; ici le sbire :
#    `AfterUnitBeDefeated(HeroResponse, CardFinder(card_type=Minion, trait="SKRULL"), op)`.
#  - **`Worlds.GetIconsNum(effect, ["Crisis", "Acceleration", "Amplify", "Hazard"])`** (worlds.py:343) : le
#    total des icones EN JEU (chaque icone compte, pas chaque carte) ; fiches `mots-cles/crisis.md`,
#    `acceleration.md`, `amplify.md`, `hazard.md`.
#
# ⚠ Mots-pieges :
#  - « a SKRULL minion » (elite ou non) ; « HERO Response » : jouable en forme heros seulement ;
#  - « 1 card FOR EACH icon » : le compte est lu A LA RESOLUTION (apres le paiement), cartes de TOUS les joueurs ;
#    une carte a deux icones compte deux fois ; « to a MAXIMUM of 3 » : plafond de 3 cartes ; 0 icone : rien ;
#  - « exhaust Pool-O-Vision » est un COUT.


def GetAbilities() -> Sequence['Ability']:

    def pool_o_vision(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        n = Worlds.GetIconsNum(effect, ["Crisis", "Acceleration", "Amplify", "Hazard"])
        n = min(3, n)
        if n > 0:
            joueur.DrawUp(n, effect)

    return [
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.HeroResponse,
            CardFinder(card_type=Minion, trait="SKRULL"),
            pool_o_vision,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
