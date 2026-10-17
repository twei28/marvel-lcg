from . import *

# Martial Arts Training — AMELIORATION 1 (aucune icone de ressource imprimee), aspect Basic (TMNT Aspects). TRAINING.
# Starting. (You may add this card to your hand before drawing your starting hand.)
# Your hero gains the [[MARTIAL ARTIST]] trait.
#
# NOUVELLE. Cartes de reference : 60038 Innate Reflexes (Starting + « Your hero gets +1 DEF » : meme
# squelette, `WhenGameBeginSetup` + `MayChooseOneAbility` + `GiveKeywordToAttached(Hero, ...)`) ; sm012 Web
# Cape (« Your hero gains the X trait » = `GiveKeywordToAttached(..., trait=...)`). Fiche mots-cles/starting.md.
# Pas de ressource imprimee : `desc.RES` absent, comme 60038.
# TEXTE CONTRE CODE : « YOUR HERO » : le trait ne vaut qu'en forme heros (cible `Hero`, comme 60038) ;
#   « You MAY add » : choix facultatif.


def GetAbilities() -> Sequence['Ability']:
    def starting(effect: 'Effect', message: 'Message.WhenGameBeginSetup') -> None:
        this = effect.this.CastTo(Upgrade)
        if not this.card.area.flags.is_player_deck:
            return
        player = this.GetControlByOrOwner()

        def ajouter(targets: Sequence['CardFace']) -> None:
            Faces.AddToHand([this], player, effect)

        player.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility('Add this card to your starting hand', ajouter),
        )
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            *AbilityFactory.GiveKeywordToAttached(Hero, trait="MARTIAL ARTIST"),
            AbilityFactory.WhenGameBeginSetup(starting).NoOutOfPlayLimit()]
