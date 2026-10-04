from . import *

# She Devil with a Sword — ressource signature, x1 (12/15). Cout aucun
# (ressource), icones [G][Y] empilees (compte comme les DEUX types quand
# depensee, verifie contre `data/cards.json` : `Resources.FromText` additionne
# chaque lettre, cf. `45010 Stored Energy RY`).
# Hero Response: After you spend this card, ready a weapon upgrade you
# control.
#
# CARTE DE REFERENCE : `AbilityFactory.AfterYouSpendThisCard` (resources.py:508),
# filtree nativement sur `effect.this in message.faces` -- pas de montage a
# la main necessaire, contrairement a ce que suggerait `wave/65001a.py` (qui
# visait un besoin different, capter TOUTES les cartes depensees). Cible du
# redressement : `spdr/31022.py`/`deadpool/44009.py`,
# `.SetTarget(Upgrade, trait="WEAPON", canbe_ready=True,
# from_where=["YouControlCards"])`.

def GetAbilities() -> Sequence['Ability']:

    def she_devil_with_a_sword(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(this, message)

        if effect.targets:
            Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.HeroResponse,
            she_devil_with_a_sword,
        ).SetTarget(Upgrade, trait="WEAPON", canbe_ready=True,
                    from_where=["YouControlCards"], range=(0, 1)),
    ]
