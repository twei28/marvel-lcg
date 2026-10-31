from . import *

# * Michael Korvac — SBIRE nemesis. COSMIC ENTITY. ELITE. SCH 2, ATK 2, PV 8, boost 4.
# Villainous. Retaliate 1.
# Threat cannot be removed from Korvac's Future.
# When Revealed: Search the encounter deck, discard pile, and set-aside area for Korvac's Future and reveal it.
#
# CARTES DE REFERENCE
#  - `21177` Enchantress : `Search.EncounterCard(.., include_discard_pile=True, include_set_aside=True, name=..)` pour
#    « search the encounter deck, discard pile, and set-aside area ».
#  - `10027` Total Destruction : `ThreatCannotBeRemovedFromWhile(from_where, while_face_is_in_play=..)`.
#
# TEXTE CONTRE CODE
#  « Villainous. Retaliate 1 » -> `desc` (Villainous 1, Retaliate 1), AUCUN module. Chiffres : retaliate 1, PV 8, boost 4.
#  « Threat cannot be removed from Korvac's Future » -> imprime sur KORVAC : l'effet dure TANT QUE KORVAC EST EN JEU
#    (il vit sur sa carte), et vise le complot « Korvac's Future ».
#  « find ... and reveal it » -> `Reveal`, le complot entre alors en jeu (When Revealed).


def GetAbilities() -> Sequence['Ability']:

    def korvac_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        joueur = message.GetToPlayer()
        face = Search.EncounterCard(
            effect,
            joueur,
            include_discard_pile=True,
            include_set_aside=True,
            name=NOM_FUTURE,
            card_type=EncounterSideScheme,
        )
        if face:
            face.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            korvac_revealed,
        ),
        AbilityFactory.ThreatCannotBeRemovedFromWhile(
            CardFinder(name=NOM_FUTURE),
            while_face_is_in_play=CardFinder(name=NOM_KORVAC),
        ),
    ]
