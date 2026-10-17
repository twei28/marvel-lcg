from . import *

# * Ram-Shell (Raph) — ALLIE 4 [physical], aspect Justice (TMNT Aspects, Inkwire). TURTLE. WARRIOR.
# Bandeau « ✦ Spider-Woman » (unique_also, decision Q-R1).
# PV 3, THW 2 (2 degats consecutifs), ATK 2 (2 degats consecutifs).
# Response: After a character you control thwarts, place 1 momentum counter here (to a maximum of 8). You
#   may discard Ram-Shell to deal 1 damage to an enemy for each momentum counter here.
#
# MODIFIEE par rapport a `61016` Spider-Woman (Mattie Franklin) : « limb counter » -> « momentum counter »,
# nom de la carte. Pas d'`ability_link` (le compteur change) : script propre, copie de 61016 adaptee.
#
# CARTES DE REFERENCE
#  - `61016` (officielle) : `AfterUnitThwartScheme(Response, "You", None, op)` +
#    `PlaceCountersInternal(1, '<compteur>', effect, maximum=8)`. ⚠ « You » n'est PAS une regle connue de
#    `Condition.CheckWhichCard` (le texte dit « a character you control ») : mesure le 16/10/2026, la Reponse
#    ne partait JAMAIS (0 compteur apres un contre). Ici `"YouControlCharacter"` (card_type.py).
#  - « You may ... » dans le corps d'une Reponse : `joueur.MayChooseOneAbility(...)` (Annuler offert).
#
# ⚠ ECART AVEC LE MODULE DE 61016, VOULU : 61016 code « You may discard Spider-Woman to deal ... » comme une
#   ACTION separee (`WhenInYourPlayTurn(Action).SetPlay()`), utilisable a tout moment de ton tour. Le scan
#   imprime cette phrase DANS la Reponse (meme paragraphe, apres la pose du compteur) : ici la defausse n'est
#   proposee qu'a la resolution de la Reponse, juste apres la pose du compteur. (61016 n'est pas modifiee.)
#
# TEXTE CONTRE CODE (PROCESSUS-CARTE etape 5)
#  ⚠ « After a CHARACTER YOU CONTROL thwarts » : ton identite ou un de tes allies (Ram-Shell compris).
#  ⚠ « place 1 momentum counter HERE (to a maximum of 8) » : sur Ram-Shell, plafond 8.
#  ⚠ « You MAY discard Ram-Shell TO deal 1 damage to AN enemy FOR EACH momentum counter here » : facultatif ;
#    une seule cible, degats = compteurs (comptes AVANT la defausse).
#  Compteur « momentum » : deja dans `CardFace.COUNTER` (Juggernaut) ; c'est le mot imprime.


def GetAbilities() -> Sequence['Ability']:

    def elan(effect: 'Effect', message: 'Message.AfterUnitThwartScheme') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        this.PlaceCountersInternal(1, 'momentum', effect, maximum=8)
        joueur = effect.GetInitiator()
        if joueur is None or not this.IsInPlay():
            return

        def charger(cibles: Sequence['CardFace']) -> None:
            n = this.GetCounters('momentum')
            if Faces.DiscardAll([this], effect) == [this] and n > 0:
                this.DealDamage(list(cibles), n, effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard Ram-Shell to deal 1 damage to an enemy for each momentum counter here", charger,
            ).SetTarget(Enemy),
        )

    return [
        AbilityFactory.AfterUnitThwartScheme(AbilityType.Response, "YouControlCharacter", None, elan),
    ]
