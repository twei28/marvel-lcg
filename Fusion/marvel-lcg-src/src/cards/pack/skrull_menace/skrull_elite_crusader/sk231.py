from . import *

# * Crusader — SBIRE (Skrull Elite - Crusader). ELITE. SKRULL. MNG 2, ATQ 2, PV 4[per_hero],
# Victory 1, une etoile de boost (aucune icone chiffree).
# Victory 1.
# When Revealed: Deal 1 damage to each character you control. Give the villain 1 facedown boost
#   card for each character defeated this way.
# [star] Boost: Put Crusader into play engaged with you.
#
# Cartes de reference :
#  - « Deal 1 damage to each character you control » : **`sk139`** Imperial Kree Army
#    (`player.GetControlCharacters()` + `TakeDamage(this, n, effect)`).
#  - « defeated this way » : `TakeDamage` rend un `AfterUnitDefeatedUnit` quand la cible tombe
#    (can_health.py) ; on compte ces messages.
#  - « Give the villain N facedown boost card » : **`sk167`** White Tiger / `30037` Solus
#    (`Faces.GiveFacedownBoostCards`).
#  - Boost qui met la carte en jeu : **`hs007`** Regular Rats (`PutIntoPlay(message.GetToPlayer())`).
#
# ⚠ Mots-pieges : « EACH character YOU control » (identite + allies de CE joueur) ; « defeated THIS
# WAY » (seulement ceux que CE coup abat, pas un personnage deja vaincu) ; « FOR EACH » : une carte de
# boost par personnage vaincu, aucune s'il n'y en a pas ; Victory 1 est natif (desc) ; « engaged
# with YOU » (le joueur qui retourne la carte de boost) ; HP 4* = 4 par joueur.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        vaincus = 0
        for personnage in list(joueur.GetControlCharacters()):
            if not personnage.IsInPlay():
                continue
            resultat = personnage.CastTo(Unit2).TakeDamage(this, 1, effect)
            if isinstance(resultat, Message.AfterUnitDefeatedUnit):
                vaincus += 1
        DonnerBoostAuMechant(effect, vaincus)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        MettreEnJeuEngage(effect, effect.this, message.GetToPlayer())

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
