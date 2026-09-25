from cards.pack import *
ASPECT_OR_BASIC_CLASSES = ('Aggression', 'Justice', 'Leadership', 'Protection', 'Basic', "'Pool")
def IsAspectOrBasicEvent(face: 'CardFace') -> bool:
    if not Event.IsType(face):
        return False
    return face.IsClass(*ASPECT_OR_BASIC_CLASSES)
def GetPrintedCostValue(face: 'CardFace') -> int:
    value = face.paper.desc.get('Cost', '')
    value = str(value).replace('*', '')
    try:
        cost = int(value)
    except ValueError:
        return 0
    return max(cost, 0)


# ----------------------------------------------------------------------------
# Photographic Reflexes (60040a / 60040b / 60040c), les TROIS variantes.
#
# « [star] If you are in hero form, you can discard Photographic Reflexes from
#   your hand to play an event tucked under Echo as if it were in your hand.
#   Reduce the cost to play that event by 2. You cannot trigger Echo's
#   "Watch and Learn" ability for that event. »
#
# Meme texte sur les trois, seule l'icone de ressource change (Y / B / R, lue
# dans `desc`) : un seul constructeur, appele par les trois modules.
#
# ⚠ POURQUOI CE MODULE EXISTE (21/09/2026, signalement n°17 de Yarro).
# Jusqu'ici les trois modules etaient VIDES : toute la mecanique vivait sur
# Echo, qui rendait la carte GLISSEE jouable et defaussait Photographic
# Reflexes en consequence. Le resultat en jeu etait juste, mais le joueur
# tenait en main une carte ni jouable ni defaussable, et en a conclu — a bon
# droit — a un defaut. Le texte, lui, part bien de Photographic Reflexes.
# Les DEUX chemins existent maintenant, et aucun n'a ete retire :
#   A : cliquer Photographic Reflexes -> choisir l'evenement glisse ;
#   B : cliquer l'evenement glisse -> Photographic Reflexes part seule.
#
# Cartes de reference :
#  - `an006` Angelic Ribbons / `al014` Lurking : « discard this card → » est un
#    COUT, donc `SetCostFunc(CostFunc.Discard("This"))`, jamais l'effet ;
#  - `21185` System Shock et `21032` Pip the Troll : une capacite DECLENCHEE
#    depuis la MAIN se monte sur `.CanWorkOnlyInHand()` ;
#  - `16130` Crystal Ball : « may play a card ..., reducing its resource cost »
#    -> `player.PlayOneCardLikeInTurn(faces, effect)`, qui demande LAQUELLE
#    puis la joue en payant vraiment.
#
# ⚠ `AbilityType.HeroAction` porte a lui seul le « If you are in hero form »
# (`Ability.GetAbilityTypeCondition` : `effect.GetInitiator().IsHero()`).
# ⚠ La reduction de 2 n'est PAS ici : elle est sur Echo, appliquee a toute
# carte payee depuis sa zone glissee, pour que les chemins A et B paient la
# meme chose et qu'une seconde copie en main ne la double pas.


# Drapeau pose par le chemin A pendant qu'il joue l'evenement glisse.
# ⚠ SANS LUI, DEUX Photographic Reflexes PARTENT POUR UN SEUL REJEU (mesure du
# 21/09/2026 : main ['60040a','60040b','60040c'], on clique 60040b, il reste
# ['60040c']). Le chemin A defausse la carte cliquee comme COUT ; Echo, elle,
# defausse une Photographic Reflexes des qu'une carte est jouee depuis sa zone
# glissee — ce qui est juste pour le chemin B, ou rien n'a encore ete paye, et
# faux pour le chemin A. Le drapeau dit a Echo « c'est deja paye ».
# Idiome repris de Magik (`aoa/magik/45030a.py`, `initiator.flag`).
REFLEXES_DEJA_PAYEES = "ECHO_REFLEXES_DEJA_PAYEES"


def EchoDeCeJoueur(effect: 'Effect') -> 'CardFace|None':
    """L'identite Echo du joueur qui declenche, ou None."""
    joueur = effect.GetInitiator()
    if joueur is None:
        return None
    identite = joueur.GetIdentity()
    if identite is None or not identite.IsName('Echo'):
        return None
    return identite


def EvenementsGlissesSousEcho(effect: 'Effect') -> List['CardFace']:
    """Les evenements actuellement glisses sous l'Echo de ce joueur."""
    identite = EchoDeCeJoueur(effect)
    if identite is None:
        return []
    zone = identite.GetPlacedCardArea()
    if zone is None:
        return []
    return [face for face in zone.Get(True)
            if face is not None and Event.IsType(face)]


