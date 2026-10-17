from . import *

# Toss — EVENEMENT 1 [mental], Taijutsu (TMNT Shinobi, Inkwire). DEFENSE. THWART.
# Hero Interrupt (defense/thwart): When you would take any amount of damage from an attack, prevent 3 of that damage
#   and remove 1 threat from a scheme. If you paid for this card with an ATTACK event, daze that enemy.
#
# Mots-cles (fiches lues AVANT le code) : Dazed / « daze » (dazed.md) ; Shinobi (shinobi.md).
#
# Cartes de reference :
#  - `donatello/td003` Bo Tobu : « prevent 3 of that damage and remove N threat from a scheme » en Interruption
#    (`WhenUnitWouldTakeDamage(HeroInterrupt, "You", op, is_from_attack=True)` + `SetLabel('defense', 'thwart')`),
#    cible `Scheme2` comme l'officielle `gam/18004` Crosscounter (le moteur y ajoute `has_threat=True`, ability.py : sans menace
#    sur aucune manigance la carte n'est pas offerte, comme Crosscounter ; convention moteur, voir le gabarit) ;
#  - `donatello/td004` Chudan-Ura-Uke : « that / the attacking enemy » = `message.attacker` ;
#  - `jennika/tj004` : « if you paid for this card with an ATTACK event » = `PayeAvecUnEvenement`.
#
# TEXTE CONTRE CODE
#  ⚠ « any amount of damage FROM AN ATTACK » -> `is_from_attack=True` ; « prevent 3 OF THAT damage » : au plus 3.
#  ⚠ « THAT enemy » : l'attaquant lu sur le message (« from an attack » n'a pas d'autre ennemi nomme plus haut),
#    encore en jeu ; un attaquant qui n'est pas un ennemi (aucun cas) ne recoit rien.
#  ⚠ « daze that enemy » est sous la condition de paiement par un evenement ATTACK ; un evenement DEFENSE/THWART ne compte pas.
#  ⚠ « Remove 1 threat from A scheme » : une manigance au choix.


def GetAbilities() -> Sequence['Ability']:

    def toss(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)

        message.PreventDamage(3, effect)
        this.RemoveThreatFromSchemes(effect.targets, 1, effect)

        if PayeAvecUnEvenement(effect, "ATTACK"):
            attaquant = getattr(message, "attacker", None)
            if attaquant is not None and Enemy.IsType(attaquant) and attaquant.IsInPlay():
                ShinobiDaze(effect, [attaquant])

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            toss,
            is_from_attack=True,
        ).SetPlay().SetLabel('defense', 'thwart')
        .SetTarget(Scheme2),
    ]
