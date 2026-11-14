# Consequential damage (dégâts consécutifs, icône ☆ sous une stat d'ally)

**Texte imprimé / définition** : l'étoile ☆ sous le THW/ATK d'un allié = il subit 1 dégât consécutif après avoir utilisé cette capacité (déjouer ou attaquer). Un texte peut aussi infliger « N consequential damage » à une carte (ex. Merged Sentry allié : « takes 1 consequential damage after he thwarts or attacks »).

**Mécanisme moteur** : `src/game/card/face/card_type/ally.py` (`take_consequential_damage`, sur `AfterUnitUseBasicPower`) ; côté prévention : `damage.py::check_is_consequential_damage` (un dégât consécutif peut être empêché comme un autre dégât). Par script : `this.DealDamage([cible], 1, effect)` après l'attaque/déjouer.

**Carte exemple** : les alliés `*` de `cards.json` (clé `ATK`/`THW` à `"2*"`), `sk283` / `sk056` (pack skrull_menace) pour un effet nommé.

**Pièges connus** : une carte qui passe sous contrôle d'un joueur « comme allié » (Merged Sentry, When Defeated) doit recevoir ce comportement par script, car sa face est un SBIRE, pas un allié : l'étoile de la stat ne suffit pas.

**Variantes maison** : aucune.
