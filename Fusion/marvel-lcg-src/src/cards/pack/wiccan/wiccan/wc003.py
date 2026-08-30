from . import *

# Impenetrable Barrier (1/2) — custom « CptScorp »
# Cout 2, [energy], classe Hero, traits SPELL / SUPERPOWER.
# Hero Action: Give your hero a Tough status card. Give up to X friendly
#   characters a Tough status card, where X is equal to the amount of boost
#   icons on the top card of the encounter deck.
#
# Exemplaire physique 1 de 2 (wc003, wc004 : meme texte, deux card_id
# distincts — modele ok004/ok005, il021/il022). Commentaire complet ici,
# pointeur bref sur wc004.
#
# Statut Tough -> `Faces.GiveStatus(faces, "Tough", effect)`
# (game/operate/faces.py:169), la brique standard du depot.
#
# « your hero » -> `initiator.GetIdentity()`, sans condition ni ciblage : la
# premiere phrase est INCONDITIONNELLE et ne consomme aucun des X. C'est le
# piege `your` de PROCESSUS-CARTE : la portee est le heros DU JOUEUR QUI JOUE
# la carte, pas « un heros ».
#
# « up to X friendly characters » -> `initiator.AskChooseFaces(candidats,
# (0, X), effect, not_move=True)`. La plage commence a ZERO (« up to »), donc
# le pilote de test choisit 0 par defaut : le cas dedie emploie
# `accepter_choix: True` pour exercer la branche. Modele du ciblage :
# ag001b/Hex Bolt, qui imbriquent le choix DANS le handler plutot que de
# poser un `.SetTarget` au niveau de l'abilite — indispensable ici, puisque
# le nombre de cibles depend d'une valeur calculee au moment de la resolution.
#
# « friendly characters » -> `Worlds.GetOnFieldFriendlyCharacters`
# (worlds.py:289) = les identites ET les allies de TOUS les joueurs. C'est
# bien la portee imprimee : le texte ne dit ni « you control » ni « friendly
# characters you control » (contrairement a la capacite Boost de wc021, qui
# le precise, elle).
# Filtre `CardFinder(canbe_status="Tough")` (checker.py:244) : une carte deja
# Tough ne peut pas recevoir un second exemplaire du meme statut, la proposer
# poserait un choix qui ne fait rien.
#
# X = 0 (aucune icone, ou obligation wc018 active, ou deck vide) -> aucune
# question posee, le heros garde quand meme son Tough : lecture fidele du
# texte imprime.

def GetAbilities() -> Sequence['Ability']:

    def impenetrable_barrier(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        identite = initiator.GetIdentity()
        if identite is not None:
            Faces.GiveStatus([identite], "Tough", effect)

        icones = IconesBoostDuDessus(effect, initiator)
        if icones <= 0:
            return

        candidats = Worlds.GetOnFieldFriendlyCharacters(
            effect,
            CardFinder(canbe_status="Tough"),
        )
        if not candidats:
            return

        choisies = initiator.AskChooseFaces(
            candidats,
            (0, icones),
            effect,
            prompt="Give a Tough status card",
            not_move=True,
        )
        if choisies:
            Faces.GiveStatus(choisies, "Tough", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            impenetrable_barrier,
        ).SetPlay(),
    ]
