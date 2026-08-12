# TODO / SPEC — L'aspect « Determination » (DesignHacker)

**Statut :** conçu le 2026-08-12, non planifié, non implémenté
**Origine :** demande utilisateur (« créer un nouvel aspect qui vient d'ici
https://designhacker.ca/ »)
**Prérequis :** `2026-08-12-nommage-contenu-fanmade.md` (le préfixe `dh`)
**Source :** https://designhacker.ca/ — « This site compiles custom fan content
for the Marvel Champions: The Living Card Game ». Téléchargements par le Workshop
Steam (Tabletop Simulator) et par Google Drive.

---

## 1. Ce que c'est

Un **cinquième aspect** de construction de deck, à côté de Aggression, Justice,
Leadership et Protection. Relevé sur le site le 12/8/2026 :

| Type | Cartes (ordre de grandeur) |
|---|---|
| Alliés | ~45 |
| Événements | ~40 |
| Améliorations | ~40 |
| Supports | ~10 |
| Ressources | 4 |
| Complots personnels | 2 |
| **Total** | **~140** |

À recompter précisément au plan : le site annonce « plus de 100 cartes » et la
répartition ci-dessus est une lecture de ses sections, pas un inventaire.

## 2. Pourquoi ce n'est PAS un ajout de contenu ordinaire

**Les sept héros ajoutés jusqu'ici (Wonder Man, Hercules, Echo…) n'ont jamais
touché au moteur.** Un aspect, si. C'est ce qui distingue ce chantier de la
méthode rodée en 7 étapes de `~/marvel-work/TODO.md`.

**Les aspects sont une liste FERMÉE dans le moteur**, mesuré le 12/8 :

`src/game/card/face/base/card_player.py:18-37` déclare deux `Literal` :

```python
ASPECT_CLASS_TYPE = Literal['Aggression', 'Justice', 'Leadership', 'Protection', "'Pool"]
CARD_CLASS        = Literal["Aggression", "Justice", "Leadership", "Protection",
                            "'Pool", "Basic", "IdentitySpecific", "Encounter",
                            "Campaign", "Aspect"]
```

Trois choses à en tirer :

1. **Un cinquième aspect a DÉJÀ été ajouté** : `'Pool` (Deadpool). Le moteur sait
   donc en accueillir un de plus ; le chemin existe.
2. **`card_player.py` est un fichier refidélisé.** Le modifier est une divergence
   volontaire, à marquer comme les autres (`CORRECTIF` commenté, ligne dans
   `QUALITE-V2.csv`).
3. Une classe `"Aspect"` générique existe déjà (« Non-Hero Non-basic card »).
   **À mesurer avant de coder** : peut-elle porter Determination sans toucher aux
   `Literal` ? Si oui, le chantier moteur disparaît presque entièrement. C'est la
   première question du plan.

### Les autres endroits qui énumèrent les aspects

Chacun est un endroit où un cinquième aspect change un comportement de jeu, pas
seulement une déclaration :

| Fichier | Ce qu'il fait |
|---|---|
| `engine/lib/image_creator.py:136` | la couleur d'aspect. Determination en a besoin d'une |
| `cards/pack/fne/echo/__init__.py:2` | `ASPECT_OR_BASIC_CLASSES`, utilisé par Echo |
| `cards/pack/moon_knight/76006.py:12` | `ASPECTS`, une carte qui parcourt les quatre |
| `game/achievements.py:154` | les hauts faits par aspect |

**Une carte qui dit « choisissez un aspect » doit-elle proposer Determination ?**
C'est une question de RÈGLE, pas de code : le livret de DesignHacker doit
trancher, et à défaut c'est une décision à prendre et à écrire.

## 3. Le nommage

Préfixe **`dh`**, selon `2026-08-12-nommage-contenu-fanmade.md` : `dh001`…
Surtout pas un préfixe numérique — les 61 à 79 sont déjà pris et FFG arrive à 61.

## 4. Les chantiers

1. **Mesurer** si la classe `"Aspect"` existante suffit, ou s'il faut étendre les
   `Literal`. Décide de tout le reste.
2. **Le préfixe `dh`** et son registre (fiche nommage).
3. **Les données** : les ~140 entrées de `cards.json`, section `dh`, plus
   `sets_info.json`.
4. **Les images** : 140 scans à récupérer. ⚠️ Voir la dette mesurée le 12/8 —
   les scans récents pèsent 577 Ko en moyenne et l'archive livrable a triplé.
   **Redimensionner à l'import**, ne pas répéter l'erreur.
5. **Les modules** : ~140 fichiers `src/cards/pack/dh/**`. C'est le gros du travail.
   La méthode en 7 étapes de `~/marvel-work/TODO.md` s'applique.
6. **La construction de deck** : le wizard et le deck-builder doivent proposer
   Determination. `public/js/prepare/` et `public/deck-builder.html`.
7. **Les tests** : `test_cards`, `test_generate_cards` (obligatoire après tout
   ajout, il attrape ce que `test_cards` ne voit pas), et l'autoplay.

## 5. À trancher

- **Tout ou une part ?** 140 cartes, c'est plus que Hercules (40) et Wonder Man
  (25) réunis. Un premier jet « les 20 cartes qui font l'aspect » serait jouable
  bien plus tôt, et dirait si le moteur suit.
- **Que faire des cartes dont l'effet n'a pas de crochet moteur ?** L'audit du
  28/7 a montré qu'une part du contenu custom reste approximée. Les approximations
  doivent être **écrites**, jamais silencieuses.
- **Determination casse-t-il l'équilibre des hauts faits ?** `achievements.py`
  compte par aspect.

## 6. Comment on saura que c'est fait

Une partie menée avec un deck Determination, du wizard à la victoire, sans
`/debug`, et `test_generate_cards` vert sur les ~140 cartes.
