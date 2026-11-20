from cards.pack import *

# Helpers partages du set « Warriors Three » (Phenexian et Mysteltainn, prefixe `wt`).
# ⚠ Un helper vit ICI, jamais dans le `__init__.py` du PACK (NameError avale, lecon hk005).

NOMS_HEROS = ("Fandral", "Hogun", "Volstagg")
ID_SOUTIEN = {"Fandral": "wt003", "Hogun": "wt004", "Volstagg": "wt005"}
ID_TITRE = "wt002"


def joueur_de(effect: 'Effect') -> 'Player|None':
    """Le joueur de l'effet : l'initiateur, ou le controleur de la carte (capacite passive)."""
    joueur = effect.GetInitiator()
    if joueur is None:
        try:
            joueur = effect.this.GetControlByPlayer()
        except Exception:
            joueur = None
    return joueur


def nom_du_heros_actif(joueur: 'Player|None') -> 'str|None':
    """« your active hero » : Fandral / Hogun / Volstagg quand l'identite est sur une face HEROS, sinon None (alter ego)."""
    if joueur is None:
        return None
    identite = joueur.GetIdentity()
    if identite is None or not Hero.IsType(identite):
        return None
    for nom in NOMS_HEROS:
        if identite.IsName(nom):
            return nom
    return None


def soutien(joueur: 'Player', nom: str) -> 'CardFace|None':
    """Le soutien PERSONA du heros `nom` (wt003-wt005), en jeu, ou None."""
    for face in joueur.GetControlCards(CardFinder(name=nom, card_type=Support)):
        if face.paper.card_id == ID_SOUTIEN[nom]:
            return face
    return None


def titre(joueur: 'Player') -> 'CardFace|None':
    """La carte-titre « The Warriors Three » (wt002), en jeu."""
    for face in joueur.GetControlCards(CardFinder(card_type=Upgrade)):
        if face.paper.card_id == ID_TITRE:
            return face
    return None


def inactif(nom: str):
    """Condition « ce heros n'est PAS le heros actif » (son soutien peut alors servir)."""
    def condition(effect: 'Effect', message=None) -> bool:
        return nom_du_heros_actif(effect.this.GetControlByPlayer()) != nom
    return condition


def soutiens_persona(joueur: 'Player') -> List['CardFace']:
    """Les soutiens PERSONA que le joueur controle ET qui sont vraiment des soutiens : le soutien du heros ACTIF
    n'en est pas un (ce heros est l'identite)."""
    actif = nom_du_heros_actif(joueur)
    trouves: List['CardFace'] = []
    for face in joueur.GetControlCards(CardFinder(card_type=Support)):
        if not face.HasTrait("PERSONA"):
            continue
        if actif is not None and face.paper.card_id == ID_SOUTIEN[actif]:
            continue
        trouves.append(face)
    return trouves


def paye_avec(effect: 'Effect', nom: str) -> bool:
    """« if you used <nom> to pay for this card » : les EFFETS qui ont paye (`context.paid_this_res_effects`), chacun
    porte sa carte sur `.this` (modele `MarteauAPaye`, beta_ray_bill). Le heros ACTIF est l'identite, un heros inactif son soutien :
    les deux se nomment pareil."""
    for res_effect in (getattr(effect.context, "paid_this_res_effects", None) or []):
        face = getattr(res_effect, "this", None)
        if face is not None and face.IsName(nom):
            return True
    return False


def changer_de_heros(effect: 'Effect') -> None:
    """« Change your active hero » : une AUTRE face HEROS de l'identite (changement de forme). Avec deux choix possibles, le
    joueur designe le heros (les trois faces se distinguent par leur NOM, pas par leurs traits, qui sont communs)."""
    joueur = joueur_de(effect)
    if joueur is None:
        return
    identite = joueur.GetIdentity()
    if identite is None or not Hero.IsType(identite):
        return
    autres = [f for f in joueur.GetAllIdentityFace(exclude=identite) if Hero.IsType(f)]
    if not autres:
        return
    if len(autres) == 1:
        cible = autres[0]
    else:
        # Ordre ALPHABETIQUE : les choix s'affichent toujours dans le meme ordre (et le pilote du harnais, qui prend le premier,
        # est deterministe : Fandral, Hogun, Volstagg).
        par_nom = {f.printed_name.lstrip("* ").strip(): f for f in autres}
        cible = par_nom[joueur.AskChooseOneText(sorted(par_nom))]
    identite.ChangeToFace(cible, effect)


