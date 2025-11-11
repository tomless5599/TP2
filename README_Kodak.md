# 📊 Calculateur Kodak (2004) — Évaluation de la charge de travail physique

Ce projet est une **application web interactive** permettant d’évaluer la **charge de travail physique** selon la **méthode Kodak (2004)**.  
Elle classe les efforts physiques en fonction de leur **intensité**, **durée**, et **type d’activité**, afin de calculer un **score total de points** et la **consommation d’oxygène (VO₂)** associée.

---

## 🧠 Objectif

La méthode Kodak (2004) vise à quantifier la charge de travail physique pour des tâches industrielles ou ergonomiques.  
L’outil permet de reproduire cette évaluation de façon dynamique et visuelle, directement dans le navigateur.

---

## ⚙️ Fonctionnalités

### 🔹 Efforts principaux
- Ajout, suppression et modification d’efforts principaux.  
- Classification automatique selon la **Figure 8 (Kodak 2004)** :
  - **Lever/transporter**
  - **Application de forces**
  - **Monter/grimper**
- Détermination automatique du **degré d’effort** (`léger`, `modéré`, `intense`) selon :
  - Le type d’effort  
  - La charge ou force (kg ou N)  
  - Le maniement (`facile` ou `difficile`)  
- Attribution de points selon la **durée d’exposition (% du temps)** et la **Figure 9**.

### 🔹 Efforts secondaires
- Ajout, suppression et paramétrage d’efforts secondaires selon la **Figure 10** :
  - Posture, cadence, petits muscles, etc.  
- Sélection automatique des points associés selon les conditions d’exposition.

### 🔹 Résultats automatiques
- Calcul du **total des points** (principaux + secondaires).  
- Conversion en **consommation d’O₂ (VO₂)** selon :
  \[
  \text{VO₂ (l/min)} = 0.012 \times (\text{Total des points} - 9)
  \]
- Indication visuelle des résultats dans une interface sombre ergonomique.

---

## 💻 Technologies utilisées

- **HTML5 / CSS3** — Structure et style, thème sombre moderne.
- **JavaScript pur (ES6)** — Gestion dynamique des tableaux, calculs automatiques et interactions en temps réel.
- **Responsive design** — Interface adaptable à toutes tailles d’écran.

---

## 🧩 Structure du projet

```
Kodak.html
│
├── <head>
│   ├── <style>   → Thème sombre, mise en page et typographie
│   └── <script>  → Fonctions de calcul et de gestion des efforts
│
├── <body>
│   ├── Efforts principaux
│   ├── Efforts secondaires
│   ├── Résultats
│   └── Aide / Classification (référence Kodak 2004)
```

---

## 📖 Références

- **Kodak (2004)** – Méthode d’évaluation de la charge de travail physique  
  (Figures 8, 9, 10 : classification et barèmes de points)
- Adapté pour des usages en **ergonomie industrielle**, **analyse de poste**, et **évaluation de risques physiques**.

---

## 🚀 Utilisation

1. Ouvre le fichier `Kodak.html` dans un navigateur web.
2. Clique sur **“Ajouter un effort principal”** ou **“Ajouter un effort secondaire”**.
3. Saisis les données :
   - Poids, type d’effort, pourcentage de temps, conditions, etc.
4. Observe les résultats calculés automatiquement (points et VO₂).

---

## 🧪 Exemple d’interprétation

| Type d’effort | Poids | Maniement | % du temps | Degré | Points |
|----------------|--------|------------|-------------|--------|---------|
| Lever/transporter | 25 kg | Difficile | 40 % | Modéré | 38 |

Résultat total (incluant efforts secondaires) → **VO₂ ≈ 1.2 l O₂/min**

---

## 🧰 Limitations

- Ne remplace pas une évaluation ergonomique complète sur le terrain.  
- La méthode repose sur des plages de valeurs simplifiées selon les tableaux Kodak.
