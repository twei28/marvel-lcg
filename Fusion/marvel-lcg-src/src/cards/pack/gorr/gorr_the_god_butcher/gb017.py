from . import *

# Gleeful Savagery — TRAITRISE. 1 icone de boost + une etoile.
#
# When Revealed (Alter-Ego): Take 1 indirect damage. This card gains surge.
# When Revealed (Hero): Gorr the God Butcher attacks you. Take 2 indirect
#   damage or discard the top 2 cards of your deck.
# [star] Boost: Take 2 indirect damage or discard the top 2 cards of your deck.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Deux « When Revealed » selon la forme : 01145 (Rage of Ultron), qui a
#   exactement cette structure — `WhenThisRevealed("Alter-Ego", ...)` et
#   `WhenThisRevealed("Hero", ...)`, avec `villain.DoAttackYou(player, effect)`.
# - Surge conditionnel : helper `ThisCardGainSurge` (modele ag014).
# - Choix impose entre deux effets : `ChooseAbilities`, comme gb015 et gb016.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « (Alter-Ego) » / « (Hero) » -> deux capacites exclusives, jamais les deux.
# « Gorr the God Butcher ATTACKS YOU » -> une vraie attaque du vilain contre le
#   joueur qui revele, cartes de boost comprises, PUIS le choix.
# « Take 2 INDIRECT damage » -> degats indirects, que le joueur repartit ; ce
#   n'est pas la meme chose que 2 degats a l'identite.
# Le ★ Boost reprend le choix de la branche HEROS, sans l'attaque, et
#   s'applique quelle que soit la forme du joueur.


def GetAbilities() -> Sequence['Ability']:

    def choix_degats_ou_defausse(effect: 'Effect', joueur: 'Player') -> None:
        def subir(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            # Les degats indirects se posent sur l'IDENTITE, par
            # `identity.TakeIndirectDamage(source, n, effect)` (modele aa014,
            # lui-meme copie de kb019). Le joueur n'a pas cette methode.
            identite = joueur.GetIdentity()
            if identite is not None:
                identite.TakeIndirectDamage(effect.this, 2, effect)

        def defausser(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            joueur.DiscardDeckTopCards(2, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Take 2 indirect damage", subir),
            AbilityFactory.ForChoiceAbility(
                "Discard the top 2 cards of your deck", defausser),
        )

    def sauvagerie_alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity() if joueur else None
        if identite is not None:
            identite.TakeIndirectDamage(effect.this, 1, effect)
        ThisCardGainSurge(effect)

    def sauvagerie_heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        vilain = TrouverGorr(effect)
        if vilain and joueur:
            vilain.DoAttackYou(joueur, effect)
        if joueur:
            choix_degats_ou_defausse(effect, joueur)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        if joueur:
            choix_degats_ou_defausse(effect, joueur)

    return [
        AbilityFactory.WhenThisRevealed("Alter-Ego", sauvagerie_alter_ego),
        AbilityFactory.WhenThisRevealed("Hero", sauvagerie_heros),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
