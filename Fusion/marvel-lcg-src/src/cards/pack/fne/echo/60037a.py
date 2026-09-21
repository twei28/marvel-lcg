from . import *

# * Echo (Maya Lopez), face heros.
#
# Watch and Learn — Response: After a player plays an aspect or basic event,
#   tuck that event under here from that player's discard pile. Then, if there
#   are more than 3 tucked cards here, discard all but 3 of those cards.
#
# Le reste du texte d'Echo est porte par Photographic Reflexes (60040a/b/c) :
#   « If you are in hero form, you can discard Photographic Reflexes from your
#     hand to play an event tucked under Echo as if it were in your hand.
#     Reduce the cost to play that event by 2. You cannot trigger Echo's
#     "Watch and Learn" ability for that event. »
#
# DEUX CHEMINS mènent au même état de jeu, et les deux sont voulus :
#  - chemin A : on clique sur Photographic Reflexes EN MAIN, le moteur demande
#    quel evenement glisse rejouer. C'est la lecture litterale du texte, et
#    c'est le module 60040a/b/c qui le porte (voir `__init__.py`).
#  - chemin B : on clique directement sur la carte glissee, qui est rendue
#    « comme en main » par `YouMayPlayCardLikeInHand` ci-dessous, et
#    Photographic Reflexes se defausse toute seule en consequence.
# La reduction de 2 vit a UN SEUL endroit (`reduire_le_cout_des_glissees`),
# pour que les deux chemins paient exactement la meme chose.


