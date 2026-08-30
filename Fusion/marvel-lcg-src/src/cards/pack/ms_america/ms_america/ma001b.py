from . import *

# * America Chavez — FACE ALTER-EGO, custom « jakxin »
# STARLING. PV 14 / REC 5 / main 6.
#
# You may include upgrade cards that modify your basic powers from any aspect
#   in your deck.
# Thinking With Portals — Action: Discard a card from your hand → search your
#   discard pile for a card and shuffle it into your deck.
#   (Limit once per round.)
#
# PV/REC/main sont lus NATIVEMENT depuis `desc`.
#
# ---------------------------------------------------------------------------
# LA PREMIERE PHRASE N'EST PAS UNE CAPACITE DE JEU
#
# « You may include upgrade cards that modify your basic powers from any
# aspect in your deck » est une REGLE DE CONSTRUCTION DE DECK. Le moteur ne
# valide JAMAIS un deck au chargement (GUIDE §5.2) : elle vit dans le
# deck-builder, `public/js/deckbuilder/app.js`, fonction
# `exemptDeLaLimiteAspect` (GUIDE §14.1), troisieme cas apres Madame Web
# (Arachnophilia) et Patriot (Leader). RIEN a coder ici — coder une capacite
# fantome serait une faute.
#
# ---------------------------------------------------------------------------
# THINKING WITH PORTALS
#
# Carte de reference : `sd001b` Thomas Shepherd / Accelerated Perception
# (pack speed) — meme fabrique `WhenInYourPlayTurn(AbilityType.Action, ...)`
# sur une face ALTER-EGO, meme `.LimitOncePerRound()`, meme couple
# `Search.PlayerCard(include_discard_pile=True)` + `Faces.ShuffleAllTo(...,
# player.player_deck, ...)`. Modeles d'origine : `ok011` Upanga et `60014`
# Karen Page.
#
# « Action: » NU sur une face alter-ego -> `AbilityType.Action`, comme
# `sd001b`, `wc001b`, `ss001b`, `10001b` et `01029b`. `AlterEgoAction` est
# reserve aux cartes JOUEUR qui doivent declarer ce mode.
#
# LA FLECHE EST UN COUT : « Discard a card from your hand → search... ». Le
# cout est porte par la capacite elle-meme
# (`CostFunc.Discard("YourHandCards")`, idiome de `01015`, `03001a`,
# `45014`), donc le moteur ne propose PAS l'action quand la main est vide
# (`CostFunc.Base.HasTargets`, cost_func.py:49). C'est la seule construction
# qui rend « cout impayable = rien ne se passe » sans le reecrire a la main.
#
# « search your discard pile for A CARD » : aucun filtre de type, contrairement
# a `sd001b` qui dit « an event ». On ne recopie pas une carte sur l'autre
# (mot-piege `that <nom>` du PROCESSUS-CARTE §5).
#
# ECART DOCUMENTE : le cout etant paye AVANT le corps (`Effect
# .ProcessSelfCost`, effect.py:135), la carte defaussee pour payer est deja
# dans la pile de defausse quand la recherche s'ouvre — elle peut donc etre
# celle qu'on remonte. C'est la lecture litterale du texte, et c'est ce qui
# fait de cette action un outil de FILTRAGE (on echange une carte de la main
# contre une carte de la defausse). Rien a corriger.


def GetAbilities() -> Sequence['Ability']:

    def thinking_with_portals(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        player = effect.GetInitiator()
        if player is None:
            return

        face = Search.PlayerCard(
            effect,
            player,
            include_player_deck=False,
            include_discard_pile=True,
        )
        if face:
            Faces.ShuffleAllTo([face], player.player_deck, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            thinking_with_portals,
        ).SetName("Thinking With Portals")
        .SetCostFunc(CostFunc.Discard("YourHandCards"))
        .LimitOncePerRound(),
    ]
