from cards.pack import *

# ===========================================================================
# ZEUS (Mozilla, set 171, prefixe `ze`) — helpers partages du pack.
#
# Le pack tourne autour de DEUX choses, et le set nemesis vise les deux :
#
# 1. L'ECLAIR, une RESSOURCE MAISON (cinquieme couleur du moteur, lettre `L`,
#    ajoutee le 11/09/2026, fiche docs/reference/mots-cles/eclair.md). Elle
#    n'a que deux sources : les quatre Thunder Strike (`ze003`), qui la portent
#    imprimee, et Mount Olympus (`ze011`), qui transforme une energie en
#    eclair. *Skyfather's Tempest* exige de payer un meme evenement avec une
#    ENERGIE officielle ET un ECLAIR.
#
# 2. Les capacites « Special ». Sept cartes du set heros en portent une. Elles
#    ne partent JAMAIS en jouant la carte : c'est le Tempest qui les resout au
#    paiement, Hera (`ze002`) qui en resout une depuis la main, et Skyfather
#    (`ze009`) qui en DONNE une aux evenements qui n'en ont pas.
#
# Vocabulaire, arrete avec l'utilisateur le 11/09/2026 : « energie » = la
# ressource officielle jaune (`Y`), « eclair » = la ressource maison (`L`).
# ===========================================================================

TEMPEST = "Skyfather's Tempest"
GOD_OF_LIGHTNING = "God of Lightning"
ALCOHOL_PROBLEMS = "Alcohol Problems"
SKYFATHER = "Skyfather"
THUNDER_STRIKE = "Thunder Strike"
THUNDERBOLT = "Thunderbolt"
COMPTEUR_EGIDE = 'aegis'


def APrintedSpecial(face: 'CardFace') -> bool:
    """« a printed "Special" ability » : la carte DECLARE une capacite Special.

    ⚠ On lit `face.ability` (les capacites declarees par le module, donc
    imprimees), pas `face.effect` (les effets ENREGISTRES, qui dependent de la
    zone ou se trouve la carte). Hera choisit dans la MAIN, Total Eclipse
    regarde des cartes DEFAUSSEES : il faut une lecture qui ne depende pas de
    la zone. Et « printed » exclut le Special que Skyfather DONNE.
    """
    if face is None:
        return False
    return bool(face.ability.Find(type=AbilityType.Special))


def SkyfatherDe(joueur: 'Player', effect: 'Effect') -> "CardFace|None":
    """Le Skyfather (`ze009`) en jeu et controle par ce joueur, ou None."""
    for face in Worlds.FindCardsOnField(effect, name=SKYFATHER, card_type=Upgrade):
        if face.GetControlBy() is joueur:
            return face
    return None


def ResoudreLeSpecialDe(face: 'CardFace', joueur: 'Player', effect: 'Effect') -> bool:
    """Resout « the "Special" ability on that card », Skyfather compris.

    Deux cas, dans cet ordre :
    - la carte a un Special IMPRIME : `ResolveSpecialAbility`, la brique du
      moteur (card_face.py:906), qui envoie `WhenResolveSpecialAbility` a la
      carte ;
    - sinon, si c'est un EVENEMENT que le joueur POSSEDE et que son Skyfather
      est en jeu : « Special: Deal 2 damage to an enemy », le Special que
      Skyfather donne a chaque evenement sans Special imprime.

    ⚠ POURQUOI SKYFATHER NE « DONNE » PAS VRAIMENT UNE CAPACITE. Le moteur
    n'a pas de fabrique qui greffe une capacite sur les cartes d'un autre
    proprietaire (main, deck, defausse compris), et `ResolveSpecialAbility`
    ne fait rien quand `effect.Find(type=Special)` est vide. Le seul endroit
    ou ce Special peut etre resolu, ce sont les deux appelants de ce pack
    (Tempest et Hera) : on le rend donc ICI, au moment de resoudre. Hera
    exige un Special « printed » et Total Eclipse aussi : eux ne voient pas
    celui de Skyfather, et c'est conforme au texte.

    Rend True si un Special a ete resolu.
    """
    if face is None:
        return False
    if APrintedSpecial(face):
        # ⚠ `ResolveSpecialAbility` cherche les effets ENREGISTRES de la carte
        # (`effect.Find`), et une carte en MAIN n'en a aucun : le message ne
        # partait pas, « Zeus resolves Thunder Strike's » suivi de rien (vu au
        # premier passage du harnais, 11/09/2026). On enregistre donc le
        # Special le temps de le resoudre, comme un effet temporaire.
        if not face.effect.Find(type=AbilityType.Special):
            face.effect.RegisterTemp(*face.ability.Find(type=AbilityType.Special),
                                     unregister_after_exec=True)
        face.ResolveSpecialAbility(joueur, effect)
        return True
    if not Event.IsType(face) or face.GetOwner() is not joueur:
        return False
    skyfather = SkyfatherDe(joueur, effect)
    if skyfather is None:
        return False
    ennemis = Worlds.FindCardsOnField(effect, card_type=Enemy)
    if not ennemis:
        return True
    cible = joueur.AskChooseFace(ennemis, effect)
    if cible:
        # ⚠ Pas `skyfather.DealDamage` : une amelioration ne peut infliger des
        # degats que dans SON propre effet (upgrade.py:68, assert). Les degats
        # partent de la carte qui resout (Zeus pour le Tempest, Hera).
        effect.this.DealDamage([cible], 2, effect)
    return True


def AlcoholProblemsDe(joueur: 'Player', effect: 'Effect') -> "CardFace|None":
    """L'obligation Alcohol Problems (`ze012`) en jeu chez ce joueur, ou None.

    Tant qu'elle est la, « Zeus cannot resolve his Skyfather's Tempest
    ability » : c'est le Tempest (`ze001a`) qui la consulte dans ses
    conditions, l'obligation elle-meme n'a rien a intercepter.
    """
    # ⚠ Une obligation revelee va dans `obligations_area` du joueur
    # (obligation.py:96, `OnPutIntoPlay`), une zone que `Worlds.FindCardsOnField`
    # ne balaie pas depuis l'effet du heros (vu au harnais le 11/09/2026 : la
    # carte etait « entered play » et introuvable). On lit la zone elle-meme.
    if joueur is None:
        return None
    for face in joueur.obligations_area.Get():
        if getattr(face.paper, "name", "") == ALCOHOL_PROBLEMS:
            return face
    return None


def PaieEnergieEtEclair(res: 'Resources') -> bool:
    """« spend both [energy] and [lightning] resources » sur un meme paiement.

    Un joker vaut n'importe quelle couleur (decision de l'utilisateur,
    11/09/2026, et defaut du moteur), mais UNE ressource n'a qu'UNE couleur :
    un seul joker ne peut pas etre a la fois l'energie et l'eclair. D'ou les
    trois inegalites : de quoi faire une energie, de quoi faire un eclair, et
    au moins deux ressources parmi celles-la.
    """
    y = res.GetColor("Y", convert_green_res=False)
    l = res.GetColor("L", convert_green_res=False)
    g = res.GetColor("G", convert_green_res=False)
    return y + g >= 1 and l + g >= 1 and y + l + g >= 2


def ChoisirUnEnnemi(joueur: 'Player', effect: 'Effect') -> "CardFace|None":
    """« an enemy » choisi par le joueur, ou None s'il n'y en a aucun."""
    ennemis = Worlds.FindCardsOnField(effect, card_type=Enemy)
    if not ennemis:
        return None
    return joueur.AskChooseFace(ennemis, effect)
