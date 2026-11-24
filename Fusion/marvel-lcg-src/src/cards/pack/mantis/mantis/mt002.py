from . import *

# * Drax : ALLIE (GUARDIAN), cout 3, [physical]. THW 1*, ATQ 2*, PV 3. Unique. Hero Class.
# Drax cannot attack minions.
# [star] While Drax is confused, add his THW to his ATK and his basic attacks gain piercing and ignore the guard keyword.
# (Version du 04/03/2024 de l'auteur, relevee sur son Drive le 24/11/2026 : cout 4 -> 3, THW 2 -> 1, perforant et « ignore Garde » ne valent plus que TANT QUE Drax est desoriente.)
#
# CARTES DE REFERENCE
#  - `18019` Drax (officiel) : `UnitCannotAttackTarget("This", cannot_attack=Minion)`.
#  - `24016` Mandrill (`ThisGainKeywordForEachFaceInPlay` + `change_on_event=OnEvent.Status(.., 'Confused')`) et `bw016` Hulk Out (`GiveKeywordToInPlayWhenApplyThis(.., get_new_value=fn, attack=1)`) :
#    un bonus d'ATQ dont la valeur se relit a chaque changement d'etat.
#  - `bf017` Angel / `04012` Black Knight : `UnitAttackGainKeyword("This", piercing=True)` ; `32002` Shadowcat : `UnitIgnoreKeywordIcons("This", guard=True)` (ici limite au pouvoir de base d'ATQ).
#
# TEXTE CONTRE CODE
#  « cannot attack MINIONS » : les sbires seulement, le vilain reste attaquable. « While Drax IS confused » : UNE seule condition, le statut Desoriente, qui commande les TROIS effets : bonus egal a sa
#    MENEE COURANTE (« add HIS THW to HIS ATK », relu quand le statut est pose ou retire), « his BASIC attacks gain piercing » et « ignore the guard keyword » (son attaque de base, pas les attaques d'une
#    carte). Sans le statut : ni bonus, ni perforant, ni Garde ignoree (ce n'est qu'avec la version du 04/03/2024 que le perforant en depend).
#  Chiffres : cout 3, THW 1, ATQ 2, PV 3, consequence 1 etoile chacune.


def GetAbilities() -> Sequence['Ability']:

    def menee_courante_si_confus(effect: 'Effect', face: 'CardFace') -> int:
        drax = effect.this.CastTo(Ally)
        Unused(face)
        return drax.thwart if drax.IsConfused() else 0

    def attaque_de_base(effect: 'Effect', message: 'Message.CheckIfEffectIsIgnoreKeyWord') -> bool:
        capacite = message.effect.ability
        return capacite.flags.is_basic_power and capacite.IsFunction("ATK")

    def drax_est_confus(effect: 'Effect', message: 'Message2') -> bool:
        Unused(message)
        return bool(effect.this.CastTo(Ally).IsConfused())

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
            is_basic_attack=True,
            piercing=True,
            conditions=[drax_est_confus],
        ),
        AbilityFactory.UnitIgnoreKeywordIcons(
            "This",
            guard=True,
            conditions=[attaque_de_base, drax_est_confus],
        ),
    ]
