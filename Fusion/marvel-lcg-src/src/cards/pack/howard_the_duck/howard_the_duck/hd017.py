from . import *

# Nexus of all Realities — amelioration, Setup. Permanent.
# Setup. Permanent.
# Interrupt: When a character enters play, choose a play area that character
#   is played to.
# Interrupt: When an ally you control leaves play, search your deck for an
#   event card, and add it to your hand.
#
# « Setup » et « Permanent » sont lus par le moteur dans `desc.Setup` /
# `desc.Permanent` : aucune ability ICI. C'est l'IDENTITE (hd001b) qui met
# cette carte en jeu a la mise en place, via `AbilityFactory.SetupPutIntoPlay
# (["hd017"])` — voie idiomatique du depot, partagee par Wolverine (35002),
# Vision (26002a/b), Spider-Man Rainy (sr012), Storm, Doctor Strange... La cle
# `set_aside: ["hd017"]` du deck de depart est purement DOCUMENTAIRE : le
# moteur ne la lit jamais dans le chemin `SceneLoader.NewScene`.
# `desc.Setup` seul ne suffirait PAS : `World.GameSetup` ne cherche les cartes
# Setup que dans `player_deck`, `set_aside_nemesis_sets`, les decks de
# rencontre et `world.additional_decks` (world.py:531-539) — jamais dans le
# set aside du joueur. Point trouve par le cas test_capacites de hd017 le
# 30/08/2026, ou la carte n'apparaissait NULLE PART dans le journal.
#
# ---------------------------------------------------------------------------
# PREMIER INTERRUPT : DELIBEREMENT NON CODE, ET NON UN OUBLI.
# « choose a play area that character is played to » est une mecanique
# MULTI-ZONES : elle suppose plusieurs aires de jeu (une par joueur) entre
# lesquelles on peut router un personnage a son entree. Ce moteur n'expose
# aucun crochet pour cela : `Message.WhenCardEnterPlay` (sender_card.py:995)
# ne porte AUCUNE destination modifiable, et `Message.WhenCardPutIntoPlay`
# (sender_card.py:388) porte bien un `target_game_area` mais declare `Final`,
# donc figé avant que l'interruption ne puisse s'exprimer. En SOLO — le seul
# mode ou ce heros a ete valide — il n'existe qu'une seule aire de jeu : le
# choix est vide de consequence, et ne rien coder produit exactement le meme
# etat du monde que le texte imprime. Precedent de clause imprimee laissee
# sans code, assumee et documentee : ok023 (« gains villainous for this
# attack ») et kb003 (« cannot place arrow counters »).
# A VERIFIER EN PARTIE REELLE (multijoueur) : ce qui manque est precisement
# la possibilite d'envoyer un allie/personnage dans l'aire de jeu d'un AUTRE
# joueur au moment ou il entre en jeu.
# ---------------------------------------------------------------------------
#
# SECOND INTERRUPT : `AbilityFactory.WhenCardLeavePlay(AbilityType.Interrupt,
# <cible>, ...)` (card_move.py:208) — la carte est encore manipulable a ce
# stade, et l'allie qui part est bien identifie. Cible
# `("YouControl", CardFinder(card_type=Ally))` : tuple deja utilise par ok010
# et ok014 pour rendre « an ally YOU control ». Recherche : `Search.PlayerCard
# (include_player_deck=True, include_discard_pile=False, card_type=Event)` —
# le texte dit « search your DECK », pas la defausse — puis
# `initiator.GainCard` (modele ok001b / ss001b).


def GetAbilities() -> Sequence['Ability']:

    def nexus_allie_part(effect: 'Effect', message: 'Message.WhenCardLeavePlay') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=False,
            card_type=Event,
        )
        if face:
            initiator.GainCard(face, effect)

    return [
        AbilityFactory.WhenCardLeavePlay(
            AbilityType.Interrupt,
            ("YouControl", CardFinder(card_type=Ally)),
            nexus_allie_part,
        ),
    ]
