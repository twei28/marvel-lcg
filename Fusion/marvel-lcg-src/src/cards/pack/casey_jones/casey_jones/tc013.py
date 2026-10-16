from . import *

# * Casey's Bag — AMELIORATION, [mental] (resource imprimee, PAS de cout). ITEM.
# UNIQUE. Permanent.
# You may play cards tucked here as if they were in your hand.
# Hero Action: Exhaust this card → tuck the bottommost WEAPON upgrade in your
#   discard pile under this card.
#
# MOTS-CLES : PERMANENT — fiche `docs/reference/mots-cles/permanent.md`
# (`desc.Permanent = "1"`, AUCUN SCRIPT) ; TUCK — fiche `mots-cles/tuck.md`.
#
# SANS COUT IMPRIME : la carte n'est jamais jouee depuis la main (aucune
# capacite `Play`, comme `04159a`). Elle entre en jeu par le Setup de `tc001b`
# et s'attache a l'identite (`Upgrade.GetAbilities`, cas `ma006`). Tiree en main
# elle ne sert que de ressource [mental].
#
# CARTES DE REFERENCE
#  - `td012` Donatello's Shell : `AttachedCardCanPlayLikeInHand()` (jouer les
#    cartes rangees) et `TuckCardUnderHere`. Ici SEULEMENT « play » (pas
#    `also_spend` / `also_discard`) et AUCUN plafond de cartes rangees.
#  - `hd013` Beverly Switzler : « the BOTTOMMOST ... card in your discard pile » =
#    `discard_pile.Get()` rend du fond vers le dessus, le premier element
#    filtre est le bon.
#  - `ho010` : `WhenInYourPlayTurn(HeroAction, op).SetCostFunc(Exhaust("This"))`.
#
# TEXTE CONTRE CODE
#  ⚠ « play cards tucked here » : TOUT type de carte, jouee en payant son cout
#    (pas de reduction) ; seul « play » est donne, pas « spend » / « discard ».
#  ⚠ « the BOTTOMMOST WEAPON upgrade » : la plus basse de la defausse PARMI les
#    armes (n'importe quelle arme, pas seulement celles de Casey). L'Action
#    n'est pas offerte sans arme dans la defausse, pour ne pas incliner le Sac
#    pour rien (« Exhaust » est un COUT).
#  ⚠ « tuck ... under THIS card » : sous le Sac, hors jeu, pas defaussee.
#  ⚠ « Hero Action » : forme heros seulement.


def GetAbilities() -> Sequence['Ability']:

    def une_arme_dans_la_defausse(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        return ArmeLaPlusBasseDeLaDefausse(JoueurDeCetteCarte(effect)) is not None

    def ranger_la_plus_basse(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        arme = ArmeLaPlusBasseDeLaDefausse(JoueurDeCetteCarte(effect))
        if arme is not None:
            this.TuckCardUnderHere(arme, effect)

    return [
        *AbilityFactory.AttachedCardCanPlayLikeInHand(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            ranger_la_plus_basse,
            conditions=[une_arme_dans_la_defausse],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
