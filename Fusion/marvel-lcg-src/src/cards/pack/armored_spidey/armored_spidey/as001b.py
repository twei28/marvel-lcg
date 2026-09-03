from . import *

# * Peter Parker (Earth-31198) — face ALTER-EGO. PV 10, REC 3, main 6.
# BUSINESSMAN. VARIANT.
# Setup: Put your Spider Armor upgrade into play, [[OPERATIONAL]] side faceup.
#   Place 3 metal counters on it.
# Egomaniac — Response: After a player plays a card under your control,
#   draw 1 card (limit once per round per player).
#
# Cartes de reference :
#  - **`34001b`** * Jean Grey : « Setup: Put your Phoenix Force upgrade into
#    play, [[RESTRAINED]] side faceup. Place 4 power counters on it. » C'est
#    la MEME phrase, au nom et au chiffre pres :
#    `SetupPutIntoPlay(["34002a,34002b"], operation=...)` +
#    `Faces.PlaceCountersOn(faces, 4, 'power', effect)`.
#  - `31002a` * Peni Parker pour `flip_to_trait=` (« [[Inactive]] side
#    faceup »), et `26001b` * Vision pour `flip_to_name=`.
#  - `17022` * Knowhere pour `AfterPlayerPlayedCard` + pioche.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « After **a player** plays a card **under your control** » : deux
#    joueurs differents dans la meme phrase. Celui qui JOUE peut etre
#    n'importe qui ; c'est la carte qui doit arriver sous VOTRE controle.
#    `AfterPlayerPlayedCard` teste justement `message.to_player`, donc
#    `which_player="You"` rend « under your control », pas « joue par vous ».
#  - « limit once per round **per player** » : PAS une limite globale (piege
#    `wd056b`). `LimitOncePerRoundPerPlayer()`, pas `LimitOncePerRound()`.
#  - « a card », sans type : allie, evenement, soutien, amelioration,
#    ressource. Aucun filtre de type.
#  - La capacite est imprimee sur la face CIVILE : elle n'existe pas en forme
#    heros, et aucun `alter_ego_form_only` n'est necessaire pour ca.
#  - ⚠ `flip_to_trait="OPERATIONAL"` est REDONDANT (as002a EST la face
#    OPERATIONAL, donc celle du dessus a la creation), mais il est ecrit
#    quand meme : c'est le texte imprime, et il protege d'un futur
#    changement d'ordre des faces dans data/cards.json. Meme choix que
#    `31002a`, dont la face `a` est deja INACTIVE.


def GetAbilities() -> Sequence['Ability']:

    def setup(effect: 'Effect', faces: List['CardFace']) -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        Faces.PlaceCountersOn(faces, 3, 'metal', effect)

    def egomaniac(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        initiator.DrawUp(1, effect)

    return [
        AbilityFactory.SetupPutIntoPlay(
            ["as002a,as002b"],
            flip_to_trait="OPERATIONAL",
            operation=setup,
        ),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFace,
            egomaniac,
        ).SetName("Egomaniac")
        .LimitOncePerRoundPerPlayer(),
    ]
