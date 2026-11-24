from cards.pack import *

# Helpers partages du set « Quasar » (Galactic Storm, Kajislav).
#
# Tout le kit tourne autour d'UNE carte, gs301 * Quantum Bands (amelioration
# PERMANENTE posee au Setup par gs300b, « Hero Resource: Exhaust → generate a
# [wild] resource ») :
#  - trois cartes la REDRESSENT (gs300a Channel the Bands, gs302 Epoch,
#    gs311 Quantum Energy) ;
#  - cinq cartes reagissent a un paiement FAIT AVEC elle (gs309 Unbreakable
#    Guard, gs313 Quantum Absorption, gs315 Quantum Jump, gs316 Quantum
#    Weapon, gs349 Quantum Bubble).
#
# « Pay for X with Quantum Bands » : sa capacite de ressource, en jeu, est un
# `CanGenerateResources` ; quand elle paie, le moteur envoie
# `Message.WhenCardBeSpendAsResource(face=Bandes, res, for_effect, joueur)`
# (factory/resources.py, `generate_resource`), dont `pay_for_card` est la carte
# JOUEE (None si le paiement finance une capacite qui n'est pas un « jouer »).
# Apres coup, l'effet paye garde la liste de ses payeurs dans
# `effect.context.paid_this_res_effects` (`.this` = la carte qui a paye).

NOM_BANDES = "Quantum Bands"


def EstLesBandes(face: 'CardFace|None') -> bool:
    """Vrai pour LA carte Quantum Bands (par son NOM imprime, sans l'etoile
    d'unicite : RECETTES §6, un `* ` dans un nom cherche ne trouve rien)."""
    return face is not None and Upgrade.IsType(face) and face.IsName(NOM_BANDES)


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur qui controle (ou possede) la carte qui agit.

    ⚠ Pas `effect.GetInitiator()` en premier : il leve un assert quand
    l'initiateur n'est pas un joueur, et le moteur avale l'exception (lecon
    lady_sif, meme helper que ares / night_thrasher)."""
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        joueur = porteur.GetControlByOrOwner()
        if Player.IsType(joueur):
            return joueur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None


def BandesDe(joueur: 'Player|None') -> 'Upgrade|None':
    """Les Quantum Bands EN JEU sous le controle de `joueur` (ou None)."""
    if joueur is None:
        return None
    for face in joueur.GetControlCardsByType(upgrade=True):
        if EstLesBandes(face) and face.IsInPlay():
            return face.CastTo(Upgrade)
    return None


def BandesInclinees(effect: 'Effect') -> bool:
    """Condition des « ready Quantum Bands » : une capacite ne s'initie que si
    son effet peut changer l'etat du jeu (Rules Reference) ; des Bandes
    absentes ou deja pretes ne le permettent pas."""
    bandes = BandesDe(JoueurDeCetteCarte(effect))
    return bandes is not None and not bandes.IsReady()


def RedresserLesBandes(effect: 'Effect') -> bool:
    bandes = BandesDe(JoueurDeCetteCarte(effect))
    if bandes is None or bandes.IsReady():
        return False
    Faces.ReadyAll([bandes], effect)
    return True


def PayeeAvecLesBandes(effect: 'Effect') -> bool:
    """« If you paid for this card with Quantum Bands » : lu APRES le paiement,
    sur la liste des payeurs de l'effet joue (modele `jennika/tj004`)."""
    return any(EstLesBandes(e.this) for e in effect.context.paid_this_res_effects)


def BandesPaient(effect: 'Effect', message: 'Message.WhenCardBeSpendAsResource', finder: 'CardFinder|None') -> bool:
    """Condition des Interruptions / Reponses « When / After you pay for <X>
    with Quantum Bands » : le message vient des Bandes du MEME joueur que la
    carte qui reagit, et la carte payee (`pay_for_card`) passe le filtre."""
    joueur = JoueurDeCetteCarte(effect)
    if joueur is None or message.GetToPlayer() != joueur:
        return False
    if not EstLesBandes(message.trigger):
        return False
    carte = message.pay_for_card
    if carte is None:
        return False
    return finder is None or finder.Check(carte)


def QuandLesBandesPaient(ability_type: 'AbilityType', finder: 'CardFinder|None',
                         operation: Callable[['Effect', 'Message.WhenCardBeSpendAsResource'], None]) -> 'Ability':
    """« Hero Interrupt / Response: When / After you pay for <X> with Quantum
    Bands, ... » : fenetre ouverte par le paiement des Bandes elles-memes
    (`WhenCardBeSpendAsResource`, envoye par `generate_resource` APRES que les
    Bandes ont paye leur cout d'inclinaison). Fabrique `AfterGenerateResources`
    (factory/resources.py), seul point d'ecoute de ce message. Le filtre va dans
    `conditions` et JAMAIS dans le corps (RECETTES §1 : sinon la question est
    posee au joueur a chaque paiement)."""
    return AbilityFactory.AfterGenerateResources(
        ability_type,
        "You",
        operation,
        conditions=[lambda effect, message: BandesPaient(effect, message, finder)],
    )


def BandesPeuventPayer(joueur: 'Player|None') -> bool:
    """Avant tout paiement : les Bandes sont-elles en etat de payer ? (en jeu,
    pretes, et identite en forme HEROS : « Hero Resource »)."""
    bandes = BandesDe(joueur)
    return bandes is not None and bandes.IsReady() and Hero.IsType(joueur.GetIdentity())


def RienPayeEncore(effect: 'Effect') -> bool:
    """Vrai tant que l'effet n'a encore rien paye (phase de CIBLAGE : le moteur
    choisit les cibles avant le paiement, effect_checker `check_target` puis
    `check_pay`).

    ⚠ Pas `paid_this_resources.val == 0` : ce champ n'est PAS remis a zero
    entre deux activations (effect_context.py, absent de
    `ResetAfterOperation`) ; la liste des payeurs, elle, l'est."""
    return effect.context.paid_this_res_effects == []
