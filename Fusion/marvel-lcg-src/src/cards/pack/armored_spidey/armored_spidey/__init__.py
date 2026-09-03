from cards.pack import *

# Helpers partages du set « Armored Spidey ».
#
# ⚠ Douze cartes du pack posent la MEME question : « ou est la Spider Armor
# de ce joueur, et que porte-t-elle ? ». Un seul chemin pour tout le monde,
# pour que les douze ne puissent pas diverger — c'est la leçon des deux
# empreintes d'autoplay du 03/09/2026, qui lisaient chacune un sous-ensemble
# different du monde.

NOM_ARMURE = "Spider Armor"
MAX_METAL = 3


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit.

    ⚠ NE PAS se rabattre sur `effect.GetInitiator()` en premier : il leve un
    assert quand l'initiateur n'est pas un joueur, et le moteur AVALE
    l'exception — la carte ne fait alors rien, et aucun outil ne le voit
    (leçon `Player.GetHero()`, pack lady_sif, 03/09/2026). Les capacites
    continues (as012, as013) sont evaluees hors tour de jeu, sans initiateur.
    `GetControlByOrOwner` retombe sur le PROPRIETAIRE quand la carte n'est
    pas en jeu, ce qui couvre aussi l'evenement en cours de resolution.
    """
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None


def ArmureDuJoueur(joueur: 'Player|None') -> 'CardFace|None':
    """La Spider Armor que CE joueur controle, quelle que soit sa face.

    ⚠ `GetControlUpgrade` balaie les ameliorations attachees aux personnages
    du joueur, pas le terrain entier : en multijoueur, l'armure d'un autre
    Armored Spidey n'est jamais rendue. C'est le montage employe par le
    moteur lui-meme pour « your suit form upgrade » de Nick Fury
    (`selector_target_helper.py:264`).
    """
    if joueur is None:
        return None
    trouvees = joueur.GetControlUpgrade(CardFinder(card_type=Upgrade, name=NOM_ARMURE))
    if not trouvees:
        return None
    return trouvees[0]


def MonArmure(effect: 'Effect') -> 'CardFace|None':
    """Raccourci : la Spider Armor du joueur de la carte qui agit."""
    return ArmureDuJoueur(JoueurDeCetteCarte(effect))


def ArmureCible(effect: 'Effect') -> Sequence['CardFace']:
    """Cible de COUT : `Select.From` accepte une fonction, c'est celle-ci.

    ⚠ Toutes les cartes qui ecrivent « remove N metal counter(s) from Spider
    Armor **->** » passent par ici, dans le COUT et jamais dans le corps.
    Ecrit dans le corps, l'effet resout meme quand l'armure est vide : la
    capacite ne fait rien, le moteur la repropose a l'identique, et la partie
    tourne en rond. Correctif paye en autoplay sur le pack
    iron_man_model_42 le 03/09/2026, meme defaut que le blocage Underling.
    """
    armure = ArmureDuJoueur(Select.GetYou(effect))
    return [armure] if armure else []


def CompteursMetal(effect: 'Effect') -> int:
    """Nombre de compteurs `metal` sur la Spider Armor du joueur."""
    armure = MonArmure(effect)
    return armure.GetCounters('metal') if armure else 0


def ArmureOperationnelle(effect: 'Effect') -> bool:
    """« While Spider Armor has the [[OPERATIONAL]] trait » (as012, as013).

    ⚠ Le trait se lit sur l'AMELIORATION, pas sur le heros : as002a le porte,
    as002b porte DESTROYED a la place. Une armure absente du terrain n'est
    pas operationnelle. Modele `IfAlertLevelIsHighSide`
    (src/cards/pack/aos/batroc/__init__.py:6), meme montage sur une carte
    recto-verso dont le trait est la seule difference lisible.
    """
    armure = MonArmure(effect)
    return armure is not None and armure.HasTrait("OPERATIONAL")


def RetirerUnMetal(effect: 'Effect') -> bool:
    """Retire 1 compteur `metal` de la Spider Armor, et dit si ca a marche.

    ⚠ Reserve aux « You MAY remove 1 metal counter **to** <bonus> » (as006,
    as008, as009), ou l'effet PRINCIPAL de la carte tombe de toute facon :
    la carte ne peut donc pas resoudre en ne faisant rien, et le blocage
    d'autoplay du pack iron_man_model_42 ne s'applique pas. Pour les
    « remove ... **->** effet », ou la fleche fait du retrait un COUT, passer
    par `CostFunc.Counter(ArmureCible, ...)` et surtout pas par ici.

    Le RETOUR est la raison d'etre du helper : sans compteur, le bonus ne
    doit PAS tomber, et `Faces.RemoveCountersOn` ne dit rien de ce qu'il a
    reellement enleve.
    """
    armure = MonArmure(effect)
    if armure is None or armure.GetCounters('metal') < 1:
        return False
    Faces.RemoveCountersOn([armure], 1, 'metal', effect)
    return True


def EstMonArmure(effect: 'Effect', face: 'CardFace|None') -> bool:
    """La face declenchante est-elle MA Spider Armor ? (as005)

    ⚠ « After **you** remove a metal counter from Spider Armor » : en
    multijoueur, l'armure d'un autre Armored Spidey ne doit rien declencher.
    """
    return face is not None and face is MonArmure(effect)


def CoutPrintedAuMoins(face: 'CardFace|None', seuil: int) -> bool:
    """« a card with the printed cost of 2 or more » (as010, as014).

    ⚠ Cout IMPRIME : une reduction de cout ne change rien, et une carte sans
    cout imprime (identite, obligation, carte rencontre) ne compte pas.
    `has_printed_cost` est le drapeau que le moteur pose lui-meme quand
    `desc.Cost` existe (has_cost.py:15) ; le lire evite de compter une carte
    a 0 par defaut.
    """
    if face is None or not getattr(face, "has_printed_cost", False):
        return False
    return face.printed_cost.val >= seuil
