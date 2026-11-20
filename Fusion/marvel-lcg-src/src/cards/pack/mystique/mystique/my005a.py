from . import *

# Friend (face VISIBLE, `a`) : AMELIORATION (CONDITION. SUPERPOWER.) PERMANENTE, forme metamorphe. Sans cout.
# Shapeshift Form. Permanent.
# Action: Exhaust Friend -> ready a hero other than Mystique or an ally.   (FR 1.1.1 ; l'EN beta 4.2 dit « ready a character other than Mystique » : le FR, plus recent, prime)
# Forced Response: When this card is turned faceup, flip each other shapeshift form upgrade facedown.
#
# CARTES DE REFERENCE
#  - `23016` Command Team : `Action` + `CostFunc.Exhaust("This")` + `Faces.ReadyAll(cibles, effect)` pour « ready an ally » ; la cible « hero OU ally » ne s'exprime pas par un seul `SetTarget` : choix dynamique
#    par `joueur.AskChooseFace` (modele `my002`).
#  - `26002b` Dense (vision) / `state.py` : `AfterCardFlipToThisSide` pour « when THIS card is turned faceup ».
#
# TEXTE CONTRE CODE
#  « ready a HERO OTHER THAN MYSTIQUE or an ALLY » : un heros (identite en forme heros) de n'importe quel joueur autre que Mystique, ou un allie de n'importe quel joueur ; jamais l'alter-ego, jamais Mystique. Seules
#    les cartes INCLINEES sont proposees (redresser une carte prete n'est pas un effet). « Exhaust Friend » : cout. « WHEN THIS CARD IS TURNED FACEUP » : le retournement de b vers a, pas la mise en jeu.
#  Chiffres : aucun.


def GetAbilities() -> Sequence['Ability']:

    def candidats(effect: 'Effect') -> List['CardFace']:
        return [f for f in Worlds.GetOnFieldFriendlyCharacters(effect)
                if (Ally.IsType(f) or (Hero.IsType(f) and not f.IsName(NOM_MYSTIQUE))) and not f.IsReady()]

    def un_candidat(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        return bool(candidats(effect))

    def redresser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        cibles = candidats(effect)
        if not cibles:
            return
        choisie = joueur.AskChooseFace(cibles, effect, prompt="Choose a hero other than Mystique, or an ally, to ready", peek=True, not_move=True)
        if choisie is not None:
            Faces.ReadyAll([choisie], effect)

    def retourner_les_autres(effect: 'Effect', message: 'Message.AfterCardFlip') -> None:
        Unused(message)
        this = effect.this
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        for forme in Formes(joueur):
            if forme.card is not this.card and EstVisible(forme):
                RetournerCachee(forme, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            redresser,
            conditions=[un_candidat],
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.AfterCardFlipToThisSide(
            AbilityType.ForcedResponse,
            retourner_les_autres,
        ),
    ]
