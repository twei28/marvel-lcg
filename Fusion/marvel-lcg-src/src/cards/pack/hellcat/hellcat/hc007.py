from . import *
# Cat-Like Reflexes — EVENEMENT, cout 1, [mental]. DEFENSE. x2.
# Hero Interrupt (defense): When Hellcat defends against an attack → you get
#   +2 DEF for this defense. Search your discard pile for a card not named
#   Cat-Like Reflexes with a printed [mental] resource and add it to your hand.
#
# Modeles : 14014 Never Back Down (`WhenUnitDefendAgainstAttack(HeroInterrupt,
# "You", ..., is_basic_defense=True)` + `GainDEFForThisAttack`), recherche
# manuelle dans la defausse (aucun `CardFinder` n'exclut un nom : on filtre
# la liste, puis `AskChooseFaces` + `Faces.AddToHand`).

def GetAbilities() -> Sequence['Ability']:

    def cat_like_reflexes(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Event)
        message.GainDEFForThisAttack(2, effect)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        candidates = [f for f in CartesDeLaDefausse(joueur)
                      if AMentalImprime(f) and not f.IsName(this.name)]
        if not candidates:
            return
        choisies = joueur.AskChooseFaces(candidates, (1, 1), effect, prompt="Add to hand")
        if choisies:
            Faces.AddToHand(list(choisies), joueur, effect)

    return [
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.HeroInterrupt,
            "You",
            cat_like_reflexes,
            is_basic_defense=True,
        ).SetPlay().SetLabel('defense'),
    ]
