from . import *

# * Emperor Madrox : SBIRE UNIQUE (set nemesis, 2/5). DUPLICATE. SCH 1 / ATQ 3★ / PV 4, boost 2, icone Hazard 1 (comparee a Breakin' & Takin' 01107).
# ★ When Emperor Madrox attacks you, his attack targets an ally you control.
# Dupe allies may not attack Emperor Madrox.
# (Multiple Man's nemesis minion.)
#
# CARTES DE REFERENCE : `41028` (Psionic Illusion) / `ca022` / `gmw16019` (`WhenUnitWouldAttackUnit(.., "This", Unit2, op)` + `message.ChangeTarget(unit, effect)`), `hg029` (`UnitCannotBeAttacked(cible,
#  conditions=[attaquant_est_un_allie])` sur `CheckIfUnitCanBeAttackBy`, `message.attacker`).
# TEXTE CONTRE CODE : « ★ » : le etoile du champ ATQ (RRG « Star Icon »), `NonKeywordStar` (convention `mots-cles/special.md`), obligatoire. « attacks YOU » : une attaque dirigee contre l'identite du joueur ;
#  « targets an ALLY YOU CONTROL » : le joueur choisit lequel ; sans allie, l'attaque garde sa cible (rien a rediriger). « Dupe allies MAY NOT attack » : un allie nomme Dupe ne peut pas le choisir.
#  Chiffres : SCH 1, ATQ 3, PV 4, boost 2.


def GetAbilities() -> Sequence['Ability']:

    def vise_un_allie(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        cible = message.target
        if not (Hero.IsType(cible) or AlterEgo.IsType(cible)):
            return
        joueur = cible.GetControlByOrOwner()
        if not EstJoueur(joueur):
            return
        allies = [f for f in joueur.allies.Get() if f.IsInPlay()]
        if not allies:
            return
        choisi = joueur.AskChooseFace(allies, effect, forced=True) if len(allies) > 1 else allies[0]
        if choisi is not None:
            message.ChangeTarget(choisi, effect)

    def attaquant_est_un_dupe(effect: 'Effect', message: 'Message.CheckIfUnitCanBeAttackBy') -> bool:
        Unused(effect)
        return EstDupe(message.attacker)

    return [
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.NonKeywordStar,
            "This",
            Unit2,
            vise_un_allie,
        ),
        AbilityFactory.UnitCannotBeAttacked(
            "This",
            conditions=[attaquant_est_un_dupe],
        ),
    ]
