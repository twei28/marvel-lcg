from . import *

# Plasmacaster — ATTACHEMENT. WEAPON. Boost 2. Uses (3 plasma counters).
# Attach to Predator Warlord. Otherwise, this card gains surge.
# Uses (3 plasma counters).
# [star] Forced Interrupt: When Predator Warlord attacks you, remove 1 plasma counter from here and discard the top card of your deck →
#   take indirect damage equal to that card's printed cost.
#
# Cartes de reference :
#  - « Attach to X. Otherwise, surge » : `AttachToFaceWhenPutIntoPlay(CardFinder(name=), if_cannot_gain_surge=True)` (tk Accessoire) ;
#  - Uses : `desc.Uses "3,plasma"`, natif (fiche uses.md : la carte part seule au dernier compteur) ; compteur `plasma` ajoute a
#    `CardFace.COUNTER` et a `compteurs-fr.ts` ;
#  - « When X attacks you » : `WhenUnitAttackYou(ForcedInterrupt, ..)` ; « discard the top card of your deck » : `DiscardDeckTopCards(1)` ;
#    « printed cost » : `FacesCounter.GetPrintedCost` (27170) ; « indirect damage » : `DealIndirectDamage(identite, n)` (16026).
#
# ⚠ Mots-pieges :
#  - « attacks YOU » : pas une attaque contre un allie ni contre un ennemi ;
#  - le compteur retire est un COUT (fleche) : le 3e usage fait partir la carte (natif) apres avoir inflige ses degats ;
#  - « that card's PRINTED cost » : une carte sans cout (ressource, Alien Scout distribue au lieu d'etre defausse) = 0 degat.


def GetAbilities() -> Sequence['Ability']:

    def tir(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.property.against_player
        if not Player.IsType(joueur) or this.GetCounters('plasma') <= 0:
            return
        Faces.RemoveCountersOn([this], 1, 'plasma', effect)
        defaussees = [f for f in joueur.DiscardDeckTopCards(1, effect) if not f.IsInPlay()]
        cout = FacesCounter.GetPrintedCost(defaussees) if defaussees else 0
        if cout > 0:
            this.DealIndirectDamage(joueur.GetIdentity(), cout, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name=WARLORD, card_type=Villain), if_cannot_gain_surge=True),
        AbilityFactory.WhenUnitAttackYou(AbilityType.ForcedInterrupt, CardFinder(name=WARLORD, card_type=Villain), tir),
    ]
