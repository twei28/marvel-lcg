from . import *
# * Mental Training — AMELIORATION, cout 2, [energy]. PSIONIC. SKILL.
# Hero Interrupt: When you pay for an ATTACK or THWART event using only
#   [mental] resources, that event deals 1 additional damage or removes 1
#   additional threat.
#
# Modele exact pour la moitie ATTAQUE : 28017 Honed Technique
# (`WhenPlayerPlayCard` + `RegisterTemp(WhenFaceWouldDealDamage(...,
# by_which_effect=message.played_effect), until_event_end=message)`).
# Moitie CONTRE : meme montage sur `WhenSchemeWouldRemoveThreat`, dont la
# valeur est relue APRES l'envoi (scheme.py:142) : `message.value += 1`.
# « using ONLY » : `message.paid_resources.OnlyHasColor("B")` en condition,
# la ou 28017 se contente de `using_res="B"` (« using a »).

def GetAbilities() -> Sequence['Ability']:

    def paye_en_mental_seulement(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> bool:
        return message.paid_resources.OnlyHasColor("B")

    def mental_training(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> None:
        this = effect.this.CastTo(Upgrade)
        face = message.played_face
        if face.HasTrait("ATTACK"):
            this.effect.RegisterTemp(
                AbilityFactory.WhenFaceWouldDealDamage(
                    AbilityType.Temp0,
                    None,
                    lambda deal_effect, deal_message: deal_message.IncreaseDamage(1, effect),
                    by_which_effect=message.played_effect,
                    allow_zero_damage=True,
                ),
                unregister_after_exec=False,
                until_event_end=message,
            )
        if face.HasTrait("THWART"):
            def plus_une_menace(remove_effect: 'Effect', remove_message: 'Message.WhenSchemeWouldRemoveThreat') -> None:
                remove_message.value += 1
            this.effect.RegisterTemp(
                AbilityFactory.WhenSchemeWouldRemoveThreat(
                    AbilityType.Temp0,
                    Scheme2,
                    plus_une_menace,
                    conditions=[lambda e, m: m.by_effect is message.played_effect],
                ),
                unregister_after_exec=False,
                until_event_end=message,
            )

    return [
        AbilityFactory.WhenPlayerPlayCard(
            AbilityType.HeroInterrupt,
            "You",
            CardFinder(card_type=Event),
            mental_training,
            # ⚠ `CardFinder(trait=[...])` n'accepte pas de liste (TypeError
            #   unhashable, vu le 11/09/2026) : le trait se teste en condition.
            conditions=[lambda e, m: m.played_face.HasTrait("ATTACK") or m.played_face.HasTrait("THWART"),
                        paye_en_mental_seulement],
        ),
    ]
