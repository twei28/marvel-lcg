from cards.pack import *

# ===========================================================================
# Helpers partages du set « Sunfire » (Rainy, set 163, prefixe `sf`).
#
# ⚠ TOUT LE PACK TOURNE AUTOUR DE `sf009` BURNING : une AMELIORATION JOUEUR
# ATTACHEE A UN ENNEMI, qui revient dans la reserve au lieu de partir en
# defausse. C'est la BRIQUE 6 du plan de portage, et le pack la pousse plus
# loin que `blink` ou `yondu` : SIX exemplaires en circulation permanente.
#   - `sf001b` en met 6 de cote a la mise en place ;
#   - `sf001a` en pose une a chaque attaque ET a chaque defense de base ;
#   - `sf002`, `sf003`, `sf005` en posent une ou plusieurs ;
#   - `sf004` se declenche quand une est posee ;
#   - `sf006` alourdit ses degats, `sf007` recompense l'ennemi qu'elle a tue ;
#   - `sf009` elle-meme se remet de cote apres avoir brule.
# HUIT cartes sur seize la posent, la lisent ou la recyclent.
#
# ⚠⚠ « PERMANENT » N'EST PAS UN OBSTACLE ICI, C'EST LE MECANISME.
# `HasPermanent.OnWhenCardLeavePlay` (has_permanent.py:16-35) bloque la sortie
# de jeu d'une carte Permanente **SAUF si l'effet qui la fait sortir vient du
# MEME `set_name`** (ligne 34 : `elif self.paper.set_name != by_effect.this
# .paper.set_name: return False`). Burning porte `set_name = "Sunfire"` :
# aucune carte du VILAIN ne peut donc la retirer, et toutes les cartes de
# Sunfire le peuvent. C'est exactement ce que le texte imprime veut dire, et
# le moteur le rend NATIVEMENT.
# ⚠ Corollaire a ne pas oublier : un helper appele depuis une carte d'un autre
# set echouerait en silence. Tout le pack passe donc par `RemettreDeCote`.
#
# ⚠ HOMONYMES :
#  - « * Sunfire » est DEJA `35014`, un ALLIE du pack wolverine. Les cartes du
#    pack qui nomment le heros passent par le TYPE ou par `"YourHero"`.
#  - « Hot Pursuit » est DEJA `24058`, une manigance annexe du set State of
#    Emergency. Le texte francais s'ecrit sur le `card_id`.
#  - « Burning » n'a aucun homonyme, mais SIX exemplaires : jamais de
#    `FindCardOnField(name=...)` qui n'en rendrait qu'un.
#
# ⚠ LES TRAITS `HAND` ET `NINJA` SONT NEUFS AU DEPOT (0 carte avant ce pack).
# Un trait ne se declare nulle part, il vit dans `traits` : rien a enregistrer,
# mais `sf011` Hand Ambush est la SEULE carte qui lit `HAND`, et elle lit le
# trait de ses propres sbires.
# ===========================================================================

NOM_HEROS = "Sunfire"
NOM_ALTER_EGO = "Shiro Yoshida"
NOM_BRULURE = "Burning"
SET_HEROS: 'CardFace.SETNAMES' = "Sunfire"

# « begins the game with 6 Burning upgrades set aside » — imprime sur sf001b.
BRULURES_MISES_DE_COTE = 6


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit.

    ⚠ NE PAS se rabattre sur `effect.GetInitiator()` en premier : il leve un
    assert quand l'initiateur n'est pas un joueur, et le moteur AVALE
    l'exception (lecon `Player.GetHero()`, pack lady_sif).

    ⚠ Passer le joueur EXPLICITEMENT depuis une carte de RENCONTRE : c'est le
    cas du set nemesis et de l'obligation `sf010` (lecon yd013 / dr010 /
    tt020 / br012 / tg011 / sn011).
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


def HerosDuJoueur(effect: 'Effect', joueur: 'Player|None' = None) -> 'CardFace|None':
    """La face HEROS (« Sunfire »), ou None si le joueur est en civil.

    ⚠ LE FILTRE EST LE TYPE, JAMAIS LE NOM : `35014` * Sunfire est un ALLIE du
    pack wolverine, et un `CardFinder(name="Sunfire")` l'attraperait.
    """
    if joueur is None:
        joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return None
    identite = joueur.GetIdentity()
    if identite is None or not Hero.IsType(identite):
        return None
    return identite


def Hote(face: 'CardFace|None') -> 'CardFace|None':
    """A QUI cette carte est-elle accrochee ? `None` si elle ne l'est pas.

    Accesseur SUR, a employer partout a la place de `GetBindFace()`.
    Modele `blink` et `yondu`, les deux autres packs de la brique 6.
    """
    return getattr(face, "bind_face", None) if face is not None else None


def BrulureDeCote(effect: 'Effect', joueur: 'Player|None' = None) -> 'CardFace|None':
    """UNE copie de Burning encore dans la reserve, ou None s'il n'en reste pas.

    ⚠ « a SET-ASIDE copy of Burning » : la reserve, pas le deck ni la
    defausse. Le moteur l'appelle `set_aside_deck`, alias de
    `additional_discard_pile` — c'est la que `BeginGameWithSetAside` depose
    les six exemplaires (setup.py:68).

    ⚠ SIX EXEMPLAIRES, DONC JAMAIS `FindCardOnField(name=...)` : on ne cherche
    pas « la » Burning, on en prend « une ».
    """
    if joueur is None:
        joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return None
    for face in list(joueur.set_aside_deck.GetAll()):
        if face is not None and face.IsName(NOM_BRULURE):
            return face
    return None


