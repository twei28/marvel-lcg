from . import *

# * Mystique (face HEROS) : SPY. X-MEN. THW 2 / ATQ 2 / DEF 2, main 5, PV 10.
# True Form — Response: After you flip a shapeshift form upgrade, if all shapeshift form upgrades are facedown, ready your identity.
# (FR 1.1.1 : « Forme véritable — Réponse : après avoir retourné une Forme Métamorphose, si elles sont toutes face cachée, redressez votre identité. »)
# Capacite additionnelle (PAS imprimee sur la face) : « While Infiltration is in the victory display, Mystique ignores the guard and patrol keywords » (my007).
#
# CARTES DE REFERENCE
#  - `hf041` / `hf110` : `Ability(Response, Message.AfterCardFlip, [conditions], op)` pour « after you flip <une AUTRE carte> » (`AfterCardFlipToThisSide` ne vise que la carte elle-meme).
#  - `bm010` Grapple Gun : `UnitIgnoreKeywordIcons(CardFinder(name=..), guard=True, patrol=True)` ; `pd001a` `ActionHonorHuntEnVitrine` : une capacite « en vitrine de victoire » vit sur
#    l'IDENTITE (la carte en vitrine ne declenche jamais ses propres capacites ; RECETTES §3bis), condition = la carte est dans `Worlds.VictoryDisplay`.
#
# TEXTE CONTRE CODE
#  « After YOU flip » : le retournement d'une forme de CE joueur (l'identite de Mystique ne retourne que ses formes). « all shapeshift form upgrades are facedown » : les TROIS formes sont face `b`
#    (apres le retournement). « ready your IDENTITY » : l'identite, pas seulement le heros (forme heros ici de toute facon). « Response » : optionnel (« you may »), jouable en forme heros seulement.
#  Chiffres : PV 10, main 5, ATQ/CTR/DEF 2.


def GetAbilities() -> Sequence['Ability']:

    def forme_du_joueur_retournee(effect: 'Effect', message: 'Message.AfterCardFlip') -> bool:
        joueur = JoueurDeCetteCarte(effect)
        flipped = message.to_face
        if joueur is None or flipped is None or not EstUneForme(flipped) or not flipped.card.IsOnField():
            return False
        return flipped in Formes(joueur) and ToutesCachees(joueur)

    def forme_veritable(effect: 'Effect', message: 'Message.AfterCardFlip') -> None:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None:
            Faces.ReadyAll([joueur.GetIdentity()], effect)

    return [
        Ability(
            AbilityType.Response,
            Message.AfterCardFlip,
            [forme_du_joueur_retournee],
            forme_veritable,
        ).SetName("True Form"),
        AbilityFactory.UnitIgnoreKeywordIcons(
            CardFinder(name=NOM_MYSTIQUE, card_type=Hero),
            guard=True,
            patrol=True,
            conditions=[InfiltrationEnVitrine],
        ).SetName("Infiltration (victory display)"),
    ]
