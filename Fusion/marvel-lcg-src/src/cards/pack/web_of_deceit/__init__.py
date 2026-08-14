from cards.pack import *


def RetirerMenaceDUneManigance(effect: 'Effect', valeur: int) -> None:
    """« Remove N threat from a side scheme. »

    La manigance est CHOISIE par le premier joueur, et le choix compte : dans
    la campagne Web of Deceit, la manigance qui tient la victoire (The Long
    Night) est une manigance secondaire comme une autre. On ne propose que
    celles qui portent de la menace, sans quoi le choix serait vide de sens.
    """
    schemes = [x for x in Worlds.GetAllSideSchemes(effect)
               if x.CastTo(CanPlaceToken).GetTokens('threat') > 0]
    if not schemes:
        return
    joueur = Worlds.GetFirstPlayer(effect)
    cible = joueur.AskChooseFace(schemes, effect, prompt="Remove threat from")
    Faces.RemoveTokensOn([cible or schemes[0]], valeur, 'threat', effect)


def ChercherEtReveler(effect: 'Effect', **finder) -> 'CardFace|None':
    """Cherche une carte dans le deck rencontre ET sa defausse, puis la revele.

    `Find.FindAndReveal` regarde les deux : c'est ce que demandent les textes
    « search the encounter deck and discard pile for X and reveal it »."""
    return Find.FindAndReveal(
        effect,
        Worlds.GetFirstPlayer(effect),
        finder=CardFinder(**finder)
    )


def VoteForFisk(menace: int) -> 'Ability':
    """« After the villain schemes, place N threat on the side scheme with the
    lowest amount of threat. »

    L'environnement de campagne, en jeu dans CHAQUE scenario (livret p.3). La
    manigance visee est la moins chargee : `Worlds.FilterSideScheme` sait la
    designer, c'est le meme filtre que le moteur utilise pour ses propres
    cartes.
    """
    def voter(effect: 'Effect', message: 'Message.AfterEnemySchemeAndPlaceThreat') -> None:
        this = effect.this.CastTo(Environment)
        cible = Worlds.FilterSideScheme(effect, least_threat=True)
        if cible:
            this.PlaceThreatOnSchemes([cible], menace, effect)

    return AbilityFactory.AfterEnemySchemeAndPlaceThreat(
        AbilityType.ForcedResponse,
        Villain,
        MainScheme,
        voter
    )


def GobelinExpert() -> 'Ability':
    """« When Revealed: Take 2 indirect damage. Shuffle each TECH attachment in
    the encounter discard pile into the encounter deck. »

    Le meme texte sur les deux gobelins experts : une seule ecriture.
    """
    def gobelin(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)

        joueur = message.GetToPlayer()
        joueur.GetIdentity().TakeIndirectDamage(this, 2, effect)

        attachements = CardFinder(card_type=Attachment, trait="TECH").Checks(
            Worlds.GetEncounterDiscardPile(effect).Get())
        if attachements:
            Faces.ShuffleAllTo(attachements, "EncounterDeck", effect)

    return AbilityFactory.WhenThisRevealed(
        None,
        gobelin
    )


def MettreVoteForFiskEnJeu(effect: 'Effect') -> None:
    """« Put the "Vote for Fisk" environment into play » (livret p.3).

    Deux cartes distinctes, standard et experte : la mise en place choisit.
    """
    joueur = Worlds.GetFirstPlayer(effect)
    nom = "wd031" if Worlds.IsExpert(effect) else "wd030"
    carte = Search.SearchForCard(
        effect,
        joueur,
        include_set_aside=True,
        card_ids=[nom],
    )
    if carte:
        carte.PutIntoPlay(joueur, effect)
