from . import *

# * Doctor Pym (HANK PYM) — ALLIE de campagne (Identity-Specific / Campaign, n° 230). Cout 2.
# THW 1* / ATK 1*, 2 PV. GENIUS. SCIENTIST.
# Honorary.
# Alter-Ego Action: Exhaust Doctor Pym -> your identity gets +1 to each of its basic powers until the
#   end of the round.
#
# Cartes de reference :
#  - **`fne/daredevil/60017`** : `identity.GainUntilRoundEnd(effect, trait=[...])`, meme methode
#    (`face_action.py:440`) qui accepte aussi `attack`/`defense`/`scheme`/`thwart` — exactement « gets +1
#    to each of its basic powers until the end of the round » (les 4 pouvoirs de base).
#  - **`aoa/dystopian_nightmare/45072`** (et d'autres) : `AbilityFactory.WhenInYourPlayTurn(
#    AlterEgoAction, ...)` pour le type d'ability dedie « Alter-Ego Action ».
#
# ⚠ Mots-pieges :
#  - « YOUR IDENTITY » : l'identite du controleur, pas Doctor Pym lui-meme ;
#  - « to EACH of its basic powers » : les 4 (ATK/THW/DEF/SCH), pas seulement l'attaque ;
#  - « until the end of the round » : `GainUntilRoundEnd`, pas une capacite constante.
#  - **verifie en ecrivant le cas de test** : l'Alter-Ego n'a PAS d'ATK/DEF (`HasAttack`/`HasDefense` ne
#    s'appliquent qu'au Heros, `HasScheme` qu'a l'Alter-Ego). Premiere hypothese fausse : croire que
#    `GainUntilRoundEnd` ne s'applique qu'a la FACE ACTIVE au moment de l'appel, et qu'il fallait poser le
#    gain sur les DEUX faces (comme le hack « 31002a/31002b » de `TemporaryGain` pour `hand_size`). Le cas
#    de test prouve le contraire : un gain pose une seule fois sur l'Alter-Ego (ATK/DEF silencieusement
#    ignores, THW/SCH acceptes) PERSISTE correctement une fois passe en forme Heros (ATK/DEF/THW mesures
#    a +1 apres `Puzzle.ChangeForm`) — `ignore_flip=True` (par defaut) de `TemporaryGain` suit `this.card.face`
#    (la face COURANTE de la carte), pas une face figee. Poser le gain sur les deux faces DOUBLAIT le
#    bonus (+2 au lieu de +1), vu au premier run du cas.


def GetAbilities() -> Sequence['Ability']:

    def doctor_pym(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        joueur.GetIdentity().GainUntilRoundEnd(effect, attack=1, defense=1, scheme=1, thwart=1)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            doctor_pym,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
