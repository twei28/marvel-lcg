from . import *

# * Moja — ALLIE unique 3 [energy], Ninjutsu (TMNT Shinobi, Inkwire). NINJA. TURTLE.
# THW 1 (1 degat consecutif), ATK 1 (1 degat consecutif), PV 3.
# Response: After Moja enters play, cloak her.
# Response: After Moja takes consequential damage ([consequential]), discard a Ninjutsu card from your hand -> cloak Moja.
#
# NOUVELLE. Mots-cles (fiches lues AVANT le code) : Cloak / Cloaked (cloak.md, cloaked.md), Shinobi (shinobi.md).
# Icones verifiees contre un scan du pack d'aspects (ub017, ub031 : etoile verte = RES G ; up007 Cyber Ninja : etoile
# des degats consecutifs = « 1* » sur ATK et THW), jamais a vue.
#
# Cartes de reference :
#  - `up024` Nobody / `ud004` : « After X enters play, cloak X » = `AfterCardEnterPlay(Response, "This", fn)` +
#    `Faces.GiveStatus([this], "Cloaked", effect)` ;
#  - `ud003` Heavy Metal : « After X takes consequential damage ... » = `AfterAllyTakeConsequentialDamage(Response, "This",
#    fn, conditions=[encore en jeu])` (ne part que si des degats consecutifs sont REELLEMENT subis : Coriace les empeche) ;
#  - `se005`/`se004` : « a Shinobi card from your hand » = `Select.From("YourHandCards", finder=CarteShinobi(...),
#    range=(1, 1))` dans un `CostFunc.Discard`.
#
# TEXTE CONTRE CODE
#  ⚠ DEUX Reponses distinctes, optionnelles. « After Moja ENTERS PLAY, cloak HER » : sur elle-meme, a la mise en jeu.
#  ⚠ « After Moja TAKES consequential damage » : degats consecutifs reellement subis (pas « would take ») ; « discard a
#    NINJUTSU card FROM YOUR HAND -> » est le COUT : une carte de classe Ninjutsu (une Dual Ninjutsu compte ; ni Bushido seule,
#    ni Taijutsu seule, ni Basic) ; sans telle carte en main, la Reponse n'est pas proposee ; « cloak Moja » : si elle l'est
#    deja, le cout est paye pour rien (une seule Cloaked).
#  ⚠ Unique (✦). THW/ATK « 1* » (degats consecutifs).


def GetAbilities() -> Sequence['Ability']:

    def se_camoufler(effect: 'Effect', message: 'Message') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        if this.IsInPlay():
            ShinobiCloak(effect, this)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            se_camoufler,
        ),
        AbilityFactory.AfterAllyTakeConsequentialDamage(
            AbilityType.Response,
            "This",
            se_camoufler,
            conditions=[lambda effect, message: effect.this.IsInPlay()],
        ).SetCostFunc(CostFunc.Discard(
            Select.From("YourHandCards", finder=CarteShinobi("Ninjutsu"), range=(1, 1)),
        )),
    ]
