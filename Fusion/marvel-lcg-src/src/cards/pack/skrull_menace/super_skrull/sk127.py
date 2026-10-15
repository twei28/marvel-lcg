from . import *

# Lord Kl'rt — ATTACHEMENT (Super-Skrull). TITLE. Icone d'amplification (desc
# Amplify), icone ★ de boost seule (pas d'icone Y).
# Attach to Super-Skrull.
# Hero Action: Reveal the top card of the SUPERPOWER deck → discard this card.
# ★ Boost: Reveal this card.
#
# Cartes de reference :
#  - **`gb014`** Vicious Tendrils : « Attach to <vilain> » + Action de heros qui
#    defausse la carte, avec un cout a gauche de la fleche
#    (`PlayerActionToDiscardThis(HeroAction).SetCostFunc(...)`).
#  - **`gmw/collector_1/16074`** : `CostFunc.Custom(Select.From("This"), fn)` pour
#    un cout qui n'est pas une ressource ; `CostFunc.LookAtDeck` pour la forme
#    « cout impossible si le paquet est trop petit » (`check_effect_fn`).
#  - **`sk115`** (Army of Skrulls) : `WhenCardBecomeBoost("This", RevealThisCard)`.
#  - **`16054`** Vendetta / fiche amplify.md : l'icone d'amplification est une cle
#    desc (`"Amplify": "1"`), aucun script.
#
# ⚠ Mots-pieges : la FLECHE separe cout et effet : reveler la carte du dessus du
# paquet SUPERPOWER est le COUT (il donne un pouvoir de plus au mechant), defausser
# Lord Kl'rt l'EFFET ; paquet vide : le cout ne peut pas etre paye, l'action n'est
# pas proposee (lecture litterale) ; « Hero Action » (forme heros, pas alter ego) ;
# l'icone du centre de la boite de texte est l'AMPLIFICATION (croix + avion,
# convention validee le 15/10/2026) : la transcription l'avait prise pour une
# « icone de heros ».


def GetAbilities() -> Sequence['Ability']:

    def paquet_non_vide(effect: 'Effect', face: 'CardFace') -> bool:
        return PaquetNonVide(effect)

    def reveler_le_dessus(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        return RevelerSuperpouvoir(effect)

    cout = CostFunc.Custom(Select.From("This", finder=CardFinder(check_effect_fn=paquet_non_vide)), reveler_le_dessus)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name=NOM_MECHANT, card_type=Villain)),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCostFunc(cout),
        AbilityFactory.WhenCardBecomeBoost("This", RevealThisCard),
    ]
