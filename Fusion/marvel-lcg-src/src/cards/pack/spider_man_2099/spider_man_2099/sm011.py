from . import *

# Spinnerets — AMELIORATION, cout 1 [wild]. CONDITION. SUPERPOWER.
# Hero Response: After you resolve your hero's Acceleration ability, place
#   1 web counter here (to a maximum of 2).
# Hero Resource: Remove X web counters from here -> generate X [wild]
#   resources for an event.
#
# CARTES DE REFERENCE
#  - `ab007` * Donald Pierce : ecouter une capacite nommee d'une AUTRE carte
#    (`WhenResolveSpecialAbility(CardFinder(...), op)`), ici sur
#    `NOM_ACCEL_FINI`.
#  - `53006` Falcon's Flock : LE modele de la seconde capacite —
#    `CanGenerateResources(Resource, Resources(...), <CardFinder de la carte a
#    payer>).SetCostFunc(CostFunc.Counter("This", 1, '<compteur>'))`, plus
#    `SetToAvailableTimesFn` pour autoriser autant d'usages qu'il reste de
#    pions.
#  - `55055` Unified Front : meme montage, ressource wild.
#  - `ma005`, `ab007` : `CostFunc` sur une CanGenerateResources.
#
# TEXTE CONTRE CODE
#  ⚠ « place 1 web counter here (TO A MAXIMUM OF 2) » : le plafond est sur la
#    carte, pas sur le nombre de declenchements. Au-dela de 2 pions, la
#    Reponse ne doit RIEN faire — et comme c'est une Response optionnelle, le
#    test va dans `conditions`, sinon la question est posee pour rien a chaque
#    Acceleration (RECETTES §1, lecon `bc010`).
#  ⚠ Le compteur s'appelle `web` et il EXISTE DEJA dans l'enum `COUNTER`
#    (card_face.py) : rien a ajouter, contrairement a `blood`/`thirst` pour
#    Blade.
#  ⚠⚠ « Remove X web counters → generate X resources » est ecrit comme « retire
#    1 pion → 1 ressource, autant de fois que tu as de pions », et c'est
#    EQUIVALENT EN JEU : les ressources generees s'additionnent sur le meme
#    paiement. Le montage direct (`size=(1, 2)` et un `resources_fn` qui relit
#    le nombre retire) est un PIEGE connu : `resources_fn` est evalue a
#    l'ANNONCE, avant `PayCost` (RECETTES §4, lecon `ho009`), il lirait donc
#    toujours zero. `53006` Falcon's Flock, carte officielle au texte
#    « Remove 1 ... → generate a ... », emploie exactement ce montage-ci.
#  ⚠ « for an EVENT » : la ressource ne sert qu'a payer un evenement. C'est
#    l'argument `for_card` de la fabrique, pas une condition maison —
#    `53006` le fait avec `CardFinder2("AERIAL")`.
#  ⚠ « UNE SEULE `CanGenerateResources` par carte » (assert du moteur,
#    RECETTES §4) : il n'y en a bien qu'une.
#  ⚠ « Hero Response » et « Hero Resource » : la Reponse passe par
#    `WhenResolveSpecialAbility`, qui FORCE `AbilityType.Special` — impossible
#    d'y declarer le sous-type « heros ». L'ecart est nul en pratique : la face
#    `sm001a` n'est en jeu qu'en forme heros, donc le message `NOM_ACCEL_FINI`
#    ne part jamais en civil. La RESSOURCE, elle, porte bien `HeroResource`.
#  ⚠ Aucune limite « once per » imprimee : etape 7 bis sans objet. Le plafond
#    de 2 pions joue ce role et exige, lui, son propre cas : trois
#    Accelerations d'affilee doivent laisser 2 pions, pas 3.


def GetAbilities() -> Sequence['Ability']:

    def sous_le_plafond(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> bool:
        Unused(message)
        return PionsDeToile(effect.this) < 2

    def tisser(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        # `maximum=2` double la condition ci-dessus : la condition evite la
        # question inutile, le plafond garantit le chiffre meme si un autre
        # effet posait des pions entre-temps (modele `bl001b` pour l'appel).
        Faces.PlaceCountersOn([this], 1, COMPTEUR_TOILE, effect, maximum=2)

    return [
        AbilityFactory.WhenResolveSpecialAbility(
            CardFinder(card_ids=[ID_HEROS]),
            tisser,
            conditions=[sous_le_plafond],
        ).SetName(NOM_ACCEL_FINI),

        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G"),
            CardFinder(card_type=Event),
        ).SetCostFunc(CostFunc.Counter("This", 1, COMPTEUR_TOILE))
        .SetToAvailableTimesFn(
            lambda effect, message: PionsDeToile(effect.this)
        ),
    ]
