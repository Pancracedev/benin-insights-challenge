# Comment le monde voit le Bénin

**Transformer les données mondiales en insights locaux pour le Bénin**

Bénin Insights Challenge 2026 — **IROKO Analytics** (Équipe 7) | iSHEERO × DataCamp Donates

---
## Qui sommes-nous ?

Nous sommes **IROKO Analytics** — comme l'arbre sacré du Bénin, nos racines plongent dans les données et notre vision porte loin.

| Rôle | Membre | Contribution |
|---|---|---|
| 🔧 Data Engineer | **GODJEDO Aubrey** | Pipeline ETL automatisé, extraction BigQuery, 72 tests unitaires |
| 📊 Data Analyst | **GUIDIGBI Randyx Emery Vianney** | Dashboard interactif Streamlit, 16 visualisations, filtres dynamiques |
| 🤖 ML Engineer | **RANDRIANIRINA Mahenina** | Modèle prédictif Random Forest, prédiction du ton médiatique |
| 🧠 Data Scientist | **Pancrace KANHONOU** | Définition des questions analytiques, coordination de l'équipe, transformation des résultats en insights, rédaction du rapport, storytelling et représentation devant le jury |

## Pourquoi c'est important

Chaque jour, des centaines de médias internationaux publient des articles qui façonnent l'image du Bénin dans le monde. Mais qui contrôle ce récit ? Quel ton domine ? Et quand le Bénin fait-il la une ?

Notre équipe a analysé **31 504 événements** et **168 000 articles de presse** couvrant le Bénin en 2025, extraits de **GDELT**, la plus grande base de données ouverte d'événements géopolitiques au monde. Nos résultats s'adressent à trois publics : les **décideurs publics**, les **journalistes** et les **chercheurs**.

---

## Notre méthode

**GDELT → Nettoyage → Analyse → Visualisation**

1. **Extraction** depuis Google BigQuery avec un filtrage intelligent séparant le Bénin de Benin City (Nigeria).
2. **Nettoyage** de 31 504 événements, enrichis de métadonnées (ton, acteurs, géolocalisation).
3. **Analyse** autour de 5 questions structurantes + 2 analyses bonus.
4. **Dashboard interactif** Streamlit avec 16 visualisations, filtres dynamiques et insights automatiques.
5. **Modèle prédictif** Random Forest pour anticiper le ton médiatique d'un événement.

Pipeline couvert par **72 tests unitaires** — 100 % de réussite.

---

## Cinq insights clés

### 1 — Décembre explose : le coup d'État déjoué change tout

Le mois de décembre 2025 totalise **30 785 articles**, soit le double de la moyenne. Le 7 décembre, le ministre de l'Intérieur **Alassane Seidou** annonce qu'une **tentative de coup d'État** a été déjouée après une brève occupation de la télévision nationale. Cet événement déclenche un pic massif de couverture.

> 🏛️ **Décideurs** : Anticiper les périodes d'attention intense pour positionner une communication institutionnelle proactive.
> 📰 **Journalistes** : Le pic de décembre est directement lié au coup d'État déjoué — un angle éditorial fort sur la stabilité politique en Afrique de l'Ouest.
> 🔬 **Chercheurs** : Les pics de couverture suivent-ils un cycle saisonnier ou sont-ils purement événementiels ? Corréler avec le calendrier politique régional.

### 2 — L'image du Bénin est dominée par les crises

**44 % des articles** ont un ton négatif. Seulement **24 % sont positifs**. Le ton moyen est de **−1,37**. Le Bénin fait la une quand ça va mal — rarement quand le pays progresse.

> 🏛️ **Décideurs** : Accompagner chaque crise d'une communication positive (accords économiques, progrès sociaux) pour rééquilibrer l'image.
> 📰 **Journalistes** : Ce ton négatif dominant reflète-t-il la réalité ou un biais éditorial ? Comparer avec le Togo et le Ghana pour investiguer.
> 🔬 **Chercheurs** : La divergence entre Goldstein (+0,68) et AvgTone (−1,37) révèle un décalage entre stabilité géopolitique réelle et perception médiatique — un cas d'étude en *framing theory*.

