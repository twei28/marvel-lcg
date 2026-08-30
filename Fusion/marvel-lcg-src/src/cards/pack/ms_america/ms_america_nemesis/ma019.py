from . import *

# Search for the Cure — MANIGANCE ANNEXE nemesis, custom « jakxin »
# Carte PAYSAGE. `Boost 3`, `Hazard 1`. AUCUNE menace de depart imprimee dans
# `desc` : elle est CALCULEE (voir plus bas).
#
# When Revealed: Each player searches their discard pile for an ally and
#   attaches it to this card. This card's starting threat is equal to the
#   combined resource cost of the attached cards. For each player that did
#   not attach an ally to this card, this card gets an additional
#   2[per_hero] starting threat.
#
# ---------------------------------------------------------------------------
# ⚠ L'ICONE EST `Hazard`, VERIFIEE PAR DECOUPE D'IMAGE — NE PAS RE-LITIGER
#
# Contre trois temoins : `ag011` (qui declare Crisis ET Acceleration),
# `hd022` (Hazard, carte-plus NUE) et `hd026` (Acceleration, carte-plus
# SOULIGNEE). C'est la version NUE : `Hazard`, et rien d'autre. A vue on
# aurait dit Acceleration. Point clos.
#
# `Hazard` est lu NATIVEMENT dans `desc` (`HasHazard`,
# has_hazard.py) : aucun module a ecrire pour lui. Fiche :
# docs/reference/mots-cles/hazard.md. Idem `Boost 3`.
#
# ---------------------------------------------------------------------------
# TYPE : `SideScheme` EN JSON = CLASSE `EncounterSideScheme` DANS LE SCRIPT
# (piege connu, GUIDE §10).
#
# ---------------------------------------------------------------------------
# ECART ASSUME — LA MENACE DE DEPART EST « X », CABLEE A LA MAIN
#
# `desc.StartingThreat` ne sait porter qu'un nombre (eventuellement etoile) :
# il ne peut pas dire « la somme du cout des cartes attachees ». La menace de
# depart est donc posee par le When Revealed lui-meme, sur une manigance qui
# entre en jeu a 0. Precedents EXACTS du depot, avec le meme commentaire :
# `mw018` The Grim Hunt (menace cible et escalade cablees) et `wc019a` New
# Vessel (seuil d'accomplissement cable). Ce n'est pas une invention.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « EACH PLAYER searches THEIR discard pile » -> une boucle sur
#   `Worlds.GetPlayers(effect)`, chacun fouillant SA pile. C'est le seul
#   montage possible : `Search.PlayerCard` n'a pas d'option « n'importe quel
#   joueur », son argument `player` designe a la fois le proprietaire de la
#   pile ET celui qui choisit (search_internal.py:77). Modele : `59022`
#   (pack hercules) et `lj027`, tous deux « each player searches... ».
#   `may=True` : « searches ... for an ally » n'oblige pas a en trouver un,
#   et la suite du texte prevoit explicitement le cas « did not attach ».
# « ATTACHES IT TO THIS CARD » -> `this.PlaceCardHere(face, True, effect)`,
#   FACE VISIBLE (le texte ne dit pas « facedown », contrairement a ma004) —
#   et il FAUT qu'elle soit visible, puisqu'on lit son cout juste apres.
#   Modele `04003` Hawkeye's Quiver, meme `PlaceCardHere(face, True, ...)`.
# « the COMBINED RESOURCE COST of the attached cards » ->
#   `FacesCounter.GetPrintedCost(faces)` (faces_counter.py:109-114), qui
#   somme les `printed_cost`. Modeles `42025`, `50006`, `50119`.
# « For each player that DID NOT attach an ally » -> on compte les joueurs
#   qui n'ont rien pose, pas les allies manquants : un joueur sans allie dans
#   sa defausse et un joueur qui refuse comptent pareil.
# « an additional 2[per_hero] » -> `Worlds.ConvertPerPlayerIconToInt("2*",
#   effect)` (worlds.py:666-670), soit 2 x le nombre de joueurs, PAR joueur
#   sans allie. En solo : 2 x 1 = 2. A quatre joueurs, si personne ne pose
#   d'allie : 4 x (2 x 4) = 32. C'est ce que le texte dit.


MENACE_PAR_JOUEUR_SANS_ALLIE = "2*"


def GetAbilities() -> Sequence['Ability']:

    def search_for_the_cure(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(message)

        attaches: List['CardFace'] = []
        sans_allie = 0

        for joueur in Worlds.GetPlayers(effect):
            face = Search.PlayerCard(
                effect,
                joueur,
                include_player_deck=False,
                include_discard_pile=True,
                may=True,
                card_type=Ally,
            )
            if face:
                this.PlaceCardHere(face, True, effect)
                attaches.append(face)
            else:
                sans_allie += 1

        menace = FacesCounter.GetPrintedCost(attaches)
        if sans_allie:
            menace += sans_allie * Worlds.ConvertPerPlayerIconToInt(
                MENACE_PAR_JOUEUR_SANS_ALLIE, effect)

        if menace > 0:
            this.PlaceThreatOnSchemes([this], menace, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            search_for_the_cure,
        ),
    ]
