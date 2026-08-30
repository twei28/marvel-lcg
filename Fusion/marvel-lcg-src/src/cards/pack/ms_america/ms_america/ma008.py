from . import *

# Energy Infusion — RESSOURCE signature, custom « jakxin »
# `desc.RES = "GG"` : DEUX icones [wild] imprimees (releve par decoupe
# d'image en planche, 30/08/2026). Aucun cout : c'est une carte de type
# `Resource`, elle ne se joue pas, elle se depense.
#
# Hero Response: After you spend this card to pay for a [[SUPERPOWER]] card,
#   resolve "Star-Gaze" an additional time as the same printed resource as
#   the played event.
#
# ---------------------------------------------------------------------------
# CARTE DE REFERENCE
#
# `12006` Pym Particles (pack ant) : meme fabrique
# `AbilityFactory.AfterYouSpendThisCard(AbilityType.HeroResponse, ...)`,
# meme situation (la carte est DEJA a la defausse quand la reponse part —
# la fabrique porte `.NoOutOfPlayLimit()` d'office, resources.py:547, c'est
# ce qui rend la Response atteignable). `dz018` (pack dazzler) est le meme
# montage avec un filtre de carte payee.
#
# Le filtre « pour payer une carte SUPERPOWER » est porte par le kwarg dedie
# `to_pay_card=` (resources.py:511 et 530-533), qui teste
# `message.pay_for_card`.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « After you SPEND THIS CARD » -> `AfterYouSpendThisCard`, dont la condition
#   interne est `effect.this in message.faces` (resources.py:517-518) : la
#   Response ne part que si c'est bien CETTE carte qui a paye.
# « to pay for a [[SUPERPOWER]] CARD » -> `to_pay_card=CardFinder(
#   trait=TRAIT_SUPERPOWER)`. Le mot imprime est « card », pas « event » :
#   payer une AMELIORATION SUPERPOWER (ma005, ma006, ma007) declenche aussi.
# « resolve "Star-Gaze" AN ADDITIONAL TIME » -> on rappelle `ResoudreStarGaze`
#   (helper du set), donc la MEME resolution, une seconde fois. Le premier
#   passage est celui de ma001a, declenche par `AfterPlayerPlayedCard`.
# « as the same printed resource as the PLAYED EVENT » -> la couleur n'est
#   PAS celle d'Energy Infusion (qui serait [wild] deux fois), c'est celle de
#   la carte PAYEE. On relit donc `CouleursImprimeesDe(effect,
#   message.pay_for_card)`, exactement comme Star-Gaze — Star Light (ma005)
#   comprise, si elle a change la ressource imprimee de cette carte.
#   ⚠ Sans cette lecture, la carte se contenterait de redoubler la branche
#   [wild] et vaudrait toujours « redresse Ms. America » : ce serait un autre
#   effet, plus fort.
#
# ECART DE VOCABULAIRE DE L'AUTEUR, non corrige : le texte dit « the played
# EVENT » dans la seconde moitie de la phrase alors que la premiere dit « a
# SUPERPOWER card ». On suit la premiere moitie, qui est la condition de
# declenchement : la carte payee, quel que soit son type. Lire « event » au
# sens strict rendrait la clause de couleur INAPPLICABLE quand une
# amelioration SUPERPOWER est payee, alors que la Response, elle, serait
# partie — la capacite n'aurait alors aucun effet, ce qui n'est ecrit nulle
# part.
#
# ⚠ Aucune icone de ressource n'est a coder : `desc.RES = "GG"` est lu
# nativement (has_resources.py). Coder une `CanGenerateResources` ici serait
# une capacite fantome.


def GetAbilities() -> Sequence['Ability']:

    def energy_infusion(effect: 'Effect',
                        message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(this)

        carte_payee = message.pay_for_card
        if carte_payee is None:
            return

        player = message.GetToPlayer()
        if player is None:
            return

        couleurs = CouleursImprimeesDe(effect, carte_payee)
        ResoudreStarGaze(effect, player, couleurs)

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.HeroResponse,
            energy_infusion,
            to_pay_card=CardFinder(trait=TRAIT_SUPERPOWER),
        ),
    ]
