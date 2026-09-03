from . import *

# * Kingpin — sbire NEMESIS d'Armored Spidey. CRIMINAL. ELITE.
# PV 6, MAN 1*, ATQ 2, Boost 2. `desc.Nemesis` = « Peter Parker ».
# [star] Forced Response: After Kingpin schemes, discard the top card of the
#   encounter deck, place 1 threat on "The Kingpin of Crime" side-scheme for
#   each boost icon discarded this way.
#
# Cartes de reference :
#  - `AfterUnitSchemeEnd(ForcedResponse, "This", op)` (do_scheme.py:70) pour
#    « After Kingpin schemes ». ⚠ PAS `AfterEnemySchemeAndPlaceThreat`, qui
#    ajoute la condition `placed_threat > 0` : le texte ne l'impose pas, et
#    une manigance bloquee a 0 menace declencherait quand meme.
#  - **`15004`** / `ho014` : `Worlds.DiscardEncounterTopCard(effect)` puis
#    `FacesCounter.CountTotalBoostIcons([face])`.
#  - `50134` / `ho015` pour `this.PlaceThreatOnSchemes(cibles, n, effect)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « place 1 threat on **"The Kingpin of Crime" side-scheme** » : un complot
#    ANNEXE NOMME, `as024`. S'il n'est pas en jeu, rien ne se passe — la
#    menace ne se reporte PAS sur le complot principal.
#  - « for **each boost icon** discarded this way » : les icones de la carte
#    rencontre defaussee, pas celles de Kingpin. Une carte a 0 icone ne pose
#    aucune menace.
#  - « After Kingpin **schemes** » : la manigance, pas l'attaque ni
#    l'engagement (piege `attacks` vs `attacks or engages`).
#  - « [star] » sans « In expert mode » : capacite TOUJOURS active, convention
#    moteur (cf. 04125).
#  - « **ELITE** » : trait imprime, aucune consequence a scripter, mais il
#    interdit les cartes qui ne visent que les sbires non-Elite.
#  - « MAN 1* » : valeur par joueur, convertie nativement par le moteur.


def GetAbilities() -> Sequence['Ability']:

    def kingpin(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        defaussee = Worlds.DiscardEncounterTopCard(effect)
        if defaussee is None:
            return

        icones = FacesCounter.CountTotalBoostIcons([defaussee])
        if icones <= 0:
            return

        complot = Worlds.FindCardOnField(
            effect,
            name="“The Kingpin of Crime”",
            card_type=SchemeSide2,
        )
        if complot is None:
            return
        this.PlaceThreatOnSchemes([complot], icones, effect)

    return [
        AbilityFactory.AfterUnitSchemeEnd(
            AbilityType.ForcedResponse,
            "This",
            kingpin,
        ),
    ]
