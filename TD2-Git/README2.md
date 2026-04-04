# TD2 : Maîtrise de Git & GitHub

Ce guide récapitule les commandes essentielles utilisées lors du TD pour la gestion de versions.

---

## 🔍 Inspection du Dépôt

- **État actuel :** `git status`
  - *Indique les modifications locales non commitées ou non poussées.*
- **Historique :** `git log`
- **Historique compact :** `git log --oneline`
- **Différences :** `git diff`
  - *Affiche les changements entre la version actuelle et le dernier commit.*

## 💾 Gestion des Modifications

- **Staging (indexation) :** `git add .` (ou `git add readme.txt`)
- **Validation (commit) :** `git commit -m "Add readme file"`

## 🌿 Gestion des Branches

- **Lister les branches :** `git branch -a`
- **Créer une branche :** `git branch feature-script`
- **Changer de branche :** `git checkout feature-script`
- **Créer et basculer (raccourci) :** `git checkout -b dev`
- **Vérifier la branche active :** `git branch` (indiquée par une `*`)

> **Note :** Si un fichier (ex: `install.sh`) n'est pas visible, c'est probablement parce qu'il appartient à une autre branche que celle actuellement active.

## 🤝 Fusion & Nettoyage

1. Retourner sur la branche principale : `git checkout main`
2. Fusionner la branche : `git merge feature-script`
3. Vérifier les fichiers fusionnés : `ls`
4. Supprimer la branche obsolète : `git branch -d feature-script`

## 🚀 GitHub & Collaboration

- **Lier un dépôt distant :**
  ```bash
  git remote add origin https://github.com/XXXXX/XXXXX
  ```
- **Pousser vers le serveur :**
  ```bash
  git push -u origin main
  ```
- **Résultat attendu :** Les commits, fichiers et l'arborescence sont visibles sur l'interface web de GitHub.
