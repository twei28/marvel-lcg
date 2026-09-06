from . import *

# * Alligator Loki — SBIRE nemesis (N 2/5). ASGARD. CREATURE. UNIQUE.
#   MNG 1* / ATQ 3* — 5 PV, 2 icones de boost.
# Forced Response: After Alligator Loki enters play, find Chomped and attach
#   it to your identity.
# [star] Forced Interrupt: When Alligator Loki schemes and places threat,
#   place that much threat on each side scheme.
# [star] Alligator Loki's attacks gain piercing.
#
# ⚠ HOMONYME DU HEROS `al001a` (pack `alligator_loki`, set 140). Rien de
# commun : 5 PV contre 9, un sbire contre une identite, aucun code partage.
# `desc.Nemesis = "Throg"` marque celui-ci comme LE sbire nemesis du heros,
# ce que `01190` Shadow of the Past va chercher.
#
# MOTS-CLES (fiches lues avant d'ecrire)
#  - `piercing` (mots-cles/piercing.md) : les degats ignorent les statuts
#    Tenace. C'est dirige contre tg010 Throg's Armor, qui en distribue.
#  - `special` (mots-cles/special.md) : les deux `[star]` sont des capacites
#    PERMANENTES, sans mention « In expert mode » — convention du projet, on
#    les code TOUJOURS actives. Le premier porte en plus un type imprime
#    (`Forced Interrupt`), c'est donc ce type-la qu'on ecrit, pas
#    `NonKeywordStar` ; le second n'a pas de type et devient une capacite
#    continue de mot-cle.
#
# CARTES DE REFERENCE
#  - `56137` / `56092` / `56168` (pack cw) : `Find.FindAndAttachTo(effect,
#    <cible>, who_perform=<joueur>, name=..., card_type=Attachment)`.
#  - `wd042` / `as023` / `sr015` : `AfterEnemySchemeAndPlaceThreat(<type>,
#    <qui>, <sur quelle manigance>, op)`, avec la quantite posee lue sur
#    `message.placed_threat`.
#  - `43009` Adamantium Lacing / `27078` : `UnitAttackGainKeyword("This",
#    piercing=True)`.
#
# TEXTE CONTRE CODE
#  « find Chomped » -> « find » couvre le deck de rencontre, sa defausse, la
#    reserve et le terrain. `Find.Find` les balaie tous (find.py:118-131).
#  ⚠ « attach it to YOUR identity » -> sur une carte de RENCONTRE, « you » est
#    le joueur engage avec ce sbire, pas le premier joueur. On passe donc
#    `this.GetEngagedPlayer()` explicitement (leçon gb010 : « discard the top
#    card of YOUR deck » -> le joueur engage).
#  ⚠ « place THAT MUCH threat » -> la quantite REELLEMENT posee
#    (`message.placed_threat`), pas la MNG imprimee : un effet qui reduit la
#    menace posee doit se repercuter. Mot-piege « equal number » (`wd037`).
#  ⚠ « on EACH SIDE SCHEME » -> les complots ANNEXES seulement, pas le
#    principal, et pas celui qu'il vient de maniganser s'il s'agissait du
#    principal. Le litteral moteur est `"EachSideScheme"` (card_face.py:695) ;
#    `"EachScheme"` engloberait le principal et doublerait la mise.
#  ⚠ ECART ASSUME sur le TYPE de la premiere etoile : le texte imprime dit
#    « Forced INTERRUPT: When ... schemes AND PLACES THREAT ». On ne peut pas
#    connaitre « that much » avant que la menace soit posee : la quantite
#    n'existe qu'apres. Le moteur n'a qu'une prise pour ca,
#    `AfterEnemySchemeAndPlaceThreat`, qui est un « apres ». La contradiction
#    est dans le texte imprime (meme famille que « Forced Interrupt: After
#    Maniac schemes », The Made Men) et n'a aucune consequence observable ici :
#    rien ne peut s'intercaler entre les deux moments.


def GetAbilities() -> Sequence['Ability']:

    def appeler_la_morsure(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        joueur = this.GetEngagedPlayer()
        if not Player.IsType(joueur):
            return
        identite = joueur.GetIdentity()
        if identite is None:
            return
        Find.FindAndAttachTo(
            effect,
            identite,
            who_perform=joueur,
            name=NOM_MORSURE,
            card_type=Attachment,
        )

    def repandre_la_menace(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        this = effect.this.CastTo(Minion)

        pose = message.placed_threat
        if pose > 0:
            this.PlaceThreatOnSchemes("EachSideScheme", pose, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            appeler_la_morsure,
        ),
        AbilityFactory.AfterEnemySchemeAndPlaceThreat(
            AbilityType.ForcedInterrupt,
            "This",
            Scheme2,
            repandre_la_menace,
        ),
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
        ),
    ]
