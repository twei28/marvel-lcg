from . import *

# Cricket Willow — AMELIORATION, cout 2, [energy]. WEAPON. Restricted.
# Your hero gets +1 ATK.
# Hero Response: After you attack an enemy, discard Cricket Willow → stun that
#   enemy.
#
# MOT-CLE : RESTRICTED — fiche `restricted.md` (`desc.Restricted = "1"`, AUCUN
# SCRIPT pour la limite).
#
# CARTES DE REFERENCE
#  - `04159a` Basic Thwart Upgrade : « Your hero gets +1 THW » =
#    `GiveKeywordToAttached(Hero, thwart=1)` ; ici `attack=1`.
#  - `iw001a` / `ho001a` : « After you attack an enemy » =
#    `AfterUnitAttackEnd(type, "You", op, against_who=Enemy)` ; le champ du
#    message est `attacked_targets` (RECETTES §1).
#  - `22014` : cout `CostFunc.Discard("This")` (« discard X → ... »).
#  - `raphael/tr004` : `Faces.GiveStatus(vivants, "Stunned", effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « YOUR HERO gets +1 ATK » : la FACE HEROS (`Hero`) : un bonus d'ATQ ne vaut
#    qu'en forme heros, mais le filtre est ecrit pour ne rien donner a l'alter-ego
#    (contre-cas dans tmnt_casey.py).
#  ⚠ « After you attack AN ENEMY » : vilain ou sbire. « THAT enemy » = les
#    cibles de CETTE attaque ; un ennemi vaincu par l'attaque n'est plus en jeu,
#    il n'y a rien a etourdir.
#  ⚠ « discard Cricket Willow → » : la defausse est un COUT (fleche), payee avant
#    d'etourdir. DECISION UTILISATEUR (16/10/2026, Q3) : la
#    Reponse n'est offerte QUE si un ennemi attaque peut encore etre etourdi
#    (condition `une_cible_a_etourdir`) ; sinon on defausserait le Willow pour un
#    effet impossible.
#  ⚠ « Hero Response » : forme heros seulement.


def GetAbilities() -> Sequence['Ability']:

    def etourdir(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        cibles = [t for t in message.attacked_targets if t is not None and t.IsInPlay() and t.CanbeStunned()]
        if cibles:
            Faces.GiveStatus(cibles, "Stunned", effect)

    def une_cible_a_etourdir(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
        Unused(effect)
        return any(t is not None and t.IsInPlay() and t.CanbeStunned() for t in message.attacked_targets)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(Hero, attack=1),
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.HeroResponse,
            "You",
            etourdir,
            against_who=Enemy,
            conditions=[une_cible_a_etourdir],
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
