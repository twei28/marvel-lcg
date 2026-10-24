from . import *

# The Life Stealer — MANIGANCE ANNEXE NEMESIS (4 par heros, Victory 1). (card_id ch020, 2/5)
# Victory 1.
# Forced Response: After resolving step one of the villain phase, place 1 mystic counter here. After a third mystic counter is
#   placed here, deal 3 indirect damage to each hero and ally in play and remove The Life Stealer from the game.
#
# Cartes de reference :
#  - `01107` Breakin' & Takin' : menace PAR HERO posee a la revelation, `this.PlaceThreatOnSchemes([this], "1*", effect)`
#    (la valeur « N* » = N par joueur ; ici « 4* »).
#  - `pu033` / `39026b` : `AbilityFactory.AfterResolveVillainPhaseStep(type, 1, op)` (etape 1 de la phase du vilain).
#  - `45113` / `27071` : `this.DealDamage(Worlds.GetOnFieldFriendlyCharacters(effect), N, effect)`.
#  - `Victory` : base automatique (`desc.Victory`).
#
# ⚠ Mots-pieges :
#  - « 4 [per hero] » : menace de depart 4 PAR HERO (le scan imprime 4 + icone joueur) : posee par un « When Revealed » de la
#    carte (`desc.StartingThreat = 0`), comme les manigances annexes officielles a menace par joueur.
#  - « After a THIRD mystic counter is placed » : au 3e, pas au 1er ni au 2e ; la carte part ENSUITE.
#  - DECISION UTILISATEUR (24/10/2026) : « deal 3 indirect damage to each hero and ally » = 3 degats DIRECTS a CHAQUE heros et
#    allie en jeu (aucune repartition).
#  - « remove The Life Stealer FROM THE GAME » : jamais defausse, jamais victoire (Victory 1 ne se paie que si on la vainc).
#  - « step ONE of the villain phase » : l'etape 1 (placement de la menace de la manigance principale).


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(message)

        this.PlaceThreatOnSchemes([this], "4*", effect)

    def compteur(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(message)

        Faces.PlaceCountersOn([this], 1, 'mystic', effect)
        if this.GetCounters('mystic') >= 3:
            this.DealDamage(list(Worlds.GetOnFieldFriendlyCharacters(effect)), 3, effect)
            Faces.RemoveAllFromGame([this], effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelee,
        ),
        AbilityFactory.AfterResolveVillainPhaseStep(
            AbilityType.ForcedResponse,
            1,
            compteur,
        ),
    ]
