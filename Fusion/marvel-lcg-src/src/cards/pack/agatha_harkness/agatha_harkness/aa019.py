from . import *

# * Wiccan (William Kaplan) — allie d'aspect JUSTICE (carte bonus du pack).
# AVENGER. MYSTIC. Cout 2 / PV 3 / THW 1* / ATK 1*
# Response: After Wiccan thwarts, discard the top card of the encounter
#   deck. For each boost icon discarded this way, deal 1 damage to an enemy.
#
# Cartes de reference (RECETTES) : `AfterUnitAttackOrThwart` (do_attack.py,
# la branche THWART filtree par le type de message), ag004/15004 pour la
# defausse rencontre et le comptage d'icones, 08013 pour la cible au choix.
#
# ⚠ Homonymes : le HEROS fan-made wc001a, l'allie Justice officiel 15011,
# l'allie signature 56030 (Hulkling) et le sbire 57061 — regle d'unicite en
# jeu, et JAMAIS cette carte dans un deck wiccan (allie au nom du heros).
# ⚠ « deal 1 damage to AN enemy » PAR icone : cibles libres, une par icone.

def GetAbilities() -> Sequence['Ability']:

    def wiccan(effect: 'Effect', message: 'Message.AfterUnitThwartEnd') -> None:
        this = effect.this.CastTo(Ally)

        initiator = effect.GetInitiator()
        defaussees = Worlds.DiscardEncounterCards(1, effect)
        icones = FacesCounter.CountTotalBoostIcons(defaussees)

        def frapper(cibles: Sequence['CardFace']) -> None:
            this.DealDamage(list(cibles), 1, effect)

        for _ in range(icones):
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Deal 1 damage to an enemy", frapper,
                ).SetTarget(Enemy),
            )

    def seulement_thwart(effect: 'Effect', message: 'Message2') -> bool:
        return isinstance(message, Message.AfterUnitThwartEnd)

    return [
        AbilityFactory.AfterUnitAttackOrThwart(
            AbilityType.Response,
            "This",
            wiccan,
            conditions=[seulement_thwart],
        ),
    ]
