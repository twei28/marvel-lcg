from . import *

# * Drax : ALLIE (GUARDIAN), cout 4, [physical]. THW 2*, ATQ 2*, PV 3. Unique. Hero Class.
# Drax cannot attack minions.
# While Drax is confused, add his THW to his ATK.
# [star] Drax's basic attack gains piercing and ignores the guard keyword.
#
# CARTES DE REFERENCE
#  - `18019` Drax (officiel) : `UnitCannotAttackTarget("This", cannot_attack=Minion)`.
#  - `24016` Mandrill (`ThisGainKeywordForEachFaceInPlay` + `change_on_event=OnEvent.Status(.., 'Confused')`) et `bw016` Hulk Out (`GiveKeywordToInPlayWhenApplyThis(.., get_new_value=fn, attack=1)`) :
#    un bonus d'ATQ dont la valeur se relit a chaque changement d'etat.
#  - `bf017` Angel / `04012` Black Knight : `UnitAttackGainKeyword("This", piercing=True)` ; `32002` Shadowcat : `UnitIgnoreKeywordIcons("This", guard=True)` (ici limite au pouvoir de base d'ATQ).
#
# TEXTE CONTRE CODE
#  « cannot attack MINIONS » : les sbires seulement, le vilain reste attaquable. « While Drax IS confused, add HIS THW to HIS ATK » : bonus egal a sa MENEE COURANTE, uniquement tant qu'il porte le statut
#    Desoriente (relu quand le statut est pose ou retire). « [star] Drax's BASIC attack » : son attaque de BASE, pas les attaques d'une carte ; perforante ET ignore Garde.
#  Chiffres : cout 4, THW 2, ATQ 2, PV 3, consequence 1 etoile chacune.


def GetAbilities() -> Sequence['Ability']:

    def menee_courante_si_confus(effect: 'Effect', face: 'CardFace') -> int:
        drax = effect.this.CastTo(Ally)
        Unused(face)
        return drax.thwart if drax.IsConfused() else 0

    def attaque_de_base(effect: 'Effect', message: 'Message.CheckIfEffectIsIgnoreKeyWord') -> bool:
        capacite = message.effect.ability
        return capacite.flags.is_basic_power and capacite.IsFunction("ATK")

    return [
        *AbilityFactory.UnitCannotAttackTarget(
            "This",
            cannot_attack=Minion,
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "This",
            attack=1,
            get_new_value=menee_courante_si_confus,
            change_on_event=OnEvent.Status("This", 'Confused'),
        ),
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
        ),
        AbilityFactory.UnitIgnoreKeywordIcons(
            "This",
            guard=True,
            conditions=[attaque_de_base],
        ),
    ]
