from cards.pack import *

# Aides communes aux sets du pack Punisher MC×DC 2026 (hors Jigsaw et Hobgoblin, qui ont leur propre __init__).

def FaceCacheeAuJoueur(effect: 'Effect', this: 'CardFace', joueur: 'Player|None') -> None:
    """« Deal this card to yourself as a facedown encounter card » (boost). Modele shredder/__init__.py
    (`FaceCacheeAuPremierJoueur`) et brawn/brawn_nemesis/bw021.py : une carte de boost est rangee par le moteur APRES
    la resolution de son effet, on DETOURNE donc son rangement vers les cartes distribuees du joueur (UNE seule fois :
    sinon une carte donnee puis revelee dans le meme round reboucle, constate en autoplay le 16/10/2026)."""
    if joueur is None:
        return
    fait = False

    def rediriger(effet_temp: 'Effect', message2: 'Message.WhenCardWouldDiscard') -> None:
        nonlocal fait
        if fait:
            return
        fait = True
        message2.SetToArea(joueur.dealt_encounter_cards)

    this.effect.RegisterTemp(
        AbilityFactory.WhenCardWouldDiscard(AbilityType.Temp0, "This", rediriger),
        unregister_after_exec=True,
        until_round_end=True,
    )


def CartesQueTuControles(joueur: 'Player') -> List['CardFace']:
    """« a card you control » en jeu : allies, ameliorations (y compris celles des allies) et soutiens. Ni l'identite
    ni les cartes de la main."""
    allies = [c for c in joueur.GetControlCharacters() if Ally.IsType(c)]
    return allies + list(joueur.GetControlUpgrade()) + list(joueur.supports.Get())


def AuChoixDuJoueur(effect: 'Effect', joueur: 'Player', operation: Callable[[Sequence['CardFace']], Any], **filtre: Any) -> None:
    """« <verbe> a character you control » : le JOUEUR choisit parmi SES personnages (identite et allies).
    `filtre` : canbe_stunned / canbe_confused / canbe_exhaust. Modele skrull_menace/paibok/__init__.py."""
    joueur.ChooseAbilities(
        effect,
        AbilityFactory.ForChoiceAbility("", lambda cibles: operation(cibles)).SetTarget("YouControlUnit", **filtre),
    )


def TousLesJoueurs(effect: 'Effect') -> 'List[Player]':
    """TOUS les joueurs, quelle que soit leur zone (`Worlds.GetPlayers` filtre par la zone de la carte qui resout : un complot de la zone commune
    n'y voit AUCUN joueur)."""
    return [j for j in effect.world.const_players if j.area_hero.GetSize() > 0]

# Les 4 defis MC×DC 2026 (p279-p282). ⚠ Le dossier porte le nom du set nettoye (`Punisher Challenges`).
# Aide commune aux defis 1 a 3 : « When the villain stage advances, advance the main scheme to 2A. » (modele : pack challenges/2412_wrath_of_the_mad_titan,
# qui avance le complot a 2A a la mise en place ; ici le declencheur est `AfterVillainAdvanced`).


def ComplotEn2A() -> 'Ability':
    def avancer(effect: 'Effect', message: 'Message.AfterVillainAdvanced') -> None:
        # Seulement si un stade 2 attend encore dans la pile des complots (un complot deja au stade 2 ne bouge plus : le moteur l'exige).
        if effect.world.main_schemes_deck.FindCard(CardFinder(stage=2), card_type=MainScheme) is None:
            return
        for complot in Worlds.GetAllMainSchemes(effect):
            complot.Advance("2A", effect)
            return

    return Ability(AbilityType.Challenge, Message.AfterVillainAdvanced, [], avancer)
