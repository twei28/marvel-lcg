from . import *

# * Dr Hank McCoy — alter-ego. SCIENTIST. GENIUS. MUTANT. REC 4, MNG 6, 13 PV.
# Scientific Discovery — Forced Response: After you change to this form,
#   shuffle 1 random discovery card into your deck.
# Setup: All cards you mulligan from your hand during setup are shuffled back
#   into your deck.
#
# Cartes de reference :
#  - mise de cote du pool Discovery : 36001b * Ororo Munroe (pack storm),
#    `AbilityFactory.BeginGameWithSetAside([...])` puis relecture par
#    `set_aside_deck.Get()`. Comparable parce que Storm garde elle aussi un
#    petit pool ferme de cartes hors-deck, pioche dedans en cours de partie,
#    et que le pool s'epuise. Seule difference : les climats de Storm ENTRENT
#    EN JEU, les Discovery de Beast partent dans le DECK.
#  - « After you change to this form » : 01019a * She-Hulk,
#    `AfterUnitChangeForm(type, "You", op, to_this_form=True)` (recette §1).
#  - le tirage au sort : `Rand.RandomChoice(liste, effect)`
#    (game/operate/rand.py). Il est DETERMINISTE quand le monde tourne avec
#    `disable_shuffle` — il rend alors le premier element — ce qui rend les
#    cas de test reproductibles sans truquer la carte.
#  - remelange dans le deck du joueur : `Faces.ShuffleAllTo(faces, deck, ...)`
#    (game/operate/faces.py:48), qui melange APRES avoir deplace.
#
# ⚠ « 1 RANDOM discovery card » : c'est le hasard qui choisit, pas le joueur.
# Passer par `AskChooseFace` (ce que fait Ororo) trahirait la carte : tout le
# sel du pool est de ne pas savoir ce qui tombe.
#
# ⚠ Le pool s'epuise et ne se recharge jamais : cinq passages en alter-ego au
# maximum sur une partie. Quand `GetDiscoveryDeck` rend une liste vide, la
# capacite ne fait rien — pas d'erreur, pas de message.
#
# ⚠ SETUP / MULLIGAN : le moteur n'avait AUCUN point d'accroche sur l'etape 15
# de `World.Setup`. Le message `WhenPlayerResolveMulligans` existait mais
# n'etait jamais `.Send()`. Ajoutes le 31/08/2026, tous les trois ADDITIFS
# (aucune carte existante n'ecoute ce message) :
#   - `Message.AfterPlayerResolveMulligans` (sender_player.py), qui porte
#     `discarded_faces` ;
#   - son envoi dans `PlayerPhase.ResolveMulligans`, APRES le `DrawUp("Max")`
#     pour que les cartes remises ne soient pas repiochees dans la foulee ;
#   - `AbilityFactory.AfterPlayerResolveMulligans` (factory/setup.py).
# Le journal de portage (§4) le consigne : ce sont trois fichiers moteur
# PARTAGES, la batterie complete est due.
#
# ⚠ On remelange `message.discarded_faces`, PAS la pile de defausse : un autre
# effet de mise en place pourrait l'avoir garnie, et le texte ne parle que des
# cartes « you mulligan ».

def GetAbilities() -> Sequence['Ability']:

    def scientific_discovery(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        faces = GetDiscoveryDeck(effect)
        if not faces:
            return

        face = Rand.RandomChoice(faces, effect)
        Faces.ShuffleAllTo([face], initiator.player_deck, effect)

    def mulligan_retour_au_deck(effect: 'Effect', message: 'Message.AfterPlayerResolveMulligans') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        faces = [f for f in message.discarded_faces if f is not None]
        if faces:
            Faces.ShuffleAllTo(faces, initiator.player_deck, effect)

    return [
        AbilityFactory.BeginGameWithSetAside([
            "bt014",
            "bt015",
            "bt016",
            "bt017",
            "bt018",
        ]),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.ForcedResponse,
            "You",
            scientific_discovery,
            to_this_form=True,
        ).SetName("Scientific Discovery"),
        AbilityFactory.AfterPlayerResolveMulligans(
            AbilityType.Setup,
            mulligan_retour_au_deck,
        ),
    ]
