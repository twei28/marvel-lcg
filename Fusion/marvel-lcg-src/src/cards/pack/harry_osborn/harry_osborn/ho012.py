from . import *

# "That Had to Hurt" — amelioration signature. CONDITION. Cout 1. x2
# Temporary. Hero form only. Attach to an enemy. Max 1 per enemy.
# Attached character loses the stalwart or steady keyword.
# Response: After attached character gets a status card, deal 1 damage to it.
#
# Cartes de reference :
#  - 50144 Solid Sound Constructs (pack aos), quasi jumeau : attache a un
#    ennemi, `GiveKeywordToAttached(..., stalwart=-1)`, et le MEME
#    declencheur `AfterStatusCardPlaceOn` sur l'attache ;
#  - 33005 Exploit Weakness (pack cyclops) pour le cote JOUEUR :
#    `CanPlayThisUpgradeCard(Enemy)` + « Max 1 per enemy » (desc.MaxPerUnit)
#    + Temporary (desc.Temporary, defausse par ProcessTemporary — fiche
#    mots-cles/temporary.md) ;
#  - « Hero form only » : 01009 Webbed Up, `.SetPlay(hero_form_only=True)`.
#
# ⚠ « loses the stalwart OR steady keyword » : la carte retire CELUI que
# l'ennemi possede — les deux retraits sont poses en continu (stalwart=-1,
# steady=-1), un retrait sur un mot-cle absent est neutre (compteur plancher).
# ⚠ « gets a status card » sans restriction de type : stun, confuse ET tough
# declenchent la Response — y compris un tough donne par le scenario.
# Le « deal 1 damage to IT » vise le personnage attache lui-meme.

def GetAbilities() -> Sequence['Ability']:

    def blesser(effect: 'Effect', message: 'Message.AfterStatusCardPlaceOn') -> None:
        this = effect.this.CastTo(Upgrade)

        attache = this.attached_face
        if attache is not None and attache.IsInPlay():
            this.DealDamage([attache], 1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            Enemy,
        ).SetPlay(hero_form_only=True),
        *AbilityFactory.GiveKeywordToAttached(
            "Character",
            stalwart=-1,
            steady=-1,
        ),
        AbilityFactory.AfterStatusCardPlaceOn(
            AbilityType.Response,
            "AttachedEnemy",
            ["Confused", "Stunned", "Tough"],
            blesser
        ),
    ]
