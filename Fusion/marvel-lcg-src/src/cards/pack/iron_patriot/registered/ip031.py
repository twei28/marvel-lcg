from . import *

# * Loki — SBIRE du deck REGISTERED (18/20). 4 PV, ATQ 1, MNG 4, boost 4.
# ASGARD. ELITE. MYSTIC.
# Incite 2. Stalwart.
# Forced Response: After you resolve a treachery, heal 1 damage from Loki.
# Trickster Magic — Special: Search the encounter deck for a treachery and
#   discard it. (Shuffle.)
#
# ⚠ LES DEUX MOITIES SE REPONDENT : sbire, Loki se soigne de chaque traitrise
# qui vous tombe dessus ; allie, il en retire une du deck avant qu'elle ne
# sorte. Le meme personnage, des deux cotes de la table.
#
# CARTES DE REFERENCE
#  - `31015` * Spider-Man Noir : `AbilityFactory.AfterYouResolveTreachery(
#    AbilityType.Response, op)` — la fenetre existe telle quelle.
#  - `Search.EncounterCard(effect, joueur, include_discard_pile=False, ...)`
#    (search.py:47) : fouiller le DECK de rencontre seul.
#
# TEXTE CONTRE CODE
#  ⚠ « After YOU resolve a treachery » : le joueur qui controle Loki, pas
#    n'importe lequel. `AfterYouResolveTreachery` teste deja le « you ».
#  ⚠ « Search THE ENCOUNTER DECK » : le deck seul, pas la defausse — d'ou
#    `include_discard_pile=False`. C'est ce qui borne la carte : une traitrise
#    deja defaussee ne se retire pas deux fois.
#  ⚠ « and DISCARD it » : elle part en defausse de rencontre, elle n'est pas
#    retiree de la partie. Elle peut revenir au remelange.
#  ⚠ Deck de rencontre sans traitrise : rien ne se passe, la carte ne plante
#    pas.
#  ⚠ Incite 2 et Stalwart sont des BASES NATIVES de sbire.


def GetAbilities() -> Sequence['Ability']:

    def se_repaitre(effect: 'Effect', message: 'Message.AfterCardRevealedEnd') -> None:
        this = effect.this.CastTo(Unit2)
        Unused(message)
        if this is not None:
            this.HealHealth(1, effect)

    def magie_du_farceur(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        face = Search.EncounterCard(
            effect,
            joueur,
            include_discard_pile=False,
            card_type=Treachery,
        )
        if face is not None:
            Faces.DiscardAll([face], effect)

    def apres_une_traitrise_du_joueur(effect: 'Effect',
                                      message: 'Message.AfterCardRevealed') -> bool:
        # ⚠⚠ ON NE PEUT PAS UTILISER `AbilityFactory.AfterYouResolveTreachery`.
        # Sa condition appelle `effect.GetInitiator()` (reveal.py:198), qui
        # AFFIRME que l'initiateur est un joueur. Or Loki est d'abord un SBIRE,
        # controle par le SCENARIO : la condition levait
        # `AssertionError: self.initiator=Klaw` a chaque traitrise revelee.
        # 48 fois sur 16 parties d'autoplay, le 10/09/2026 — et jamais dans un
        # cas, ou Loki est toujours deja allie.
        # On refait donc la condition a la main, en commencant par verifier
        # qu'il Y A un joueur.
        joueur = getattr(effect, "initiator", None)
        if not Player.IsType(joueur):
            return False
        return joueur == message.GetToPlayer() and Treachery.IsType(message.trigger)

    return [
        Ability(
            AbilityType.ForcedResponse,
            Message.AfterCardRevealed,
            [apres_une_traitrise_du_joueur],
            se_repaitre,
        ),
        SpecialRegistered("Trickster Magic", magie_du_farceur),
    ]
