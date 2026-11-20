from . import *

# * Buffy Summers (face alter-ego) : REC 3, main 6, PV 10. STUDENT.
# Setup: Set the HELLMOUTH deck aside, out of play. Find the Harvest and The Master, and reveal them.
# Chosen — Action: Search your deck and discard pile for Mr. Pointy and add it to your hand.
#
# CARTES DE REFERENCE
#  - `ok001b` / `an001b` : `WhenCardSetup("This", op)` + `Search.PlayerCard(include_player_deck=True, include_discard_pile=True, ..)`
#    + `GainCard` pour une recherche dans le deck ET la defausse.
#  - `Faces.SetAside(faces, effect)` : la mise de cote (zone `aside_deck`).
#  - `mv013` (Michael Korvac) : `Search.EncounterCard(.., include_discard_pile=True, include_set_aside=True, name=..)` +
#    `face.Reveal(joueur, effect)` pour « find ... and reveal ». Fiches `mots-cles/find.md` et `setup.md` (`WhenCardSetup` convient a une
#    IDENTITE ; c'est pour une carte mise en jeu par le mot-cle Setup qu'il faut `AfterGameSetup`).
#
# ⚠ MIS A JOUR le 31/10/2026 (cartes HELLMOUTH recues) : Harvest est un COMPLOT ANNEXE (pas un sbire), The Master un sbire ; le paquet HELLMOUTH est
#   cree mis de cote au demarrage (`BeginGameWithSetAside`), puis les deux sont retrouves et reveles. Les lignes ci-dessous decrivent l'ancienne
#   version provisoire (filtre Minion).
# TEXTE CONTRE CODE
#  « Set the HELLMOUTH deck aside, out of play » -> toutes les cartes du deck rencontre portant le trait HELLMOUTH passent en
#    zone de mise de cote. Le paquet HELLMOUTH n'est pas fourni par le Drive : sans carte, rien ne bouge.
#  « Find the Harvest and The Master, and reveal them » -> DEUX recherches dans le deck rencontre, sa defausse ET la zone de mise
#    de cote (Rules Reference v1.8, « find » : toute zone ou la carte peut se trouver ; fiche `mots-cles/find.md`), chacune
#    suivie de `Reveal`. Elles se font APRES la mise de cote : un sbire HELLMOUTH mis de cote par la premiere etape est donc
#    retrouve par la seconde. Harvest et The Master ne sont pas fournis : sans carte, rien n'est revele (pas une erreur).
#  « Search your deck and discard pile for Mr. Pointy and add it to your hand » -> deck ET defausse du joueur, par NOM, puis main.
#    Mr. Pointy n'est pas fourni : la recherche ne trouve rien. Action NUE (`AbilityType.Action`), sans limite imprimee, sans cout.
#  Chiffres : aucun.


def GetAbilities() -> Sequence['Ability']:

    def setup(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        # « Find the Harvest and The Master, and reveal them » : le paquet HELLMOUTH est DEJA mis de cote (cree par `BeginGameWithSetAside`).
        for nom, type_carte in ((NOM_HARVEST_COMPLOT, EncounterSideScheme), (NOM_THE_MASTER, Minion)):
            face = Search.SearchForCard(
                effect,
                joueur,
                include_encounter_deck=True,
                include_encounter_discard_pile=True,
                include_set_aside=True,
                name=nom,
                card_type=type_carte,
            )
            if face:
                face.Reveal(joueur, effect)

    def chosen(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            include_discard_pile=True,
            name=NOM_MR_POINTY,
        )
        if face:
            joueur.GainCard(face, effect)

    return [
        AbilityFactory.BeginGameWithSetAside(CARTES_HELLMOUTH),
        AbilityFactory.WhenCardSetup(
            "This",
            setup,
        ),
        (AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            chosen,
        )
            .SetName("Chosen")),
    ]
