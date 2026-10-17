from . import *

# Delirium — AMELIORATION 1 [mental], aspect Justice (TMNT Aspects, Inkwire). CONDITION. FERAL. WOUND.
# Attach to a minion that your hero attacked this turn. If attached to a non-[[ELITE]] minion, it gains
#   vulnerable.
# Interrupt: When attached minion leaves play, remove 2 threat from a scheme.
#
# MOT-CLE (fiche lue AVANT le code) : VULNERABLE — docs/reference/mots-cles/vulnerable.md. Mot-cle lu par
# le moteur (`HasVulnerable`, `desc.Vulnerable`) : un personnage vulnerable est defausse s'il est ou devient
# etourdi ou desoriente. Ici il est DONNE par l'amelioration : `GainVulnerable(diff)` via la porte `apply`
# de `GiveKeywordToAttached` (modele `wd098`, qui donne des icones par `apply`).
#
# CARTES DE REFERENCE
#  - `wx012` Puncture Wound : « Attach to an enemy that <X> attacked this turn » =
#    `CanPlayThisUpgradeCard(CardFinder(..., check_effect_fn=...))` qui relit
#    `world.stat.this_turn_made_attack` (attaquant, _, cibles) et exige que l'attaquant soit le TIEN.
#  - `wd098` (pack web_of_deceit) : mot-cle donne a l'attache par `GiveKeywordToAttached(apply=...)`.
#  - `37034` Psionic Shield : « When attached minion leaves play » =
#    `WhenCardWouldLeavePlay(<Interrupt>, "AttachedMinion", op)`.
#
# TEXTE CONTRE CODE (PROCESSUS-CARTE etape 5)
#  ⚠ « a MINION » (pas un vilain) ; « that YOUR HERO attacked » : ton identite EN FORME HEROS, pas un de
#    tes allies, pas le heros d'un autre joueur ; « THIS TURN » : l'historique du tour courant.
#  ⚠ « If attached to a NON-ELITE minion, IT gains vulnerable » : le SBIRE (pas la carte) ; un sbire ELITE
#    peut recevoir Delirium mais ne gagne rien. Lu en continu (un sbire qui devient ELITE perd le mot-cle).
#  ⚠ « Interrupt » (pas Forced) : optionnel ; « leaves play » : toute sortie (vaincu, defausse, retour...).
#  ⚠ « remove 2 threat from A scheme » : principale ou annexe, au choix.
#  Aucune limite imprimee.


def AttaqueParTonHeros(effect: 'Effect', face: 'CardFace') -> bool:
    joueur = effect.GetInitiator()
    if joueur is None:
        return False
    identite = joueur.GetIdentity()
    if not Hero.IsType(identite):
        return False
    for attaquant, _, cibles in effect.world.stat.this_turn_made_attack:
        if attaquant == identite and face in cibles:
            return True
    return False


def SbireNonElite(effect: 'Effect', face: 'CardFace', faces: List['CardFace']) -> int:
    Unused(effect, faces)
    return 0 if face.HasTrait("ELITE") else 1


def GetAbilities() -> Sequence['Ability']:

    def delirium(effect: 'Effect', message: 'Message.WhenCardWouldLeavePlay') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Minion, check_effect_fn=AttaqueParTonHeros),
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Minion,
            get_new_value=SbireNonElite,
            apply=lambda effect, face, diff: face.CastTo(HasVulnerable).GainVulnerable(diff, effect),
        ),
        AbilityFactory.WhenCardWouldLeavePlay(
            AbilityType.Interrupt,
            "AttachedMinion",
            delirium,
        ).SetTarget(Scheme2),
    ]
