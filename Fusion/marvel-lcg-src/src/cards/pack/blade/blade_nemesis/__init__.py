from cards.pack import *

# ===========================================================================
# Set nemesis « Blade Nemesis » : Dracula et sa horde. HUIT cartes, pas cinq :
# Blood Hunt, Dracula, Vampire x2, Bandolier of Stakes (attachement),
# Embraced x2, Turned. Le Setup d'Eric Brooks (bl001b) melange tout SAUF
# Dracula dans le deck rencontre des la mise en place.
#
# ⚠ L'OBLIGATION `bl011` The Thirst N'EST PAS ICI : son bandeau imprime dit
# « BLADE », son module vit dans `blade/blade/` (treizieme fois : ar010, sf010,
# bc012, sn011...).
#
# ⚠ DEUX CARTES SONT DES COPIES DU SET HORROR DE MOJO : `39051` Vampire et
# `39048` Bandolier of Stakes. Leurs modules sont les MODELES EXACTS de bl014
# et bl015 ; Dracula (bl013) est un Vampire a 12 PV, 3/3, Elite.
#
# « Attacks with piercing deal double damage to X » = 
# `AbilityFactory.UpdateAttacksDealDamage(with_piercing=True, deal_damage_to=X,
# update_damage_rule="Double")` : le doublement se fait au
# `WhenRecalculateAttackDamage`, APRES les bonus (arbitrage du 07/09/2026 :
# bonus puis doublement).
# ===========================================================================

TRAIT_VAMPIRE: 'CardFace.TRAITS' = "VAMPIRE"
COMPTEUR_PIEU: 'CardFace.COUNTER' = 'stake'


def EstJoueur(objet: Any) -> bool:
    return objet is not None and hasattr(objet, "IsPlayer") and Player.IsType(objet)


def Hote(face: 'CardFace|None') -> 'CardFace|None':
    return getattr(face, "bind_face", None) if face is not None else None


def DoubleDegatsPercants(cible: Any) -> 'Ability':
    """« Attacks with piercing deal double damage to <cible> »."""
    return AbilityFactory.UpdateAttacksDealDamage(
        with_piercing=True,
        deal_damage_to=cible,
        update_damage_rule="Double",
    )


def BoireLeSang(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
    """Forced Response commune a Vampire et Dracula : soigner tous ses degats,
    sinon (rien a soigner) une carte Tenace. Copie de `39051`."""
    this = effect.this.CastTo(Minion)
    Unused(message)
    soin = this.HealHealth(this.sustained, effect)
    if soin and soin.value:
        return
    Faces.GiveStatus([this], "Tough", effect)


def CapacitesDeVampire() -> List['Ability']:
    return [
        DoubleDegatsPercants("This"),
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse,
            "This",
            None,
            BoireLeSang,
        ),
    ]
