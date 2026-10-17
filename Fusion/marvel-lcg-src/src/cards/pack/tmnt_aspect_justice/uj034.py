from . import *

# Turtle Line — AMELIORATION 2 [energy], aspect Justice (TMNT Aspects, Inkwire). NINJA. WEAPON.
# Attach to a friendly character. While attached to an identity, this card gains restricted. Uses (3 rope
#   counters).
# Response: After attached character uses a basic power, exhaust this card and remove 1 rope counter from
#   here → remove 2 threat from a scheme.
#
# MOTS-CLES (fiches lues AVANT le code) : RESTRICTED — restricted.md (limite lue par le moteur, `restricted`
# courant de la carte) ; USES — uses.md (`desc.Uses "3,rope"` : pions poses et sortie au dernier pion, AUCUN
# code ; compteur « rope » AJOUTE a `CardFace.COUNTER`).
#
# CARTES DE REFERENCE
#  - `54018` * Bambino (MEME gabarit imprime : « While attached to an identity, this card gains restricted.
#    Uses (3 ... counters). ») : `ThisGainKeyword(lambda effect, ui: Identity.IsType(bind_face),
#    restricted=1, change_on_event=OnEvent.AttachedMove("This"))` et un cout `CostFunc.Counter("This", 1, ...)`.
#  - `sk064` : « Attach to a friendly character » = `CanPlayThisUpgradeCard(Friend)`.
#  - RECETTES §1 : « After <X> uses a basic power » = `AfterUnitUseBasicPower(type, <qui>, op)` ; « basic
#    power » = ATK, THW, DEF et REC (lecture de cloaked.md, Rules Reference « Basic Power ») : `powers=None`.
#
# TEXTE CONTRE CODE (PROCESSUS-CARTE etape 5)
#  ⚠ « a FRIENDLY character » : identite ou allie, de n'importe quel joueur.
#  ⚠ « While attached to an IDENTITY, this card gains restricted » : sur un allie, elle n'est PAS restricted.
#  ⚠ « exhaust this card AND remove 1 rope counter → » : deux couts ; le dernier pion retire fait sortir la
#    carte (Uses, moteur) APRES le retrait de menace.
#  ⚠ « remove 2 threat from A scheme » : principale ou annexe.
#  Pas de limite imprimee (l'inclinaison est le cout qui borne a un usage tant qu'elle n'est pas prete).


def GetAbilities() -> Sequence['Ability']:

    def corde(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(Friend),
        AbilityFactory.ThisGainKeyword(
            lambda effect, ui: Identity.IsType(effect.this.CastTo(Upgrade).bind_face),
            restricted=1,
            change_on_event=OnEvent.AttachedMove("This"),
        ),
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "AttachedCharacter",
            corde,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'rope'))
        .SetTarget(Scheme2),
    ]