def AbilitesPhotographicReflexes() -> Sequence['Ability']:
    def check_pas_payer_sa_propre_glissee(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> bool:
        """CORRECTIF (25/09/2026, signale en jeu). Sur le CHEMIN B, la
        permission de jouer la carte glissee (`check_tucked_playable`) est
        accordee DES que Photographic Reflexes est en main, et sa vraie
        defausse n'arrive qu'APRES coup (`discard_photographic_reflexes`,
        WhenPlayerPlayCard). Entre les deux, rien n'empechait de la depenser
        comme RESSOURCE GENERIQUE (regle de base, n'importe quelle carte en
        main) pour payer le cout — deja reduit de 2 — de la carte glissee
        qu'elle vient elle-meme d'autoriser. Le joueur gagnait alors la
        reduction ET la valeur de ressource sur la MEME carte, alors que
        `discard_photographic_reflexes` ne trouvait plus rien a defausser
        ensuite (elle avait deja quitte la main via la zone de ressources).

        Avec UNE SEULE copie en main, la depense comme ressource est donc
        refusee : il faut qu'une carte de la main paie normalement, et
        Photographic Reflexes partira comme prevu apres coup. Avec une
        SECONDE copie disponible pour porter ce vrai cout, rien ne l'empeche
        : ce n'est plus la meme carte qui financerait les deux avantages.
        """
        joueur = message.GetToPlayer()
        if joueur is None:
            return True
        identite = joueur.GetIdentity()
        if identite is None or not identite.IsName('Echo'):
            return True
        zone = identite.GetPlacedCardArea()
        if zone is None:
            return True
        paying_for = message.paying_for_effect.this
        if paying_for.card.area != zone:
            return True
        autres = [x for x in joueur.hand_cards.Get()
                  if x.IsName('Photographic Reflexes') and x != effect.this]
        return bool(autres)

    def il_y_a_un_evenement_glisse(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        # Sans evenement sous Echo, la carte ne doit pas etre cliquable du
        # tout : la defausser pour rien recreerait le defaut d'origine sous
        # une autre forme.
        return bool(EvenementsGlissesSousEcho(effect))

    def photographic_reflexes(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = effect.GetInitiator()
        faces = EvenementsGlissesSousEcho(effect)
        if joueur is None or not faces:
            return
        # `PlayOneCardLikeInTurn` DEMANDE laquelle quand il y en a plusieurs,
        # puis la joue comme si elle etait en main, cout reellement paye.
        #
        # ⚠ ARBITRAGE ASSUME : LE COUT EST PAYE D'ABORD, ET IL N'EST PAS RENDU.
        # `CostFunc.Discard("This")` defausse Photographic Reflexes AVANT cet
        # appel. Si le joueur renonce ensuite, ou s'il ne peut pas payer
        # l'evenement glisse, la carte cliquee est perdue et rien n'est joue.
        # Le chemin B, lui, ne consomme Photographic Reflexes qu'une fois le jeu
        # effectif : LES DEUX CHEMINS DIVERGENT DONC SUR CE SEUL POINT.
        # C'est la lecture litterale du texte imprime — « you can DISCARD
        # Photographic Reflexes from your hand TO play an event » fait de la
        # defausse un COUT, et un cout paye ne se reprend pas — et c'est le
        # comportement ordinaire du moteur pour `SetCostFunc`. Arbitrage non
        # confirme par un ruling : aucun n'existe (recherche du 21/09/2026).
        #
        # ⚠ Le drapeau couvre toute la resolution, pas seulement la carte
        # choisie. Sans effet observable : `discard_photographic_reflexes` ne
        # part que sur une carte jouee DEPUIS la zone glissee, et le chemin A
        # n'en joue qu'une.
        joueur.flag.Update(REFLEXES_DEJA_PAYEES, +1)
        try:
            joueur.PlayOneCardLikeInTurn(faces, effect)
        finally:
            joueur.flag.Update(REFLEXES_DEJA_PAYEES, -1)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            photographic_reflexes,
            conditions=[il_y_a_un_evenement_glisse],
        ).SetCostFunc(CostFunc.Discard("This"))
        .CanWorkOnlyInHand(),
        # Remplace la depense-comme-ressource par defaut de ClassCard (une
        # seule declaration : `ClassCard.GetAbilities` ne pose plus la sienne
        # des qu'elle en trouve une portant ce nom). Meme montant que le
        # comportement d'origine (`effect.this.printed_resource`), une garde
        # de plus.
        AbilityFactory.CheckThisCanDropPay(conditions=[check_pas_payer_sa_propre_glissee]),
    ]
