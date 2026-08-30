from . import *

# * Hawkingbird — ALLIE signature, custom « CptScorp »
# Cout 3, PV 1, ATQ 0, CTR 1* (degats consecutifs), ressource [physical],
# trait YOUNG AVENGER, sous-titre « Kate Bishop ».
#
# Allies you control get +1 hit point.
# Response: After Hawkingbird enters play, you may search your deck and
#   discard pile for an upgrade that can be attached to allies and add it to
#   your hand.
#
# ⚠ Le sous-titre « Kate Bishop » est aussi celui de l'officielle `04011`
# Hawkeye. Les NOMS different (« Hawkingbird » / « Hawkeye ») : aucune
# collision moteur. Corollaire : on ne cherche JAMAIS une carte par son
# sous-titre.
#
# ---------------------------------------------------------------------------
# CAPACITE 1 : « Allies you control get +1 hit point »
#
# Carte de reference : `50075` Destroy Evidence, meme fabrique
# `GiveKeywordToInPlayWhenApplyThis`, qui donne un mot-cle a TOUTES les
# cartes en jeu repondant a un filtre — a la difference de
# `GiveKeywordToAttached`, qui ne sert qu'a une carte ATTACHEE (une
# amelioration sur son porteur).
#
# `control_by="You"` rend « you control » : le bonus ne touche pas les allies
# du voisin (mot-piege `you control` du PROCESSUS-CARTE §5).
#
# ⚠ ELLE-MEME COMPRISE. Le texte imprime « Allies you control », PAS « OTHER
# allies you control » : le defaut de la fabrique (`not_include_this=False`)
# est donc le bon. Ce n'est pas un detail : Hawkingbird a 1 PV imprime, elle
# mourrait au premier degat sans son propre bonus, et l'exemplaire suivant
# n'aurait plus rien a proteger. `50075` passe au contraire
# `not_include_this=True`, parce que son texte dit « each OTHER encounter
# card » : c'est le contre-exemple qui prouve que le parametre est bien lu.
#
# ---------------------------------------------------------------------------
# CAPACITE 2 : la Response d'entree en jeu
#
# Carte de reference : `29024` Vivian (pack ironheart), meme fabrique
# `AfterCardEnterPlay(AbilityType.<Response>, "This", ...)` pour « After X
# enters play ». Le texte imprime « Response: » nu (pas « Hero Response »),
# d'ou `AbilityType.Response`.
#
# « you MAY search » -> `may=True` sur `Search.PlayerCard`, qui elargit la
# plage de selection a (0, 1) (search_internal.py:53-58). Sans lui la
# recherche serait FORCEE.
#
# ⚠ LE FILTRE N'EST PAS « UNE AMELIORATION »
#
# Le texte dit « an upgrade THAT CAN BE ATTACHED TO ALLIES ». Le moteur sait
# le rendre exactement : `CardFinder(card_type=Upgrade, canbe_attach_to=<un
# allie>)` appelle `Upgrade.CanAttachTo(face)` (card_type/upgrade.py:83), qui
# relit le selecteur de la capacite « Play » de l'amelioration examinee. Une
# amelioration qui se pose sur l'identite (Patriot's Shield, par exemple) est
# donc ECARTEE, ce qu'un simple `card_type=Upgrade` n'aurait pas fait.
#
# L'allie temoin passe au filtre est HAWKINGBIRD ELLE-MEME : elle vient
# d'entrer en jeu, elle est donc toujours disponible, meme si c'est le seul
# allie du joueur. Consequence voulue de `Asset2.CanAttachTo`
# (base/asset.py:69-73) : une amelioration `MaxPerUnit 1` deja posee SUR
# Hawkingbird ne serait pas proposee une seconde fois pour elle — c'est la
# regle du jeu, pas un ecart.
#
# Cartes du deck de depart qui passent le filtre : pt013 Revenge, pt015
# Throwing Stars, pt016 Working Together et `01074` Inspired.
#
# « search your deck AND DISCARD PILE » -> les deux zones. Le remelange du
# deck est fait par la recherche elle-meme (search_internal.py:61-66).
#
# Les valeurs 3 / 1 PV / ATQ 0 / CTR 1* sont lues nativement dans `desc` :
# le `*` du CTR est le marqueur de degats consecutifs du moteur, aucun module
# ne le recode.


def GetAbilities() -> Sequence['Ability']:

    def chercher_une_amelioration(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)

        joueur = this.GetControlByPlayer()
        if joueur is None:
            return

        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            include_discard_pile=True,
            may=True,
            finder=AmeliorationAttachableA(this),
        )
        if face:
            joueur.GainCard(face, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Ally,
            control_by="You",
            health=1,
        ),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            chercher_une_amelioration,
        ),
    ]
