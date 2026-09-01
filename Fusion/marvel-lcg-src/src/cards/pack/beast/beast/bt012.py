from . import *

# Civilian Disguise — soutien signature. ITEM. Cout 1. RES [mental]
# (Enters play with 3 disguise counters.)
# Response: After defending an attack, remove 1 disguise counter -> draw 1 card.
#
# Cartes de reference :
#  - les compteurs a l'entree en jeu : 01008 Web-Shooter, `desc.Uses` au
#    format `"3,disguise"`. Base automatique lue nativement par le moteur :
#    aucun module ne pose les compteurs, et c'est `Uses` qui defausse la carte
#    quand le dernier part.
#  - « After defending an attack » : la fabrique `AfterUnitDefendAgainstAttack`
#    (do_attack.py:288), la meme que bt001a Thick Skinned du meme pack —
#    SANS son `take_no_damage`, puisque Civilian Disguise pioche quel que soit
#    le nombre de degats encaisses.
#  - la depense d'un compteur en cout : 23016 Command Team, meme couple
#    « Uses + retrait d'un compteur en cout ».
#
# ⚠ ARBITRAGE (utilisateur, 31/08/2026) : le texte imprime ne dit PAS ce que
# devient la carte a 0 compteur. Codee avec `Uses`, donc **elle se defausse**,
# comme toute carte a usages du jeu. Consigne au §6 du journal de portage,
# point 3 de la section B... voir point « bt012 » (§6, question 6 de la liste
# auteur).
#
# ⚠ Le compteur `disguise` a du etre AJOUTE a l'enum `COUNTER` de
# `card_face.py` : sans lui, `IsCounter('disguise')` refuse le nom et la carte
# tombe des la construction du deck (meme panne que 'style' pour kate_bishop).
# C'est un fichier moteur PARTAGE, la batterie complete est due (§4 du
# journal).
#
# ⚠ « remove 1 disguise counter » est ecrit AVANT la fleche : c'est le COUT.
# Sans compteur, pas de pioche — et de toute facon la carte n'est plus la.
#
# ⚠ « After DEFENDING an attack » : il faut avoir ete le defenseur declare.
# Encaisser une attaque sans se defendre ne declenche rien.

def GetAbilities() -> Sequence['Ability']:

    def civilian_disguise(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        initiator.DrawUp(1, effect)

    return [
        AbilityFactory.AfterUnitDefendAgainstAttack(
            AbilityType.Response,
            "You",
            civilian_disguise,
        # ⚠ La classe est `CostFunc.Counter`, PAS `RemoveCounter` (qui n'existe
        # pas) : meme appel que 23016 Command Team pour son compteur 'command'.
        ).SetCostFunc(CostFunc.Counter("This", 1, 'disguise')),
    ]
