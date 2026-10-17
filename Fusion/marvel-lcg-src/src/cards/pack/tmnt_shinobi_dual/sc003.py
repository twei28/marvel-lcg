from . import *

# Omawari — EVENEMENT DUAL Bushido/Ninjutsu, cout 1, [physical]. SKILL.
# Classe : « Bushido;Ninjutsu ».
# Hero Action: Exhaust a WEAPON upgrade you control -> cloak your hero and give them a tough status card.
#
# Mots-cles (fiches lues AVANT le code) : Cloak (cloak.md, cloaked.md) ; Tough (tough.md) ; Shinobi (shinobi.md).
#
# Cartes de reference :
#  - cout « Exhaust a <trait> upgrade you control » : `tmnt_aspect_*/td005` Improvised Tactics ;
#  - « cloak your hero » : `jennika/tj005` Moonlighting et `tmnt_shinobi_paths/se001` Kagemusha
#    (`ShinobiCloak(effect, joueur.GetHero())`) ;
#  - « give ... a tough status card » : `Faces.GiveStatus([...], "Tough", effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « Exhaust a WEAPON upgrade you control » : COUT (devant la fleche), amelioration inclinee et non defaussee.
#  ⚠ « cloak YOUR HERO AND give THEM a tough status card » : les DEUX statuts, tous deux sur le HEROS (jamais sur l'alter-ego
#    ni un allie) ; « them » = le heros. Un heros deja camoufle ne recoit pas un second Cloaked (un seul par personnage) mais
#    recoit quand meme Tenace.
#  ⚠ « Hero Action » : forme heros seulement. Aucun libelle `(attack)` imprime.


def GetAbilities() -> Sequence['Ability']:

    def omawari(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None or not joueur.IsHero():
            return
        heros = joueur.GetHero()
        ShinobiCloak(effect, heros)
        Faces.GiveStatus([heros], "Tough", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            omawari,
        ).SetPlay().SetLabel()
        .SetCostFunc(CostFunc.Exhaust(
            card_type=Upgrade,
            trait="WEAPON",
            from_where=["YouControlCards"],
        )),
    ]
