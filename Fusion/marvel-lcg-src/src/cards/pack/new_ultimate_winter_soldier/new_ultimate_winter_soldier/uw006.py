from . import *

# Berserker Fury — evenement signature, x2. ATTACK. Cout 1, [physical].
# Hero Action (attack): Discard 1 card from your hand at random -> deal 2 damage to an enemy. This attack deals X additional
# damage, where X is equal to the numeral in the printed resource cost of that card. If this attack defeated an enemy, you
# may take 2 damage to repeat this ability.
#
# Carte de reference : `35008` Berserker Barrage (Wolverine officiel), MEME TEXTE de repetition (« If this attack defeats an
# enemy, you may take 2 damage -> repeat this ability ») : on reprend son montage (temp `AfterUnitDefeatedUnitInternal`
# + `MayChooseOneAbility`) tel quel.
#
# ⚠ ARBITRAGE DU 26/10/2026 (FAQ du Rules Reference v1.8, Across the Spider-Verse : « repeating the ability on this card includes
# the repeat effect itself ») : « repeat this ability » rejoue la capacite EN ENTIER, COUT COMPRIS. Chaque repetition defausse donc
# une NOUVELLE carte au hasard (nouveau X) ; main vide = repetition impossible (elle n'est pas proposee) ; la repetition peut elle-meme
# se repeter si elle vainc un ennemi. Difference avec 35008 Berserker Barrage, dont la repetition n'a pas de cout avant la fleche.


def GetAbilities() -> Sequence['Ability']:

    def berserker_fury(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()

        def repeter() -> None:
            # « repeat this ability » = tout rejouer : si la main est vide le cout ne peut pas etre paye, on ne propose rien.
            if not UneCarteADefausser(effect):
                return

            def repeter_interne(cibles: 'Sequence[CardFace]') -> None:
                initiator.GetIdentity().TakeDamage(this, 2, effect)
                # le COUT de la capacite, repaye : nouvelle carte au hasard, donc nouveau X (`effect.uw_defaussee`)
                if not DefausserAuHasard([], effect):
                    return
                action(cibles)

            initiator.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Take 2 damage → repeat this ability",
                    repeter_interne,
                ).SetLabel('attack')
                .SetTarget(Enemy),
            )

        def action(cibles: 'Sequence[CardFace]') -> None:
            degats = 2 + XDeLaCarteDefaussee(effect)
            this.effect.RegisterTemp(
                AbilityFactory.AfterUnitDefeatedUnitInternal(
                    AbilityType.Temp0,
                    None,
                    cibles,
                    lambda defeat_effect, defeat_message: repeter(),
                    conditions=[
                        lambda defeat_effect, defeat_message:
                            defeat_message.would_atk_message is not None and
                            defeat_message.would_atk_message.by_effect == effect and
                            defeat_message.target in cibles,
                    ],
                ),
                unregister_after_exec=True,
                until_turn_end=True,
                until_resolve_effect=effect,
            )
            this.DealDamage(cibles, degats, effect)

        action(effect.targets)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            berserker_fury,
            conditions=[UneCarteADefausser],
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CoutDefausseAuHasard())
        .SetTarget(Enemy),
    ]
