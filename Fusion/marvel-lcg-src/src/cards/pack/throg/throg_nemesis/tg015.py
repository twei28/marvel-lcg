from . import *

# « Lost » Property — COMPLOT ANNEXE nemesis (N 4/5). 1 icone de boost.
#   Menace de depart 3[per_hero]. Aucune icone de mot-cle.
# When Revealed: Each player tucks an identity-specific upgrade they control
#   under this card. It cannot be found while under here.
# When Defeated: Add each card under here to its owner's hand.
#
# ⚠ LA VRAIE PUNITION DU PACK. Frogjolnir (tg009) est une amelioration
# specifique a l'identite : c'est elle que ce complot confisque en priorite, et
# cinq des onze cartes du set heros la citent nommement. Sans elle, tg001a ne
# peut plus redresser Throg, tg004 ne peut plus frapper, et tg002 n'a plus
# qu'une moitie d'effet.
#
# CARTES DE REFERENCE
#  - `br012` Unworthy (pack beta_ray_bill, meme auteur) : le jumeau exact du
#    mecanisme — `this.TuckCardUnderHere(face, effect)` et le constat, verifie
#    par un cas, qu'une carte glissee dessous n'est trouvable par AUCUNE
#    fouille. `TuckCardUnderHere` vit sur `CardFace` (card_face.py:1016) : elle
#    marche donc aussi bien sur un complot annexe que sur une obligation.
#  - `58002` Ionic Physiology : `this.GetPlacedCardArea().Get()` pour relire
#    ce qui a ete glisse dessous.
#  - `40059` * Superpower Training : `WhenSchemeBeDefeated(AbilityType
#    .WhenDefeated, "This", op)` pour un « When Defeated » de complot, et
#    `Search.PlayerCard(..., card_class="IdentitySpecific")` pour « an
#    identity-specific upgrade ».
#  - `01151` Under Attack : `Players.ForEachPlayer` pour « EACH PLAYER ».
#
# TEXTE CONTRE CODE
#  ⚠ « an identity-specific upgrade they CONTROL » -> EN JEU, pas dans le deck
#    ni dans la main. C'est la difference avec `40059`, qui fouille le deck et
#    la defausse : ici on ne regarde que le terrain. Le predicat moteur est
#    `face.IsClass("IdentitySpecific")` (card_player.py:170), et le controle
#    se lit par `GetControlByPlayer()`.
#  ⚠ « EACH player TUCKS » -> obligatoire, pas « may ». Un joueur qui contröle
#    plusieurs ameliorations specifiques CHOISIT laquelle ; un joueur qui n'en
#    contröle aucune ne fait rien, et le complot n'en tient pas rigueur.
#  ⚠ « It cannot be found while under here » -> AUCUN CODE N'EST NECESSAIRE,
#    et c'est verifie par un cas. Une carte glissee sous un complot n'est ni en
#    jeu, ni dans le deck, ni en defausse, ni en main : les fouilles de tg001b
#    (`Worthy`) et de tg008 la manquent NATIVEMENT. Meme constat que `br012`,
#    ou il avait ete mesure plutot que suppose.
#  ⚠ « Add each card under here to ITS OWNER'S hand » -> a son PROPRIETAIRE,
#    pas au joueur qui vainc le complot. A plusieurs, chacun recupere la
#    sienne. `Faces.ReturnToHand(faces, "Owner", effect)` — le litteral
#    "Owner", jamais le joueur courant.
#  « WHEN DEFEATED » et non « When this leaves play » : un complot annexe
#    retire du jeu autrement (fin de partie, effet qui l'exile) ne rend rien.
#    C'est `AbilityType.WhenDefeated` qui porte cette distinction.


def GetAbilities() -> Sequence['Ability']:

    def confisquer(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(message)

        def pour_chaque_joueur(joueur: 'Player') -> None:
            candidats = [
                f for f in Worlds.FindCardsOnField(effect, card_type=Upgrade)
                if f is not None
                and f.card.IsOnField()
                and f.GetControlByPlayer() is joueur
                and ClassCard.IsType(f)
                and f.IsClass("IdentitySpecific")
            ]
            if not candidats:
                return
            choisie = joueur.AskChooseFaces(
                candidats, (1, 1), effect,
                prompt="Tuck an identity-specific upgrade under this card",
            )
            for face in choisie:
                this.TuckCardUnderHere(face, effect)

        Players.ForEachPlayer(effect, pour_chaque_joueur)

    def rendre_les_affaires(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(message)

        dessous = list(this.GetPlacedCardArea().Get())
        if dessous:
            Faces.ReturnToHand(dessous, "Owner", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            confisquer,
        ),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            rendre_les_affaires,
        ),
    ]
