from cards.pack import *

# Helpers partages du set « Yondu ».
#
# ⚠ NEUF cartes du pack posent la MEME question : « ou est la Yaka Arrow, et
# comment la deplacer ? ». Un seul chemin pour tout le monde, pour que les
# neuf ne puissent pas diverger — c'est la leçon des deux empreintes
# d'autoplay du 03/09/2026, qui lisaient chacune un sous-ensemble different du
# monde, et celle du helper unique de `alligator_loki`.

NOM_FLECHE = "Yaka Arrow"
NOM_TAHLEI = "Tahlei"
NOM_HEROS = "Yondu"


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit.

    ⚠ NE PAS se rabattre sur `effect.GetInitiator()` en premier : il leve un
    assert quand l'initiateur n'est pas un joueur, et le moteur AVALE
    l'exception — la carte ne fait alors rien, et aucun outil ne le voit
    (leçon `Player.GetHero()`, pack lady_sif). `GetControlByOrOwner` retombe
    sur le PROPRIETAIRE quand la carte n'est pas en jeu, ce qui couvre
    l'evenement en cours de resolution.
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


def Hote(face: 'CardFace|None') -> 'CardFace|None':
    """A QUI cette carte est-elle accrochee ? `None` si elle ne l'est pas.

    ⚠ NE JAMAIS appeler `GetBindFace()` en direct : il fait `assert face`
    (card_face.py:1063) et leve donc une AssertionError des que la carte n'est
    PAS attachee. Le moteur AVALE l'exception, la capacite ne fait rien, et
    aucun cas de test ne le voit — c'est l'autoplay qui l'a sorti le
    04/09/2026, 2 fois sur 128 parties, depuis la condition de yd015.
    La Yaka Arrow est justement une amelioration qui passe son temps a etre
    detachee : tout le pack lit son hote par ici.
    """
    return getattr(face, "bind_face", None) if face is not None else None


def LaFleche(effect: 'Effect') -> 'CardFace|None':
    """La Yaka Arrow EN JEU, ou qu'elle soit accrochee.

    ⚠ Elle ne vit PAS la ou vivent les autres ameliorations : elle peut etre
    attachee a un ENNEMI, donc `GetControlUpgrade` du joueur ne la voit pas.
    C'est tout le terrain qu'il faut balayer, d'ou `Worlds.FindCardOnField`.
    ⚠ « Yaka Arrow cannot be attached to cards unless it is IN PLAY » : une
    fleche en main ou en defausse n'est pas une cible, et ce helper rend
    `None` — c'est ce qui distingue « la deplacer » de « la convoquer ».
    """
    return Worlds.FindCardOnField(effect, name=NOM_FLECHE, card_type=Upgrade)


def LaTahlei(effect: 'Effect', joueur: 'Player|None'=None) -> 'CardFace|None':
    """La Tahlei en jeu du joueur qui agit.

    ⚠ `joueur` EXPLICITE quand la carte qui agit n'appartient PAS au joueur :
    c'est le cas de l'obligation yd013, une carte de RENCONTRE donnee au
    joueur. `JoueurDeCetteCarte` part de `effect.this` et ne rend alors aucun
    joueur, si bien que la Tahlei restait introuvable et que la branche
    « defaussez la fleche ET inclinez la Tahlei » n'inclinait rien. Trouve le
    04/09/2026 par le cas de la seconde branche de Banished.
    """
    if joueur is None:
        joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return None
    trouvees = joueur.GetControlUpgrade(CardFinder(card_type=Upgrade, name=NOM_TAHLEI))
    return trouvees[0] if trouvees else None


def Convoquer(effect: 'Effect', nom: str, card_type: Any=Upgrade) -> 'CardFace|None':
    """MOT-CLE MAISON `summon` : fouiller le DECK **ET** la DEFAUSSE.

    ⚠ DEFINITION ARBITREE PAR L'UTILISATEUR (03/09/2026), l'auteur ne la
    donne nulle part et aucune carte officielle n'imprime ce mot. Fiche
    complete : `docs/reference/mots-cles/summon.md`.

    ⚠ LA DEFAUSSE EST LA MOITIE QUI COMPTE. `yd013` Banished DEFAUSSE
    explicitement la Yaka Arrow : sans elle, la fleche serait perdue pour la
    partie et NEUF cartes du pack deviendraient mortes. Un cas de test qui ne
    place la carte que dans le DECK passe au vert dans les deux montages — le
    contre-cas obligatoire la met dans la DEFAUSSE.

    Le « (Shuffle.) » est le comportement PAR DEFAUT de `Search`, il ne se
    code pas (modeles an001b, ok001b, ls005).
    """
    joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return None
    face = Search.PlayerCard(
        effect, joueur,
        include_player_deck=True,
        include_discard_pile=True,
        name=nom,
        card_type=card_type,
    )
    if face is None:
        return None
    joueur.GainCard(face, effect)
    return face


