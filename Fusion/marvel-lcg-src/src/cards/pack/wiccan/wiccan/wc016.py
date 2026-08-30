from . import *

# * Wiccan's Cloak — AMELIORATION signature, custom « CptScorp »
# Cout 3, [physical], classe Hero, trait ITEM.
# Response: After you play a [[SPELL]] event that counts the amount of boost
#   icons on an encounter card, exhaust Wiccan's Cloak and discard the top
#   card of the encounter deck -> resolve that event again.
#
# Aucune capacite « Play » declaree : `Upgrade.GetAbilities` en pose une
# d'office (`CanPlayThisUpgradeCard()`, upgrade.py:12-19), qui attache la
# carte a l'identite du joueur. C'est ce que fait deja ag008 (Agent 13's
# Pistol), amelioration signature de la meme forme. Le texte n'imprime aucun
# « Attach to... » : rien a cibler.
#
# Declencheur -> `AbilityFactory.AfterPlayerPlayedCard(AbilityType.Response,
# "You", <finder>, ...)` (game/ability/factory/play.py:275). « you play »
# borne au joueur qui controle la cape ("You"), jamais "AnyPlayer".
#
# « a [[SPELL]] event that counts the amount of boost icons on an encounter
# card » -> la liste `EVENEMENTS_QUI_COMPTENT_LES_BOOSTS` du
# `wiccan/__init__.py`, etablie carte par carte sur le texte imprime. Choix
# assume : un filtre par TRAIT (`CardFinder(trait="SPELL", card_type=Event)`)
# serait FAUX ici — wc013 Transmutation est un evenement SPELL du pack qui ne
# compte AUCUNE icone, et la cape la rejouerait a tort. La condition imprimee
# n'est pas « un evenement SPELL », c'est « un evenement SPELL QUI COMPTE des
# icones ». Le filtre porte donc sur les card_id, et le trait SPELL est
# verifie en plus (`f.HasTrait("SPELL")`), pour que la liste reste vraie meme
# si un exemplaire changeait de trait.
#
# Couts -> `CostFunc.Exhaust("This")` (modele ag008) ET une defausse du dessus
# du deck de rencontre. Aucune `CostFunc` du moteur ne defausse une carte de
# rencontre : on passe par `CostFunc.Custom(None, ...)` qui appelle
# `Worlds.DiscardEncounterTopCard(effect)` (worlds.py:577). Le cout a DEUX
# parties, les deux sont payees — piege « and remove » de PROCESSUS-CARTE.
# Le cout `Custom` rend False quand le deck de rencontre est vide : le cout ne
# peut alors pas etre paye, la Response ne part pas. C'est la lecture stricte
# du texte imprime (« exhaust ... AND discard the top card ... -> »).
#
# « resolve that event again » -> on re-resout l'EFFET DE JEU de l'evenement,
# `message.play_effect`, en lui repassant son message d'origine
# (`play_effect.bind_message`) et en sautant le cout :
# `play_effect.ResolveSelf(bind_message, effect, to_player=..., skip_cost=True)`.
# L'evenement est donc REJOUE SANS ETRE REPAYE, ce que le texte imprime veut
# (« resolve that event again », pas « play it again »).
#
# CORRECTIF (trouve par test_capacites.py, 30/08/2026) : la voie evidente
# etait `message.played_face.ResolveAbility(joueur, message.play_effect.
# ability.type, effect)` (card_face.py:793), la brique qu'emploie
# `ResolveEachWhenRevealedAbilityAdditionalTime` (ability_factory.py:482-499).
# Elle PLANTE ici : `ResolveAbility` passe par `ResolveToPlayer`, qui appelle
# `ResolveSelfInternal` SANS message, et cette fonction porte une liste
# blanche de declencheurs re-resolubles (effect_invoke.py:195-205) —
# WhenCardRevealed, WhenUnitBeDefeated, WhenCardBecomeBoost... mais PAS
# `WhenPlayerInTurn`, le declencheur de toute capacite « Play ». Resultat
# observe : `AssertionError` a la ligne 197 et zero degat supplementaire.
# Repasser le message d'origine remet la resolution sur le chemin normal
# (`isinstance(message, ability.when)` vrai, effect_invoke.py:189-192).
#
# CIBLES DE LA SECONDE RESOLUTION : elles sont RECHOISIES, pas recopiees. Les
# cibles legales sont rafraichies (`play_effect.checker.UpdateLegalTargets()`,
# exactement ce que fait `ResolveAbility` avant de resoudre), puis le joueur
# choisit dans la plage imprimee de la carte. Un Magic Bolt rejoue peut donc
# viser un autre ennemi — et surtout ne se perd pas sur un ennemi que la
# premiere salve vient de vaincre.
#
# La re-resolution ne redeclenche PAS la cape : `ResolveAbility` resout un
# effet, il n'envoie aucun `AfterPlayerPlayedCard`. Et la cape est de toute
# facon inclinee par son propre cout.

def GetAbilities() -> Sequence['Ability']:

    def est_un_sort_qui_compte(face: 'CardFace') -> bool:
        card_id = getattr(face.paper, "card_id", None)
        return card_id in EVENEMENTS_QUI_COMPTENT_LES_BOOSTS and face.HasTrait("SPELL")

    def defausser_le_dessus(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(targets)
        return Worlds.DiscardEncounterTopCard(effect) is not None

    def wiccans_cloak(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        joueur = message.GetToPlayer()
        if joueur is None:
            return

        play_effect = message.play_effect
        play_effect.checker.UpdateLegalTargets()
        mini, maxi = play_effect.context.target_range
        legales = list(play_effect.context.all_legal_targets)

        if mini > 0 and legales:
            play_effect.context.targets_internal = joueur.AskChooseFaces(
                legales,
                (mini, maxi),
                effect,
                prompt="Resolve that event again",
                not_move=True,
            )
        else:
            play_effect.context.targets_internal = []

        play_effect.ResolveSelf(
            play_effect.bind_message,
            effect,
            to_player=joueur,
            skip_cost=True,
        )

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFinder(card_type=Event, check_face_fn=est_un_sort_qui_compte),
            wiccans_cloak,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Custom(None, defausser_le_dessus)),
    ]
