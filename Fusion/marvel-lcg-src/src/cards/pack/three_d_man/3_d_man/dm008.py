from . import *

# True Sight (Upgrade)
#
# Hero form only.
# Interrupt: When this card enters play from your hand, remove 2 threat from a scheme.
# Hero Action: Discard True Sight, choose:
#  - Remove an attachment from play with the text "Hero Action" or "Hero Response"
#  - Remove a status card from any character.
#
# CARTES DE REFERENCE
#  - `mt008` Fortified Mind (Mantis) : "Hero form only" -> `.SetPlay(hero_form_only=True)` sur
#    `CanPlayThisUpgradeCard()`.
#  - `03002` Agent 13 (OFFICIELLE) : TEXTE DE MEME FAMILLE ("After Agent 13 enters play, remove 2 threat from a
#    scheme") -> `.SetTarget(Scheme2)` + `this.RemoveThreatFromSchemes(effect.targets, 2, effect)`. Difference :
#    dm008 est un "Interrupt: When this enters play" (pas "Response: After"), modele `hp011`/dm007 ->
#    `AbilityFactory.WhenCardEnterPlay(Interrupt, "This", op)`.
#  - `tl008` Iaijutsu (Leonardo) : "WITH a \"Hero Action\" ability" -> `face.effect.Find(type=AbilityType.HeroAction)`
#    dans un `check_fn`, PAS une recherche de texte litteral. Ici "with the text \"Hero Action\" OR \"Hero
#    Response\"" -> meme `check_fn`, avec un deuxieme `Find(type=AbilityType.HeroResponse)` en OU.
#  - `16155` Creative Solution : "remove a status card from any character" -> `.SetTarget(StatusCard)` +
#    `Faces.RemoveAllFromGame(targets, effect)`.
#  - `an006` Angelic Ribbons : "discard this card" est un COUT -> `CostFunc.Discard("This")`.
#
# TEXTE CONTRE CODE
#  "from your hand" : comme dm007, aucune autre carte du kit ne met True Sight en jeu autrement que depuis la
#    main -> pas de condition de provenance a coder.
#  "an attachment FROM PLAY" : pas de "you control" imprime -> cible n'importe quel attachement en jeu (le sien,
#    celui d'un allie, ou meme celui d'un ennemi/du vilain), `from_where` non restreint a "YouControlCards".
#  "choose" (sans flèche de cout avant) : un choix de DEUX effets exclusifs apres la defausse, pas un cout
#    optionnel -> `initiator.ChooseAbilities` (modele 16155), pas un `SetCostFunc` supplementaire.
#
# Chiffres : remove 2 threat (Interrupt) ; aucun chiffre sur le Hero Action (retrait pur, pas de montant).

def GetAbilities() -> Sequence['Ability']:

    def true_sight_entree_en_jeu(effect: 'Effect', message: 'Message.WhenCardEnterPlay') -> None:
        this = effect.this.CastTo(Upgrade)
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)

    def attachement_hero_action_ou_response(effect: 'Effect', face: 'CardFace') -> bool:
        if not Upgrade.IsType(face):
            return False
        return bool(face.effect.Find(type=AbilityType.HeroAction)) or bool(face.effect.Find(type=AbilityType.HeroResponse))

    def true_sight_choix(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        initiator = effect.GetInitiator()

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove an attachment from play with the text \"Hero Action\" or \"Hero Response\"",
                lambda targets: Faces.RemoveAllFromGame(targets, effect),
            ).SetTarget(check_fn=attachement_hero_action_ou_response, range=(1, 1)),
            AbilityFactory.ForChoiceAbility(
                "Remove a status card from any character",
                lambda targets: Faces.RemoveAllFromGame(targets, effect),
            ).SetTarget(StatusCard),
        )
        Unused(this)

    return [
        AbilityFactory.CanPlayThisUpgradeCard().SetPlay(hero_form_only=True),
        AbilityFactory.WhenCardEnterPlay(
            AbilityType.Interrupt,
            "This",
            true_sight_entree_en_jeu,
        ).SetTarget(Scheme2),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            true_sight_choix,
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
