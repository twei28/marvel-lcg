from . import *

# Getting it Done (Event)
#
# Hero Interrupt: When you make a basic attack, you get +3 ATK for this attack. You may split this damage
#   between enemies. If you reduced this card's cost, ready your hero.
#
# CARTES DE REFERENCE
#  - `ah011` Kinetic Stomp : "Hero Interrupt: When you make a basic attack, you get +X ATK for that attack" ->
#    `AbilityFactory.WhenUnitMakeAttack(HeroInterrupt, "You", op, is_basic_attack=True).SetPlay()` +
#    `message.GainATKForThisAttack(X, effect)`.
#  - `16155` Creative Solution / `13006` Wasp Sting : "deal a total of N damage divided among enemies as you
#    choose" -> `.SetTarget(Enemy, range=(1, N), repeat_rules="Health")` (chaque occurrence = 1 point), puis
#    `this.DealDamage(effect.targets, 1, effect)`. N = 4 ici (ATQ imprimee 1 + bonus 3 de cette carte) : les
#    boosts d'ATQ externes eventuellement deja actifs au moment de l'interruption ne sont PAS pris en compte
#    dans ce total (limite assumee, comme les autres cartes "divided" du depot qui fixent N a la construction).
#  - CONFIRME PAR L'AUTEUR DE LA CARTE (RTimMorris, Discord, 05/11/2026) : "split this damage between enemies"
#    porte sur TOUT le degat de l'attaque (base + bonus), pas seulement le bonus +3 -- partage REEL du total
#    (l'ennemi engage peut recevoir MOINS que le total), pas une attaque qui touche aussi d'autres ennemis en
#    entier. Le seul moyen d'y parvenir : ANNULER la resolution normale de l'attaque (`message.SetBeInstead`)
#    et distribuer le total en degats directs (`DealDamage`) -- CONSEQUENCE ASSUMEE : la portion partagee ne
#    passe plus par l'etape de defense (une attaque normale peut etre defendue, un `DealDamage` direct non).
#  - "You MAY split" : optionnel -> `initiator.ChooseAbilities` avec un choix "Ne pas partager" (rien de plus)
#    et un choix "Partager" portant sa propre cible (modele `16155`).
#  - `CoutReduit` (pack `three_d_man/__init__.py`) + `Faces.ReadyAll` (modele `sk019`) pour "ready your hero".

def GetAbilities() -> Sequence['Ability']:

    def getting_it_done(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Event)
        message.GainATKForThisAttack(3, effect)

        initiator = effect.GetInitiator()

        def ne_pas_partager(targets: Sequence['CardFace']) -> None:
            Unused(targets)

        def partager(targets: Sequence['CardFace']) -> None:
            message.SetBeInstead(effect)
            this.DealDamage(targets, 1, effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Don't split this damage", ne_pas_partager),
            AbilityFactory.ForChoiceAbility(
                "Split this damage between enemies",
                partager,
            ).SetTarget(Enemy, range=(1, 4), repeat_rules="Health"),
        )

        if CoutReduit(effect):
            identite = initiator.GetIdentity()
            if identite is not None:
                Faces.ReadyAll([identite], effect)

    return [
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.HeroInterrupt,
            "You",
            getting_it_done,
            is_basic_attack=True,
        ).SetPlay(),
    ]
