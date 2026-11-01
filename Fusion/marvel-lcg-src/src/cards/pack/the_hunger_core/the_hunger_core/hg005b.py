from . import *

# The Innards — MANIGANCE PRINCIPALE, stade 2, face B. Starting threat 1[per_hero]. Escalade +1[per_hero] (★).
# Seuil 11[per_hero].
# When Revealed: Put "Inside Galactus" and 2 Metazombies into play (max. 3 in play).
# If this scheme is completed, the players lose.
#
# Cartes de reference :
#  - « When Revealed: Put ... into play » : `SetupCards.PutIntoPlay` (generique, pas reserve au Setup —
#    modele ap005a) pour Inside Galactus ; `commun.MettreUnMetazombieEnJeu` x2 pour les Metazombies, qui
#    applique DEJA le « max. 3 in play » (commun.MAX_METAZOMBIES_EN_JEU).
#  - « If this stage is completed, the players lose » : meme capacite que hg004b (`PerdQuandAccompli`),
#    dupliquee ici (texte identique imprime sur CE stade).
#
# ⚠ hg005b est la DERNIERE carte de `main_schemes_deck` (scenario.json, champ `schemes`) : le moteur a deja
# un repli generique pour « la derniere etape du complot principal est accomplie »
# (`World.AdvanceMainScheme`, branche `CountMainSchemesOfSameArea == 1` -> `SetGameOverByRule`), qui fait
# perdre TOUT AUSSI SUREMENT sans cette capacite. Preuve par substitution (03/09/2026->27/10/2026, mesuree) :
# le cas d'accomplissement de hg005b reste VERT meme sans ce module — PAS un defaut du cas, le texte imprime
# est bel et bien code, seulement sa consequence est structurellement identique au filet generique de fin de
# partie sur CETTE carte precise (contrairement a hg004b, stade 1, dont le cas ROUGIT sans le module : la
# carte suivante existe, le moteur avancerait sinon au lieu de faire perdre). Assume ici, pas maquille.


def GetAbilities() -> Sequence['Ability']:

    def innards_revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        SetupCards.PutIntoPlay(effect, "FirstPlayer", False, name="Inside Galactus", card_type=Environment)
        joueur = Worlds.GetFirstPlayer(effect)
        MettreUnMetazombieEnJeu(effect, joueur)
        MettreUnMetazombieEnJeu(effect, joueur)

    def perdu_si_accompli(effect: 'Effect', message: 'Message.WhenMainSchemeStageWouldBeCompleted') -> None:
        Unused(effect)
        message.SetBeInstead(effect)
        Worlds.SetGameOver(False, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, innards_revele),
        AbilityFactory.WhenMainSchemeStageWouldBeCompleted(AbilityType.WhenCompleted, "This", perdu_si_accompli),
    ]
