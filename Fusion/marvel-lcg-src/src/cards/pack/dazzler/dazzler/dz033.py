from . import *

# Duet
# SONG.
# Max 2 per deck.
# Response: After you play a SONG card, ready your hero and another friendly
#   character.
#
# ATTENTION au piege : Duet est elle-meme un [[SONG]]. Sans garde, la jouer
# declencherait sa propre Response. Le texte dit « after you play A SONG
# CARD », donc une AUTRE : on exclut `effect.this`.


def GetAbilities() -> Sequence['Ability']:

    def pas_ton_heros(effect: 'Effect', face: 'CardFace') -> bool:
        """« ANOTHER friendly character » : pas ton heros, il est deja servi."""
        joueur = effect.GetInitiator()
        return joueur is None or face is not joueur.GetIdentity()

    def duo(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        joueur = effect.GetInitiator()
        identite = None if joueur is None else joueur.GetIdentity()
        # « your HERO » : en alter ego il n'y a pas de heros a redresser
        # (20/10/2026 : l'alter ego etait redresse a la place).
        heros = identite if identite is not None and Hero.IsType(identite) else None
        # « READY YOUR HERO and another friendly character » : le heros n'est
        # pas un choix, il est nomme. Seul le second personnage se selectionne.
        cibles = ([] if heros is None else [heros]) + list(effect.targets)
        Faces.ReadyAll(cibles, effect)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFinder(trait=TRAIT_SONG),
            duo,
            conditions=[
                lambda effect, message: message.played_face is not effect.this,
            ],
        ).SetPlay()
        # CORRECTIF : `range=(1, 2)` sur « YouControlUnit » laissait redresser
        # DEUX allies sans jamais toucher au heros, alors que le texte le nomme.
        # Le heros est desormais redresse d'office par l'operation, et le
        # selecteur ne propose plus que l'AUTRE personnage. La fourchette part
        # de zero : s'il n'y a personne d'autre a redresser, la carte reste
        # jouable et fait ce qu'elle peut.
        # « another FRIENDLY character » : `Friend`, les personnages de TOUS les
        # joueurs (avant le 20/10/2026 : « YouControlUnit »). Minimum dynamique
        # (modele 09035) : obligatoire des qu'un autre personnage peut etre
        # redresse, zero sinon pour que la carte reste jouable pour le heros.
        # `check_fn` n'est pas transmis par le selecteur (commente dans
        # selector/factory.py) : le filtre « pas ton heros » passe par
        # `check_effect_fn` du `CardFinder`.
        .SetTarget(CardFinder(card_type=Friend, canbe_ready=True,
                              check_effect_fn=pas_ton_heros),
                   range=(lambda effect: min(1, len(effect.context.all_legal_targets)), 1)),
    ]
