from . import *

# * Maelstrom — SBIRE NEMESIS de Quasar (QUASAR NEMESIS 1/5, numero imprime 99).
# DEVIANT. INHUMAN. MNG 1, ATQ 2, 5 PV (pastille ronde), 2 icones de boost.
# When Revealed: Tuck Quantum Bands under Maelstrom.
# Forced Response: After Maelstrom leaves play, put Quantum Bands into play
#   under the Quasar player's control.
# (Quasar's nemesis minion.)
#
# card_id gs099q : le numero 99 est AUSSI celui de Hobgoblin (Imperial Guard).
# Suffixe q provisoire, question Q-GS2-1 (.planning/todos/2026-10-20-gs2-questions.md).
#
# Cartes de reference :
#  - **`se005`** The Last Ronin / `td012` : glisser une carte sous une autre =
#    `face.TuckCardUnderHere([carte], effect)` (fiche tuck.md, enveloppe de
#    `PlaceCardHere`, zone hors jeu de la carte porteuse).
#  - **`sk038`** (meme auteur) : « After X leaves play » =
#    `AfterCardLeavePlay(type, "This", op)` (la fabrique pose
#    `NoOutOfPlayLimit` pour "This" : la carte est deja hors jeu).
#  - **`sk032`** Empress R'Klll : sbire nemesis du meme auteur,
#    `WhenThisRevealed(None, op)` ; `desc.Nemesis` = nom de l'alter ego.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Tuck QUANTUM BANDS » : LA carte de Quasar (unique), ou qu'elle soit en
#    jeu. Elle est PERMANENTE : le moteur refuse qu'une carte d'un AUTRE set la
#    fasse quitter le jeu (has_permanent.py). Le texte de Maelstrom la vise
#    nommement : exception ajoutee au moteur (CORRECTIF du 20/10/2026,
#    has_permanent.py, sur le modele « Milano » deja present).
#  - Glissee, elle est hors jeu : plus de ressource, plus d'AERIAL, plus de
#    Bandes a redresser.
#  - « After Maelstrom LEAVES PLAY » : vaincu, defausse, retire... pas
#    seulement vaincu. Reponse FORCEE.
#  - « put into play under THE QUASAR PLAYER'S control » : le joueur Quasar,
#    meme si c'est un autre joueur qui a vaincu Maelstrom.
#  - Pas de Villainous ni de Guard : la pastille ronde (5) est les PV.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)
        if not this.IsInPlay():
            return
        for bandes in Worlds.FindCardsOnField(effect, name=NOM_BANDES, card_type=Upgrade):
            if EstLesBandes(bandes) and this.TuckCardUnderHere([bandes], effect):
                this.card.bandes_glissees_par_maelstrom = bandes.card
                return

    def retour(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        this = effect.this
        Unused(message)
        carte = getattr(this.card, "bandes_glissees_par_maelstrom", None)
        this.card.bandes_glissees_par_maelstrom = None
        if carte is None:
            return
        bandes = carte.face
        if bandes is None or bandes.IsInPlay():
            return
        joueur = JoueurQuasar(effect, bandes)
        if joueur is None:
            return
        Faces.FlipAllTo([bandes], True, effect)
        carte.face.PutIntoPlay(joueur, effect, under_control=True)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation,
        ),
        AbilityFactory.AfterCardLeavePlay(
            AbilityType.ForcedResponse,
            "This",
            retour,
        ),
    ]
