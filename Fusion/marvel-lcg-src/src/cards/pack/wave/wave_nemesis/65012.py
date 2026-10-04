from . import *

# The Reyna Sirena — SBIRE, WAVE NEMESIS 2/5. SCH 2, ATK 2, HP 5. ATLAS.
# ELITE. SIRENA.
# As an additional cost for the engaged player to play an event, that player
# must take 1 damage.
# Boost: You are stunned.
#
# « EngagedPlayer » est un `PLAYER_TYPE` NATIF (game/ability/condition/
# player_type.py:70, `from_effect.this.CastTo(Minion).engaged_player`) : pas
# besoin de le reconstruire a la main, `WhenPlayerPlayCard(..., "EngagedPlayer",
# ...)` le lit directement depuis CE sbire.
# « must take 1 damage » sans echec possible (contrairement a un cout en
# ressources, qui peut manquer) : applique directement, pas de veritable
# `CostFunc` externe n'existant dans ce depot pour imposer un cout de degats
# sur la carte D'UN AUTRE joueur -- meme lecture pragmatique que
# `60137b`/`bc004` pour les regles « apres coup mais indissociables ».
# « that player must take 1 DAMAGE » : un degat porte sur UN JOUEUR (son
# identite courante, heros ou alter-ego), jamais sur un allie -- contrairement
# a `Utility.DealDamageToCharacterYouControl` (game/operate/utility.py:33),
# qui OFFRE UN CHOIX parmi tous les personnages controles, allies compris.
# Ecart trouve le 22/9/2026 en testant la carte : la premiere version passait
# par cet utilitaire, et le degat ne partait plus des lors que le choix
# interactif devait etre repondu HORS du fil de jeu normal (harnais de test).
# Le fond du defaut n'est pas le harnais mais la semantique : « a player »
# n'est jamais « a character you control ». `joueur.GetIdentity()` cible
# directement, sans choix.
# Boost « You are stunned » : modele `51035` M.U.S.I.C. (pack black_panther),
# `AbilityFactory.WhenCardBecomeBoost("This", ...)` + `Faces.GiveStatus(
# [joueur.GetIdentity()], "Stunned", effect)`.

def GetAbilities() -> Sequence['Ability']:

    def cout_supplementaire(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> None:
        this = effect.this.CastTo(Minion)

        joueur = message.to_player
        if not isinstance(joueur, Player):
            return
        this.DealDamage([joueur.GetIdentity()], 1, effect)

    def reyna_sirena_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        joueur = message.GetToPlayer()
        Faces.GiveStatus([joueur.GetIdentity()], "Stunned", effect)

    return [
        AbilityFactory.WhenPlayerPlayCard(
            AbilityType.ForcedResponse, "EngagedPlayer", CardFinder(card_type=Event),
            cout_supplementaire,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            reyna_sirena_boost,
        ),
    ]
