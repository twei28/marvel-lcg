from . import *

# * Blooded Predator — SBIRE unique. YAUTJA. SCH 2, ATK 2, PV 4. Boost 3.
# When Revealed: Stun your identity. If you are already stunned, take 3 damage.
# When Defeated: Give Predator Warlord a tough status card. If you cannot, give this card to the active villain as a facedown boost card.
#
# Cartes de reference : `GiveStatus("Stunned"|"Tough")`, `IsStunned` / `IsTough` ; « give this card ... as a facedown boost card » : 60075.
#
# ⚠ Mots-pieges :
#  - « If you are ALREADY stunned » : 3 degats A LA PLACE (pas de seconde carte Sonne) ;
#  - « If you cannot » : Predator Warlord absent (vaincu) ou deja Tenace ;
#  - 4 PV : Expanding Hive l'a peut-etre deja donne comme boost : il y reste (arbitrage du 25/10/2026).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = JoueurDuMessage(message, effect)
        identite = joueur.GetIdentity()
        if identite.IsStunned():
            identite.TakeDamage(effect.this, 3, effect)
        else:
            Faces.GiveStatus([identite], "Stunned", effect)

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this
        Unused(message)
        warlord = MechantNomme(effect, WARLORD)
        if warlord is not None and not warlord.IsTough():
            Faces.GiveStatus([warlord], "Tough", effect)
        elif EncoreLibre(this):
            DonnerCommeBoost(this, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        # NoOutOfPlayLimit : Expanding Hive a peut-etre deja donne la carte en boost ; son « When Defeated » se resout quand meme.
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu).NoOutOfPlayLimit(),
    ]
