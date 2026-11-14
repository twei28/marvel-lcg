from . import *

# * Nuke — SBIRE NEMESIS unique (1/5). CYBORG. SOLDIER. SCH 1, ATK 2, PV 5. Boost 1.
# Forced Interrupt: When Nuke makes an attack against you, discard the top card from your deck. If an Aggression (red)
# card, or a card with a printed [physical] resource was discarded this way, that attack deals 1 additional damage.
#
# Cartes de reference :
#  - `45129` Velociraptor / `09028` Baron Mordo : `WhenUnitAttackYou(ForcedInterrupt, "This", op)` + `message.GetAgainstPlayer()`
#    + `joueur.DiscardDeckTopCard(effect)` ; `FacesCounter.GetPrintedResources([face])` (`.r` = [physical] imprime).
#  - `sender_damage.py` `WhenUnitWouldAttack.DealAdditionalDamage(n, effect)` : « that attack deals N additional damage ».
#  - `28013` No Quarter : `ClassCard.IsType(face) and face.IsClass("Aggression")` pour « an Aggression card ».
#
# ⚠ Mots-pieges :
#  - « An Aggression card OR a card with a printed [physical] resource » : DEUX tests en OU sur la MEME carte defaussee ;
#    une seule carte est defaussee, +1 degat au plus (jamais +2).
#  - « printed [physical] » : l'icone IMPRIMEE rouge ([wild] ne compte pas : `res.r`), verifiee contre un scan officiel.
#  - « against YOU » : attaque contre CE joueur ; le deck vide ne defausse rien (aucun supplement).
def GetAbilities() -> Sequence['Ability']:

    def nuke(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        joueur = message.GetAgainstPlayer()
        face = joueur.DiscardDeckTopCard(effect)
        if face is None:
            return
        agression = ClassCard.IsType(face) and face.IsClass("Aggression")
        physique = FacesCounter.GetPrintedResources([face]).r > 0
        if agression or physique:
            message.DealAdditionalDamage(1, effect)

    return [
        AbilityFactory.WhenUnitAttackYou(
            AbilityType.ForcedInterrupt,
            "This",
            nuke,
        ),
    ]
