from . import *
# * Havok: Alex Summers (Justice, allie 4 [mental], 1*/1*, PV 3). STARJAMMER. X-MEN.
# Forced Response: After Havok enters play, tuck the top 3 cards of the encounter deck under him.
# [star] Forced Interrupt: When Havok uses a basic power, discard a card tucked under him. He gets +1 to that basic power for each icon
# ([star] and [boost]) in that card's boost area.
#
# Cartes de reference : cr002 Hepzibah (`WhenUnitUseBasicPower(.., "This", op)` + `message.GainValue(N, effect)`, carte glissee sous un
# AUTRE hote : le choix et la defausse sont faits dans l'operation) ; 53021 / 53018 (`TuckCardUnderHere(faces, effect)`) ; fiche tuck.md.
# ⚠ « each icon ([star] AND [boost]) » : `CountTotalBoostStarAndBoost` (RECETTES §3), PAS `CountTotalBoostIcons` ; dans la zone « glissee »
# `CountBoostIconsInternal` rend `printed_boost`. La carte est comptee AVANT d'etre defaussee.
# « Forced » : pas de choix de declencher ; le joueur choisit LAQUELLE des cartes glissees (cr002 : `AskChooseFace`).
def GetAbilities() -> Sequence['Ability']:
    def havok_entre(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        faces = Worlds.GetEncounterDeck(effect).GetTops(3)
        if faces:
            this.TuckCardUnderHere(faces, effect)
    def havok_pouvoir(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        glissees = Glissees(this)
        joueur = JoueurDe(effect)
        if joueur is None or not glissees:
            return
        choisie = glissees[0] if len(glissees) == 1 else joueur.AskChooseFace(
            glissees, effect, prompt="Discard a card tucked under Havok", forced=True)
        if choisie is None:
            return
        icones = NbIcones(choisie)
        if Faces.DiscardAll([choisie], effect) and icones > 0:
            message.GainValue(icones, effect)
    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            havok_entre,
        ),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.ForcedInterrupt,
            "This",
            havok_pouvoir,
        ),
    ]
