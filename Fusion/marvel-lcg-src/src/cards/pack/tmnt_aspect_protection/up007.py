from . import *

# * Cyber Ninja (Donnie) — ALLIE 2 [mental], aspect Protection (TMNT Aspects, Inkwire). GENIUS. NINJA. TURTLE.
# THW 1 (1), ATK 1 (1), PV 2.
# Response: After Cyber Ninja enters play, discard an upgrade from your hand -> draw 1 card and cloak
#   Cyber Ninja.
#
# NOUVELLE. MOT-CLE (fiches lues AVANT le code) : CLOAK (cloak.md) = poser une carte d'etat Cloaked
# (cloaked.md) : `Faces.GiveStatus([face], "Cloaked", effect)`.
#
# CARTES DE REFERENCE
#  - `09012` Brother Voodoo : `AfterCardEnterPlay(Response, "This", ...)`.
#  - `ar010` / `53001b` : cout « discard a card from your hand » = `CostFunc.Discard("YourHandCards", ...)`,
#    ici filtre `card_type=Upgrade`, exactement 1 (`range=(1, 1)`).
#  - `td005` Improvised Tactics : « Cloak » d'un personnage ami = `Faces.GiveStatus([...], "Cloaked")`.
#
# TEXTE CONTRE CODE
#  ⚠ « discard AN UPGRADE from YOUR HAND » : cout (avant la fleche), une amelioration de la main, une seule.
#    Sans amelioration en main, la Reponse n'est pas proposee (cout impayable).
#  ⚠ « draw 1 card AND cloak Cyber Ninja » : les deux, sur la carte elle-meme (pas l'identite).
#  ⚠ Un seul Cloaked par personnage (cloaked.md) : un 2e est refuse par le moteur, aucun cas ici.


def GetAbilities() -> Sequence['Ability']:

    def cyber_ninja(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is not None:
            joueur.DrawUp(1, effect)
        if this.IsInPlay():
            Faces.GiveStatus([this], "Cloaked", effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            cyber_ninja,
        ).SetCostFunc(CostFunc.Discard("YourHandCards", card_type=Upgrade, range=(1, 1))),
    ]