def noter_le_heros_avant(effect: 'Effect', message=None) -> None:
    """AVANT tout changement de forme de l'identite : memorise le heros actif (ou None = alter ego). Lu par
    `synchroniser_formes` apres le changement ; auto-reparateur (un `Puzzle.ChangeToFace` silencieux de mise en place ne
    laisse donc aucun etat perime)."""
    joueur = effect.this.GetControlByPlayer()
    if joueur is not None:
        effect.this.wt_actif = nom_du_heros_actif(joueur)


def deplacer_cartes_d_etat(faces: 'List[CardFace]', source, destination) -> None:
    """Fait passer des cartes d'etat d'une zone d'etat a une autre (celle de l'identite <-> celle d'un soutien PERSONA)."""
    for face in list(faces):
        source.Remove(face.card)
        destination.Insert(-1, face.card)


def synchroniser_cartes_d_etat(effect: 'Effect', joueur: 'Player', identite: 'CardFace', avant: 'str|None', apres: 'str|None') -> None:
    """Notice de l'auteur (face B) : « Status cards on your inactive heroes will remain on them, but wont be relevant until they
    become the active hero » ; ceux de la carte The Warriors Three « remain on the card when it flips, but they are treated as if
    they were on your active hero ». Le moteur porte les etats sur l'IDENTITE, qui change de face : un heros qui devient inactif
    EMPORTE donc ses etats sur son soutien PERSONA (zone d'etat du soutien), et les retrouve en redevenant actif. Les etats
    de la carte-titre (ceux presents quand un heros devient actif, `wt_base_etats`) restent sur l'identite pour tous les heros."""
    this = effect.this
    zone_identite = identite.components.status.deck
    if avant is not None:
        sout = soutien(joueur, avant)
        base = getattr(this, "wt_base_etats", None) or []
        if sout is not None:
            deplacer_cartes_d_etat([f for f in zone_identite.GetAll() if f.card not in base], zone_identite, sout.components.status.deck)
    if apres is None:
        this.wt_base_etats = []
        return
    this.wt_base_etats = [f.card for f in zone_identite.GetAll()]
    sout = soutien(joueur, apres)
    if sout is None:
        return
    zone_soutien = sout.components.status.deck
    deplacer_cartes_d_etat(zone_soutien.GetAll(), zone_soutien, zone_identite)
    # Un personnage n'a qu'UNE carte Sonne / Desoriente / Etourdi, et au plus `tough_max` Tough : ce que la carte-titre portait deja
    # et ce que le heros a retrouve ne se cumulent pas.
    for nom, nombre, maximum in (("Stunned", identite.stunned, 1), ("Confused", identite.confused, 1), ("Dazed", identite.dazed, 1),
                                 ("Tough", identite.tough, identite.tough_max)):
        if nombre > maximum:
            identite.LoseState(nom, effect, nombre - maximum)


def donner_etat_a_un_heros(effect: 'Effect', joueur: 'Player', nom: str, etat: str) -> None:
    """« give <heros> a <etat> status card » : le heros ACTIF (l'identite) la porte, un heros inactif la garde sur son soutien."""
    if nom_du_heros_actif(joueur) == nom:
        Faces.GiveStatus([joueur.GetIdentity()], etat, effect)
        return
    sout = soutien(joueur, nom)
    if sout is not None:
        sout.components.status.GiveStatusCard(etat, effect)


def synchroniser_formes(effect: 'Effect', message=None) -> None:
    """Apres tout changement de forme de l'identite : chaque HEROS (et la carte-titre pour l'alter ego) garde SON etat
    pret/epuise, comme les cartes physiques qui se retournent (FAQ : « plusieurs activations de heros par tour »). L'etat de la
    face qui vient de PASSER ACTIVE est lu sur son soutien (ou sur la carte-titre pour l'alter ego) ; l'etat de l'identite
    d'AVANT va sur celui de l'ancienne. Les cartes d'etat suivent le heros : voir `synchroniser_cartes_d_etat` (26/10/2026)."""
    this = effect.this
    joueur = this.GetControlByPlayer()
    if joueur is None:
        return
    identite = joueur.GetIdentity()
    avant = getattr(this, "wt_actif", None)
    apres = nom_du_heros_actif(joueur)
    if avant == apres:
        return
    if identite is not None:
        synchroniser_cartes_d_etat(effect, joueur, identite, avant, apres)
    ancien = soutien(joueur, avant) if avant else this
    nouveau = soutien(joueur, apres) if apres else this
    this.wt_actif = apres
    if ancien is None or nouveau is None or identite is None:
        return
    pret_identite = identite.card.state.is_ready
    pret_nouveau = nouveau.card.state.is_ready
    ancien.card.state.is_ready = pret_identite
    identite.card.state.is_ready = pret_nouveau
