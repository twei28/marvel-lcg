from . import *

# * The Maker — SBIRE (New Revengers). ELITE. REVENGER. PV 3, MNG 3, ATQ 1, 3 boosts.
# The Maker cannot take damage while another REVENGER enemy is in play.
# When Revealed: Search the encounter deck and discard pile for The Revenge Time side scheme and reveal it.
#
# Cartes de reference :
#  - Invulnerable tant que : **`msm 05027`** * Thomas Edison (`ThisCannotTakeDamageWhile(conditions=[fn])`,
#    condition sur l'etat du plateau).
#  - Fouille + revelation d'un complot annexe : **`core 01136`** * Ultron (`Search.EncounterCard(
#    include_discard_pile=True, name="Ultron's Imperative", card_type=SchemeSide2)` puis `Reveal`).
#
# ⚠ Mots-pieges : « ANOTHER REVENGER enemy » : le Maker est lui-meme un Revenger, il ne se compte pas ;
# « enemy » (sbire OU mechant devenu Revenger par The Revenge Time) ; « cannot take damage » = toute source,
# pas seulement les attaques ; « search the encounter deck AND DISCARD PILE » ; The Revenge Time deja en jeu
# ou absent : la fouille ne trouve rien (aucun doublon).


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        ChercherEtReveler(effect, message.GetToPlayer(), name="The Revenge Time", card_type=SchemeSide2)

    return [
        AbilityFactory.ThisCannotTakeDamageWhile(conditions=[AutreEnnemiRevenger]),
        AbilityFactory.WhenThisRevealed(None, revelation),
    ]
