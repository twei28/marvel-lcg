from . import *

# * Tony Stark (face alter-ego) — GENIUS.
# REC 3 — HS 6 / PV 10
# Inventor — Setup: Discard 1 card from your hand -> search your deck for a
#   TECH upgrade and add it to your hand.
# Action: Reduce the cost of the next upgrade played this round by 1.
#   (Limit once per round.)
#
# Cartes de reference :
#  - le Setup : **`an001b`** * Aldrif Odinsdottir et `ok001b` * Okoye —
#    `WhenCardSetup("This", op)` + `Search.PlayerCard(include_player_deck=True,
#    trait=...)` + `GainCard` ;
#  - la defausse de cout : `10025` Inner Demons (`player.DiscardHandCards`) ;
#  - la reduction : **`16024` Deft Focus**, via `aa009` * The Witches' Road —
#    `Worlds.UpdateNextCardPlayCost(joueur, -1, effect, finder=..., in_this=)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Discard 1 card from your hand **->** » : la fleche en fait un COUT. Si
#    rien n'est defausse, on ne cherche pas. A la mise en place la main est
#    pleine, le cas est donc toujours payable, mais on lit quand meme le
#    RETOUR plutot que de le supposer.
#  - « a **TECH UPGRADE** » : le trait ET le type. Une carte TECH qui ne
#    serait pas une amelioration ne compte pas — et le pack en a justement,
#    puisque `im007`, `im008`, `im009`, `im010`, `im012` et `im013` sont TECH
#    tandis que rien d'autre ne l'est.
#  - « search your DECK » seulement : contrairement a `ls005` To Arms! du pack
#    precedent, la defausse n'est PAS fouillee. Pas de
#    `include_discard_pile` : le mot n'est pas imprime.
#  - « the next UPGRADE played » : le type, pas un trait. `CardFinder(
#    card_type=Upgrade)`, ce qui inclut les ameliorations d'aspect.
#  - « (Limit once per ROUND) » sur l'Action.
#  - Le type imprime de l'Action est **nu**, comme le Setup : la carte EST la
#    face civile.
#
# ⚠ ECART ASSUME, ET IL EST DANS LE MOTEUR. La carte dit « this **ROUND** » ;
# `UpdateNextCardPlayCost` n'accepte que `in_this="Phase"` ou `"Turn"`
# (worlds.py:815), il n'y a pas de portee « Round ». On prend `"Phase"`, la
# plus large des deux. La difference ne se verrait que si une amelioration
# etait jouee pendant la phase du VILAIN, ce qui n'arrive pas dans le jeu de
# base. Signale plutot que masque.


def GetAbilities() -> Sequence['Ability']:

    def inventor_setup(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return

        if not joueur.DiscardHandCards((1, 1), effect):
            return

        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            trait="TECH",
            card_type=Upgrade,
        )
        if face:
            joueur.GainCard(face, effect)

    def inventor_action(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        Worlds.UpdateNextCardPlayCost(
            joueur,
            -1,
            effect,
            finder=CardFinder(card_type=Upgrade),
            in_this="Phase",
        )

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            inventor_setup,
        ).SetName("Inventor"),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            inventor_action,
        ).LimitOncePerRound(),
    ]
