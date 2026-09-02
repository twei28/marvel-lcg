from . import *

# Heroes' Labor — TRAITRISE a DOS DE CARTE JOUEUR (×4), mise de cote au setup.
# Le complot 2A en melange une copie dans le deck de chaque joueur.
#
# Incite 1.
# Forced Response: After you draw Heroes' Labor or discard it from the top of
#   your deck, reveal it.
# When Revealed: Place 1 timer counter on the Godbomb environment, if able.
#   Otherwise, place 1 necro counter on the All-Black Necroverse environment.
#   Put this card into your discard pile (instead of discarding it to the
#   encounter discard pile).
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - `Incite` (mots-cles/incite.md) : BASE AUTOMATIQUE, `desc.Incite = "1"`.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « After you DRAW this card ... reveal it » : 45178 (Panicked Refugees,
#   pack aoa) — `AfterCardEnterHand(ForcedResponse, "This", ...)` puis
#   `this.Reveal(player, effect)`. Le moteur n'a pas de message « After you
#   draw X » : `AfterCardEnterHand` couvre la pioche.
# - « or DISCARD IT FROM THE TOP OF YOUR DECK » : aa007 (Occult Knowledge),
#   `AfterCardDiscardInternal(..., from_where="PlayerDeckTop")`.
# - Le DOS JOUEUR ne se declare pas ici : il vient de ce que la carte est
#   CREEE dans `player.player_deck` (card.py:815-838), ce que fait gb005a.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « After YOU draw » -> le joueur qui pioche, pas le premier joueur.
# « IF ABLE ... OTHERWISE » -> deux branches exclusives, et la premiere
#   n'echoue que si Godbomb n'est pas en jeu (retournee ou pas encore posee) :
#   c'est le retour booleen de l'helper `PoserTimer` du pack.
# « Put this card into YOUR DISCARD PILE (instead of ...) » -> la carte finit
#   dans la defausse du JOUEUR, pas dans celle de rencontre : elle reviendra
#   donc dans son deck au prochain melange. C'est une horloge qui ne s'arrete
#   jamais.


def GetAbilities() -> Sequence['Ability']:

    def reveler(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Treachery)

        joueur = this.card.GetOwner()
        if isinstance(joueur, Player):
            this.Reveal(joueur, effect)

    def labeur_des_heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        if not PoserTimer(effect, 1):
            PoserNecro(effect, 1)

        joueur = message.GetToPlayer()
        if joueur:
            Faces.DiscardAll([this], effect, into_area=joueur.discard_pile)

    return [
        AbilityFactory.AfterCardEnterHand(
            AbilityType.ForcedResponse,
            "This",
            reveler,
        ),
        AbilityFactory.AfterCardDiscardInternal(
            AbilityType.ForcedResponse,
            "This",
            reveler,
            from_where="PlayerDeckTop",
        ),
        AbilityFactory.WhenThisRevealed(None, labeur_des_heros),
    ]
