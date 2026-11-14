from . import *

# * Moon Knight (Marc Spector) — ALLIE 4 [energy], aspect Protection (Elektra Natchios 39). DEFENDER. MARTIAL ARTIST.
#   PV 5, THW 2**, ATK 2**.
# Interrupt: When Moon Knight defends, spend up to 3 resources → if you spent at least 1:
#   [energy] — Prevent 2 damage from this attack.
#   [mental] — Discard 1 boost card from the attacker.
#   [physical] — Deal 2 damage to the attacker.
#
# CARTES DE REFERENCE
#  - `47012` Husk : MEME FORMAT imprime (« spend up to 3 resources → if you spent at least 1: [energy] — ... [mental] — ... [physical] — ... ») =
#    `.SetCost(Cost("3", up_to=True))` + `effect.GetPaidResources(True)` + `res.HasColor("Y"/"B"/"R")` : un effet PAR TYPE de ressource depensee.
#  - `62012` Iron Fist (Luke Cage) : « prevent damage from that attack » = `WhenUnitWouldTakeDamage(Temp0, ..., is_from_attack=...)` +
#    `PreventDamage(n)` avec un BUDGET pour toute l'attaque (leçon du 17/09/2026 : plusieurs paquets de degats pour une meme attaque).
#  - `64015` Defiance : cartes de boost de l'attaquant (`components.boostable.GetDeck()`), `Faces.DiscardAll`.
#
# TEXTE CONTRE CODE
#  ⚠ « when Moon Knight DEFENDS » : quand il est declare defenseur (pas quand il est attaque comme cible).
#  ⚠ « up to 3 resources → IF YOU SPENT AT LEAST 1 [type] » : chaque icone est un effet independant, donne par au moins UNE ressource de ce type ;
#    trois ressources de trois types donnent les trois effets ; zero ressource ne donne rien.
#  ⚠ « Prevent 2 damage FROM THIS ATTACK » : 2 points en tout pour l'attaque entiere (budget), pas 2 par paquet de degats.
#  ⚠ « Discard 1 boost card FROM THE ATTACKER » : une carte de boost face cachee de l'attaquant (aucune s'il n'en a pas).
#  ⚠ « Deal 2 damage TO THE ATTACKER » : 2 degats de carte (pas une attaque), a l'ennemi qui attaque.


def GetAbilities() -> Sequence['Ability']:

    def moon_knight(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Ally)
        res = effect.GetPaidResources(True)
        attaque = message.would_atk_message
        attaquant = attaque.attacker
        if res.HasColor("Y"):
            restant = [2]

            def prevent(inner_effect: 'Effect', damage_message: 'Message.WhenUnitWouldTakeDamage') -> None:
                if restant[0] <= 0:
                    return
                a_prevenir = min(restant[0], damage_message.will_take_damage)
                if a_prevenir <= 0:
                    return
                restant[0] -= damage_message.PreventDamage(a_prevenir, effect)

            effect.this.effect.RegisterTemp(
                AbilityFactory.WhenUnitWouldTakeDamage(
                    AbilityType.Temp0,
                    None,
                    prevent,
                    is_from_attack=attaque,
                ),
                unregister_after_exec=False,
                until_event_end=attaque,
            )
        if res.HasColor("B") and attaquant is not None:
            paquet = attaquant.components.boostable.GetDeck()
            if paquet.GetSize() > 0:
                Faces.DiscardAll([paquet.GetTop()], effect)
        if res.HasColor("R") and attaquant is not None and attaquant.IsInPlay():
            this.DealDamage([attaquant], 2, effect)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.Interrupt,
            "This",
            moon_knight,
        ).SetCost(Cost("3", up_to=True)),
    ]
