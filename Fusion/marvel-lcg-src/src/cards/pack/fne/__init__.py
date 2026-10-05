from cards.pack import *

def DiscountAbility(value: int, traits: Sequence['CardFace.TRAITS']) -> 'Ability':
    def check_control_trait(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        player = effect.this.GetControlByOrOwner()
        if not Player.IsType(player):
            return False
        for face in Worlds.FindCardsOnField(effect):
            if (face.GetControlBy() == player) and any(face.HasTrait(t) for t in traits):
                return True
        return False
    return AbilityFactory.ReduceCostToPlayThis(value, conditions=[check_control_trait])


def PeutCouvrirLeCout(joueur: 'Player', effect: 'Effect', cout: 'Cost') -> bool:
    """« You may spend X resources to ... Otherwise, ... » : la branche payante
    ne doit etre OFFERTE que si le joueur peut la payer, sinon le moteur la
    propose seule (Otherwise ne sort que quand aucune autre option n'existe),
    le paiement echoue et la carte ne fait rien. Mesure sur 60127 Tug of War
    (18/09/2026) : « couvert = 2 » sur un cout RRR, et pas d'Otherwise.

    On interroge les memes sources que `EffectChecker.UpdatePayResources`
    (message CheckPlayerCanPayCost) et on additionne ce qu'elles generent ;
    `Resources.CanPayThisCost` tranche, wild compris.
    """
    # ⚠⚠ NE PAS envoyer `Message.CheckPlayerCanPayCost` depuis une condition de
    # ChooseAbility : l'effet de choix n'a pas de couts calcules
    # (`cost_for_different_target` vide) et chaque carte en main qui repond au
    # message plante dans `add_to_pay_list` (« KeyError: None »,
    # resources.py:216). Vu par l'autoplay du 18/09/2026 (5 a 7 tracebacks par
    # partie), jamais par le harnais. On lit donc les icones IMPRIMEES de la
    # main et de la reserve, ce qui couvre le cas courant ; les generateurs en
    # jeu (supports a ressource) ne sont pas comptes : ecart assume, note au
    # gabarit de 60127.
    faces = list(joueur.hand_cards.Get()) + list(joueur.reserve.Get())
    total = FacesCounter.GetPrintedResources(faces)
    # ⚠ `Resources.CanPayThisCost` ne teste que la COULEUR (rbyg.py:110) : un
    # cout « 2 » y passe avec une seule carte. On exige aussi la QUANTITE.
    return total.CanPayThisCost(cout) and total.val >= cout.rbyga.total


def RetournerLAttachement(this: 'Attachment', effect: 'Effect', *, call_reveal: bool=True) -> None:
    """Retourne un attachement recto-verso SANS le perdre (Adamantium-Laced
    Spine, Out Front / Alongside, Mary Walker...). `card.Flip` DETACHE la carte
    (CanAttach.OnBeforeFlip -> DetachFrom2 -> MarkAsRemoved) et ne la raccroche
    (OnAfterFlip) que si sa zone est encore la zone d'ameliorations, ce qui
    n'est plus le cas : la face B restait dans les limbes (harnais du
    18/09/2026, RECETTES-MOTEUR §7quater). On memorise le porteur, on demarque
    la carte et on rejoue l'accrochage. `call_reveal` : la face qui apparait
    resout son When Revealed (Alongside, FAQ du livret)."""
    hote = this.GetBindFace()
    this.card.Flip(effect, call_reveal=call_reveal)
    nouvelle = this.card.face
    if hote is None or nouvelle is None:
        return
    carte = nouvelle.card
    carte.area.UnMarkAsRemoved(carte)
    nouvelle = nouvelle.CastTo(Attachment)
    if nouvelle.GetBindFace() is hote:
        nouvelle.AttachTo2(hote, effect)
        if not carte.state.is_attached:
            nouvelle.OnAttachTo(hote, True)
    else:
        nouvelle.AttachTo2(hote, effect)

def KingpinEnJeu(effect: 'Effect') -> 'Enemy|None':
    """« If Kingpin is in play » : le SBIRE Kingpin (nemesis d'Echo) OU le VILAIN
    Kingpin du scenario The King's Gambit.

    ⚠ `card_type=Minion` seul ne voit jamais le vilain, et dans ce scenario le
    sbire est justement retire du jeu par le Setup : « Pawn of the Kingpin »
    prenait surge au lieu de faire comploter Kingpin, et « Master Manipulator »
    en boost ne se revelait pas (signalement n°55, 04/10/2026). Regle choisie
    par l'utilisateur : le vilain compte, il s'appelle Kingpin et il est en jeu.
    """
    return (Worlds.FindCardOnField(effect, name='Kingpin', card_type=Minion)
            or Worlds.FindCardOnField(effect, name='Kingpin', card_type=Villain))
