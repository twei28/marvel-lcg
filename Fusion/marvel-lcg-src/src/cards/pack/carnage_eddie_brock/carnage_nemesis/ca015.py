from . import *

# * Torment : SBIRE NEMESIS de Carnage (CRIMINAL. ELITE. KILLER.), SCH 2, ATK 1 (consecutif), PV 6, boost 3. Set « Carnage Nemesis ».
# Quickstrike. Villainous.
# When Revealed: Search the encounter deck, discard pile, and set-aside area for Death Spiral and reveal it.
# [star] Forced Interrupt: When Torment attacks a friendly character, if there is an ally or PERSONA support with the same classification as that character under your control or in your hand (identity-specific, aspect, or basic), cancel this attack and discard that card instead.
#
# CARTES DE REFERENCE
#  - Quickstrike / Villainous : mots-cles natifs lus dans `desc` (fiches mots-cles/quickstrike.md, villainous.md), AUCUN code.
#  - « Search the encounter deck, discard pile and set-aside area for X and reveal it » : `49022` (Face the Past : meme balayage deck + defausse + zone de cote) + `find.md` (`Search.EncounterCard(.., include_discard_pile=True, include_set_aside=True, name=..)` puis `face.Reveal(joueur, effect)`) ;
#    `bw021` (Imperius Rex) pour la recherche d'une carte du set nemesis.
#  - Interruption forcee « when X attacks a friendly character → cancel » : `sk242` (`WhenUnitWouldAttack(ForcedInterrupt, .., op)`) + `hf120` (`message.CancelThisAttack`) ; helpers `EchangerContreUnSacrifice` / `CibleAmie` (carnage_nemesis/__init__.py), partages avec Death Spiral (ca017).
#
# TEXTE CONTRE CODE
#  « When Revealed: SEARCH the encounter deck, discard pile AND set-aside area for Death Spiral AND REVEAL it » : une carte, trois zones, revelee (son attache a Torment resout alors). Absente (deja en jeu ou introuvable) : rien d'autre.
#  « [star] Forced Interrupt: When TORMENT attacks a FRIENDLY character » : l'attaquant est Torment lui-meme (`"This"`) ; cible = identite ou allie du joueur. « an ALLY OR PERSONA SUPPORT with the SAME CLASSIFICATION as THAT CHARACTER, under your control OR IN YOUR HAND » : classe imprimee (identite = `Hero`).
#    « cancel this attack AND discard THAT CARD instead » : annulation + defausse de la carte choisie. Sans carte sacrifiable l'attaque a lieu. Chiffres : PV 6, ATK 1, SCH 2, boost 3.


def GetAbilities() -> Sequence['Ability']:

    def torment_revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        joueur = message.GetToPlayer()
        face = Search.EncounterCard(
            effect,
            joueur,
            include_discard_pile=True,
            include_set_aside=True,
            name="Death Spiral",
        )
        if face is not None:
            face.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            torment_revele,
        ),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            "This",
            EchangerContreUnSacrifice,
            conditions=[CibleAmie],
        ),
    ]
