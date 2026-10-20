from . import *

# Quantum Bubble — amelioration signature (QUASAR 14/16, numero imprime 49 :
# card_id gs349, decision du 20/10/2026). SUPERPOWER. Cout 2, [wild].
# Hero Response: After you pay for an ally with Quantum Bands, give that ally a
#   tough status card.
#
# Cartes de reference :
#  - **`sj012`** / `sj018` (« After you play a ... card ») : factory `AfterPlayerPlayedCard(type, "You", CardFinder(
#    card_type=Ally), op, conditions=[...])` (play.py) : le message porte
#    `paid_res_effects` (les payeurs, sender_player.py) et `played_face`
#    (l'allie, deja EN JEU quand la Reponse se resout).
#  - `05015` / `19001a` pour `Faces.GiveStatus([...], "Tough", effect)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « After you PAY FOR AN ALLY » : la Reponse se resout apres le paiement ;
#    une carte d'etat ne se pose que sur un personnage EN JEU, donc a l'entree
#    en jeu de l'allie paye (meme fenetre « apres avoir joue » que le moteur
#    ouvre pour toute carte jouee). Un allie dont la mise en jeu echoue ne
#    recoit rien : il n'y a pas de « that ally » a rendre Tenace.
#  - « WITH QUANTUM BANDS » : un des payeurs est la ressource des Bandes.
#  - « THAT ally » : l'allie paye, pas un autre (`message.played_face`).
#  - « **Hero** Response » : forme heros (les Bandes ne paient d'ailleurs
#    qu'en forme heros). Facultative.
#  - Filtre en `conditions`, jamais dans le corps (RECETTES §1).


def GetAbilities() -> Sequence['Ability']:

    def payee_par_les_bandes(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> bool:
        return any(EstLesBandes(e.this) for e in message.paid_res_effects) \
            and message.played_face.IsInPlay()

    def bulle(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        Faces.GiveStatus([message.played_face], "Tough", effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.HeroResponse,
            "You",
            CardFinder(card_type=Ally),
            bulle,
            conditions=[payee_par_les_bandes],
        ),
    ]
