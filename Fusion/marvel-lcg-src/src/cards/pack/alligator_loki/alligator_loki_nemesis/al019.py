from . import *

# * Throg — sbire NEMESIS. ASGARD, CREATURE. SCH 1, ATK 1, 4 PV, Boost 1 (`desc`).
# Forced Interrupt: When this minion would enter play, discard any other Throg
#   from play. Place a random card from your hand facedown here.
# When Defeated: Return each facedown card here to its owner's hand.
#
# Cartes de reference :
#  - 22028 * Gamora (nemesis de Nebula) : « When this minion would enter play,
#    discard any other Gamora from play » -> `WhenCardWouldEnterPlay(
#    ForcedInterrupt, "This", op)` + `Worlds.FindCardsOnField` +
#    `Faces.DiscardAll` ;
#  - 09029 Open the Dark Dimension / dz014 Lightbringr : « facedown here »
#    -> `this.PlaceCardHere(face, False, effect)` ;
#  - 50104a : « a random card » -> `Rand.RandomChoice(faces, effect)` (respecte
#    le mode sans melange des tests) ;
#  - 33027 Lost Visor : rendre les cartes placees ici par
#    `GetPlacedCardArea().Get()` ; ici « to its OWNER's hand » ->
#    `Faces.ReturnToHand(..., "Owner", effect)` (faces.py:306).
#
# ⚠ « ANY OTHER THROG » : le sbire de joueur al002 aussi. C'est le sens de
# la carte : la grenouille nemesis chasse la grenouille alliee. Recherche par
# NOM (les deux s'appellent Throg), en excluant `this`.
# ⚠ PLACER LA CARTE : « here » n'existe pas tant que le sbire n'est pas en jeu
# (`PlaceCardHere` refuse hors plateau, card_face.py:985). L'interruption ne
# peut donc pas placer elle-meme : la seconde phrase s'execute juste apres
# l'entree en jeu (`AfterCardEnterPlay(ForcedResponse, "This")`). Meme
# resultat pour le joueur, sans fenetre de reponse entre les deux.
# ⚠ « YOUR hand » sur une carte de rencontre = le joueur engage avec Throg
# (`GetEngagedPlayer`). Main vide : rien a placer.
# ⚠ « When Defeated » seulement : Throg defausse autrement (Alligator Antics
# qui le sort du jeu, un autre Throg qui entre) NE rend PAS les cartes, elles
# suivent le sort par defaut des cartes placees (defausse). Fidele au texte.

def GetAbilities() -> Sequence['Ability']:

    def chasser_l_autre_throg(effect: 'Effect', message: 'Message.WhenCardWouldMoveToArea') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)
        autres = [f for f in Worlds.FindCardsOnField(effect, name="Throg")
                  if f is not this]
        Faces.DiscardAll(autres, effect)

    def placer_une_carte(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)
        joueur = this.GetEngagedPlayer()
        if joueur is None:
            return
        main = joueur.hand_cards.Get()
        if not main:
            return
        carte = Rand.RandomChoice(main, effect)
        this.PlaceCardHere(carte, False, effect)

    def rendre_les_cartes(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)
        cartes = list(this.GetPlacedCardArea().Get())
        if cartes:
            Faces.ReturnToHand(cartes, "Owner", effect)

    return [
        AbilityFactory.WhenCardWouldEnterPlay(
            AbilityType.ForcedInterrupt,
            "This",
            chasser_l_autre_throg,
        ),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            placer_une_carte,
        ),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            rendre_les_cartes,
        ),
    ]
