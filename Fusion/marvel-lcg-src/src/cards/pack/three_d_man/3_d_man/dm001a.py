from . import *

# * 3-D Man (face heros)
#
# Action: Reduce the resource cost of the next card you play this phase by 1.
# Strength & Spirit of Three Men -- Interrupt: When you use a basic power, discard a card from your hand and
#   choose -> set that basic power's printed value to 3 until the end of the round.
#
# CARTES DE REFERENCE
#  - `us009` Solid Gear / `42010` Techno-Organic Wings (Archangel) : "reduce the resource cost of the next card you
#    play this phase by N" -> `Worlds.UpdateNextCardPlayCost(joueur, -N, effect, finder=CardFinder(), in_this="Phase")`.
#    Pas de restriction de classe ("the next card", pas "the next <aspect> card") -> `CardFinder()` sans filtre.
#  - `tv001a` Venus (face heros, texte "Action:" nu) : `AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, op)`,
#    sans `.SetPlay(hero_form_only=True)` (deja garanti par la face).
#  - `rs002` Conan (Red Sonja) : `AbilityFactory.WhenUnitUseBasicPower(AbilityType.Interrupt, "This", op)` +
#    `CostFunc.Discard("YourHandCards")` pour "discard a card from your hand". Difference : Conan donne +X POUR CET
#    USAGE SEULEMENT (`message.GainValue`) ; 3-D Man donne un bonus PERSISTANT jusqu'a la fin du round, modele
#    `bw008` Heavy Lifting : `heros.GainUntilRoundEnd(effect, attack=...)`.
#
# TEXTE CONTRE CODE
#  "set that basic power's printed value to 3" : le moteur n'a pas de "fixe a X" absolu sur un pouvoir de base
#    (seulement un gain additif, `GainUntilRoundEnd`). ARBITRAGE UTILISATEUR (04/11/2026) : calculer l'ECART entre 3
#    et la valeur IMPRIMEE actuelle du pouvoir concerne (`this.printed_attack` / `this.printed_thwart` /
#    `this.printed_defense`) et l'appliquer en gain, plutot qu'un +2 fige -- si un autre effet venait un jour
#    augmenter la valeur IMPRIMEE de 3-D Man (aucun cas aujourd'hui dans ce pack), le calcul resterait juste. Si
#    l'ecart est <= 0 (le pouvoir est deja a 3 ou plus), aucun gain n'est applique (deja au moins 3).
#  "and choose" : pas un second choix a coder -- le cout (defausser une carte) est deja OPTIONNEL (l'interruption ne
#    part que si le joueur paie) ; "choose" est juste la formulation imprimee de ce choix, pas une cible de plus.
#  "until the end of the round" -> `GainUntilRoundEnd`, jamais `GainValue` (qui ne vaudrait que pour cet usage).
#  "a basic power" (ATK/THW/DEF, pas REC/SCH : seul un allie/sbire a REC/SCH de base) -> `powers=["ATK","THW","DEF"]`.
#
# Chiffres : -1 sur le cout de la prochaine carte (Action, "Phase"). Valeur cible 3 pour le pouvoir de base
# (Interrupt) ; ecart calcule contre this.printed_attack/thwart/defense, tous les trois a 1 sur cette carte -> bonus
# +2 en pratique pour chacun des trois pouvoirs.

PUISSANCE_VERS_GAIN = {
    "ATK": "attack",
    "THW": "thwart",
    "DEF": "defense",
}


def GetAbilities() -> Sequence['Ability']:

    def reduire_cout_prochaine_carte(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = effect.GetInitiator()
        Worlds.UpdateNextCardPlayCost(
            joueur, -1, effect,
            finder=CardFinder(),
            in_this="Phase",
        )

    def strength_and_spirit_of_three_men(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Hero)
        pouvoir = message.power
        if pouvoir not in PUISSANCE_VERS_GAIN:
            return
        valeur_imprimee = {
            "ATK": this.printed_attack,
            "THW": this.printed_thwart,
            "DEF": this.printed_defense,
        }[pouvoir]
        bonus = 3 - valeur_imprimee
        if bonus <= 0:
            return
        this.GainUntilRoundEnd(effect, **{PUISSANCE_VERS_GAIN[pouvoir]: bonus})

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            reduire_cout_prochaine_carte,
        ),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.Interrupt,
            "This",
            strength_and_spirit_of_three_men,
            powers=["ATK", "THW", "DEF"],
        ).SetCostFunc(CostFunc.Discard("YourHandCards")).SetName("Strength & Spirit of Three Men"),
    ]
