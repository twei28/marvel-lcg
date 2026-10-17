from . import *

# Gratitude — AMELIORATION OATH, classe Bushido (Inkwire, TMNT Shinobi). Cout 0, [physical].
# Uses (2 samurai counters).
# Action: Exhaust this card and remove 1 samurai counter from it -> heal 1 damage from your identity. You may discard 1 status
#   card from your identity.
#
# Mots-cles (fiches lues AVANT le code) : Uses (uses.md, NATIF) ; samurai counter / OATH (samurai-counter.md).
#
# Cartes de reference :
#  - « Action: Exhaust this card and remove 1 <compteur> counter from it -> » : `jennika/tj006` Fearless Resolve
#    (`CostFunc.Exhaust("This")` + `CostFunc.Counter("This", n, 'samurai')`), en Action (toutes formes) au lieu de Hero Action ;
#  - « heal 1 damage from your identity » : `wonder_man/58002` Ionic Physiology (`identity.HealHealth(1, effect)`) ;
#  - « discard 1 status card from your identity » : `fne/daredevil/60016` Sister Maggie (cartes d'etat de l'identite =
#    `identity.components.status.GetDeck().Get(True)`, choisies par `ChooseAbilities(...SetTarget(cartes))`), ici FACULTATIF :
#    `MayChooseOneAbility`.
#
# TEXTE CONTRE CODE
#  ⚠ « Action » (pas Hero Action) : proposee en forme heros ET en forme alter-ego ; `AbilityType.Action`.
#  ⚠ « Exhaust this card AND remove 1 samurai counter FROM IT » : DEUX couts obligatoires ; une fois inclinee la carte ne se
#    redresse qu'au redressement de fin de round ; le 2e compteur est le dernier (Uses defausse la carte).
#  ⚠ « heal 1 damage from your IDENTITY » : l'identite (heros ou alter-ego), pas un allie ; 1 seul degat.
#  ⚠ « You MAY discard 1 status card » : facultatif ; UNE carte d'etat, de n'importe quelle sorte (Sonne, Desoriente, Tenace,
#    Camoufle, Hebete, ...) ; la phrase est independante du soin (sans degat a soigner on peut quand meme defausser).


def GetAbilities() -> Sequence['Ability']:

    def gratitude(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        identite.HealHealth(1, effect)
        cartes_d_etat = list(identite.components.status.GetDeck().Get(True))
        if not cartes_d_etat:
            return

        def defausser(cibles: 'Sequence[CardFace]') -> None:
            Faces.DiscardAll(list(cibles), effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility("Discard a status card from your identity", defausser).SetTarget(cartes_d_etat, range=(1, 1), not_move=True),
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            gratitude,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'samurai')),
    ]
