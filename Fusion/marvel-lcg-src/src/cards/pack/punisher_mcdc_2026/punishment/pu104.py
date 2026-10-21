from . import *

# Flash-Bang — TRAITRISE. WEAPON. Boost ★.
# When Revealed : Stun each character you control. Stun the TARGETED villain and each minion engaged with you.
# ★ Boost : Stun a character you control.
#
# Cartes de reference : `Faces.GiveStatus(..., "Stunned", effect)` (pu064/pu115), `commun.AuChoixDuJoueur`.
# ⚠ « Stun each character you control » : y compris l'identite et les allies (un personnage Stalwart ne peut pas etre etourdi :
# le moteur l'ignore) ; le vilain cible peut etre etourdi (il n'est pas Steady/Stalwart) ; Boost : UN personnage au choix du joueur.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        cibles = list(joueur.GetControlCharacters()) + list(joueur.engaged_minions.Get())
        cible = VilainCible(effect)
        if cible is not None:
            cibles.append(cible)
        Faces.GiveStatus(cibles, "Stunned", effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        if joueur is not None:
            AuChoixDuJoueur(effect, joueur, lambda cibles: Faces.GiveStatus(cibles, "Stunned", effect), canbe_stunned=True)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
