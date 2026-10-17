from . import *

# Yōjimbō — PATH hybride (avance), classes Bushido + Ninjutsu (Inkwire, TMNT Shinobi). BUSHIDO. NINJUTSU.
# Permanent. You get -1 hand size.
# Bodyguard — Hero Interrupt: When an enemy attacks, exhaust this card -> declare your hero as the defender
#   without exhausting them.
# « I stand with you. »
#
# Mots-cles (fiches lues AVANT le code) : Permanent (permanent.md) ; Shinobi / Path (shinobi.md).
#
# Cartes de reference :
#  - « When an enemy attacks, declare your hero as the defender without exhausting them » : `56047`
#    "I Can Do This All Day" (`WhenUnitWouldAttack(HeroInterrupt, Enemy, op).SetTarget("YourHero")` +
#    `message.DeclareDefender`) ; `48006` Bamf! (cout de carte + meme declaration).
#
# TEXTE CONTRE CODE
#  ⚠ « When AN enemy attacks » : n'importe quel ennemi (« an enemy attacks », pas « attacks YOU » : comme
#    56047, la cible est le heros du joueur) ; « declare YOUR HERO as the defender » : le heros, pas un allie.
#  ⚠ « WITHOUT EXHAUSTING THEM » : le heros defend sans s'incliner ; verifie par le cas (le heros reste pret).
#  ⚠ « exhaust THIS card -> » : le cout est l'inclinaison de la Voie ; une fois par redressement.
#  ⚠ « Hero Interrupt » : forme heros seulement.


def GetAbilities() -> Sequence['Ability']:

    def bodyguard(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Path)
        Unused(this)
        cibles = [t for t in effect.targets if t is not None]
        if not cibles:
            return
        assert isinstance(cibles[0], Unit2)
        message.DeclareDefender(cibles[0], effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis("You", hand_size=-1),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            Enemy,
            bodyguard,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget("YourHero"),
    ]
