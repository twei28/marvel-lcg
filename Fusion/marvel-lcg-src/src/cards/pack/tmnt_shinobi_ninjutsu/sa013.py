from . import *

# Up in Smoke — EVENEMENT 0 [energy], Ninjutsu (TMNT Shinobi, Inkwire). TACTIC.
# Hero Action: Ready a NINJA ally.
# Hero Interrupt: When an ally would be discarded from play, return it to its owner's hand instead.
# « Time to shake up the board. » —Ronin
#
# NOUVELLE. Mots-cles (fiches lues AVANT le code) : aucun (pas de Cloak sur le texte imprime).
#
# Cartes de reference :
#  - `vz015` Stronger Together / `Faces.ReadyAll` : « Ready ... ally » = `SetTarget(Ally, trait=..., canbe_ready=True)` ;
#  - `19032` Regroup : « return it to its owner's hand instead » = `Faces.ReturnToHand([carte], "Owner", effect)` ;
#  - `27087b` Maze of Mirrors : « would be discarded ... instead » = `WhenCardWouldDiscard` + `message.SetBeInstead(effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ DEUX capacites distinctes sur UN evenement : Action (ready) OU Interruption (sauvetage).
#  ⚠ « a NINJA ally » : un allie au trait NINJA, incline (rien a redresser sinon) ; pas l'identite.
#  ⚠ « WOULD be discarded FROM PLAY » : un allie EN JEU qui va etre defausse (vaincu ou defausse par un effet), pas une
#    carte defaussee de la main ou du deck ; « return it to its OWNER'S hand INSTEAD » : dans la main de son PROPRIETAIRE
#    (pas de son controleur), l'allie n'arrive PAS en defausse.
#  ⚠ Hero Action / Hero Interrupt : forme heros seulement.


def GetAbilities() -> Sequence['Ability']:

    def redresser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        Faces.ReadyAll(effect.targets, effect)

    def sauver(effect: 'Effect', message: 'Message.WhenCardWouldDiscard') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        message.SetBeInstead(effect)
        Faces.ReturnToHand([message.trigger], "Owner", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            redresser,
        ).SetPlay().SetLabel()
        .SetTarget(Ally, trait="NINJA", canbe_ready=True),
        AbilityFactory.WhenCardWouldDiscard(
            AbilityType.HeroInterrupt,
            Ally,
            sauver,
            conditions=[lambda effect, message: message.trigger.IsInPlay()],
        ).SetPlay().SetLabel(),
    ]
