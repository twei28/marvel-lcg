from . import *

# * Throg — SBIRE DE JOUEUR, cout 0, 4 PV, MNG 0 / ATQ 0. ASGARD. CREATURE.
#
# Patrol.
# Interrupt: When Alligator Loki attacks Throg, that attack gains overkill.
# When Defeated: Remove 3 threat from a scheme. Shuffle Throg into the
#   Alligator Loki player's deck.
#
# ⚠ TYPE DE CARTE NEUF : `PlayerMinion`, defini par l'encart du pack. Voir
# `game/card/face/card_type/minion_player.py`. Le sbire est joue depuis la main
# contre son cout imprime et s'engage avec son proprietaire.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - `Patrol` (mots-cles/patrol.md) : BASE AUTOMATIQUE. Le moteur lit
#   `desc.Patrol` et applique l'interdiction de contrer le complot principal
#   dans `MainScheme.CanBeThwartBy`. AUCUN script. ⚠ Ici le sbire est engage
#   avec SON PROPRE camp : Throg empeche donc son proprietaire de contrer le
#   complot principal tant qu'il est la, ce qui est bien l'intention (c'est un
#   cout, pas un cadeau).
# - `overkill` (mots-cles/overkill.md) : se donne a l'ATTAQUE, par
#   `AttackProperty(overkill=...)`, jamais au personnage.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - donner overkill a une attaque en cours : dd004 et 01053, qui posent
#   `AttackProperty`. Ici l'attaque n'est pas la notre : on modifie celle qui
#   arrive, par `message.property`.
# - « When Defeated » sur un sbire : jj013 / 01166, `WhenUnitBeDefeated`.
# - remelanger une carte dans le deck du joueur : an014, `ShuffleAllTo`.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « When ALLIGATOR LOKI attacks Throg » -> l'attaquant doit etre le heros
#   Alligator Loki, pas n'importe qui : un allie qui frappe Throg ne gagne
#   rien.
# « that ATTACK gains overkill » -> la propriete est posee sur le message de
#   l'attaque, pas sur le heros.
# « Remove 3 threat from A SCHEME » -> une manigance au choix, principale ou
#   annexe, d'ou le helper commun du pack qui ne propose que celles qui portent
#   de la menace.
# « Shuffle Throg into the ALLIGATOR LOKI PLAYER's deck » -> le deck du
#   PROPRIETAIRE, pas celui du joueur qui l'a vaincu. En solo c'est le meme ;
#   a plusieurs, non.


def GetAbilities() -> Sequence['Ability']:

    def donner_overkill(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.property.overkill = True

    def quand_vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        RetirerMenaceDUneManigance(effect, 3)
        proprietaire = this.card.GetOwner() or effect.GetInitiator()
        # ⚠ `ShuffleAllTo` prend un OBJET deck, pas un libelle : la signature
        # est `(faces, deck, by_effect)` (faces.py:48).
        Faces.ShuffleAllTo([this], proprietaire.player_deck, effect)

    return [
        # ⚠ `attack_targets="This"` est la CONDITION de declenchement, pas un
        # simple test dans l'operation : un Interrupt nu pose une question au
        # joueur a chaque declenchement. Filtre dans l'operation seulement, la
        # question « Throg ? » revenait a CHAQUE attaque du heros (Rhino
        # compris) sans rien faire, et le garde-fou anti-repetition de
        # l'autoplay finissait par bloquer la partie (graine 5, 01/09/2026).
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.Interrupt,
            CardFinder(name="Alligator Loki"),
            donner_overkill,
            attack_targets="This",
        ),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            quand_vaincu,
        ),
    ]
