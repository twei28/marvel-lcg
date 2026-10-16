from cards.pack import *

# ===========================================================================
# Helpers partages du set « Raphael » (Inkwire, TMNT Heroes, prefixe `tr`).
# Decisions de l'utilisateur : .planning/tmnt/decisions-phase-b.md (fait loi).
#
# MECANIQUE CENTRALE : le compteur `rage`, pose sur la CARTE d'identite (les
# deux faces, Raphael et Raph, partagent le meme stock de compteurs).
#  - `tr001a` : chaque compteur se depense comme une ressource [physical]
#    (modele `30001a` * Spider-Ham, compteur `toon` -> ressource wild).
#  - PLAFOND DE 3 PARTOUT : Raphael est limite a 3 compteurs de rage au
#    maximum, quelle que soit la source (Yaban Hito `tr001a`, Casey Jones
#    `tr002`, Seething Rage `tr007`, Gekido `tr010`, Sai `tr011`/`tr012`) :
#    `PLAFOND_PARTOUT = True`. DECISION DU 16/10/2026, qui REMPLACE celle du
#    15/10 (plafond seulement ou imprime).
#  - « Raphael » en forme CIVILE (`tr002`, `tr007`, `tr010`) : les effets visent
#    l'IDENTITE (soin, degats, rage sur la carte d'identite meme en alter-ego),
#    pas la seule face heros (decision du 15/10/2026) : voir
#    `IdentiteDuJoueur`.
#
# LES DEUX SAI (`tr011`, `tr012`) : chacune « fait gagner » une capacite a
# TOUTE amelioration [[SAI]] que le joueur controle, elle-meme comprise. Il
# n'existe que ces deux cartes SAI : plutot que de simuler un « gains » moteur
# (`GiveAbilityToInPlayWhenApplyThis` est concu pour les cartes de rencontre),
# CHAQUE Sai porte les DEUX capacites, chacune conditionnee a la presence de
# la carte qui la donne (`SaiEnJeu`). Resultat observable identique : deux Sai
# en jeu = deux Actions d'attaque et deux Reponses de pioche, une par carte.
# L'encart « Sai Weapon Rules » fait loi : chaque usage d'une Sai = action
# d'attaque + 1 rage (max 3).
# ===========================================================================

NOM_HEROS = "Raphael"
NOM_ALTER_EGO = "Raph"
RAGE = 'rage'
PLAFOND_RAGE = 3
TRAIT_SAI = "SAI"
ID_SAI = "tr011"        # Raphael's Sai : donne l'Action d'attaque
ID_AUTRE_SAI = "tr012"  # Raphael's Other Sai : donne la Reponse qui fait piocher

# True = Raphael ne depasse jamais 3 rage (decision du 16/10/2026, remplace
# celle du 15/10 : plafond seulement ou imprime).
PLAFOND_PARTOUT = True


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (modele sunfire).

    ⚠ NE PAS se rabattre sur `effect.GetInitiator()` en premier : il leve un
    assert quand l'initiateur n'est pas un joueur, et le moteur AVALE
    l'exception. Pour une carte de RENCONTRE ou l'obligation `tr013`, passer
    le joueur explicitement.
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


def IdentiteDuJoueur(effect: 'Effect', joueur: 'Player|None' = None) -> 'CardFace|None':
    """L'IDENTITE du joueur (Raphael OU Raph) : la cible de « Raphael ».

    Decision du 15/10/2026 : les effets qui nomment « Raphael » (soin, degats,
    rage) visent l'identite, meme quand le joueur est en forme civile. Les
    compteurs de rage vivent sur la carte d'identite, partagee par les deux faces.
    """
    if joueur is None:
        joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return None
    return joueur.GetIdentity()


def HerosDuJoueur(effect: 'Effect', joueur: 'Player|None' = None) -> 'CardFace|None':
    """La face HEROS (« Raphael »), ou None si le joueur est en civil.

    ⚠ LE FILTRE EST LE TYPE, JAMAIS LE NOM.
    """
    if joueur is None:
        joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return None
    identite = joueur.GetIdentity()
    if identite is None or not Hero.IsType(identite):
        return None
    return identite


def PlacerRage(effect: 'Effect', joueur: 'Player|None' = None, *,
               plafonne: bool = True) -> int:
    """« Place 1 rage counter on Raphael [(to a maximum of 3)]. »

    `plafonne=True` seulement la ou le texte imprime « to a maximum of 3 ».
    La rage se pose sur l'IDENTITE, quelle que soit sa forme. Rend le nombre
    de compteurs effectivement poses.
    """
    identite = IdentiteDuJoueur(effect, joueur)
    if identite is None:
        return 0
    maximum = PLAFOND_RAGE if (plafonne or PLAFOND_PARTOUT) else None
    place = Faces.PlaceCountersOn([identite], 1, RAGE, effect, maximum=maximum)
    return int(place or 0)


