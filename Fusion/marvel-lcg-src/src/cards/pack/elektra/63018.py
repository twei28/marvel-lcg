from . import *

# 22/10/2026 : carte OFFICIELLE du pack Elektra Natchios (MC63, n° de collection 18), ex-`ua008` (aspects TMNT d'Inkwire, meme texte). `ua008` n'existe plus : c'est maintenant
# l'art alternatif « tmnt » de `63018` (data/arts_alternatifs.json). Script, cas et gabarit PROCESSUS-CARTE repris tels quels.
# Chain Reaction — EVENEMENT 2 [physical], aspect Aggression (TMNT Reskins, Inkwire). ATTACK.
# Hero Action (attack): Deal 2 damage to an enemy. If that enemy is defeated, deal 2 damage to a second
#   enemy. If that enemy is defeated, deal 3 damage to a third enemy.
#
# CARTES DE REFERENCE
#  - `35018` Precision Strike : « Deal 2 damage to an enemy. If this attack defeats that enemy, ... » =
#    `this.DealDamage(effect.targets, 2, effect)` puis `effect.targets[0].IsDefeated()`.
#  - `60023` Know Your Enemy : une cible choisie a la RESOLUTION = `ChooseAbilities(ForChoiceAbility(...)
#    .SetTarget(...))`.
# TEXTE CONTRE CODE
#  ⚠ « a SECOND enemy » / « a THIRD enemy » : choisis APRES la defaite du precedent ; l'ennemi vaincu a
#    quitte le jeu, il ne peut pas etre rechoisi.
#  ⚠ 2, 2 puis 3 degats (le troisieme vaut 3).
#  ⚠ Si le 1er (ou le 2e) n'est pas vaincu, la chaine s'arrete.
#  Aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def chain_reaction(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()

        def frapper(cibles: Sequence['CardFace'], suite: Sequence[int]) -> None:
            if not cibles:
                return
            this.DealDamage(cibles, suite[0], effect)
            if len(suite) > 1 and cibles[0].IsDefeated():
                joueur.ChooseAbilities(
                    effect,
                    AbilityFactory.ForChoiceAbility(
                        f"Deal {suite[1]} damage to another enemy",
                        lambda autres: frapper(autres, suite[1:]),
                    ).SetTarget(Enemy),
                )

        frapper(effect.targets, [2, 2, 3])

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            chain_reaction,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
