from . import *

# * Mt'nox — SBIRE (Super-Skrull). ELITE. MYSTIC. SKRULL. SCH 2, ATK 2★, 4 PV, 1 icone Y.
# ★ Forced Response: After Mt'nox makes an undefended attack against you,
#   discard the top card of your deck. If that card's printed resource has:
#   [physical] - Give the villain a tough status card.
#   [energy]   - You are stunned.
#   [mental]   - You are confused.
#   [wild]     - All of the above.
#
# Cartes de reference :
#  - **`04145`** Hydra Flame-Soldier : « After <minion> makes an undefended attack
#    against you » = `AfterUnitAttackUnit(ForcedResponse, "This", "You", op,
#    is_undefended_attack=True)`, le joueur par `message.GetToPlayer()`.
#  - **`fne/60084`** Energy Overload : lire la ressource IMPRIMEE d'une carte
#    (`ClassCard` + `printed_resource.HasColorPrinted`) ; `sk110` : « you are
#    stunned » = `identite.GainStatus("Stunned", effect)`.
#  - **`sk114`** (Army of Skrulls) : `player.DiscardDeckTopCards(n, effect)`.
#
# ⚠ Mots-pieges : « UNDEFENDED » (pas de defenseur) ; « against YOU » ; « the top
# card of YOUR deck » ; ressource IMPRIMEE (R = physique, Y = energie, B = mental,
# G = wild ; icones verifiees contre des cartes du pack : sk049 R, sk044 Y, sk043 B, sk045 G, pas a vue) ;
# la carte peut porter PLUSIEURS icones : chaque ligne s'applique si SON icone est
# imprimee ; « wild » = TOUTES les lignes ; « the VILLAIN a tough » (le mechant
# courant) ; carte sans ressource (evenement 0, deck vide) : rien. Le ★ de la
# ligne est un marqueur (Reponse obligatoire ordinaire).


def GetAbilities() -> Sequence['Ability']:

    def deviner(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        joueur = message.GetToPlayer()
        defaussees = joueur.DiscardDeckTopCards(1, effect)
        if not defaussees:
            return
        carte = defaussees[0]
        if not ClassCard.IsType(carte):
            return
        ressource = carte.printed_resource
        toutes = ressource.HasColorPrinted("G")
        if toutes or ressource.HasColorPrinted("R"):
            mechant = Worlds.FindVillain(effect)
            if mechant is not None:
                Faces.GiveStatus([mechant], "Tough", effect)
        if toutes or ressource.HasColorPrinted("Y"):
            joueur.GetIdentity().GainStatus("Stunned", effect)
        if toutes or ressource.HasColorPrinted("B"):
            joueur.GetIdentity().GainStatus("Confused", effect)

    return [
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.ForcedResponse,
            "This",
            "You",
            deviner,
            is_undefended_attack=True,
        ),
    ]
