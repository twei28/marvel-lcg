from cards.pack import *
# Helpers partages du set « Carnage » (⚠ un helper defini dans le `__init__.py` du PACK leve un NameError avale par le moteur : lecon hk005, tout vit ICI).
NOM_CARNAGE = "Carnage"
NOM_EDDIE = "Eddie Brock"
NOM_TORMENT = "Torment"

# « you defeated an enemy THIS ROUND » : le moteur ne tient pas ce compteur (meme probleme que jj007) ; marqueur maison sur `world`, pose par une capacite
# silencieuse (Temp0) portee par les DEUX faces d'identite. Cle = identite du joueur, valeur = dernier round ou il a vaincu un ennemi.
DEFEAT_ROUNDS_ATTR = "carnage_enemy_defeat_rounds"


def _defeat_rounds(world: Any) -> Any:
    table = getattr(world, DEFEAT_ROUNDS_ATTR, None)
    if table is None:
        table = {}
        setattr(world, DEFEAT_ROUNDS_ATTR, table)
    return table


def EstJoueur(objet: Any) -> bool:
    """`Player.IsType` SANS le risque d'AttributeError (lecon sf002 / sf013)."""
    return objet is not None and hasattr(objet, "IsPlayer") and Player.IsType(objet)


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (⚠ jamais `effect.GetInitiator()` en premier : il leve un assert quand l'initiateur n'est pas un joueur)."""
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if EstJoueur(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if EstJoueur(initiateur):
        return initiateur
    return None


def NoterVictoire() -> 'Ability':
    """Capacite silencieuse a poser sur une face d'identite : « After you defeat an enemy » (attaque OU effet, vilain compris) -> round courant note."""

    def noter(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None:
            _defeat_rounds(effect.world)[id(joueur)] = effect.world.round_id

    return AbilityFactory.AfterUnitDefeatedUnit(
        AbilityType.Temp0,
        "You",
        Enemy,
        noter,
    )


def AVaincuUnEnnemiCeRound(effect: 'Effect', joueur: 'Player', round_id: int) -> bool:
    return _defeat_rounds(effect.world).get(id(joueur)) == round_id