### 3 — La couverture est instantanée : aucune marge pour réagir

**99 % des événements** béninois sont repris par les médias internationaux **en moins de 24 heures**. Un événement à Cotonou est visible dans les rédactions du monde entier le jour même. Notre carte de propagation temporelle montre que les pics d'événements et de pays couverts sont parfaitement synchrones.

> 🏛️ **Décideurs** : Mettre en place une cellule de veille GDELT automatisée. Aucune fenêtre de temps n'existe pour préparer une réponse.
> 📰 **Journalistes** : GDELT peut servir de système d'alerte pour le fact-checking en temps réel et la détection de breaking news.
> 🔬 **Chercheurs** : Le délai varie-t-il selon le type d'événement (conflit vs coopération) ou la source (locale vs internationale) ?

### 4 — Ce sont les médias nigérians qui racontent le Bénin au monde

**7 des 10 premières sources** sont nigérianes : punchng.com (1 184 événements en période normale), dailypost.ng, guardian.ng. La première source béninoise — lanouvelletribune.info — n'arrive qu'en 6e position. En crise, **saharareporters.com** surgit.

> 🏛️ **Décideurs** : Engager les rédactions nigérianes et renforcer la visibilité de la presse béninoise à l'international.
> 📰 **Journalistes** : Pourquoi 7/10 des sources sont nigérianes ? La presse béninoise est sous-représentée — un sujet d'enquête en soi.
> 🔬 **Chercheurs** : Appliquer l'analyse de réseau (*network analysis*) pour cartographier les *gatekeepers* médiatiques du Bénin.

### 5 — Le Bénin subit plus qu'il n'agit sur la scène internationale

Dans **41 % des événements**, le Bénin est un simple décor géographique. Il n'est **acteur** que dans **31 %** des cas, via son gouvernement (788 événements) et ses forces armées (153). Le Bénin est davantage un terrain qu'un protagoniste.

> 🏛️ **Décideurs** : Multiplier les initiatives diplomatiques visibles (sommets, accords, prises de position ONU/UA/CEDEAO) pour passer de « terrain » à « acteur ».
> 📰 **Journalistes** : Qui parle à la place du Bénin ? La souveraineté narrative du pays est en jeu.
> 🔬 **Chercheurs** : Appliquer le concept de *media agency* — comparer le ratio Acteur/Contexte avec d'autres pays ouest-africains.

---

## Et aussi

- **3 025 événements graves passent sous les radars** : très négatifs mais couverts par moins de 5 articles. Ce sont des exclusivités journalistiques potentielles.
- **Carte géographique** : la couverture s'étend sur **136 pays**, concentrée sur le Bénin, le Nigeria et la France.
- **Sujets dominants** : les consultations diplomatiques dominent, suivies des déclarations publiques. En décembre, les « Déclarations publiques » explosent (+491 événements).

---

## Ce que nos résultats changent

Ces chiffres ne sont pas que des statistiques. Ce sont des **leviers pour comprendre et agir** :

- Pour les **décideurs** : des outils de veille et des recommandations concrètes.
- Pour les **journalistes** : des angles éditoriaux exclusifs et des sujets sous-couverts à investiguer.
- Pour les **chercheurs** : des hypothèses de recherche validées par les données et des cadres théoriques applicables.

**Notre projet montre que les données mondiales peuvent devenir des connaissances locales utiles. Nous sommes prêts à en faire un produit concret.**

---

## Nos livrables

| Livrable | Accès |
|---|---|
| Dépôt GitHub public | [github.com/jeangodjedo/benin-insights-challenge](https://github.com/jeangodjedo/benin-insights-challenge) |
| Notebook EDA (16+ visualisations) | `notebooks/eda_benin_gdelt_2025.ipynb` |
| Dashboard interactif Streamlit | `dashboard/app.py` |
| Pipeline ETL testé (72 tests) | `pipeline/` |
| Modèle ML sauvegardé | `models/tone_classifier_rf.pkl` |

---

**Bénin Insights Challenge 2026** · **IROKO Analytics** (Équipe 7) · iSHEERO × DataCamp Donates
Données : GDELT Project (`gdelt-bq.gdeltv2.events`) · Période : janvier–décembre 2025
