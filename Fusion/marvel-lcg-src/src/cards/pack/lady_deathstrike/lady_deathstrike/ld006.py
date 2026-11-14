from . import *

# Adamantium Nanoskeleton — ATTACHEMENT, ARMOR (x2). Boost 2.
# Attach to Lady Deathstrike.
# Forced Interrupt: When a player attacks Lady Deathstrike, prevent all damage that would be dealt to her and resolve the "Special"
#   ability on the copy of Bleeding Out attached to that player's identity instead. Then, discard this card. (Max once per attack.)
#
# Cartes de reference :
#  - « Attach to <nom> » : `AttachToFaceWhenPutIntoPlay(CardFinder(...))` (`01100`, `04084`) ; ici par card_id (homonymes).
#  - « prevent all damage that would be dealt » : `WhenUnitWouldTakeDamage(ForcedInterrupt, "AttachedEnemy", op, is_from_attack=True)`
#    + `message.PreventDamage("All", effect)` (`26012` Mass Increase, `bk003`).
#
# ⚠ Mots-pieges :
#  - DECISION UTILISATEUR (25/10/2026) : « a player attacks » = TOUT personnage que le joueur controle (heros, allie, evenement
#    d'attaque) : l'armure ne se contourne pas avec un allie ; le Bleeding Out saigne est celui du joueur QUI CONTROLE l'attaquant ;
#  - « (Max once per attack) » : avec DEUX exemplaires attaches, le premier empeche tous les degats (donc le second ne voit plus rien
#    a empecher, `at_least_damage=1`) : une seule armure part par attaque ;
#  - « prevent ALL damage ... INSTEAD » : le Special remplace les degats ; « Then, discard this card » dans tous les cas.


def GetAbilities() -> Sequence['Ability']:

    def armure(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Attachment)

        message.PreventDamage("All", effect)
        source = message.source
        joueur = source.GetControlByOrOwner() if source is not None else None
        if Player.IsType(joueur):
            ResoudreSaignement(effect, joueur)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(card_ids=IDS_VILAIN)),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            "AttachedEnemy",
            armure,
            is_from_attack=True,
        ),
    ]
