from . import *

# * Lady Sif (face alter-ego) — ASGARD. SOLDIER.
# REC 4 — HS 6 / PV 13
# Shieldmaiden — Action: Ready a friendly ASGARD character.
#   (Limit once per round.)
#
# Cartes de reference :
#  - `ho011` / `vv009` pour `Faces.ReadyAll(...)` ;
#  - `aa003` * Ebony pour le montage « Action portee par la face alter-ego » ;
#  - `an013` / `aa001a` pour `.LimitOncePerRound()`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - Le type imprime est **`Action` nu**, pas `Alter-Ego Action`. La
#    distinction n'a aucune consequence ICI — la carte EST la face
#    alter-ego, elle n'existe que dans cette forme — mais on ecrit ce qui est
#    imprime : `AbilityType.Action`. Meme lecture que l'`Interrupt` nu de
#    hk001b.
#  - « a FRIENDLY [[ASGARD]] character » : un personnage amical, donc
#    l'identite elle-meme ou un allie, et pas un sbire ASGARD adverse
#    (Enchantress et Skurge du set nemesis en portent le trait !). D'ou
#    `"YouControlUnit"`, qui borne au controle du joueur.
#    ⚠ Se redresser soi-meme est legal et voulu : la face alter-ego porte le
#    trait ASGARD, et un alter-ego incline par ls013 Captivating Wiles peut se
#    remettre debout.
#  - `canbe_ready=True` : une carte deja redressee n'est pas une cible legale,
#    sinon l'action se propose pour ne rien faire (leçon du blocage Underling,
#    ou une action sans effet faisait tourner le pilote en rond).
#  - « (Limit once per ROUND) », pas par phase.


def GetAbilities() -> Sequence['Ability']:

    def shieldmaiden(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        Faces.ReadyAll(list(effect.targets), effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            shieldmaiden,
        ).SetName("Shieldmaiden")
        .LimitOncePerRound()
        .SetTarget("YouControlUnit", trait="ASGARD", canbe_ready=True),
    ]
