from . import *

# Wu Jen Tessen (sj018), Kuji-Kiri, amelioration MYSTIC WEAPON, unique (Inkwire, TMNT Shinobi).
# Restricted.
# Hero Response: After you play a Kuji-Kiri card from your hand, exhaust this card → ready your hero.
#
# Mots-cles (fiches lues AVANT le code) : Restricted (`restricted.md` : `desc.Restricted "1"`, base automatique,
# aucun code) ; Shinobi (`shinobi.md` : `CarteShinobi("Kuji-Kiri")`).
# Cartes de reference : `skrull_menace/sk009` Alliance (« After you play a card ... from your hand » :
# `AfterPlayerPlayedCard(..., from_hand=True)`) ; `jennika/tj011` (Reponse sur une carte Shinobi, cout incliner) ;
# `jennika/tj006` Fearless Resolve (« ready Jennika » : `Faces.ReadyAll([...])`) et `tmnt_aspect_protection/up003`
# Army of One (« Ready your hero »).
#
# TEXTE CONTRE CODE
#  ⚠ « Hero Response » : forme heros ; « After YOU play a KUJI-KIRI card FROM YOUR HAND » : Dual Kuji-Kiri
#    comprises, pas un Path ; jouee depuis la main.
#  ⚠ « exhaust THIS card → » : cout = incliner l'amelioration (une fois par redressement) ; « ready YOUR
#    HERO » : redresse le heros du joueur.
#  ⚠ Amelioration sans « Attach to » : posee sur l'identite (`CanPlayThisUpgradeCard()`).


def GetAbilities() -> Sequence['Ability']:

    def wu_jen_tessen(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        Faces.ReadyAll([joueur.GetHero()], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.HeroResponse,
            "You",
            CarteShinobi("Kuji-Kiri"),
            wu_jen_tessen,
            from_hand=True,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
