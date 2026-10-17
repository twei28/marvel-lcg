from . import *

# * Nightwatcher (Jenny) — ALLIE double aspect Leadership/Protection (Inkwire, TMNT Aspects).
# Cout 4, PV 2, THW 1 / ATK 2 (1 degat consecutif chacun), ressource [energy].
#
# Toughness.
# Response: After Nightwatcher takes consequential damage ([consequential]), give her a tough
#   status card.
#
# Cartes de reference :
#  - Toughness : `desc.Toughness`, lu par le moteur (fiche mots-cles/toughness.md) ;
#  - « After X takes consequential damage, give her a tough status card » : 19012 Martyr
#    (`AfterAllyTakeConsequentialDamage(Response, "This", ...)` + `Faces.GiveStatus([this],
#    "Tough", effect)`), SANS les filtres de Martyr (« from performing an attack, if that attack
#    defeated an enemy ») que Nightwatcher n'imprime pas : attaque OU contre, ennemi vaincu ou non.
#
# Mots-pieges : « TAKES » = degats reellement subis (une carte Tenace les empeche : pas de
# Reponse, cf. la note de 19012) ; « give HER » (elle-meme) ; vaincue par ces degats, elle n'est
# plus en jeu : rien a donner.


def GetAbilities() -> Sequence['Ability']:

    def tenace(effect: 'Effect', message: 'Message.AfterAllyTakeConsequentialDamage') -> None:
        Unused(message)
        this = effect.this.CastTo(Ally)
        Faces.GiveStatus([this], "Tough", effect)

    return [
        AbilityFactory.AfterAllyTakeConsequentialDamage(
            AbilityType.Response,
            "This",
            tenace,
            conditions=[lambda effect, message: effect.this.IsInPlay()],
        ),
    ]
