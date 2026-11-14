from . import *
# Accessing, evenement. Cout 0, [mental]. SUPERPOWER.
#
# Hero Action: Resolve the "Hero Response" ability on an EXOSPEX upgrade you control. Then discard that EXOSPEX upgrade.
#
# Cartes de reference : 01043a Wakanda Forever! (`SetTarget(Upgrade, trait=.., from_where=["YouControlCards"])` : choisir une amelioration
# controlee par son trait) ; la resolution d'une capacite sur une carte en jeu : `ResolveSpecialAbility` n'existe que pour « Special »,
# on rejoue donc les memes fonctions que les ameliorations (set `__init__.py`, `ResoudreLaReponseDe`).
# ⚠ « Then discard that upgrade » : la defausse suit TOUJOURS la resolution (meme sans cible legale pour la Response).
def GetAbilities() -> Sequence['Ability']:
    def accessing(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        joueur = effect.GetInitiator()
        for amelioration in list(effect.targets):
            ResoudreLaReponseDe(amelioration, joueur, effect)
            Faces.DiscardAll([amelioration], effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            accessing,
        ).SetPlay().SetLabel()
        .SetTarget(Upgrade, trait=TRAIT_EXOSPEX, from_where=["YouControlCards"]),
    ]
