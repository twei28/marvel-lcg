from . import *

# Anything Goes — AMELIORATION, cout 1, [physical]. SKILL.
# Hero Action: Exhaust Anything Goes → swap a Casey Jones WEAPON upgrade you
#   control with a Casey Jones WEAPON upgrade tucked under Casey's Bag.
#
# CARTES DE REFERENCE
#  - `td012` Donatello's Shell / `60030` : `TuckCardUnderHere` (ranger sous une
#    carte), `GetPlacedCardArea()` (relire les cartes rangees), fiche tuck.md.
#  - `raphael/tr003` : premier choix par `SetTarget(...)`, second par
#    `ChooseAbilities(... ForChoiceAbility(...).SetTarget(liste, not_move=True))`.
#  - `ho010` : amelioration a Hero Action = `CanPlayThisUpgradeCard()` +
#    `WhenInYourPlayTurn(HeroAction, op).SetCostFunc(Exhaust("This"))`.
#
# TEXTE CONTRE CODE
#  ⚠ « SWAP » = un ECHANGE de places : l'arme en jeu part SOUS le Sac (rangee,
#    pas defaussee), l'arme rangee ENTRE en jeu. Les deux ou rien : pas
#    d'effet (et l'Action n'est pas offerte) sans arme de Casey en jeu OU sans
#    arme de Casey rangee. On range d'abord (libere la limite Restricted), puis
#    on met en jeu.
#  ⚠ « a Casey Jones WEAPON upgrade you CONTROL » : arme du SET Casey Jones en
#    jeu (voir Q1) ; « tucked UNDER CASEY'S BAG » : sous le Sac tc013 seulement,
#    pas sous une autre carte (Carapace de Donatello...).
#  ⚠ « Exhaust Anything Goes » est devant la fleche : un COUT.
#  ⚠ « Hero Action » : forme heros seulement.


def GetAbilities() -> Sequence['Ability']:

    def echange_possible(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        return bool(ArmesDeCaseySousControle(joueur)) and bool(ArmesDeCaseyRangeesSousLeSac(joueur))

    def echanger(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        sac = SacDuJoueur(joueur)
        en_jeu = [t for t in effect.targets if t is not None]
        rangees = ArmesDeCaseyRangeesSousLeSac(joueur)
        if joueur is None or sac is None or not en_jeu or not rangees:
            return
        sortante = en_jeu[0]
        entrante = {"face": None}

        def choisir(cibles: Sequence['CardFace']) -> None:
            entrante["face"] = cibles[0] if cibles else None

        if len(rangees) == 1:
            entrante["face"] = rangees[0]
        else:
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Swap with a WEAPON upgrade tucked under Casey's Bag",
                    choisir,
                ).SetTarget(rangees, range=(1, 1), not_move=True),
            )
        if entrante["face"] is None:
            return
        # On range d'abord : l'arme sortante libere sa place Restricted.
        if sac.TuckCardUnderHere(sortante, effect):
            entrante["face"].CastTo(Upgrade).PutIntoPlay(joueur, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            echanger,
            conditions=[echange_possible],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(
            CardFinder(card_type=Upgrade, trait=TRAIT_ARME, set_name=ENSEMBLE_CASEY),
            from_where=["YouControlCards"],
        ),
    ]
