from . import *

# * Raph's Punching Bag — SOUTIEN, cout 1, [physical]. LOCATION. NYC. SEWERS.
# UNIQUE.
# Raph gets +2 REC.
# Alter-Ego Action: Exhaust Raph's Punching Bag and remove all rage counters
#   from your identity -> draw 1 card for each rage counter removed this way.
#
# Valide en jeu : cas `tools/cas/tmnt_raphael.py` (voir .planning/todos/2026-10-16-raphael-gabarits-processus-carte.md).
#
# CARTES DE REFERENCE
#  - `ho005` (harry_osborn) : SOUTIEN qui donne un bonus continu d'identite =
#    `*GiveKeywordToInPlayWhenApplyThis(<cible>, control_by="You", recover=N)`.
#  - `42018` Angel's Aerie : « remove all X counters -> N for each removed » =
#    `CostFunc.RemoveEachCounter(cible, nom)` en COUT, puis la valeur lue par
#    `effect.cost_func.Get(CostFunc.RemoveEachCounter).return_remove_counter`.
#    (Aussi `as019`.)
#  - `26004` / `ho005` : Action d'alter-ego sur un soutien = `WhenInYourPlayTurn(
#    AbilityType.AlterEgoAction)` + `CostFunc.Exhaust("This")`.
#
# TEXTE CONTRE CODE
#  ⚠ « RAPH gets +2 REC » : Raph est le NOM de l'ALTER-EGO (`tr001b`), pas du
#    heros (« Raphael »). Cible = `AlterEgo`, jamais `Identity` : en forme
#    heros le bonus de REC ne sert a rien et ne doit pas fuir (RECETTES §3,
#    defaut `an002` Sera). Contre-cas obligatoire en forme heros en phase C.
#  ⚠ « remove ALL rage counters FROM YOUR IDENTITY » : le compteur est sur la
#    carte (partage par les deux faces) ; ici on est en alter-ego, donc il
#    faut que les compteurs gagnes en forme heros PERSISTENT apres le
#    retournement (`Counter` est un composant de la CARTE, card.py:97 ; non
#    reinitialise au flip). A VERIFIER en partie reelle.
#  ⚠ « → draw 1 card FOR EACH rage counter removed THIS WAY » : on lit le
#    nombre REELLEMENT retire, pas le nombre de compteurs avant.
#  ⚠ Ecart connu : `RemoveEachCounter` ne laisse offrir l'Action que s'il y a au
#    moins UN compteur (`has_enough_counter`, cost_func.py:960). Le texte
#    autoriserait de la payer a vide (0 pioche) : sans effet sur le jeu, et sans
#    interet.
#  ⚠ « Exhaust Raph's Punching Bag AND remove » : deux couts, avant la fleche.


def GetAbilities() -> Sequence['Ability']:

    def sac_de_frappe(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        retires = effect.cost_func.Get(CostFunc.RemoveEachCounter).return_remove_counter
        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None and retires:
            joueur.DrawUp(retires, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            AlterEgo,
            control_by="You",
            recover=2,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            sac_de_frappe,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.RemoveEachCounter("YourIdentity", RAGE)),
    ]
