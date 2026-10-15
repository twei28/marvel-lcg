from . import *

# * Queen Veranke II — MECHANT, face B (REVEALED). SKRULL. PV 18[per_hero], MNG 2, ATQ 3.
# Forced Response: After the villain phase ends, if any player is in alter-ego form, flip Queen Veranke.
# When Defeated: Remove all suspicion counters from "Who Do You Trust?".
#
# Cartes de reference :
#  - « After the villain phase ends » : **`AbilityFactory.AfterPhaseEnd(ForcedResponse, "Villain", ...)`**
#    (turn_phase.py) ; flip : **`mojo 39012b`** Spiral (`card.Flip`).
#  - « When Defeated » d'un mechant : **`WhenUnitBeDefeated(WhenDefeated, "This", ...)`** (gb022 / 44038).
#  - « discard the top card of the encounter deck, if it is a treachery » : **`mojo 39022`** (`Worlds.DiscardEncounterCards`)
#    et **`lyja/EstTraitrise`** (decision utilisateur du 15/10/2026 : « TREACHERY card » = type Treachery OU trait TREACHERY).
#
# ⚠ Mots-pieges :
#  - « any player is in alter-ego form » : UN seul suffit (`IsAlterEgo`), pas tous ; la forme est lue a la FIN de la
#    phase du mechant.
#  - « Otherwise » (stade III) : seulement quand AUCUN joueur n'est en alter ego ; la carte defaussee EST defaussee
#    meme si elle n'est pas une traitrise.
#  - Apres sa defaite, le stade suivant arrive du MEME COTE (Queen Veranke) : natif (`AdvanceVillainStage`).
#  - « flip Queen Veranke » : elle repasse sur Spider-Woman, camouflee, invulnerable.


def GetAbilities() -> Sequence['Ability']:
    return CapacitesQueen(2)