def GetAbilities() -> Sequence['Ability']:
    def watch_and_learn(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Hero)
        controller = this.GetControlByPlayer()
        face = message.played_face
        if not (face.card.area.flags.is_discards or face.IsInProcessingArea()):
            return
        this.TuckCardUnderHere(face, effect)
        placed = this.GetPlacedCardArea().Get()
        excess = (len(placed) - 3)
        if (excess > 0):
            def action(targets: Sequence['CardFace']):
                Faces.DiscardAll(list(targets), effect)
            controller.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Discard tucked cards down to 3', action).SetTarget(list(placed), range=(excess, excess), not_move=True))

    def check_aspect_event(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> bool:
        face = message.played_face
        if not IsAspectOrBasicEvent(face):
            return False
        # « You cannot trigger Echo's Watch and Learn ability for THAT event » :
        # l'evenement joue DEPUIS la zone glissee ne s'y remet pas. C'est la
        # seule facon de jouer une carte de cette zone, donc la clause de
        # Photographic Reflexes est tenue ici, pour les deux chemins.
        return (message.from_area != effect.this.GetPlacedCardArea())

    def check_tucked_playable(effect: 'Effect', message: 'Message.CheckIfFaceIsLikeInHand') -> bool:
        this = effect.this
        face = message.which_face
        if (face.card.area != this.GetPlacedCardArea()):
            return False
        initiator = effect.GetInitiator()
        if not initiator:
            return False
        if (initiator != this.GetControlByPlayer()):
            return False
        if not initiator.IsInHeroForm():
            return False
        return (initiator.hand_cards.FindCard(name='Photographic Reflexes') != None)

    def rafraichir_les_glissees(effect: 'Effect', message: 'Message2') -> None:
        """Vide le cache « cette carte est comme en main » des cartes glissees.

        ⚠ DEFAUT MESURE LE 21/09/2026, signalement n°17 (Yarro). La reponse de
        `check_tucked_playable` depend de DEUX choses qui bougent sans que la
        carte glissee ne bouge : la FORME du joueur, et la presence de
        Photographic Reflexes dans sa main. Or `card.can_state.is_like_in_hand`
        n'est remis a zero qu'au DEPLACEMENT de la carte (`card.py`, MoveToArea)
        : la toute premiere reponse etait donc figee pour toute la vie de la
        carte sous Echo.

        Mesure, sur une carte glissee en forme heros (harnais test_capacites) :
          forme heros   -> IsLikeInHand() = True   (juste)
          forme CIVILE  -> IsLikeInHand() = True   (FAUX : la carte reste offerte)
          retour heros  -> IsLikeInHand() = False  (FAUX : elle ne l'est plus)
        Le cache vide a la main rendait bien True / False / True.

        Meme piege, meme remede que Magik (`aoa/magik/45030a.py`, qui remet
        `is_like_in_hand` a None sur les cartes du dessus de son deck).

        On ne rafraichit que les cartes ENCORE dans la zone glissee : celle
        qu'on est en train de jouer l'a deja quittee pour la zone de
        resolution, et son drapeau force par `PlayCardsLikeInTurn` ne doit pas
        etre efface en plein vol.
        """
        zone = effect.this.GetPlacedCardArea()
        if zone is None:
            return
        for face in zone.Get(True):
            if face is not None:
                face.card.can_state.is_like_in_hand = None

    def check_reflexes_quitte_la_main(effect: 'Effect', message: 'Message.WhenCardWouldMoveToArea') -> bool:
        return message.from_area.flags.is_in_hand

    def discard_photographic_reflexes(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> None:
        """Chemin B : la carte glissee est cliquee, Photographic Reflexes part seule.

        ⚠ Rien a faire sur le chemin A : la carte y a deja ete defaussee comme
        COUT, et Echo en defausserait une SECONDE (voir `REFLEXES_DEJA_PAYEES`).
        """
        this = effect.this
        player = this.GetControlByPlayer()
        if player.flag.Get(REFLEXES_DEJA_PAYEES):
            return
        prs = [x for x in player.hand_cards.Get() if x.IsName('Photographic Reflexes')]
        if not prs:
            return
        if (len({x.paper.card_id for x in prs}) <= 1):
            Faces.DiscardAll([prs[0]], effect)
            return
        def action(targets: Sequence['CardFace']):
            Faces.DiscardAll(list(targets), effect)
        player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Discard a Photographic Reflexes', action).SetTarget(prs, range=(1, 1), not_move=True))

    def check_played_from_tuck(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> bool:
        return (message.from_area == effect.this.GetPlacedCardArea())

    def reduire_le_cout_des_glissees(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> None:
        message.UpdateCost(-2, effect)

    def check_cout_d_une_glissee(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        """« Reduce the cost to play that event by 2 ».

        ⚠ CORRIGE LE 21/09/2026. C'etait `CanGenerateResources(Resources('GG'))`
        : Echo offrait DEUX RESSOURCES WILD au lieu de reduire le cout. Le
        montant paye par la main est le meme dans le cas ordinaire, mais ce
        n'est pas la meme regle — deux wild couvrent une exigence de couleur
        (`Requirement`) qu'une reduction de cout laisse a payer, et elles
        comptent comme des ressources DEPENSEES pour toute carte qui lit le
        paiement. L'idiome du depot pour cette tournure exacte est
        `WhenCalculateEffectCost` + `UpdateCost` (dz014 Lightbringr, aa002
        Scarlet Witch, meme phrase imprimee).

        La condition est « la carte payee est dans la zone glissee », sans
        regarder la main : jouer une carte de cette zone n'est possible QUE par
        Photographic Reflexes (chemin A, ou PR est deja defaussee au moment du
        paiement ; chemin B, ou elle est encore en main). Une condition « PR en
        main » ferait donc sauter la reduction sur le chemin A, et la
        DOUBLERAIT sur le chemin A si le joueur tenait une seconde copie.
        """
        if not message.is_play:
            return False
        if message.check_effect is None:
            return False
        zone = effect.this.GetPlacedCardArea()
        paying_face = message.check_effect.this
        return zone is not None and paying_face is not None and paying_face.card.area == zone

    return [AbilityFactory.AfterPlayerPlayedCard(AbilityType.Response, 'AnyPlayer', None, watch_and_learn, conditions=[check_aspect_event]).SetName('Watch and Learn'),
            *AbilityFactory.YouMayPlayCardLikeInHand(AbilityType.NonKeyword, None, conditions=[check_tucked_playable]),
            AbilityFactory.WhenPlayerPlayCard(AbilityType.Rule, 'You', None, discard_photographic_reflexes, conditions=[check_played_from_tuck]),
            AbilityFactory.WhenCalculateEffectCost(AbilityType.NonKeyword, reduire_le_cout_des_glissees, conditions=[check_cout_d_une_glissee]).NoOutOfPlayLimit(),
            # Les trois rafraichissements du cache (voir `rafraichir_les_glissees`).
            AbilityFactory.AfterUnitChangeForm(AbilityType.Rule, 'You', rafraichir_les_glissees),
            AbilityFactory.AfterCardEnterHand(AbilityType.Rule, CardFinder(name='Photographic Reflexes'), rafraichir_les_glissees),
            AbilityFactory.WhenCardWouldMoveToArea(AbilityType.Rule, CardFinder(name='Photographic Reflexes'), rafraichir_les_glissees, conditions=[check_reflexes_quitte_la_main])]
