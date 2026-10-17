from . import *

# Kensei — EVENEMENT SKILL, classe Bushido (Inkwire, TMNT Shinobi). Cout 1, [mental].
# Hero Action: Exhaust a WEAPON upgrade you control -> ready your hero.
# « A warrior is always ready. » —Raphael
#
# Mots-cles (fiches lues AVANT le code) : aucun mot-cle officiel ni maison (le trait WEAPON est un trait ordinaire).
#
# Cartes de reference :
#  - « Hero Action: <cout> -> ready your hero » sur un evenement : `sm/27016` What Doesn't Kill Me, `spdr/31023` Limitless Stamina
#    (`WhenInYourPlayTurn(HeroAction).SetPlay().SetLabel().SetTarget("YourHero", canbe_ready=True)` : le heros doit etre
#    INCLINE, sinon la carte n'est pas jouable, ce que dit le commentaire de 27016) ;
#  - cout « Exhaust a <filtre> you control » : `CostFunc.Exhaust(Select.From(fn))` (modele `sentinel/st011` pour un selecteur
#    maison ; le cout ajoute lui-meme le filtre `CanExhaust()` : une arme DEJA inclinee n'est pas payable) ;
#  - « <amelioration> you control » (identite ET allies) : `joueur.GetControlUpgrade(CardFinder(trait=...))`.
#
# TEXTE CONTRE CODE
#  ⚠ « Hero Action » : forme heros seule.
#  ⚠ « Exhaust A WEAPON upgrade YOU control -> » : COUT paye AVANT l'effet ; une amelioration de trait WEAPON sous son controle
#    (celle d'un allie comprise), PRETE (on ne peut pas incliner ce qui l'est deja).
#  ⚠ « ready YOUR HERO » : le heros, qui doit etre incline pour que la carte soit jouable (precedent 27016) : aucune
#    ressource gagnee a vide.


def GetAbilities() -> Sequence['Ability']:

    def armes_sous_controle(effect: 'Effect') -> 'Sequence[CardFace]':
        joueur = effect.GetInitiator()
        if joueur is None:
            return []
        return list(joueur.GetControlUpgrade(CardFinder(trait="WEAPON")))  # type: ignore

    def kensei(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            kensei,
        ).SetPlay().SetLabel()
        .SetTarget("YourHero", canbe_ready=True)
        .SetCostFunc(CostFunc.Exhaust(Select.From(armes_sous_controle))),
    ]
