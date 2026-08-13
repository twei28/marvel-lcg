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
