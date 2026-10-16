from . import *

# * Heavy Metal (Jenny) — ALLIE double aspect Aggression/Protection (Inkwire, TMNT Aspects).
# Cout 4, PV 2, THW 1 / ATK 2 (1 degat consecutif chacun), ressource [energy].
#
# Heavy Metal enters play with 2 amp counters on her.
# Response: After Heavy Metal takes consequential damage ([consequential]), remove 1 amp counter
#   from her -> place a status card on a character.
#
# Cartes de reference :
#  - « enters play with N <nom> counters on her » : 01066 Hawkeye (`ThisEnterPlayWithCounters(4,
#    'arrow')`) ; compteur « amp » ajoute a `CardFace.COUNTER` (16/10/2026) ;
#  - « After X takes consequential damage » : 19012 Martyr / tl009 Taicho
#    (`AfterAllyTakeConsequentialDamage(Response, "This", ...)`) : ne part que si des degats
#    consecutifs sont REELLEMENT subis (Tenace les empeche) ;
#  - « remove 1 <nom> counter from her -> » : 01066 Hawkeye (`CostFunc.Counter("This", 1, ...)`) ;
#  - « place a status card on a character » : dt084 Off the Cuff (« place a status card on that
#    character » : `AskChooseOneText` puis `Faces.GiveStatus`) ; 50020 The Pericles.
#
# ⚠ QUESTION OUVERTE Q-UD2 (.planning/tmnt/aspects-dual-aspect-questions.md) : QUELLES cartes
#   d'etat ? Lecture provisoire = l'option recommandee (toute carte d'etat que le jeu connait :
#   Stunned, Confused, Tough, Cloaked, Dazed, Exposed, Intensified ; on ne propose que celles que
#   le personnage choisi peut recevoir). Carte NON terminee tant que la question n'est pas tranchee.
#
# Mots-pieges : « a CHARACTER » = tout personnage (identite, allie, vilain, sbire), ami ou ennemi ;
# « remove 1 amp counter FROM HER » = cout (sans compteur, la Reponse n'est pas proposee) ;
# « takes » (degats reellement subis), pas « would take ».

STATUTS: List['CardFace.STATUS'] = ["Stunned", "Confused", "Tough", "Cloaked", "Dazed", "Exposed", "Intensified"]


def _recevables(face: 'CardFace') -> List['CardFace.STATUS']:
    """Les cartes d'etat que ce personnage peut recevoir maintenant (plafonds du moteur)."""
    if not CanStatus.IsType(face):
        return []
    f = face.CastTo(CanStatus)
    out: List['CardFace.STATUS'] = []
    for s in STATUTS:
        if s == "Stunned" and not f.CanbeStunned():
            continue
        if s == "Confused" and not f.CanbeConfused():
            continue
        if s == "Tough" and not f.CanGainTough():
            continue
        if s == "Dazed" and not f.CanbeDazed():
            continue
        if s == "Intensified" and not f.CanbeIntensified():
            continue
        if s == "Cloaked" and f.cloaked >= f.cloaked_max:
            continue
        out.append(s)
    return out


def GetAbilities() -> Sequence['Ability']:

    def poser_statut(effect: 'Effect', message: 'Message.AfterAllyTakeConsequentialDamage') -> None:
        Unused(message)
        initiator = effect.GetInitiator()
        for cible in effect.targets:
            choix = _recevables(cible)
            if not choix:
                continue
            statut = initiator.AskChooseOneText(choix)
            Faces.GiveStatus([cible], statut, effect)

    return [
        AbilityFactory.ThisEnterPlayWithCounters(2, 'amp'),
        AbilityFactory.AfterAllyTakeConsequentialDamage(
            AbilityType.Response,
            "This",
            poser_statut,
            # Vaincue par ces degats, elle n'a plus de compteur a retirer.
            conditions=[lambda effect, message: effect.this.IsInPlay()],
        ).SetCostFunc(CostFunc.Counter("This", 1, 'amp'))
        .SetTarget(Unit2),
    ]
