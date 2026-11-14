from cards.pack import *

# Helpers partages du set « Hepzibah » (Phenexian et Mysteltainn, prefixe `hz`).
#
# ⚠ Les modules du set font `from . import *` : un helper defini dans le `__init__.py` du PACK leve un NameError avale par
# le moteur (lecon hk005). Tout ce que les cartes appellent vit donc ICI.
#
# LE PACK EN UNE PHRASE : Hepzibah RESOUT les capacites « Special » des evenements qu'elle tient EN MAIN (apres avoir joue
# un evenement ; Corsair apres un pouvoir de base ; Energy Blaster quand il vainc). Modele de la resolution depuis la main :
# zeus/`__init__.py` (`ResoudreLeSpecialDe`, RECETTES-MOTEUR §4) ; modele du Special nomme : ze003, ab007.


def APrintedSpecial(face: 'CardFace|None') -> bool:
    """« a card in your hand that has a Special ability » : la carte DECLARE une capacite Special (capacites declarees
    par le module, pas les effets enregistres, qui dependent de la zone)."""
    if face is None:
        return False
    return bool(face.ability.Find(type=AbilityType.Special))


def CartesAvecSpecial(joueur: 'Player') -> List['CardFace']:
    return [f for f in joueur.hand_cards.Get() if APrintedSpecial(f)]


def ResoudreLeSpecialDe(face: 'CardFace', joueur: 'Player', effect: 'Effect') -> bool:
    """Resout le Special d'une carte EN MAIN. Une carte en main n'a AUCUN effet enregistre : on enregistre le Special le
    temps de le resoudre (RECETTES-MOTEUR §4, `ResoudreLeSpecialDe` de zeus)."""
    if not APrintedSpecial(face):
        return False
    if not face.effect.Find(type=AbilityType.Special):
        face.effect.RegisterTemp(*face.ability.Find(type=AbilityType.Special), unregister_after_exec=True)
    face.ResolveSpecialAbility(joueur, effect)
    return True


def ResoudreUnSpecialEnMain(joueur: 'Player|None', effect: 'Effect') -> bool:
    """« resolve the "Special" ability on a card in your hand » : le joueur CHOISIT la carte."""
    if joueur is None:
        return False
    cartes = CartesAvecSpecial(joueur)
    if not cartes:
        return False
    choisie = joueur.AskChooseFace(cartes, effect, prompt='Resolve the "Special" ability', forced=True)
    return ResoudreLeSpecialDe(choisie, joueur, effect) if choisie else False


def UnSpecialEnMain(effect: 'Effect', message=None) -> bool:
    """Condition d'une Response : au moins une carte avec un Special imprime dans la main du joueur."""
    joueur = effect.GetInitiator()
    return joueur is not None and CartesAvecSpecial(joueur) != []


def Ennemis(effect: 'Effect') -> List['CardFace']:
    return [f for f in Worlds.FindCardsOnField(effect, card_type=Enemy) if f.IsInPlay()]


def Intrigues(effect: 'Effect') -> List['CardFace']:
    return [f for f in Worlds.FindCardsOnField(effect, card_type=Scheme2) if f.IsInPlay()]


def ArmesSousControle(joueur: 'Player') -> List['CardFace']:
    """Les amelioration [[WEAPON]] que le joueur controle, en jeu."""
    return [f for f in joueur.GetControlCards() if f.IsInPlay() and Upgrade.IsType(f) and f.HasTrait("WEAPON")]


def JoueurDeLObligation(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui l'obligation est donnee.

    ⚠ `effect.GetInitiator()` d'une OBLIGATION est le mechant (« AssertionError: self.initiator=Rhino », vu au premier passage
    du harnais, 26/10/2026) : on cherche le joueur dont la zone d'obligations contient la carte."""
    this = effect.this
    for joueur in Worlds.GetPlayers(effect):
        if any(f is this for f in joueur.obligations_area.Get()):
            return joueur
    return None


def JoueurDuSpecial(effect: 'Effect', message) -> 'Player|None':
    """Dans un Special resolu depuis la main, le joueur est `message.GetToPlayer()`, pas toujours `effect.GetInitiator()`."""
    return message.GetToPlayer() or effect.GetInitiator()
