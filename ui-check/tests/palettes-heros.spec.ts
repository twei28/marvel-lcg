// L'éditeur de palettes de héros : la page s'ouvre, la carte s'agrandit, et la
// pipette remplit vraiment le champ qu'on vise.
//
// Les règles pures (hex, moyenne, coordonnées) sont éprouvées par
// tools/tests-lanceur/palettes-couleurs.test.mjs. Ici on vérifie le CÂBLAGE :
// une page qui ne s'ouvre pas, un bouton qui ne trouve pas son élément ou un
// canvas qui refuse de rendre ses pixels ne se voient que dans un navigateur.
//
//   UI_CHECK_BASE=http://127.0.0.1:40000 WSLENV=UI_CHECK_BASE npx playwright test tests/palettes-heros.spec.ts --project=pc
import { test, expect } from '@playwright/test'

test.describe('éditeur de palettes', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/palettes-heros.html')
    await expect(page.locator('#liste')).toBeVisible({ timeout: 20000 })
  })

  test('la liste montre les identités, avec leurs trois champs et un aperçu', async ({ page }) => {
    const lignes = page.locator('.p-ligne')
    await expect.poll(() => lignes.count(), { timeout: 20000 }).toBeGreaterThan(20)

    const premiere = lignes.first()
    await expect(premiere.locator('.p-hex')).toHaveCount(3)
    // Le relevé généré est déjà posé dans les champs : au moins la couleur
    // principale doit être remplie, sinon la page n'a pas lu le moteur.
    await expect(premiere.locator('.p-hex').first()).toHaveValue(/^#[0-9a-f]{6}$/)

    // L'aperçu porte le VRAI fond du plateau : un dégradé, pas un aplat.
    const fond = await premiere.locator('.p-apercu').evaluate(
      (n) => getComputedStyle(n).backgroundImage)
    expect(fond).toContain('linear-gradient')
  })

  test('la vignette agrandit la carte, et la pipette remplit le champ visé', async ({ page }) => {
    const ligne = page.locator('.p-ligne').first()
    const avant = await ligne.locator('.p-hex').first().inputValue()

    await ligne.locator('.p-scan-bouton').click()
    const loupe = page.locator('#loupe')
    await expect(loupe).toBeVisible()
    // La carte est dessinée à sa taille réelle : le canvas doit avoir des
    // pixels, sinon la pipette n'aurait rien à lire.
    await expect
      .poll(() => page.locator('#loupe-canvas').evaluate((c: HTMLCanvasElement) => c.width),
        { timeout: 20000 })
      .toBeGreaterThan(100)

    // On vise la deuxième couleur, puis on clique sur l'illustration.
    await page.locator('#loupe-cibles button').nth(1).click()
    await page.locator('#loupe-canvas').click({ position: { x: 60, y: 90 } })

    const deuxieme = ligne.locator('.p-hex').nth(1)
    await expect(deuxieme).toHaveValue(/^#[0-9a-f]{6}$/)
    // La ligne se sait modifiée : c'est ce qui rend le bouton Enregistrer utile.
    await expect(ligne).toHaveClass(/p-modifiee/)
    // Et la couleur principale n'a pas bougé : on a bien rempli la deuxième.
    await expect(ligne.locator('.p-hex').first()).toHaveValue(avant)

    // Un clic avance tout seul à la couleur suivante.
    await expect(page.locator('#loupe-cibles button').nth(2)).toHaveClass(/on/)

    await page.keyboard.press('Escape')
    await expect(loupe).toBeHidden()
  })

  test('sans compte auteur, la page le dit et n’enregistre rien', async ({ page }) => {
    // Le moteur de test n'a pas de site devant lui : `/get_site_admin` rend une
    // adresse vide, donc la page doit s'annoncer en lecture seule et garder son
    // bouton Enregistrer éteint. C'est la garde vue du joueur ; celle qui
    // compte vraiment est le 403 du moteur.
    await expect(page.locator('#message')).toContainText('Lecture seule')
    await expect(page.locator('.p-ligne').first().locator('.p-enregistrer')).toBeDisabled()
  })
})
