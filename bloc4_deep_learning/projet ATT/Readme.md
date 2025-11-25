# 📡 AT&T Spam Detector – Deep Learning & NLP Project

Ce projet propose un système complet de détection automatique de SPAM SMS pour l’entreprise AT&T.
Il combine exploration des données, pré-traitement NLP, modèles deep learning, et modèles Transformers afin d’identifier les spams à partir du seul contenu textuel du message.

L’ensemble de l’étude est structuré autour de plusieurs notebooks Jupyter permettant de suivre l’évolution du pipeline, de l’analyse exploratoire aux modèles avancés.

## 🧠 Objectif du projet

L’objectif du projet AT&T est de :

- analyser les SMS et comprendre les caractéristiques des messages SPAM vs HAM
- construire un modèle automatique capable d’identifier les spams
- tester plusieurs approches : réseau simple, modèle avec Sigmoid, modèle BERT
- mesurer les performances (Accuracy, F1-Score, ROC-AUC)
- optimiser la classification afin de réduire au maximum les faux négatifs (SPAM non détectés)

AT&T souhaite automatiser la détection du Spam afin de protéger ses utilisateurs, jusque-là dépendants d’un marquage manuel.

## 📂 Structure du projet

📁 AT&T Spam Detector
│
├── ATT_EDA.ipynb
├── ATT_Deep.ipynb
├── ATT_Deep2_sigmoid.ipynb
├── ATT_Deep3_bert.ipynb
└── README.md ← (ce fichier)

## 📘 Description des notebooks
1️⃣ ATT_EDA.ipynb – Analyse exploratoire

- Exploration du dataset SPAM/HAM
- Longueur des messages
- distribution des classes
- Visualisations (histogrammes, ratios SPAM/HAM)

2️⃣ ATT_Deep.ipynb – Modèle Deep Learning (baseline)

- Vectorisation (tokenizer)
- Création d’un réseau profond simple

Courbes d’entraînement : Loss & Accuracy
Matrice de confusion

3️⃣ ATT_Deep2_sigmoid.ipynb – Modèle amélioré (Sigmoid + tuning)
Identique au 2 mais avec l'augmentation du sigmoïd à 0.7

Courbes d’entraînement : Loss & Accuracy
Matrice de confusion

4️⃣ ATT_Deep3_bert.ipynb – Modèle avancé BERT

- Transfer Learning via un modèle pré-entraîné (bert-base-uncased)
- Tokenization BERT

Courbes d’entraînement : Loss & Accuracy
Matrice de confusion

## 🛠️ Technologies utilisées

- **Python** : Pandas, NumPy
- **Deep Learning** : PyTorch
- **model** : bert-tiny-finetuned, o200k_base
- **Évaluation DL** : Confusion Matrix, ROC AUC, Classification Report

##Lien Github
https://github.com/francois-minaret/CDSD/tree/main/bloc4_deep_learning/projet%20ATT

##📬 Contact
Auteur : MINARET François
🔗 LinkedIn : https://www.linkedin.com/in/minaret-fran%C3%A7ois-56106a105/
