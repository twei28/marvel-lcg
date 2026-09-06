from . import *

# Fancy Fedora — AMELIORATION, cout 2, [mental]. ITEM.
# Hero Action: Exhaust this card and discard a card tucked under your hero ->
#   remove 2 threat from a scheme.
# Response: After you thwart and defeat a side scheme, tuck it under your
#   identity from the encounter discard pile (to a maximum of 3 cards).
#
# CARTES DE REFERENCE
#  - `52001a` * Silk : « After you defeat a side scheme, tuck it under here »,
#    avec le filtre `card.area.flags.is_encounter_discard_pile` et
#    `.SetTarget("Targets")`. LE modele.
#  - `AfterUnitDefeatedScheme(..., is_from_thwart=True)` (scheme.py:239) : le
#    parametre qui rend « THWART and defeat » plutot que « defeat » tout court.
#
# TEXTE CONTRE CODE
#  ⚠ « After you THWART AND DEFEAT a side scheme » -> `is_from_thwart=True`.
#    Sans lui, un complot annexe vaincu autrement (une carte qui le retire,
#    un effet de fin de partie) declencherait aussi. La difference avec
#    `52001a`, qui dit seulement « defeat », est imprimee.
#  « a SIDE scheme » -> `SchemeSide2`. Le complot principal ne se glisse pas.
#    ⚠ RECETTES §3 : la classe des complots annexes est `SchemeSide2`,
#    `SideScheme` N'EXISTE PAS dans `cards.pack`.
#  « from the encounter discard pile » -> le complot vaincu y est deja quand
#    la Reponse part ; le filtre le verifie plutot que de le supposer.
#  ⚠ « RESPONSE » et non « Hero Response » : elle vaut aussi en forme civile.
#    Contre-intuitif sur une carte de heros, mais c'est ce qui est imprime, et
#    c'est jouable — un allie peut contrer pendant qu'on est en civil.
#  ⚠ La Hero Action, elle, a DEUX couts devant la fleche : incliner ET
#    defausser une carte glissee. Piege `wd005`, ou une moitie avait ete
#    perdue.


def GetAbilities() -> Sequence['Ability']:

    def cout_defausser_une_carte_glissee(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(cibles)
        return DefausserUneCarteGlissee(effect)

    def deblayer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)

    def ramasser_le_complot(effect: 'Effect', message: 'Message.AfterUnitDefeatedScheme') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        GlisserSousIdentite(effect, list(effect.targets), JoueurDeCetteCarte(effect))

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            deblayer,
            conditions=[PileNonVide],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Custom(None, cout_defausser_une_carte_glissee))
        .SetTarget(Scheme2),
        AbilityFactory.AfterUnitDefeatedScheme(
            AbilityType.Response,
            "You",
            SchemeSide2,
            ramasser_le_complot,
            is_from_thwart=True,
            conditions=[
                lambda effect, message:
                    message.scheme.card.area.flags.is_encounter_discard_pile
            ],
        ).SetTarget("Targets"),
    ]
