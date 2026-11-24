from . import *

# Supremor — SBIRE (Supreme Intelligence), x2. ELITE. KREE. STARFORCE. SCH 1, ATK 1, 3★ PV, 2 icones de boost.
# Villainous.
# ★ Supremor gets +1 hit point for each KREE minion in the victory display.
#
# Cartes de reference :
#  - **`mts/hela/21137a`** : `ThisGainKeyword(lambda: <nombre en pile de victoire>, health=..., change_on_event=
#    OnEvent.Victory(...))` = un bonus de PV qui suit le contenu de la pile de victoire.
#  - **`aos/50127`** Diplomatic Immunity : `Worlds.VictoryDisplay(effect).FindCardSize(CardFinder2(<trait>,
#    Minion))` = « for each <trait> minion in the victory display ».
#  - Villainous : base AUTOMATIQUE (`desc.Villainous`, fiche villainous.md).
#
# ⚠ Mots-pieges : « +1 hit point for EACH KREE MINION » (sbires seulement : un complot annexe KREE ou un autre
# trait ne compte pas) ; « in the VICTORY DISPLAY » (pas la defausse) ; le compte suit la pile en continu, y
# compris quand Supremor Seed (gs207) en RETIRE un sbire ; « Supremor » (CETTE carte, pas l'autre copie).
# Le ★ du badge de PV renvoie a cette ligne (convention validee du 15/10/2026) : PV imprimes = 3.


def GetAbilities() -> Sequence['Ability']:

    def sbires_kree_en_victoire(effect: 'Effect', ui: Any) -> int:
        Unused(ui)
        return Worlds.VictoryDisplay(effect).FindCardSize(CardFinder(card_type=Minion, trait="KREE"))

    return [
        AbilityFactory.ThisGainKeyword(
            sbires_kree_en_victoire,
            health=1,
            change_on_event=OnEvent.Victory(Minion),
        ),
    ]
