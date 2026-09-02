from . import *

# * Agatha Harkness (face alter-ego)
# MYSTIC.  REC 3 — HS 6 / PV 9
# Setup: Set aside Ghost Agatha. Find the Agatha All Along player side scheme
#   and add it to your hand.
# Ghost Form - Forced Response: After you are eliminated from the game, find
#   the set-aside Ghost Agatha support and put it into play.
#
# Cartes de reference (RECETTES-MOTEUR) :
#  - Setup + fouille : an001b / ok001b, `WhenCardSetup` +
#    `Search.PlayerCard(include_player_deck=True, finder=...)` + `GainCard` ;
#  - « Set aside Ghost Agatha » : `AbilityFactory.BeginGameWithSetAside`,
#    modele bt001b / 09001b / 46001b. ⚠ CORRECTION DU 02/09/2026 : le champ
#    `set_aside` de deck/starter/agatha_harkness.json ne suffit PAS. Il ne
#    sert qu'aux clients (catalogue, lanceur) ; `HeroDescriptor`
#    (scene/replay/hero.py) n'a pas ce champ et `SelectIdentity`
#    (player_setup.py:213) a la generation en commentaire. Seul le chemin
#    PUZZLE (server_new_game.py:93) versait un set_aside, donc le harnais
#    seul : en vraie partie aa013 n'existait nulle part et Ghost Form ne
#    trouvait jamais son fantome. Ecart repere en portant Alligator Loki ;
#  - la mise en jeu depuis la reserve : modele iceman
#    (`player.set_aside_deck.FindCard(...)`), puis `Faces.PutIntoPlayAll` ;
#  - l'elimination : `Message.WhenPlayerEliminated` (sender_player.py:349),
#    aucun precedent de fabrique — Ability brute.
#
# ⚠ PIEGE DU FLUX D'ELIMINATION (player.py:113-222) : main, deck, defausse,
# soutiens... sont TOUS defausses et le joueur retire de `world.players`
# AVANT l'envoi du message, et le message ne PORTE PAS le joueur elimine
# (il ne sert qu'au texte d'affichage). Deux consequences :
#  - seule l'IDENTITE survit (exclue de la defausse par
#    `non_card_type=Identity`) : c'est bien elle qui doit porter l'ecoute ;
#  - la condition ne peut pas lire le message — on teste « MON joueur est
#    elimine ET Ghost Agatha encore en reserve », idempotent par
#    construction (apres la mise en jeu, la reserve est vide). La
#    `set_aside_deck` n'est PAS videe par le flux : le fantome y survit.
# Ghost Agatha declare elle-meme « The first player controls » (aa013) : la
# mise en jeu se fait chez le proprietaire, le controle est gere par aa013.

def GetAbilities() -> Sequence['Ability']:

    def setup(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            finder=CardFinder(card_ids=["aa008"]),
        )
        if face:
            initiator.GainCard(face, effect)

        # Ghost Form est ANCREE sur la manigance principale : apres
        # l'elimination, l'identite n'est plus « en jeu » et ses ecouteurs
        # sont filtres (constate au premier passage du cas aa001b) — la
        # manigance, elle, survit au flux d'elimination.
        manigances = Worlds.GetAllMainSchemes(effect)
        if manigances:
            manigances[0].effect.RegisterTemp(
                Ability(
                    # Temp0, comme TOUT RegisterTemp du projet : un type
                    # Response/Forced enregistre ainsi n'est jamais traite
                    # (constate au cas aa001b, silencieux).
                    AbilityType.Temp0,
                    Message.WhenPlayerEliminated,
                    [lambda e, m: mon_fantome_en_reserve_de(this) is not None],
                    lambda e, m: ghost_form_de(this, e),
                ).SetName("Ghost Form"),
                unregister_after_exec=False,
            )

    def mon_fantome_en_reserve_de(identite: 'AlterEgo') -> 'CardFace|None':
        player = identite.GetOwner()
        if not isinstance(player, Player) or not player.is_eliminated:
            return None
        # `BeginGameWithSetAside` depose aa013 dans `additional_discard_pile`,
        # dont `set_aside_deck` est l'alias (player.py:100). Repli sur la
        # reserve du MONDE par precaution : certains flux y rangent les mises
        # de cote.
        fantome = player.set_aside_deck.FindCard(card_ids=["aa013"])
        if fantome is None:
            fantome = player.world.aside_deck.FindCard(card_ids=["aa013"])
        return fantome

    def ghost_form_de(identite: 'AlterEgo', effect: 'Effect') -> None:
        player = identite.GetOwner()
        fantome = mon_fantome_en_reserve_de(identite)
        if fantome is not None and isinstance(player, Player):
            # pas de Faces.PutIntoPlayAll dans le moteur : l'API vit sur la
            # face elle-meme (faces.py:406 l'appelle ainsi)
            fantome.PutIntoPlay(player, effect)

    return [
        AbilityFactory.BeginGameWithSetAside(["aa013"]),
        AbilityFactory.WhenCardSetup(
            "This",
            setup,
        ),
    ]
