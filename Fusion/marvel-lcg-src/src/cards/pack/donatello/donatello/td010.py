from . import *

# * Truevision Goggles — AMELIORATION, cout 1, [physical]. ITEM. TECH.
# Hero Interrupt: When you make a basic thwart, exhaust Truevision Goggles ->
#   you get +1 THW for that thwart. You may discard a status card from an
#   enemy.
#
# CARTES DE REFERENCE
#  - `throg tg009` Frogjolnir / `20010` / `al012` : `WhenUnitUseBasicPower(
#    HeroInterrupt, ..., op)` + `message.GainValue(+1, effect)` (GainValue
#    route seul vers THW, RECETTES §1).
#  - `WhenUnitUseBasicPower(..., powers=["THW"])` (friend.py:344) pour ne
#    viser que le contre.
#  - `dazzler __init__.py:262` : retirer UNE carte de statut = methode de la
#    FACE `DiscardStunned/Confused/Tough(effect, rule=1)`.
#
# TEXTE CONTRE CODE
#  « When YOU make a basic THWART » -> "You", `powers=["THW"]`.
#  « you get +1 THW FOR THAT THWART » -> `GainValue(+1)` sur le message, pas
#    un bonus durable.
#  « You MAY discard a status card from AN enemy » -> SECONDE phrase,
#    FACULTATIVE (`forced=False`), sur n'importe quel ennemi qui porte un
#    statut ; elle n'est PAS une cible de l'interruption (sinon, sans ennemi a
#    statut, le +1 THW ne serait jamais offert : piege `ah007`).
#  « a status card » : sonne, desoriente OU tenace — le joueur choisit quand
#    l'ennemi en porte plusieurs.


def GetAbilities() -> Sequence['Ability']:

    def lunettes(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.GainValue(+1, effect)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        candidats = [e for e in Worlds.GetOnFieldEnemies(effect) if StatutsPresents(e)]
        if not candidats:
            return
        cible = joueur.AskChooseFace(
            candidats, effect,
            prompt="You may discard a status card from an enemy",
            forced=False)
        if cible is not None:
            RetirerUneCarteDeStatut(effect, joueur, cible)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.HeroInterrupt,
            "You",
            lunettes,
            powers=["THW"],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
