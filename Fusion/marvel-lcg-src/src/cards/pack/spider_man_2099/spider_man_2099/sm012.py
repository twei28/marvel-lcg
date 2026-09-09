from . import *

# Web Cape — AMELIORATION, cout 2 [physical]. ITEM.
# Your hero gains the AERIAL trait.
# Hero Response: After you resolve your hero's Acceleration ability, exhaust
#   Web Cape -> ready your hero.
#
# CARTES DE REFERENCE
#  - `an008`, `05023`, `ho008`, `ho011` : « Your hero gains the X trait » =
#    `GiveKeywordToAttached("You", trait="AERIAL")`.
#  - `ab007` * Donald Pierce : ecouter la capacite nommee d'une autre carte, et
#    se redresser en reponse. Ici c'est le HEROS qu'on redresse, pas la carte.
#  - `an001a`, `31009`, `ho011` : `Faces.ReadyAll([...], effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « exhaust Web Cape → ready your hero » : l'inclinaison est le COUT, le
#    redressement l'effet. Une fois par tour, donc, sans qu'aucune limite ne
#    soit imprimee — c'est l'inclinaison qui borne, et un cas doit le montrer
#    (deux Accelerations dans le meme tour, le heros redresse une seule fois).
#  ⚠ « READY YOUR HERO », pas « ready Web Cape » : la cible du redressement
#    est l'identite. C'est ce qui fait la boucle du pack — attaquer, declencher
#    Acceleration, se redresser, attaquer encore.
#  ⚠ Contrairement a `sm010` Hyper-Agility, AUCUNE condition « without playing
#    an event » : Web Cape part apres TOUTE resolution d'Acceleration, jouee
#    ou non. Trois cartes ecoutent le meme message avec trois portees
#    differentes (sm010, sm011, sm012) : c'est le piege de lecture du pack.
#  ⚠ « Hero Response » : `WhenResolveSpecialAbility` force
#    `AbilityType.Special` et ne permet pas de declarer le sous-type heros.
#    Ecart nul en pratique — la face `sm001a` n'existe qu'en forme heros, donc
#    le message ne part jamais en civil (meme remarque que sm010 et sm011).
#  ⚠⚠ « YOUR HERO gains » : le trait va sur la face HEROS, pas sur l'identite.
#    Le premier argument de `GiveKeywordToAttached` est donc `Hero`, jamais
#    `"You"` — sans quoi Miguel O'Hara serait AERIAL en civil.
#  ⚠ Le trait `AERIAL` existe deja dans l'enum `TRAITS` : rien a ajouter.
#    ⚠ Mais il n'est PAS decoratif : `AERIAL` conditionne des cartes d'aspect
#    entieres (et le moteur a deja paye un defaut « AERIAL jamais essaye », 7
#    parties bloquees, journal du 20/08). Le contre-cas dans l'AUTRE forme est
#    du : en civil, l'identite ne doit PAS porter le trait.


def GetAbilities() -> Sequence['Ability']:

    def redresser(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        heros = HerosDuJoueur(effect)
        if heros is None:
            return
        Faces.ReadyAll([heros], effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            # ⚠⚠ `Hero` ET NON `"You"` : le texte dit « YOUR HERO gains the
            # AERIAL trait ». Avec `"You"` le trait est donne a l'IDENTITE,
            # donc AUSSI a la face alter-ego — mesure du 08/09/2026 : le
            # contre-cas dans l'autre forme a trouve « AERIAL PRESENT sur
            # l'identite ». C'est exactement la lecon `an002` Sera (RECETTES
            # §3), trouvee en partie reelle sur ce pack-la et jamais par les
            # tests ; ici c'est le contre-cas qui l'a attrapee.
            Hero,
            trait=TRAIT_AERIAL,
        ),

        AbilityFactory.WhenResolveSpecialAbility(
            CardFinder(card_ids=[ID_HEROS]),
            redresser,
        ).SetName(NOM_ACCEL_FINI)
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