def QuitterLHote(effect: 'Effect') -> None:
    """La moitie « removed from » de « D'ast Whistlin' » (yd001a).

    ⚠ CORRECTIF DU 04/09/2026, trouve par le cas « la fleche qui QUITTE un
    ennemi le blesse aussi », rouge : le depart ne faisait AUCUN degat.

    Le montage d'origine posait sur `yd001a` une capacite branchee sur
    `Message.AfterCardDetachFrom`. Elle ne pouvait pas fonctionner : ce message
    a pour `trigger` l'AMELIORATION (sender_card.py:204-209), pas l'hote, donc
    une capacite portee par le heros ne l'entend jamais. Et la porter sur la
    fleche ne marcherait pas davantage — `can_attach.py:99` appelle
    `MarkAsRemoved` AVANT d'emettre le message, si bien que la fleche n'est
    deja plus sur le terrain quand il part.

    On fait donc comme le pack `alligator_loki`, qui a bute sur le meme manque
    (« le moteur n'emet `AfterCardDetachFrom` qu'APRES coup, jamais un "would
    detach" », alligator_loki/__init__.py:31) : la fenetre est ouverte A LA
    MAIN, au seul endroit par lequel tout le pack passe.
    """
    fleche = LaFleche(effect)
    if fleche is None:
        return
    hote = Hote(fleche)
    if hote is not None and Enemy.IsType(hote):
        # ⚠ La frappe part de `effect.this`, JAMAIS de la fleche : `DealDamage`
        # affirme `self is by_effect.this` (assertion du moteur), et ce helper
        # est appele depuis n'importe quelle carte du pack. Passer la fleche
        # levait « AssertionError: self=Yaka Arrow by_effect.this=Whistle While
        # You Work » — AVALEE par le moteur, donc une carte simplement inerte.
        # Trouvee au journal le 04/09/2026, pas par le message d'echec du cas.
        effect.this.DealDamage([hote], 1, effect)


def RappelerLaFlecheEnMain(effect: 'Effect') -> bool:
    """« Add the Yaka Arrow upgrade to your hand. » — SEUL point d'entree.

    Le rappel en main est un DEPART comme un autre : il doit mordre l'ennemi
    quitte, exactement comme un deplacement. `Faces.ReturnToHand` appele en
    direct sauterait cette morsure, ce qui rendrait la branche « en main » de
    yd011 et de yd012 gratuite alors qu'elle ne l'est pas.
    """
    fleche = LaFleche(effect)
    if fleche is None:
        return False
    QuitterLHote(effect)
    Faces.ReturnToHand([fleche], "Owner", effect)
    return True


def AttacherLaFleche(effect: 'Effect', cible: 'CardFace|None') -> bool:
    """« Attach the Yaka Arrow upgrade to X. » — SEUL point d'entree.

    ⚠ Tout le pack passe par ici, et c'est voulu : c'est ici que vivent les
    DEUX moities de « D'ast Whistlin' » (yd001a). L'ARRIVEE est portee par une
    vraie capacite du heros (`AfterCardAttachTo`, dont le trigger convient) ;
    le DEPART, lui, est ouvert a la main par `QuitterLHote` ci-dessus, faute
    de message exploitable cote moteur. Un module qui deplacerait la fleche
    autrement priverait le heros de la moitie de ses degats.

    ⚠ `AttachTo2` detache tout seul de l'hote precedent, mais SANS que le
    heros puisse l'entendre : d'ou l'appel explicite a `QuitterLHote` AVANT.
    Un deplacement d'ennemi A vers ennemi B fait donc 1 degat a A (retrait)
    PUIS 1 degat a B (arrivee). C'est exactement ce que le texte promet, et
    c'est la raison d'etre de la carte.
    """
    if cible is None:
        return False
    fleche = LaFleche(effect)
    if fleche is None:
        return False
    if Hote(fleche) is not cible:
        QuitterLHote(effect)
    return fleche.AttachTo2(cible, effect)


def EnnemisEnJeu(effect: 'Effect') -> List['CardFace']:
    """Les ennemis du terrain, cibles legales de la fleche."""
    return list(Worlds.GetOnFieldEnemies(effect))
