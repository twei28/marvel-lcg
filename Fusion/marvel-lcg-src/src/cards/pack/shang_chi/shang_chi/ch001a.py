from . import *

# * Shang-Chi (face HEROS) — AVENGER. MARTIAL ARTIST. PV 9, THW 1, ATK 1, DEF 1, main 5.
# Chi Mastery — Response: After you resolve a "Flow" ability, ready Shang-Chi.
#
# Cartes de reference :
#  - `01019a` * She-Hulk / `tg001a` * Throg : Response imprimee sur la face HEROS, « ready <le heros> » par
#    `Faces.ReadyAll([this], effect)`.
#  - message maison `AfterPlayerResolveFlow` (sender_player.py) + fabrique du meme nom (factory/setup.py), sur le
#    modele de `AfterPlayerResolveMulligans` (bt001b) : le moteur n'avait aucun message pour un mot-cle maison.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Response » nu : optionnel (le moteur propose), pas « Hero Response » ; imprimee sur la face HEROS, donc muette
#    en alter-ego (le Flow se resout de toute facon surtout en forme heros).
#  - « After YOU resolve » : le Flow d'un autre joueur ne declenche rien (filtre de la fabrique).
#  - « a Flow ability » : n'importe lequel des six Flow ; le message n'est envoye que si le joueur ACCEPTE de le resoudre
#    (« you MAY also resolve its effects »), jamais pour un Flow refuse ou non correspondant.


def GetAbilities() -> Sequence['Ability']:

    def chi_mastery(effect: 'Effect', message: 'Message.AfterPlayerResolveFlow') -> None:
        this = effect.this.CastTo(Hero)
        Unused(message)

        Faces.ReadyAll([this], effect)

    return [
        AbilityFactory.AfterPlayerResolveFlow(
            AbilityType.Response,
            chi_mastery,
        ).SetName("Chi Mastery"),
    ]
