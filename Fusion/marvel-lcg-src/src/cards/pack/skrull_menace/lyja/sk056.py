from . import *

# * Invisible Woman (Sue Storm) — ALLIE FANTASTIC FOUR, BASIC. Cout 3, THW 1, ATK 1, 2 PV.
# Invisible Woman takes +1 consequential damage for each revelation counter on the
#   target of her basic power.
# Forced Response: After Invisible Woman uses a basic power, place 1 revelation
#   counter on the target of that power.
#
# Cartes de reference :
#  - **`ally.py:34`** (`Ally.GetAbilities`) : les degats consecutifs sont lus dans
#    `attack_consequential_damage` / `thwart_consequential_damage` par une capacite
#    `Consequential` qui part sur `AfterUnitUseBasicPower` ; `WhenAllyWouldTakeConsequentialDamage`
#    et `does_not_take_consequential_damage` restent respectes. On AJUSTE donc ces deux
#    champs juste avant, sur `WhenUnitUseBasicPower` (modele **`20010`** / **`tg009`** :
#    « when you use a basic power », message.would_message), sans reinventer le calcul.
#  - **`50117`** Psionic Force Field pour `Faces.PlaceCountersOn(cibles, n, 'nom', effect)`.
#  - **`16152`** pour les cibles d'un pouvoir (attaque : `would_message.attacked_targets` ;
#    contre : `would_message.schemes`).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « for each revelation counter ON THE TARGET » : les compteurs DEJA poses AVANT ce
#    pouvoir ; le nouveau compteur est pose ensuite (Reponse forcee, « after »).
#  - « takes +1 consequential damage » : s'AJOUTE au consecutif imprime (aucun ici : THW 1,
#    ATK 1 sans etoile).
#  - « a basic power » : attaque ET contre (pas la defense, pas la recuperation).
#  - Nouveau compteur « revelation » (enum COUNTER, card_face.py ; defs/lyja_moteur.md).


def GetAbilities() -> Sequence['Ability']:

    def cibles_du_pouvoir(message: 'Message.WhenUnitUseBasicPower') -> List['CardFace']:
        voulu = message.would_message
        if isinstance(voulu, Message.WhenUnitWouldAttack):
            return list(voulu.attacked_targets)
        if isinstance(voulu, Message.WhenUnitWouldThwart):
            return list(voulu.schemes)
        return []

    def compter(cibles: Sequence['CardFace']) -> int:
        return sum(c.CastTo(CanPlaceCounter).GetCounters('revelation') for c in cibles if CanPlaceCounter.IsType(c))

    def avant_le_pouvoir(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        n = compter(cibles_du_pouvoir(message))
        # Le bonus precedent (un pouvoir deja utilise) est retire avant d'ajouter le nouveau :
        # les champs de degats consecutifs ne se remettent a zero qu'au `Reset` de la carte.
        ancien = getattr(this, "sk056_bonus", {"ATK": 0, "THW": 0})
        this.attack_consequential_damage += (n if message.power == "ATK" else 0) - ancien["ATK"]
        this.thwart_consequential_damage += (n if message.power == "THW" else 0) - ancien["THW"]
        this.sk056_bonus = {"ATK": n if message.power == "ATK" else 0,
                            "THW": n if message.power == "THW" else 0}

    def apres_le_pouvoir(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        fin = message.end_message
        if isinstance(fin, Message.AfterUnitAttackEnd):
            cibles = list(fin.attacked_targets)
        elif isinstance(fin, Message.AfterUnitThwartEnd):
            cibles = [s for m in fin.would_thw_messages for s in m.schemes]
        else:
            cibles = []
        cibles = [c for c in Types.RemoveDuplicates(cibles) if c.IsInPlay()]
        if cibles:
            Faces.PlaceCountersOn(cibles, 1, 'revelation', effect)

    return [
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.ForcedInterrupt,
            "This",
            avant_le_pouvoir,
        ),
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.ForcedResponse,
            "This",
            apres_le_pouvoir,
            powers=["ATK", "THW"],
        ),
    ]
