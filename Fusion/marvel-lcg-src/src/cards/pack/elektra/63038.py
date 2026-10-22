from . import *

# * Moondragon (Heather Douglas) — ALLIE 4 [physical], aspect Leadership (Elektra Natchios 38). DEFENDER. MARTIAL ARTIST.
#   PV 5, THW 1*, ATK 1*.
# [star] Interrupt: When Moondragon uses a basic power, choose a number from 1 to 3. Moondragon gets +X to that power and takes +X
#   consequential damage (✪) for this use, where X is equal to the chosen number.
#
# CARTES DE REFERENCE
#  - `47012` Husk : « When X uses a basic power » = `WhenUnitUseBasicPower(Interrupt, "This", fn)` ; `message.GainValue(N, effect)` ajoute
#    N a la puissance utilisee (ATQ ou CTR) ; `message.power` dit laquelle.
#  - `tt014` Firebird : le degat consecutif « pour cet usage » = `this.GainForThisActive(effect, message, <power>_consequential_damage=N)`.
#  - `58006` Energy Siphon : « choose a number » = `joueur.DeclareNumber(min, max)`.
#  - moteur (RECETTES §3) : `Message.WhenAllyWouldTakeConsequentialDamage` n'est envoye que si la valeur IMPRIMEE est deja > 0 ;
#    Moondragon imprime ATK 1* et THW 1* (une icone chacune) : le bonus s'applique.
#
# TEXTE CONTRE CODE
#  ⚠ « choose a number FROM 1 TO 3 » : jamais 0, jamais plus de 3 (pas de choix facultatif : l'Interruption est une Interruption standard).
#  ⚠ « +X to THAT power » : ATQ si elle attaque, CTR si elle contre ; l'autre valeur ne bouge pas.
#  ⚠ « +X CONSEQUENTIAL damage for this use » : le MEME X, ajoute aux degats consecutifs imprimes (1) de cet usage seulement.
#  ⚠ Unique (✦ imprime) : « * » devant le nom.


def GetAbilities() -> Sequence['Ability']:

    def moondragon(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        x = joueur.DeclareNumber(1, 3)
        message.GainValue(x, effect)
        if message.power == "ATK":
            this.GainForThisActive(effect, message, attack_consequential_damage=x)
        elif message.power == "THW":
            this.GainForThisActive(effect, message, thwart_consequential_damage=x)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.Interrupt,
            "This",
            moondragon,
            powers=["ATK", "THW"],
        ),
    ]
