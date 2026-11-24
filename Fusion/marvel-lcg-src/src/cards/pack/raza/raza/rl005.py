from . import *
def GetAbilities() -> Sequence['Ability']:
    def warrior_apotheosis(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = JoueurDe(effect)
        if joueur is None:
            return
        # « Engage any number of minions in play » (modele throg/tg003).
        sbires = [f for f in Worlds.FindCardsOnField(effect, CardFinder(card_type=Minion))
                  if f is not None and f.card.IsOnField()]
        if sbires:
            choisis = joueur.AskChooseFaces(sbires, (0, len(sbires)), effect, prompt="Engage any number of minions")
            for sbire in choisis:
                sbire.CastTo(Minion).EngagePlayer(joueur, effect)
        # « The villain and each minion engaged with you attacks you. Do not deal the villain a boost card. »
        attaquants: List['CardFace'] = []
        vilain = Worlds.FindVillain(effect)
        if vilain is not None:
            attaquants.append(vilain)
        attaquants += [m for m in joueur.GetEngagedMinions() if m is not None]
        ont_attaque: List['CardFace'] = []
        for ennemi in attaquants:
            if not ennemi.IsInPlay():
                continue
            fait = []
            ennemi.CastTo(Enemy).DoAttackYou(
                joueur, effect,
                property=AttackProperty(do_not_give_boost=True) if Villain.IsType(ennemi) else None,
                operation=lambda m, fait=fait: fait.append(True),
            )
            if fait:
                ont_attaque.append(ennemi)
        # « Then, deal damage equal to Raza's ATK to each enemy that attacked you this way. »
        identite = IdentiteDe(effect)
        if identite is None:
            return
        degats = identite.attack
        for ennemi in ont_attaque:
            if ennemi.IsInPlay():
                this.DealDamage([ennemi], degats, effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            warrior_apotheosis,
        ).SetPlay().SetLabel(),
    ]
