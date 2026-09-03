from . import *

# Prewind Stance — amelioration signature, x1 (n/16 = 16). SKILL.
# Cout 3, ressource [energy].
# Night Thrasher gets +1 DEF and gains retaliate 1.
# Hero Interrupt: When your turn or the villain phase begins, exhaust Prewind
#   Stance -> flip the Battle Board upgrade.
#
# ⚠ NOM : la carte s'appelle « Prewind Stance », alors que le fichier du zip
# s'appelle `UPGRADE - Night Thrasher_s Suit.png`. Dans ce pack les noms de
# fichiers ne sont pas les noms de cartes (voir aussi nt008).
#
# Cartes de reference :
#  - `ok014` / `im007` pour `GiveKeywordToInPlayWhenApplyThis(..., defense=1,
#    retaliate=1)`. Riposte est une BASE automatique du moteur (fiche
#    mots-cles/retaliate.md) : on ne la recode pas, on la DONNE.
#  - **`WhenPlayerTurnBegin`** (turn_phase.py:23) et **`WhenVillainPhaseBegin`**
#    (turn_phase.py:176) : DEUX messages differents, donc DEUX capacites — un
#    seul `Ability` ne peut pas ecouter les deux.
#  - `17022` * Knowhere / `as010` pour `CostFunc.Exhaust("This")`.
#  - `RetournerLaPlanche` (helper du set).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **NIGHT THRASHER** gets +1 DEF » : NOM PROPRE, la seule face HEROS.
#    L'alter-ego s'appelle Dwayne Taylor et n'a pas de DEF.
#    `CardFinder(name="Night Thrasher")`, jamais `"You"` (piege an002).
#  - « your turn **or** the villain phase begins » : DEUX declencheurs, donc
#    deux capacites. Et deux occasions de retourner la planche par round, ce
#    qui double la cadence du pack — c'est la carte la plus chere du deck (3)
#    pour cette raison.
#  - « **exhaust** Prewind Stance -> » : la fleche en fait un COUT. Deja
#    inclinee, la carte ne declenche plus : une seule bascule gratuite par
#    tour de redressement, pas deux.
#  - « **Hero** Interrupt » : rien en forme civile — or la phase du vilain
#    commence quelle que soit la forme du joueur. La capacite ne se propose
#    donc qu'au heros en costume, et c'est bien ce qui est imprime.


def GetAbilities() -> Sequence['Ability']:

    def prewind_stance(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        RetournerLaPlanche(effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name="Night Thrasher"),
            control_by="You",
            defense=1,
            retaliate=1,
        ),
        AbilityFactory.WhenPlayerTurnBegin(
            AbilityType.HeroInterrupt,
            "You",
            prewind_stance,
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.WhenVillainPhaseBegin(
            AbilityType.HeroInterrupt,
            prewind_stance,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
