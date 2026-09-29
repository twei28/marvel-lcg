from cards.pack import *


# LES MOTS-CLES DE L'ASPECT
#
# Determination invente des mots-cles que le moteur ne connait pas. Ils sont
# ecrits ICI une fois, et pas recopies dans chaque carte : quatre cartes du lot
# dt021-dt040 portent Fragile, une quinzaine dans l'aspect entier. Une seule
# definition, un seul endroit a corriger si la lecture doit changer.


def Fragile() -> 'Ability':
    """« Fragile. (Attacks against this character gain overkill.) »

    Le crochet est officiel : 33032 (Marked) fait exactement cela pour un sbire,
    par `GainOverKill` sur la fenetre WhenUnitWouldAttackUnit. Seule la cible
    change — « This » au lieu du sbire attache.
    """
    def fragile(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        message.GainOverKill(effect)

    return AbilityFactory.WhenUnitWouldAttackUnit(
        AbilityType.NonKeyword,
        None,
        "This",
        fragile,
    )


def Reckless() -> 'Ability':
    """« Reckless. (After this character enters play, place 1 threat on each scheme.) »

    Aucun crochet dans le moteur : le mot-cle est joue tel que la carte le
    rappelle elle-meme entre parentheses.
    """
    def reckless(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        this.PlaceThreatOnSchemes("EachScheme", 1, effect)

    return AbilityFactory.AfterCardEnterPlay(
        AbilityType.ForcedResponse,
        "This",
        reckless
    )


def Fleeting() -> 'Ability':
    """« Fleeting. (This card must be discarded from play at the end of the phase.) »

    Aucun crochet natif, et le moteur ne lit AUCUN mot-cle dans le texte : sans
    cette aptitude, dt087 restait attachee jusqu'a la defaite de l'ennemi
    (constate le 29/09/2026). Modele : 44032 The Merc with the Mouth
    (`WhenPlayerPhaseEnd` + `DiscardThisCard`). Ici `phase_name=None` : la
    PREMIERE fin de phase qui suit l'entree en jeu, quelle que soit la phase
    (dt087 arrive en phase du mechant, apres des degats subis). La defausse
    passe par `Faces.DiscardAll`, donc par la fenetre `WhenCardWouldDiscard`
    que la carte ecoute pour son Interrupt de depart.
    """
    def en_jeu(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> bool:
        return effect.this.IsInPlay()

    return AbilityFactory.WhenPhaseEnd(
        AbilityType.ForcedResponse,
        None,
        DiscardThisCard,
        conditions=[en_jeu],
    )


def PeutRevenirEnMain(this: 'CardFace', initiator: 'Player', effect: 'Effect') -> None:
    """« If this is the first card you have played this round, you may take 1
    damage to return this card to your hand. »

    Deux cartes du lot le portent au mot pres (dt039, dt040). Le crochet du
    « premier » est officiel : 18012 (Clobber) lit le meme
    `IsFirstCardPlayedThisRound` — ce qui dit au passage que le moteur
    enregistre la carte jouee APRES sa resolution, sinon Clobber ne reviendrait
    jamais.
    """
    if not initiator.stat.IsFirstCardPlayedThisRound():
        return

    def revenir(targets: Sequence['CardFace']) -> None:
        initiator.GetHero().TakeDamage(this, 1, effect)
        Faces.ReturnToHand([this], initiator, effect)

    initiator.ChooseAbilities(
        effect,
        AbilityFactory.ForChoiceAbility(
            "Take 1 damage to return this card to your hand",
            revenir
        ).SetHasNoTargetEffect(),
        forced=False,
    )


def RepartirLeRetraitDeMenace(this: 'CardFace', initiator: 'Player', total: int,
                              effect: 'Effect') -> None:
    """« remove X threat from schemes divided as you choose ».

    Le moteur n'a pas d'AssignThreat symetrique d'AssignDamage : la repartition
    se dit en choisissant X fois une manigance a laquelle retirer 1 menace. C'est
    ce que fait 03011 (Falcon), avec `repeat_rules="Threat"` pour qu'une meme
    manigance puisse etre reprise tant qu'elle porte de la menace.
    """
    if total <= 0:
        return
    initiator.ChooseAbilities(
        effect,
        AbilityFactory.ForChoiceAbility(
            "Remove threat",
            lambda targets:
                this.RemoveThreatFromSchemes(targets, 1, effect)
        ).SetTarget(Scheme2, range=("Zero", total), repeat_rules="Threat")
    )


def Drain(source: 'CardFace', cibles: Sequence['CardFace'], valeur: int,
          effect: 'Effect') -> None:
    """« drain X from an enemy » : X degats a l'ennemi, X soins sur votre identite.

    Le mot-cle vient d'un autre pack du meme auteur (agent_anti_venom), qui le
    definit ainsi. Ici le soin va a l'identite du joueur qui joue la carte, pas
    a un heros nomme.
    """
    if not cibles or valeur <= 0:
        return
    source.DealDamage(cibles, valeur, effect)
    player = effect.GetInitiator()
    if player is not None:
        source.HealthUnits([player.GetIdentity()], valeur, effect)


def Alias() -> 'Sequence[Ability]':
    """« Alias. (Si vous controlez une carte au meme sous-titre, defaussez-la et
    jouez celle-ci gratuitement.) »

    Quatre cartes de l'aspect le portent (dt100, dt105, dt106, dt107). Deux
    capacites, parce que la carte fait deux choses : le cout tombe a zero tant
    que l'homonyme est controle, et l'homonyme est defausse a l'entree en jeu.
    Le texte les presente comme un tout — on ne joue gratuitement QUE parce
    qu'on defausse.
    """
    def controle_un_homonyme(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        this = effect.this
        initiator = effect.GetInitiator()
        if initiator is None:
            return False
        sous_titre = this.paper.subtitle
        if not sous_titre:
            return False
        for face in initiator.GetControlCards():
            if face is not this and face.paper.subtitle == sous_titre:
                return True
        return False

    def defausser_l_homonyme(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this
        initiator = effect.GetInitiator()
        if initiator is None:
            return
        sous_titre = this.paper.subtitle
        if not sous_titre:
            return
        homonymes = [f for f in initiator.GetControlCards()
                     if f is not this and f.paper.subtitle == sous_titre]
        if homonymes:
            Faces.DiscardAll(homonymes[:1], effect)

    return [
        # ⚠ `.val`, PAS L'OBJET `Cost` : `printed_cost` est un `Cost`, et la
        # fabrique multiplie (`base_val * fn(effect)`). Sans `.val`, TypeError
        # avalee par le moteur : la reduction ne s'appliquait jamais, meme avec
        # les sous-titres renseignes (trouve au harnais le 29/09/2026).
        AbilityFactory.ReduceCostToPlayThis(
            lambda effect: effect.this.printed_cost.val,
            conditions=[controle_un_homonyme]
        ),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            defausser_l_homonyme
        ),
    ]
