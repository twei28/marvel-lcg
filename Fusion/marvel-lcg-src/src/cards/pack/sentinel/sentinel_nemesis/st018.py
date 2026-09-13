from . import *

# Viral Assault — TRAITRISE NEMESIS, 3 icones de boost.
# When Revealed: You may discard 1 [[HACKED]] upgrade you control. If you do
#   not, take 1 damage for each [[HACKED]] upgrade you control. If you control
#   no [[HACKED]] upgrades, search the encounter deck and discard pile for the
#   Rogue Asset side scheme and put it into play. If Rogue Asset is already in
#   play, this card gains surge.
#
# Cartes de reference :
#  - `st017` Disabled : meme recherche de Rogue Asset, meme repli.
#  - `al007` / `ag004` : `MayChooseOneAbility` pour un « **You may** ».
#  - `ThisCardGainSurge(effect)` (helper de `cards/pack/__init__.py`).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - TROIS branches, pas deux, et la troisieme ne s'ouvre QUE si le joueur ne
#    controle AUCUNE amelioration HACKED. Avec des HACKED en jeu, refuser la
#    defausse ne mene jamais a Rogue Asset : on encaisse, point.
#  - « take 1 damage **for each** » : le compte se lit APRES le refus, donc sur
#    les ameliorations encore en jeu.
#  - « **this card gains surge** » : la traitrise est deja en train de se
#    resoudre, le deferlement s'ajoute a elle, il ne revele rien tout de suite.


def GetAbilities() -> Sequence['Ability']:

    def viral_assault(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        joueur = message.GetToPlayer()
        if joueur is None:
            return

        piratees = [f for f in joueur.GetControlUpgrade()
                    if f.HasTrait(TRAIT_HACKED)]

        if piratees:
            def defausser(cibles: Sequence['CardFace']) -> None:
                Faces.DiscardAll(cibles, effect)

            choix = joueur.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Discard 1 HACKED upgrade you control", defausser)
                .SetTarget(
                    Upgrade,
                    trait=TRAIT_HACKED,
                    from_where=["YouControlCards"],
                ),
            )
            if choix is None:
                encore = [f for f in joueur.GetControlUpgrade()
                          if f.HasTrait(TRAIT_HACKED)]
                this.DealDamage([joueur.GetIdentity()], len(encore), effect)
            return

        deja_en_jeu = Worlds.FindCardOnField(
            effect, name=NOM_ROGUE_ASSET, card_type=SchemeSide2)
        if deja_en_jeu is not None:
            ThisCardGainSurge(effect)
            return

        face = Search.EncounterCard(
            effect,
            include_discard_pile=True,
            name=NOM_ROGUE_ASSET,
            card_type=SchemeSide2,
        )
        if face:
            face.PutIntoPlay(joueur, effect)
        else:
            ThisCardGainSurge(effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            viral_assault,
        ),
    ]
