from . import *

# Fearless Resolve — AMELIORATION signature, x2. OATH. Cout 1, [physical].
# Classe : Jennika ET Bushido (desc.Class = « Hero;Bushido »).
# Uses (2 samurai counters).
# Hero Action: Exhaust Fearless Resolve and remove 2 samurai counters from it ->
#   ready Jennika.
#
# Mot-cle : Uses (mots-cles/uses.md) : BASE NATIVE, `desc.Uses = "2,samurai"` ; le
# moteur pose les 2 compteurs a l'entree en jeu et defausse la carte au dernier
# retire. Le compteur `samurai` est declare dans `CardFace.COUNTER` (fichier
# moteur partage, additif).
#
# Cartes de reference :
#  - `venomized/vz032` Klyntar Tendrils : deux couts chaines, `CostFunc.Exhaust(
#    "This")` + `CostFunc.Counter("This", n, '<compteur>')` ;
#  - `mf008` Neutralizer : amelioration a Uses + incliner ;
#  - `Faces.ReadyAll([heros], effect)` : an001a, 31009.
#
# ⚠ Mots-pieges :
#  - « remove 2 samurai counters » : les DEUX d'un coup (cout), donc une seule
#    utilisation par exemplaire, puis la carte quitte le jeu ;
#  - « Exhaust Fearless Resolve AND remove 2 counters » : deux couts, tous deux
#    obligatoires ;
#  - « ready JENNIKA » : le heros (Hero Action : forme heros), pas l'identite
#    alter-ego ni un allie.


def GetAbilities() -> Sequence['Ability']:

    def fearless_resolve(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None or not joueur.IsHero():
            return
        Faces.ReadyAll([joueur.GetHero()], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            fearless_resolve,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 2, 'samurai')),
    ]
