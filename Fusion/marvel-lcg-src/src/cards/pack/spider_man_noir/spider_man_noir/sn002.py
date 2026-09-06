from . import *

# Guns Blazing — EVENEMENT, cout 2, [physical]. ATTACK. TACTIC. x3.
# Hero Action (attack): Deal 4 damage to an enemy and ready Dual Pistols. If
#   this attack defeats a minion, tuck it under Spider-Man Noir from the
#   encounter discard pile (to a maximum of 3 cards).
#
# CARTES DE REFERENCE
#  - `th009` Sock 'Em / `ag006` Takedown : `if_this_attack_defeats=fn` passe a
#    `DealDamage`. La fonction est appelee PAR UNITE VAINCUE, avec l'unite en
#    argument — c'est la seule facon de conditionner un effet a « si CETTE
#    attaque-la vainc la cible ».
#  - `52001a` * Silk : glisser un sbire vaincu DEPUIS LA DEFAUSSE DE
#    RENCONTRE, et le filtre `card.area.flags.is_encounter_discard_pile` qui
#    va avec.
#  - `31009` / `an001a` : `Faces.ReadyAll`.
#
# TEXTE CONTRE CODE
#  « and ready DUAL PISTOLS » -> inconditionnel, ce n'est pas dans la branche
#    « if this attack defeats ». Le redressement tombe meme si l'attaque ne
#    vainc personne, et meme si les pistolets sont deja prets (auquel cas il
#    ne fait rien). ⚠ « Dual Pistols » n'a AUCUN homonyme au depot (verifie
#    sur les 5900 cartes) : le filtre par nom est ici legitime, contrairement
#    a « Spider-Man Noir ».
#  ⚠ « If this attack defeats A MINION » -> un SBIRE, pas « un ennemi ». Le
#    vilain vaincu ne se glisse pas. Mot-piege `Minion` vs `Enemy`, releve
#    dans RECETTES §1.
#  ⚠ « tuck IT ... FROM THE ENCOUNTER DISCARD PILE » -> le sbire vaincu y est
#    deja arrive quand la fonction est appelee. On ne le repeche donc pas, on
#    le deplace : c'est le montage de `52001a`.
#  « (to a maximum of 3 cards) » -> plafond de la pile, applique par
#    `GlisserSousIdentite`. Pile pleine, le sbire reste en defausse.
#  « Deal 4 damage to AN ENEMY » -> une seule cible, vilain ou sbire.


def GetAbilities() -> Sequence['Ability']:

    def revolvers_fumants(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)

        def si_le_sbire_tombe(unit: 'Unit2') -> None:
            # « If this attack defeats A MINION » : le vilain ne compte pas.
            if not Minion.IsType(unit):
                return
            GlisserSousIdentite(effect, [unit], joueur)

        this.DealDamage(effect.targets, 4, effect,
                        if_this_attack_defeats=si_le_sbire_tombe)

        # « and ready Dual Pistols » — inconditionnel, hors de la branche.
        pistolets = Worlds.FindCardOnField(effect, name=NOM_PISTOLETS,
                                           card_type=Upgrade)
        if pistolets is not None:
            Faces.ReadyAll([pistolets], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            revolvers_fumants,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
