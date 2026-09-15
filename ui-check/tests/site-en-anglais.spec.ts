// LES ÉCRANS DU SITE, EN ANGLAIS, DANS UN VRAI NAVIGATEUR.
//
// ⚠ POURQUOI CE FICHIER EXISTE, ALORS QU'UNE GATE LIT DÉJÀ LES SOURCES.
// `ui-app/src/site-langue.test.ts` vérifie que chaque `t('…')` a son anglais.
// Elle ne voit pas ce qui ne passe PAS par `t()` : un libellé écrit en dur dans
// le HTML, un titre d'onglet oublié. Mesure du 15/09/2026 : le salon traduisait
// tout son corps et gardait « choisis ton héros » dans l'onglet.
//
// ⚠ ET ELLE NE VOIT PAS NON PLUS UNE PAGE MORTE. Le 15/09/2026, une double
// virgule dans le dictionnaire a cassé tout le site : plus aucun script ne
// tournait. Un contrôle qui ne comptait que les lignes françaises trouvait
// alors ZÉRO — une page vide passait pour une page parfaitement traduite.
// D'où les deux gardes de ce fichier : aucune erreur JS, et assez de texte
// pour que la page ait vraiment vécu.
//
//   npm run site-en-anglais
import { expect, test } from '@playwright/test';

/**
 * Les écrans qu'un JOUEUR peut atteindre, et leur minimum de texte.
 *
 * ⚠ TROIS PAGES SONT VOLONTAIREMENT ABSENTES, et ce n'est pas un oubli :
 *  - `sandbox.html` : l'ancienne console n'est plus ouverte par le jeu, le bac
 *    à sable vit dans le plateau (voir `js/prepare/launcher.js`) ;
 *  - `fixtures.html` et `releve-images.html` : outils de chantier et
 *    d'administration, en français comme le reste de l'atelier.
 *
 * ⚠ ET `achievements.html` N'Y EST PAS ENCORE : ses 51 hauts faits arrivent du
 * MOTEUR déjà rédigés en français (`/get_achievements`), titres et
 * descriptions compris. 55 lignes françaises mesurées en anglais le
 * 15/09/2026. Les traduire demande de toucher au moteur, pas au dictionnaire
 * du site : c'est un chantier à part, pas une clé à ajouter.
 */
const ECRANS: Array<{ url: string; minimum: number }> = [
  { url: '/prepare.html?ui=new', minimum: 300 },
  { url: '/galerie.html', minimum: 1000 },
  { url: '/deck-builder.html', minimum: 2000 },
  { url: '/salon.html?p=1', minimum: 300 },
]

/**
 * Les accents ne suffisent pas à dire « ce texte est français ».
 *
 * Les NOMS DE CARTES en portent, dans les deux langues : « Coup de Grâce »
 * s'appelle ainsi en anglais aussi. Sans cette tolérance, la gate rougirait sur
 * le catalogue lui-même, qu'aucune traduction ne doit toucher.
 */
const NOMS_PROPRES = [/coup de gr[âa]ce/i, /d[ée]j[àa] vu/i, /pi[èe]ce de r[ée]sistance/i]

test.describe('le site en anglais', () => {
  for (const { url, minimum } of ECRANS) {
    test(`⚠ ${url} n'affiche pas de français`, async ({ page }) => {
      test.setTimeout(90000)
      const erreursJs: string[] = []
      page.on('pageerror', (e) => erreursJs.push(e.message))

      await page.goto('/main.html')
      await page.evaluate(() => localStorage.setItem('marvel-langue', 'en'))
      await page.goto(url, { waitUntil: 'load' })
      await page.waitForTimeout(3000)

      const vu = await page.evaluate(() => ({
        titre: document.title,
        texte: document.body.innerText,
      }))

      // 1. La page a VRAIMENT vécu. Sans ce contrôle, une page cassée passe
      //    pour une page traduite (mesuré, voir l'en-tête).
      expect(
        erreursJs,
        `erreur JavaScript sur ${url} : la page ne s'est pas chargée`
      ).toEqual([])
      expect(
        vu.texte.length,
        `${url} n'affiche que ${vu.texte.length} caractères : page vide ou cassée`
      ).toBeGreaterThan(minimum)

      // 2. Et elle parle anglais, titre de l'onglet compris.
      const francais = [vu.titre, ...vu.texte.split('\n')]
        .map((ligne) => ligne.trim())
        .filter((ligne) => ligne.length > 2 && /[àâäéèêëïîôöùûüç]/i.test(ligne))
        .filter((ligne) => !NOMS_PROPRES.some((nom) => nom.test(ligne)))
      expect(
        francais,
        `${url} affiche ${francais.length} texte(s) français en mode anglais :\n  ` +
          francais.slice(0, 10).join('\n  ')
      ).toEqual([])
    })
  }
})
