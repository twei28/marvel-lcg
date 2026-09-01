from . import *

# * Dark Beast — sbire nemesis (4/5). ELITE. MUTANT. 6 PV, MNG 4, ATQ 1.
# Stalwart.
# When Revealed: All allies are confused.
# (Beast's nemesis minion.)
#
# Cartes de reference :
#  - « When Revealed » d'une carte du set nemesis : an011 Hel's Retribution /
#    bt021 du meme pack, `WhenThisRevealed(None, op)` (recette moteur §1).
#  - donner un statut a plusieurs personnages d'un coup : 05015 Tackle /
#    01083 Mockingbird, `Faces.GiveStatus(cibles, "Confused", effect)`
#    (recette moteur §2), avec un filtre `canbe_confused=True` sur les cibles.
#
# ⚠ « Stalwart » est une base automatique lue dans `desc.Stalwart` (fiche
# docs/reference/mots-cles/stalwart.md) : AUCUN module a ecrire pour lui. Ce
# script ne porte que le « When Revealed ».
#
# ⚠ ARBITRAGE (utilisateur, 31/08/2026) : « **All** allies » n'est pas
# qualifie. Codee a la lettre — TOUS les allies en jeu, de tous les joueurs —
# alors que les sets nemesis officiels ne visent d'habitude que leur propre
# joueur. En solo la difference est nulle. Consigne au §6 du journal de
# portage, point 12, pour l'auteur.
#
# ⚠ `canbe_confused=True` : un allie deja desoriente, ou protege par Stalwart,
# n'est pas une cible legale. Sans ce filtre, le moteur empilerait des statuts
# sur des personnages qui ne peuvent pas les recevoir (recette moteur §2).

def GetAbilities() -> Sequence['Ability']:

    def dark_beast(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this, message)

        allies = Worlds.FindCardsOnField(effect, card_type=Ally, canbe_confused=True)
        if allies:
            Faces.GiveStatus(allies, "Confused", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            dark_beast,
        ),
    ]
