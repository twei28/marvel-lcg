from . import *

# Solar Flare — EVENEMENT, cout 3, RES [physical]. ATTACK. SUPERPOWER.
# Hero Action (attack): Confuse an enemy. Remove any number of solar counters from Sunspot -> deal 2 damage to that enemy
#   and each minion engaged with you for each solar counter removed.
#
# CARTES DE REFERENCE
#  - `05031` Concussive Blow : `Faces.GiveStatus(effect.targets, "Confused", effect)` puis les degats, cible `Enemy, canbe_confused=True`.
#  - `06006` Lightning Strike / `14032` Beat 'Em Up : « the villain and each minion engaged with you » (ici : la cible choisie
#    et chaque sbire engage avec le joueur).
#  - `sw007` Psionic Web Blast : X compteurs retires, X lu sur ce qui est VRAIMENT parti.
#
# TEXTE CONTRE CODE
#  ⚠ « Confuse an enemy » vient AVANT le retrait et ne coute rien : X = 0 desoriente quand meme.
#  ⚠ « 2 damage for EACH counter removed » = 2 * X, a la cible ET a chaque sbire engage avec VOUS (la cible n'est pas comptee deux fois).


def GetAbilities() -> Sequence['Ability']:

    def solar_flare(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()
        cibles = [c for c in effect.targets if c is not None]
        if joueur is None or not cibles:
            return
        Faces.GiveStatus(cibles, "Confused", effect)
        retire = RetirerSolaires(joueur, DemanderCombien(joueur, effect), effect)
        if retire <= 0:
            return
        engages = [m for m in joueur.GetEngagedMinions() if m not in cibles]
        this.DealDamage(cibles + engages, 2 * retire, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            solar_flare,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy, canbe_confused=True),
    ]
