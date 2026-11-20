from . import *

# Jigsaw's Knife — ATTACHEMENT (Jigsaw). ARME. ATQ +1★, Boost 2.
# Weapon. Attach to Jigsaw.
# ★ Jigsaw gains retaliate 1 and his attacks gain piercing.
# Hero Action : Exhaust a character you control and spend [physical][mental] → discard this card.
#
# Cartes de reference : skrull_menace/paibok/sk148.py (attache au mechant + `GiveKeywordToAttached`
# + action de defausse a cout), ts201 (`UnitAttackGainKeyword(piercing=True)`).
# `ATK+ 1**` : natif (desc). Reponse de l'utilisateur : « Exhaust a character you control » = au choix du
# joueur parmi ses personnages PRETS (identite, allies), en plus des deux icones.

NOM_JIGSAW = "Jigsaw"

def GetAbilities() -> Sequence['Ability']:

    def incliner_un_personnage(effect: 'Effect', message: 'Message2') -> None:
        joueur = effect.GetInitiator()
        prets = [c for c in joueur.GetControlCharacters() if c.IsReady()]
        if not prets:
            return
        cible = prets[0] if len(prets) == 1 else joueur.AskChooseFace(prets, effect)
        if cible is not None:
            Faces.ExhaustAll([cible], effect)

    def un_personnage_pret(effect: 'Effect', message: 'Message2') -> bool:
        joueur = effect.GetInitiator()
        return any(c.IsReady() for c in joueur.GetControlCharacters())

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name=NOM_JIGSAW, card_type=Villain)),
        *AbilityFactory.GiveKeywordToAttached(CardFinder(name=NOM_JIGSAW, card_type=Villain), retaliate=1),
        AbilityFactory.UnitAttackGainKeyword("AttachedCharacter", piercing=True),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
            conditions=[un_personnage_pret],
            ex_operation=incliner_un_personnage,
        ).SetCost(Cost("BR")),
    ]
