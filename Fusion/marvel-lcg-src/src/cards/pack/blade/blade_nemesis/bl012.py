from . import *

# Blood Hunt — MANIGANCE ANNEXE nemesis (N 1/8), 4 menaces par joueur, 2 boost.
# Non-VAMPIRE minions gain the VAMPIRE trait and the following text: "Attacks
#   with piercing deal double damage to this minion." VAMPIRE minions get +3 hit
#   points and gain teamwork (VAMPIRE).
# Response: After a VAMPIRE minion is defeated, remove 2 threat from this scheme.
#
# CARTES DE REFERENCE
#  - `ar011` Athena's Guidance / `40101` : `GiveKeywordToInPlayWhenApplyThis(
#    CardFinder(card_type=Minion), ...)`, avec `trait=`, `health=`, `teamwork=`
#    (fiche teamwork.md : le trait doit exister dans l'enum, VAMPIRE existe).
#  - `39051` Vampire : `UpdateAttacksDealDamage(with_piercing=True, ...,
#    update_damage_rule="Double")`.
#  - `39043` Goblin : `this.RemoveThreatFromSchemes([face], 2, effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ Les non-VAMPIRE GAGNENT le trait, PUIS « VAMPIRE minions get +3 hit points
#    and gain teamwork » : sous Blood Hunt, TOUS les sbires sont vampires, tous
#    ont +3 PV et teamwork (VAMPIRE). Un seul appel, sans filtre de trait.
#  ⚠ Le texte de doublement n'est donne qu'aux non-VAMPIRE IMPRIMES : un Vampire
#    (39051, bl014) ou Dracula l'ont deja, le leur donner encore ferait x4.
#    Le filtre lit les traits IMPRIMES (`paper.traits`), pas les traits en jeu.
#    ⚠ Un sbire Embraced (bl016) sous Blood Hunt cumule bien les deux textes
#    (x4) : c'est la lecture litterale, assumee.
#  ⚠ « Response » -> facultative, au joueur : `AfterUnitBeDefeated(Response,
#    Minion, op)`, l'ecriture EXACTE de `27174a` Public Outcry (carte
#    officielle de rencontre). « After a VAMPIRE minion is defeated » -> par
#    n'importe qui, n'importe comment.
#  ⚠⚠ PAS de filtre de trait sur le sbire vaincu, et c'est voulu : tant que
#    Blood Hunt est en jeu, TOUT sbire est VAMPIRE (premier paragraphe), donc
#    tout sbire vaincu compte. Et le filtre est IMPOSSIBLE : au moment du
#    « After ... defeated », le sbire a deja quitte le jeu et n'applique plus
#    Blood Hunt (journal : « n'appliquent plus » AVANT la Response), le trait
#    accorde a disparu -> un `CardFinder(trait="VAMPIRE")` ne matchait jamais
#    (cas bl012 du 07/09/2026, menace restee a 4).


def GetAbilities() -> Sequence['Ability']:

    def percante(effect: 'Effect', message: 'Message.WhenRecalculateAttackDamage') -> bool:
        Unused(effect)
        return bool(message.would_atk_message.property.piercing)

    def sbire_sans_texte_propre(effect: 'Effect', message: 'Message.WhenRecalculateAttackDamage') -> bool:
        Unused(effect)
        cible = message.target
        if cible is None or not Minion.IsType(cible):
            return False
        return TRAIT_VAMPIRE not in list(getattr(cible.paper, "traits", []) or [])

    def doubler(effect: 'Effect', message: 'Message.WhenRecalculateAttackDamage') -> None:
        message.IncreaseDamage(message.will_take_damage, effect)

    def chasse_au_sang(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(SchemeSide2)
        Unused(message)
        this.RemoveThreatFromSchemes([this], 2, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Minion),
            trait=TRAIT_VAMPIRE,
            health=3,
            teamwork=TRAIT_VAMPIRE,
        ),
        Ability(
            AbilityType.NonKeyword,
            Message.WhenRecalculateAttackDamage,
            [percante, sbire_sans_texte_propre],
            doubler,
        ),
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.Response,
            Minion,
            chasse_au_sang,
        ),
    ]
