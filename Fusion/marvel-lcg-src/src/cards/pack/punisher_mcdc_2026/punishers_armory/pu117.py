from . import *

# Punisher's SMG — ATTACHEMENT. ARMAMENT. WEAPON. ATQ +★ (badge « ★ ATK » : +0 avec renvoi au texte), Boost 2,
# Uses (1+1 par joueur ammo).
# Attach to Punisher. Otherwise, attach to the villain. Uses (1+1[per hero] ammo counters).
# When Revealed : Discard each other ARMAMENT card in play.
# ★ Forced Response : After attached character attacks, each player deals 1 damage to a character they control. Remove 1
#   ammo counter from here.
#
# Cartes de reference : pu115, `commun.AuChoixDuJoueur`, `DealDamage` (pu059).
# ⚠ « EACH player » : dans l'ordre des joueurs, chacun choisit un personnage A LUI (identite ou allie) et lui inflige 1
# degat (la carte est la source, pas une attaque) ; puis un compteur ammo est retire.

def GetAbilities() -> Sequence['Ability']:

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this
        for joueur in list(Worlds.GetPlayers(effect)):
            AuChoixDuJoueur(effect, joueur, lambda cibles: this.DealDamage(cibles, 1, effect))
        Faces.RemoveCountersOn([this], 1, 'ammo', effect)

    return [
        AttacherPunisherSinonVilain(),
        AbilityFactory.WhenThisRevealed(None, DefausserLesAutresArmements),
        AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, "AttachedCharacter", None, apres_attaque),
    ]
