from . import *

# New Vessel — manigance annexe nemesis de Wiccan (1/5), RECTO
# 4 menaces au depart, 0 d'acceleration, 8 menaces pour l'accomplir.
# Only the Billy Kaplan player can remove threat from this scheme.
# When Defeated: Remove 2 threat from the main scheme. Then, set aside New
#   Vessel and Moridun.
# When Completed: Set aside Moridun and flip this card. (8 threat.)
#
# ARBITRAGE TRANCHE PAR L'UTILISATEUR le 30/08/2026 sur les TROIS valeurs
# imprimees : 4 = menace de DEPART, 0 = acceleration, 8 = seuil qui
# ACCOMPLIT la manigance. Seul `StartingThreat: "4"` figure dans le `desc`.
#
# ECART ASSUME : le moteur ne lit `TargetThreat` et `EscalationThreat` que
# sur les complots PRINCIPAUX (`game/card/face/card_type/scheme_main.py`).
# Le seuil de 8 est donc CABLE A LA MAIN ci-dessous, dans la constante
# `MENACE_CIBLE`. Precedent exact du depot, copie ici : The Grim Hunt
# (`madame_web/the_grim_hunt_nemesis/mw018.py`), qui cable de la meme facon
# ses deux valeurs de manigance annexe, avec le meme commentaire.
# L'acceleration de 0 ne demande AUCUN code : c'est l'absence de la valeur.
# `MENACE_CIBLE` est un entier NU (8), pas « 8* » : la valeur imprimee ne
# porte pas l'icone par joueur, contrairement au « 5* » de mw018 — et la
# menace de depart imprimee, 4, ne la porte pas non plus.
#
# « Only the Billy Kaplan player can remove threat from this scheme » ->
# `AbilityFactory.PlayersCannotRemoveThreatFrom(PlayerFinder(non_name=
# "Billy Kaplan"), "This")`. Modele EXACT : Sibling Rivalry (`gam/
# gamora_nemesis/18025.py`), meme phrase imprimee, meme fabrique, meme
# `PlayerFinder(non_name=...)`. `Player.IsName` compare avec
# `check_all_face=True` (player.py:251-262) : le joueur de Wiccan est reconnu
# qu'il soit en forme heros (« Wiccan ») ou civile (« Billy Kaplan »).
#
# « When Defeated » (la derniere menace est retiree) ->
# `AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", ...)`,
# la fabrique standard (modeles jj015, 27068, 40194a).
# « Remove 2 threat from the main scheme » -> `Worlds.GetMainSchemes(effect)`.
# « Then, set aside New Vessel AND Moridun » -> `Faces.SetAside([...], effect)`
# (faces.py:158) sur LES DEUX cartes, piege « and remove » de PROCESSUS-CARTE.
# C'est bien SetAside et non une defausse : wc020 Moridun, quand il revient,
# revele « your SET-ASIDE New Vessel side scheme ».
#
# « When Completed » -> le moteur n'a pas de declencheur « manigance annexe
# accomplie ». On surveille donc chaque pose de menace sur CETTE carte
# (`AbilityFactory.AfterSchemePlaceThreat(AbilityType.ForcedResponse, "This",
# ..., has_at_least_threat=MENACE_CIBLE)`, scheme.py:89-111 — le filtre
# `has_at_least_threat` teste exactement `this.threat >= seuil`). C'est plus
# fin que le sondage de fin de phase de mw018 : la menace de New Vessel est
# posee par wc020 Moridun a chaque fois que Wiccan frappe ou contre, donc en
# pleine phase des joueurs.
# « Set aside Moridun and flip this card » -> `Faces.SetAside(moridun,
# effect)` puis `this.card.Flip(effect)` + `Reveal` de la face obtenue.
# Modele EXACT du retournement d'une manigance en ENVIRONNEMENT : Practice
# Maneuvers (`next_evol/.../40194a.py`), meme triplet `card.Flip` /
# `card.face` / `CastTo(Environment).Reveal(...)`.
#
# PIEGE DAZZLER : ce retournement n'existe QUE si la carte a ete generee avec
# SES DEUX FACES. `CardFactory.GenerateCard` cree une face par identifiant
# separe par une virgule (game/card/factory.py:63-67) ; avec le seul
# « wc019a », `card.back_faces` est vide et `CardFace.FlipTo` se contente de
# coucher la carte face cachee (card_face.py:987-989) — elle QUITTE le jeu au
# lieu de devenir The Demiurge. D'ou la forme « wc019a,wc019b » dans
# `deck/starter/wiccan.json` et `data/nemesis/wiccan_nemesis.json`.

MENACE_CIBLE = 8


def GetAbilities() -> Sequence['Ability']:

    def moridun_en_jeu(effect: 'Effect') -> List['CardFace']:
        return Worlds.FindCardsOnField(effect, name=NOM_MORIDUN)

    def quand_vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(message)

        principaux = Worlds.GetMainSchemes(effect)
        if principaux:
            this.RemoveThreatFromSchemes(principaux, 2, effect)

        Faces.SetAside([this] + moridun_en_jeu(effect), effect)

    def quand_accomplie(effect: 'Effect', message: 'Message.AfterSchemePlaceThreat') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(message)

        moridun = moridun_en_jeu(effect)
        if moridun:
            Faces.SetAside(moridun, effect)

        this.card.Flip(effect)
        face = this.card.face
        face.CastTo(Environment).Reveal(Worlds.GetFirstPlayer(effect), effect)

    return [
        AbilityFactory.PlayersCannotRemoveThreatFrom(
            PlayerFinder(non_name=NOM_BILLY),
            "This",
        ),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            quand_vaincue,
        ),
        AbilityFactory.AfterSchemePlaceThreat(
            AbilityType.ForcedResponse,
            "This",
            quand_accomplie,
            has_at_least_threat=MENACE_CIBLE,
        ),
    ]
