from . import *

# * Yondu Udonta — face ALTER-EGO. PV 10, REC 3, main 6. OUTLAW.
# Crew Cut — Action: Summon the Tahlei upgrade and add it to your hand.
#   (Limit once per round.)
# Whistlin' — Action: Exhaust Yondu Udonta -> summon the Yaka Arrow upgrade
#   and add it to your hand.
#
# Cartes de reference :
#  - **`Convoquer`** (helper du set) pour le mot-cle MAISON `summon`, arbitre
#    par l'utilisateur le 03/09/2026 : fouiller le DECK **ET** la DEFAUSSE.
#    Fiche `docs/reference/mots-cles/summon.md`. Montage : `Search.PlayerCard(
#    include_player_deck=True, include_discard_pile=True, name=...)` +
#    `GainCard`, modeles `an001b` * Aldrif Odinsdottir, `ok001b` * Okoye,
#    `ls005` To Arms!.
#  - `32030b` * Kitty Pride pour `.LimitOncePerRound()`.
#  - `31002a` * Peni Parker / `as010` pour `CostFunc.Exhaust`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « summon ... **and add it to your hand** » : en MAIN, PAS en jeu. La
#    carte devra encore etre jouee et payee. C'est la difference exacte avec
#    `yd015` Sav'rkk, qui ecrit « summon ... and reveal him » et pose donc
#    directement sur le terrain. Lire le verbe qui suit, jamais le seul mot
#    `summon`.
#  - DEUX Actions, DEUX limites DIFFERENTES : Crew Cut est « once per round »
#    et n'a AUCUN cout ; Whistlin' n'a AUCUNE limite mais coute l'inclinaison
#    de l'alter-ego, donc une fois par redressement. Ne pas uniformiser.
#  - « Exhaust Yondu Udonta **->** » : la fleche en fait un COUT.
#    `CostFunc.Exhaust("YourIdentity")`, et l'alter-ego deja incline ne peut
#    plus convoquer.
#  - « **Action** » nue sur les deux : imprimees sur la face civile, elles
#    n'existent qu'en forme alter-ego. Rien a conditionner en plus.
#  - ⚠ Si la carte cherchee est DEJA en jeu, `Search.PlayerCard` ne la trouve
#    pas (elle n'est ni au deck ni a la defausse) et l'Action ne fait rien.
#    C'est le comportement voulu : convoquer une fleche deja plantee la
#    dupliquerait.


def GetAbilities() -> Sequence['Ability']:

    def crew_cut(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        Convoquer(effect, NOM_TAHLEI)

    def whistlin(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        Convoquer(effect, NOM_FLECHE)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            crew_cut,
        ).SetName("Crew Cut")
        .LimitOncePerRound(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            whistlin,
        ).SetName("Whistlin'")
        .SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
