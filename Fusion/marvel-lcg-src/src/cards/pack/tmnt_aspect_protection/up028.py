from . import *

# Rabid Infection — AMELIORATION 0 [physical], aspect Protection (TMNT Aspects, Inkwire). CONDITION. FERAL. WOUND.
# Attach to a minion that your hero attacked this turn. If attached to a non-[[ELITE]] minion, it gains
#   vulnerable.
# Interrupt: When attached minion activates, deal 1 damage to an enemy.
#
# NOUVELLE. MOT-CLE (fiche lue AVANT le code) : Vulnerable (vulnerable.md) : « defausse s'il EST ou DEVIENT
# etourdi ou desoriente ». Le moteur ne verifie qu'a la POSE d'un statut (`can_status.py`) : un sbire deja
# Sonne au moment ou il gagne vulnerable est donc defausse ici, a la main (« is or becomes »).
#
# CARTES DE REFERENCE
#  - `43012` Puncture Wound : « Attach to an enemy that X attacked this turn » =
#    `CanPlayThisUpgradeCard(CardFinder(card_type=..., check_effect_fn=...))` + `world.stat.this_turn_made_attack`.
#  - `sk093` : un mot-cle gagne sans parametre dedie = `apply=` + `Gain<MotCle>(diff, effect)` ;
#    ici `GiveKeywordToAttached(..., get_new_value=..., apply=...)` + `GainVulnerable`.
#  - `stunned.py` / `46007` : « When attached enemy activates » = `WhenEnemyWouldActivate(..., "AttachedEnemy", ...)`.
#
# TEXTE CONTRE CODE
#  ⚠ « a MINION that YOUR HERO attacked THIS TURN » : sbire seulement (pas le vilain), attaque du heros du
#    joueur (pas d'un allie), ce tour-ci (`this_turn_made_attack`).
#  ⚠ « If attached to a NON-ELITE minion » : sans le trait ELITE ; un sbire ELITE ne gagne rien.
#  ⚠ « When attached minion ACTIVATES » : attaque OU manigance ; Interrupt (optionnel) ; « deal 1 damage to
#    AN enemy » : n'importe quel ennemi (le sbire lui-meme, un autre sbire, le vilain).


def AttaqueParVotreHeros(effect: 'Effect', face: 'CardFace') -> bool:
    joueur = effect.GetInitiator() or effect.this.GetControlByOrOwner()
    if joueur is None:
        return False
    heros = joueur.GetIdentity()
    for unite, _, cibles in effect.world.stat.this_turn_made_attack:
        if unite is heros and Hero.IsType(unite) and face in cibles:
            return True
    return False


def GetAbilities() -> Sequence['Ability']:

    def non_elite(effect: 'Effect', minion: 'CardFace', ui: List['CardFace']) -> int:
        Unused(effect, ui)
        return 0 if minion.HasTrait("ELITE") else 1

    def vulnerable(effect: 'Effect', face: 'CardFace', diff: int) -> None:
        face.CastTo(HasVulnerable).GainVulnerable(diff, effect)
        if diff > 0 and face.CastTo(CanStatus).IsVulnerable() and \
                (face.CastTo(CanStatus).IsStunned() or face.CastTo(CanStatus).IsConfused()):
            Faces.DiscardAll([face], effect)

    def rabid_infection(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        this.DealDamage(effect.targets, 1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Minion, check_effect_fn=AttaqueParVotreHeros)
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Minion,
            get_new_value=non_elite,
            apply=vulnerable,
        ),
        AbilityFactory.WhenEnemyWouldActivate(
            AbilityType.Interrupt,
            "AttachedEnemy",
            rabid_infection,
        ).SetTarget(Enemy),
    ]
