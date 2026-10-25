from cards.pack import *

# Helpers partages du set « The Vault » (voir the_vault/__init__.py pour le scenario).
#
# ⚠ Les modules du set font `from . import *` : un helper defini dans le `__init__.py` du PACK leve un NameError avale
# par le moteur (lecon hk005). Tout ce que les cartes appellent vit donc ICI.

NOM_VAULT = "The Vault"
NOM_INSPECTION = "Inspection of the Vault"


################################################################################
# Lire l'etat du scenario
def LeVault(effect: 'Effect') -> 'Environment|None':
    """L'environnement « The Vault » en jeu, ou None (avant la mise en place ou apres sa disparition)."""
    trouves = Worlds.FindCardsOnField(effect, name=NOM_VAULT, card_type=Environment)
    return trouves[0] if trouves else None


def SousLeVault(effect: 'Effect', type_: 'Any'=None) -> List['CardFace']:
    """Les cartes glissees SOUS The Vault (face cachee), de ce type si demande."""
    vault = LeVault(effect)
    if vault is None:
        return []
    faces = list(vault.GetPlacedCardArea().GetAll())
    return [f for f in faces if type_ is None or type_.IsType(f)]


def MechantsSousLeVault(effect: 'Effect') -> List['Villain']:
    return [f.CastTo(Villain) for f in SousLeVault(effect, Villain)]


def SbiresSousLeVault(effect: 'Effect') -> List['Minion']:
    return [f.CastTo(Minion) for f in SousLeVault(effect, Minion)]


def InspectionEnJeu(effect: 'Effect') -> bool:
    """« If Inspection of the Vault is in play » : l'obligation est en jeu (donnee a un joueur), pas mise de cote."""
    return bool(Worlds.FindCardsOnField(effect, name=NOM_INSPECTION, card_type=Obligation))


def NombreDeJoueurs(effect: 'Effect') -> int:
    return len(Worlds.GetPlayers(effect))


################################################################################
# Agir sur le Vault et sur le deck de vilains
def PoserSousLeVault(faces: 'Sequence[CardFace]', effect: 'Effect') -> bool:
    """« Place it beneath The Vault facedown » ; verifie ensuite la fin de partie (un vilain de plus sous le Vault)."""
    vault = LeVault(effect)
    if vault is None or not faces:
        return False
    fait = vault.TuckCardUnderHere(list(faces), effect)
    VerifierFinDePartie(effect)
    return fait


def RevelerAuHasardSousLeVault(effect: 'Effect', joueur: 'Player', type_: 'Any') -> 'CardFace|None':
    """« Reveal 1 random <type> beneath The Vault » : tirage au hasard (generateur seme du moteur), revelation (le
    « When Revealed » part), None s'il n'y en a pas (« If you cannot »)."""
    candidats = SousLeVault(effect, type_)
    if not candidats:
        return None
    choisie = Rand.RandomChoice(candidats, effect)
    choisie.Reveal(joueur, effect)
    VerifierFinDePartie(effect)
    return choisie


def RevelerProchainMechant(effect: 'Effect', joueur: 'Player') -> 'Villain|None':
    """« Reveal the top card of the villain deck » : revelation vraie (le « When Revealed » du stade II part)."""
    mechant = Villains.RevealNextVillain(joueur, effect, reveal=True)
    VerifierFinDePartie(effect)
    return mechant


def ApresDepartDUnMechant(effect: 'Effect') -> None:
    """Livret p.1 : « After the last villain leaves play, reveal the top card of the villain deck. » Puis fin de
    partie. Appele apres un vilain vaincu (retire de la partie) ou melange dans le deck de vilains."""
    if effect.world.is_game_over:
        return
    if not Villains.All(effect) and Villains.VillainDeckSize(effect) > 0:
        RevelerProchainMechant(effect, Worlds.GetFirstPlayer(effect))
    VerifierFinDePartie(effect)


def VerifierFinDePartie(effect: 'Effect') -> None:
    """The Vault (vt018) : « If all the villains are either beneath The Vault or defeated, the players win the game. »
    (plus aucun vilain en jeu ni dans le deck de vilains), « If no villain is beneath The Vault, the players lose the
    game. » La victoire PASSE EN PREMIER (arbitrage de l'utilisateur, 25/10/2026) : si les deux sont vraies ensemble,
    les joueurs gagnent."""
    if effect.world.is_game_over or LeVault(effect) is None:
        return
    if not Villains.All(effect) and Villains.VillainDeckSize(effect) == 0:
        Worlds.SetGameOver(True, effect)
        return
    if not MechantsSousLeVault(effect):
        Worlds.SetGameOver(False, effect)


################################################################################
# Les capacites que les huit vilains ont en commun
def ControleurDe(face: 'CardFace', defaut: 'Player') -> 'Player':
    controleur = face.GetControlByOrOwner()
    return controleur if Player.IsType(controleur) else defaut


def ChoixApresAttaque(libelle: str, action: 'Callable[[Effect, Message.AfterUnitAttackUnit, Player], None]') -> 'List[Ability]':
    """« Forced Response: After you attack <vilain> with a card you control, choose to either <libelle> or place 1
    threat on the main scheme. » Le joueur qui a attaque choisit (il peut choisir la menace)."""
    def apres(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Villain)
        joueur = ControleurDe(message.attacker, Worlds.GetFirstPlayer(effect))
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(libelle, lambda targets: action(effect, message, joueur)),
            AbilityFactory.ForChoiceAbility("Place 1 threat on the main scheme",
                                            lambda targets: this.PlaceThreatOnSchemes("MainScheme", 1, effect)),
        )
    return [AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, "You", "This", apres)]
