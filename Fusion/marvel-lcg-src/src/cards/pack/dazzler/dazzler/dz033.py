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
        heros = None if joueur is None else joueur.GetIdentity()
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
        .SetTarget("YouControlUnit", canbe_ready=True, range=(0, 1),
                   check_fn=pas_ton_heros),
    ]