def AttacherUneBrulure(effect: 'Effect', cible: 'CardFace|None',
                       joueur: 'Player|None' = None) -> bool:
    """« attach a set-aside copy of Burning to <cible> » — SEUL point d'entree.

    Tout le pack passe par ici, et c'est voulu : `sf004` Hot Pursuit se
    declenche « after you ATTACH a copy of Burning to an enemy », et elle
    ecoute le message `AfterCardAttachTo` que seul `AttachTo2` emet. Un module
    qui poserait la brulure autrement priverait `sf004` de son declencheur.

    ⚠ `AttachTo2` fait TOUT : il sort la carte de la reserve et l'accroche.
    Modele `Find.FindAndAttachTo` (find.py:91-93), qui ne fait rien d'autre.

    ⚠ « to an ENEMY » : on refuse tout le reste. Une brulure sur une manigance
    n'a aucun sens — ses deux Reponses forcees parlent d'« attached ENEMY ».
    """
    if cible is None or not Enemy.IsType(cible):
        return False
    brulure = BrulureDeCote(effect, joueur)
    if brulure is None:
        return False
    return brulure.AttachTo2(cible, effect)


def RemettreDeCote(effect: 'Effect', face: 'CardFace|None',
                   joueur: 'Player|None' = None) -> bool:
    """« Set this card aside. » — SEUL point d'entree.

    ⚠ C'EST ICI QUE « PERMANENT » SE JOUE. `HasPermanent.OnWhenCardLeavePlay`
    (has_permanent.py:34) refuse la sortie de jeu d'une carte Permanente des
    que `by_effect.this.paper.set_name` differe du sien. `effect` doit donc
    TOUJOURS venir d'une carte du set « Sunfire » — ce qui est le cas de
    toutes celles qui appellent ce helper, Burning elle-meme en tete.
    C'est aussi ce qui rend la brulure inarrachable par le vilain, et c'est le
    sens du mot-cle sur cette carte.
    """
    if face is None:
        return False
    if joueur is None:
        joueur = face.GetControlByOrOwner()
        if not Player.IsType(joueur):
            joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return False
    Faces.MoveAllTo([face], joueur.set_aside_deck, effect)
    return True


def BrulureSur(effect: 'Effect', cible: 'CardFace|None') -> 'CardFace|None':
    """La copie de Burning accrochee a CET ennemi, ou None."""
    if cible is None:
        return None
    for face in list(cible.GetAttachedUpgrades()):
        if face is not None and face.IsName(NOM_BRULURE):
            return face
    return None


def EnnemisEnFeu(effect: 'Effect') -> List['CardFace']:
    """Tous les ennemis du terrain qui portent une copie de Burning.

    ⚠ On balaie les ENNEMIS et on regarde ce qu'ils portent, jamais l'inverse :
    une amelioration attachee a un ennemi ne vit PAS la ou vivent les
    ameliorations du joueur, `GetControlUpgrade` ne la voit pas. Meme lecon
    que la Yaka Arrow de `yondu` et les PORTAL de `blink`.
    """
    return [e for e in Worlds.GetOnFieldEnemies(effect)
            if BrulureSur(effect, e) is not None]


def AttachementAvecActionDeHeros(face: 'CardFace') -> bool:
    """« an attachment with the text "Hero Action" or "Hero Response" ».

    ⚠ BRIQUE 3 DU PLAN DE PORTAGE : selection d'une carte par son TEXTE.
    Aucune primitive moteur — on lit `face.paper.text`. 132 attachements du
    depot en portent : ce sont exactement ceux qu'on peut normalement PAYER
    pour defausser, et le pack de Sunfire les brule au lieu de les payer.
    Meme lecture que `bc004` et `bc010` (pack black_cat), ecrite la veille.
    """
    if face is None or not Attachment.IsType(face):
        return False
    texte = getattr(face.paper, "text", "") or ""
    return "Hero Action" in texte or "Hero Response" in texte


def BrulerOuArracher(effect: 'Effect', cible: 'CardFace|None',
                     joueur: 'Player|None' = None) -> bool:
    """« <choisir un attachement...> et le defausser. SINON, poser une Burning. »

    Le corps commun de `sf003` Burning Hands et `sf005` Solar Blast, a une
    difference pres que l'appelant tranche : `sf005` ne regarde QUE les
    attachements de l'ennemi vise (« attached to that enemy »), `sf003`
    regarde TOUS ceux du terrain (son texte ne restreint pas).

    ⚠ « OTHERWISE » N'EST PAS UN CHOIX : le repli tombe quand il n'y a AUCUN
    attachement eligible. Mot-piege releve a l'etape 5, et deja paye sur
    `sn013`.

    Rend True si un attachement a ete arrache, False si on a pose une brulure.
    """
    candidats = [f for f in (cible if isinstance(cible, list) else [])
                 if AttachementAvecActionDeHeros(f)]
    if joueur is None:
        joueur = JoueurDeCetteCarte(effect)
    if candidats and joueur is not None:
        choisi = joueur.AskChooseFace(candidats, effect)
        if choisi is not None:
            Faces.DiscardAll([choisi], effect)
            return True
    return False
