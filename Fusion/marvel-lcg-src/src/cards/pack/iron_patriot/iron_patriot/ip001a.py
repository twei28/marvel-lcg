from . import *

# * Iron Patriot — HEROS. CTR 3, ATQ 1, DEF 2, main 5, 11 PV.
# AVENGER. H.A.M.M.E.R. REGISTERED.
# Each ally you control gains the REGISTERED trait.
# Authoritative Force — Response: After you attack and defeat a minion, you may
#   shuffle it into the REGISTERED deck. (Limit once per phase.)
#
# CARTES DE REFERENCE
#  - `06009` * Mjolnir : donner un TRAIT en continu, par la famille
#    `GiveKeyword...`. Mjolnir le fait a la carte attachee ; ici c'est a
#    CHAQUE allie controle, d'ou `GiveKeywordToInPlayWhenApplyThis` avec
#    `control_by="You"` (fabrique environment.py:66).
#  - `ab011` (pack albert) : `AfterUnitBeDefeated` et son `message.trigger`.
#
# TEXTE CONTRE CODE
#  ⚠ « EACH ALLY you control » : le trait va aux allies, pas a l'identite ni
#    aux soutiens. Un allie d'aspect ordinaire devient donc lui aussi une
#    cible des cartes REGISTERED du pack — c'est voulu, et c'est ce qui rend
#    `ip013` Call to Arms et `ip014` Seige jouables sans le deck REGISTERED.
#  ⚠ « After YOU ATTACK and defeat a minion » : le K.O. doit venir d'une
#    ATTAQUE de l'identite, pas d'un degat quelconque -> `by_attack=True` et
#    l'attaquant « You ».
#  ⚠ « YOU MAY shuffle » : optionnel, d'ou `MayChooseOneAbility`. Refuser doit
#    rester possible — le sbire va sinon grossir un deck qu'on ne veut pas
#    forcement diluer.
#  ⚠ « (Limit once per phase.) » -> `LimitOncePerPhase()`. Limite IMPRIMEE :
#    temoin d'epuisement exige (PROCESSUS-CARTE 7 bis).
#  ⚠ Le sbire est DEJA en defausse quand la Reponse resout : `.NoOutOfPlayLimit()`
#    n'est pas necessaire ici (la capacite est portee par le HEROS, qui est en
#    jeu), mais le sbire, lui, doit etre repeche depuis la defausse.

#  ⚠⚠ `attacker="You"` NE MARCHE PAS. `Condition.CheckWhichCard` connait
#    « This », « YourHero », « YouControlCharacter »... mais PAS « You » tout
#    court : la fonction tombe sur `assert not isinstance(check_rule,
#    Sequence)` (card_type.py:247) — une chaine EST une Sequence — et la
#    condition explose en silence sous le harnais. Mesure du 09/09/2026. On
#    ecrit donc « YourHero », qui existe et qui dit la meme chose ici : c'est
#    le HEROS qui attaque.


def GetAbilities() -> Sequence['Ability']:

    def force_autoritaire(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)
        joueur = effect.GetInitiator()
        sbire = message.trigger
        if joueur is None or sbire is None:
            return

        def remelanger(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            Faces.ShuffleAllTo([sbire], DeckRegistered(joueur), effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Shuffle that minion into the REGISTERED deck",
                remelanger,
            ).SetHasNoTargetEffect(),
        )

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Ally,
            control_by="You",
            trait=TRAIT_REGISTERED,
        ),
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.Response,
            Minion,
            force_autoritaire,
            attacker="YourHero",
            by_attack=True,
        ).LimitOncePerPhase(),
    ]
