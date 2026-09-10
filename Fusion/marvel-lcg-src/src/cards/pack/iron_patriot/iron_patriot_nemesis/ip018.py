from . import *

# Cabal Obligations — ATTACHEMENT de nemesis (3/5). Boost 3. TACTIC.
# Attach to your identity.
# Attached identity cannot ready. REGISTERED allies you control cannot attack,
#   thwart, or resolve "Special" abilities.
# Action: Spend X resources of any type, where X is 1 more than the number of
#   REGISTERED allies in play -> discard this card.
#
# ⚠⚠ LA CARTE PUNIT EXACTEMENT CE QUE LE HEROS CHERCHE A FAIRE : plus l'armee
# est grande, plus il est cher de s'en debarrasser, et plus longtemps elle
# reste inutile. L'insert : « Doctor Doom works within the Cabal to counter
# Norman's desires for dominion, using Cabal Obligations to negotiate against
# Norman for mutual benefit. »
#
# CARTES DE REFERENCE
#  - `02048` All Tied Up : `AttachToFaceWhenPutIntoPlay("YourIdentity")` +
#    `*AbilityFactory.CardCannotReady("AttachedCharacter")` +
#    `PlayerActionToDiscardThis(AbilityType.Action)`.
#  - `40082` Bolstered by Wrath : LE COUT VARIABLE —
#    `.SetCost(lambda effect, faces: Cost("1") * n)`. Sans ce modele, `SetCost`
#    fige la valeur a la construction du module, donc au chargement du jeu.
#
# TEXTE CONTRE CODE
#  ⚠ « X is 1 MORE THAN the number of REGISTERED allies IN PLAY » : « in play »,
#    pas « you control » — en multijoueur, les allies REGISTERED des autres
#    joueurs comptent aussi. Sans allie, X vaut 1 : la carte reste toujours
#    payable.
#  ⚠ « cannot attack, thwart » : ces deux-la se posent par des `Ability`
#    ecrites a la main sur `CheckIfUnitCanAttack` / `CheckIfUnitCanThwart`. Les
#    fabriques `UnitCannotAttackTarget` / `UnitCannotThwartTarget` existent,
#    mais leur branche `cannot_*=True` IGNORE le parametre `conditions`
#    (do_attack.py:1035, thwart.py:220) : impossible d'y ajouter « you
#    control ». Le moteur construit lui-meme l'`Ability` dans ce cas, on fait
#    pareil, avec la condition en plus.
#  ⚠⚠ « or resolve "Special" abilities » : `Message.WhenResolveSpecialAbility`
#    N'EST PAS annulable (`sender_player.py:405`, pas de `CanBeInstead`). On ne
#    peut donc pas intercepter la resolution. Le blocage se pose donc a la
#    SOURCE, seul endroit ou la question se pose : les trois cartes du pack qui
#    resolvent un « Special » d'allie passent toutes par
#    `AlliesRegistredPouvantResoudreUnSpecial` (voir `__init__.py`), qui rend
#    une liste VIDE tant que ce joueur porte Cabal Obligations. Le resultat vu
#    par le joueur est le bon : plus aucun allie n'est proposable.
#  ⚠ « Attached IDENTITY cannot ready » : l'identite seule, pas les allies.
#    Eux sont bloques par les deux interdictions suivantes, pas par
#    l'inclinaison.


def GetAbilities() -> Sequence['Ability']:

    def allies_registered_en_jeu(effect: 'Effect') -> int:
        return len(Worlds.FindCardsOnField(
            effect, trait=TRAIT_REGISTERED, card_type=Ally))

    def cest_un_allie_registered_du_porteur(effect: 'Effect',
                                            face: 'CardFace|None') -> bool:
        if face is None or not Ally.IsType(face):
            return False
        if not face.HasTrait(TRAIT_REGISTERED):
            return False
        porteur = effect.this.GetBindFace()
        if porteur is None:
            return False
        joueur = JoueurQuiControle(face)
        return joueur is not None and joueur is JoueurQuiControle(porteur)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            "YourIdentity",
        ),
        *AbilityFactory.CardCannotReady(
            "AttachedCharacter",
        ),
        Ability(
            AbilityType.NonKeyword,
            Message.CheckIfUnitCanAttack,
            [lambda effect, message:
                cest_un_allie_registered_du_porteur(effect, message.check_unit)],
            lambda effect, message: message.SetCannotAttack(effect),
        ),
        Ability(
            AbilityType.NonKeyword,
            Message.CheckIfUnitCanThwart,
            [lambda effect, message:
                cest_un_allie_registered_du_porteur(effect, message.check_unit)],
            lambda effect, message: message.SetCannotThwart(effect),
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.Action,
        ).SetCost(lambda effect, faces:
                  Cost("1") * (1 + allies_registered_en_jeu(effect))),
    ]