def SaisSousControle(joueur: 'Player|None') -> List['CardFace']:
    """« a/each [[SAI]] upgrade you control »."""
    if joueur is None:
        return []
    return [f for f in joueur.GetControlUpgrade()
            if f is not None and f.HasTrait(TRAIT_SAI)]


def SaiEnJeu(joueur: 'Player|None', card_id: str) -> bool:
    """La Sai `card_id` est-elle en jeu sous le controle de `joueur` ?

    Sert de condition aux capacites « gagnees » (voir l'en-tete).
    """
    for face in SaisSousControle(joueur):
        paper = getattr(face, "paper", None)
        if paper is not None and paper.card_id == card_id:
            return True
    return False


def AttachementAvecActionDeHeros(face: 'CardFace') -> bool:
    """« an attachment with the text "Hero Action" or "Hero Response" ».

    Selection par le TEXTE imprime (aucune primitive moteur) : meme lecture que
    `sunfire/__init__.py` (`bc004`, `bc010`).
    """
    if face is None or not Attachment.IsType(face):
        return False
    texte = getattr(face.paper, "text", "") or ""
    return "Hero Action" in texte or "Hero Response" in texte


# ---------------------------------------------------------------------------
# Capacites « gagnees » par chaque Sai (voir l'en-tete). Les deux cartes SAI
# les portent TOUTES LES DEUX, conditionnees a la carte qui les donne.
# ---------------------------------------------------------------------------

def CapaciteAttaqueSai() -> 'Ability':
    """Donnee par `tr011` Raphael's Sai a chaque amelioration SAI :

    « Hero Action (attack): Exhaust this card and take 1 damage -> deal 1
    damage to an enemy. »

    ⚠ L'ENCART DE REGLES du zip ajoute : c'est une action d'ATTAQUE, et il faut
    poser 1 rage sur Raphael (max 3) a chaque usage. Les degats pris en COUT ne
    sont pas « from an attack », Yaban Hito ne part donc pas : la rage est
    posee ICI, a la main (decision du 15/10/2026 : l'encart fait loi).
    ⚠ Les degats sont infliges par le HEROS (`hero.DealDamage`) : c'est ce qui
    fait de Raphael l'auteur pour « After Raphael defeats an enemy » (`tr012`).
    """
    def attaque_a_la_sai(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        heros = IdentiteDuJoueur(effect, joueur)
        cibles = [t for t in effect.targets if t is not None]
        if heros is not None and cibles:
            heros.DealDamage(cibles, 1, effect)
        PlacerRage(effect, joueur, plafonne=True)

    def donnee_par_la_sai_principale(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        return SaiEnJeu(JoueurDeCetteCarte(effect), ID_SAI)

    return (AbilityFactory.WhenInYourPlayTurn(
                AbilityType.HeroAction,
                attaque_a_la_sai,
                conditions=[donnee_par_la_sai_principale],
            ).SetLabel('attack')
            .SetTarget(Enemy)
            .SetCostFunc(CostFunc.Exhaust("This"))
            .SetCostFunc(CostFunc.TakeDamage(1, "YourIdentity")))


def CapaciteReponseSai() -> 'Ability':
    """Donnee par `tr012` Raphael's Other Sai a chaque amelioration SAI :

    « Hero Response: After Raphael defeats an enemy, exhaust this card -> draw
    1 card. »

    ⚠ « AFTER RAPHAEL defeats an enemy » : tout ennemi (vilain OU sbire) vaincu
    par le HEROS, attaque ou non (pas de `is_from_attack`). L'encart precise
    que le joueur peut utiliser UNE Sai OU LES DEUX pour un meme ennemi : chaque
    Sai a sa propre Reponse et sa propre inclinaison, donc rien a coder de plus.
    """
    def piocher(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None:
            joueur.DrawUp(1, effect)

    def donnee_par_lautre_sai(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> bool:
        return SaiEnJeu(JoueurDeCetteCarte(effect), ID_AUTRE_SAI)

    return (AbilityFactory.AfterUnitDefeatedUnit(
                AbilityType.HeroResponse,
                "YourHero",
                Enemy,
                piocher,
                conditions=[donnee_par_lautre_sai],
            ).SetCostFunc(CostFunc.Exhaust("This")))
