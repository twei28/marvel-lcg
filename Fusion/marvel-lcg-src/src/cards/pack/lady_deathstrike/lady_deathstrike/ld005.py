from . import *

# Bleeding Out — ATTACHEMENT, CONDITION (4 exemplaires, un par joueur, mis de cote par ld004a).
# Permanent. Attach to your identity.
# Special: Place 1 bleed counter here. Discard cards from the top of your deck equal to the number of bleed counters here. If you
#   discard an identity-specific card this way, take 1 damage.
# Alter-Ego Action: Discard a card from your hand → remove 2 bleed counters from here.
#
# Cartes de reference :
#  - capacite nommee « Special » : `WhenResolveSpecialAbility("This", op)` (`ab007`, `baxter_stockman`), fiche mots-cles/special.md ;
#    le corps vit dans le helper du set (`Saigner`) pour que Reaver Tracker lise « a-t-on defausse une carte d'identite ? ».
#  - « Attach to your identity » : `AttachToFaceWhenPutIntoPlay("YourIdentity")` (`sk147`, `mf016`) ; `Permanent` : `desc.Permanent`
#    natif (fiche permanent.md).
#  - defausse du dessus du deck : `joueur.DiscardDeckTopCards(n, effect)` (`56167`) ; cout « discard a card from your hand » :
#    `CostFunc.Discard("YourHandCards", range=(1, 1))` (`ar010`, `11018`).
#
# ⚠ Mots-pieges :
#  - « Place 1 bleed counter THEN discard equal to the number of counters » : le compteur est pose AVANT le compte (3 -> 4 : 4 cartes) ;
#  - « If you discard AN identity-specific card » : FAQ de l'auteur, 1 degat AU PLUS, que l'on defausse une ou plusieurs de ces cartes ;
#  - « Alter-Ego ACTION » : seulement en forme alter-ego ; « remove 2 » : retire ce qu'il y a si moins de 2 compteurs ;
#  - Permanent : ne peut pas etre defaussee (sauf par un effet du MEME set) ; copie par joueur : `LeSaignement(joueur)`.


def GetAbilities() -> Sequence['Ability']:

    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this.CastTo(Attachment)

        joueur = message.GetToPlayer()
        if joueur is None:
            return
        this.ld_defausse_heros = Saigner(effect, this, joueur)

    def panser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(message)

        Faces.RemoveCountersOn([this], 2, 'bleed', effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        AbilityFactory.WhenResolveSpecialAbility("This", special),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            panser,
        ).SetCostFunc(CostFunc.Discard("YourHandCards", range=(1, 1))),
    ]
