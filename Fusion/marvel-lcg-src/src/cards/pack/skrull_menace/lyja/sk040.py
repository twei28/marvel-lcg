from . import *

# Feign Loyalty (x2) — EVENEMENT TREACHERY, cout 1 [physique]. Etoile rouge de boost.
# Hero Action: Shuffle this card into the encounter deck.
# When Revealed: Discard an attachment with the uses keyword or the text "Hero Action"
#   or "Hero Response" from play.
# ★ Boost: Draw 2 cards.
#
# Cartes de reference :
#  - **`player.AskChooseFace(faces, effect)`** (player_ask.py:272) pour designer l'attachement ;
#    **`Worlds.GetOnFieldCards`** pour balayer ce qui est en jeu (attachements poses sur un
#    ennemi, un heros...).
#  - **`CardFinder(with_texts=["Hero Action", "Hero Response"])`** (checker.py:66) : le
#    moteur sait deja lire « le texte Hero Action / Hero Response » d'une carte ; le
#    helper du set `ADesUsagesOuUnTexteDeHeros` fait la meme lecture et y ajoute le
#    mot-cle Uses (`uses_counters`, has_uses.py).
#  - Boost « draw 2 » : `DrawUp` du joueur qui subit l'activation (message.GetToPlayer()).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « an ATTACHMENT » : carte de TYPE Attachment (rencontre) ; les ameliorations
#    joueur ne sont pas visees (lecture retenue, defs/lyja_questions.md).
#  - « with the uses keyword OR the text Hero Action OR Hero Response » : trois
#    criteres alternatifs.
#  - « from play » : en jeu, quel que soit le porteur.
#  - Boost « Draw 2 cards » : le joueur qui defend l'activation pioche (« you » d'un
#    Boost = le joueur vise, cf. WhenCardBecomeBoost).


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        # Chooser non precise : le joueur a qui la carte est revelee (regle generale).
        joueur = message.GetToPlayer()
        candidats = [f for f in Worlds.GetOnFieldCards(effect) if ADesUsagesOuUnTexteDeHeros(f)]
        if not candidats:
            return
        choisie = joueur.AskChooseFace(candidats, effect)
        if choisie is not None:
            Faces.DiscardAll([choisie], effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.GetToPlayer().DrawUp(2, effect)

    return [
        MelangerDansLeDeckRencontre(),
        AbilityFactory.WhenThisRevealed(None, revelation),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
