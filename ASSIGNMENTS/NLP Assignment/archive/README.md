# NLP Concepts Learning Dataset

## 1. Dataset Title
**NLP Concepts Learning Dataset** — A synthetic, educational collection of 15 CSV files (34,000 rows total) designed to teach Natural Language Processing from beginner to advanced level through hands-on, practical examples.

## 2. Dataset Description
This collection provides original, synthetically generated (non-copyrighted) English-language text data covering the full spectrum of core NLP concepts — from basic text statistics to Transformer-era tasks such as question answering and masked language modeling. Every file is self-contained, cleanly formatted, free of duplicate rows/IDs, and ready to load directly with `pandas.read_csv()`.

All text was generated programmatically using template- and vocabulary-based synthesis (no scraped or copyrighted source material), producing realistic, varied sentence structures, writing styles, and sentence lengths, with labels that are logically consistent with the underlying text (e.g. positive reviews have positive sentiment scores, QA answers are guaranteed to exist verbatim inside their context, spam messages read like spam, etc.).

## 3. Learning Objectives
By working through this dataset collection, learners will be able to:
- Compute basic text statistics and understand what makes text "clean" vs. "raw."
- Apply a full text-preprocessing pipeline (lowercasing, punctuation/number removal, tokenization, stopword removal, stemming, lemmatization).
- Understand and build Bag-of-Words and TF-IDF representations.
- Extract and reason about n-grams (unigrams, bigrams, trigrams).
- Train and evaluate sentiment analysis and emotion detection models.
- Perform Named Entity Recognition (NER) and understand structured entity extraction.
- Build multi-class text classifiers.
- Measure semantic similarity between sentences.
- Build intuition for word embeddings and semantic relationships.
- Understand core Transformer-era NLP tasks (QA, summarization, MLM, text generation, etc.).
- Build extractive question-answering systems.
- Build text summarization models.
- Build spam/ham classifiers.
- Perform topic modeling with LDA/NMF.
- Build a basic language identification classifier.

## 4. List of All CSV Files
| # | File | Rows | Columns |
|---|------|------|---------|
| 1 | `nlp_basics.csv` | 2,000 | 8 |
| 2 | `text_preprocessing.csv` | 2,000 | 8 |
| 3 | `bow_tfidf.csv` | 2,000 | 5 |
| 4 | `ngrams.csv` | 2,000 | 6 |
| 5 | `sentiment_analysis.csv` | 3,000 | 6 |
| 6 | `named_entity_recognition.csv` | 2,000 | 10 |
| 7 | `text_classification.csv` | 3,000 | 5 |
| 8 | `text_similarity.csv` | 2,000 | 6 |
| 9 | `word_embeddings.csv` | 2,000 | 6 |
| 10 | `transformer_examples.csv` | 2,000 | 6 |
| 11 | `question_answering.csv` | 2,000 | 6 |
| 12 | `text_summarization.csv` | 2,000 | 5 |
| 13 | `spam_detection.csv` | 3,000 | 5 |
| 14 | `topic_modeling.csv` | 3,000 | 4 |
| 15 | `language_detection.csv` | 2,000 | 4 |

Plus two supporting files: `dataset_summary.csv` (metadata overview of all 15 files) and `validate_dataset.py` (automated quality-check script).

## 5. Description of Every Column

### `nlp_basics.csv`
- `id`: Unique row identifier.
- `text`: An original English sentence.
- `language`: Language of the text (all "English" in this file).
- `sentence_length`: Categorical bucket — Short (≤8 words), Medium (9–15 words), Long (>15 words).
- `word_count`: Number of whitespace-separated words.
- `character_count`: Total character length of `text`.
- `uppercase_count`: Count of uppercase letters in `text`.
- `punctuation_count`: Count of punctuation characters in `text`.

### `text_preprocessing.csv`
- `id`: Unique row identifier.
- `original_text`: Raw, "messy" sentence (mixed case, punctuation, contractions, extra spaces).
- `lowercase_text`: `original_text` lowercased.
- `clean_text`: Punctuation and digits removed, whitespace normalized.
- `tokenized_text`: Python-list-style string of tokens from `clean_text`.
- `stopwords_removed`: Token list with common English stopwords removed.
- `stemmed_text`: Stopword-removed tokens passed through a simple suffix-stripping stemmer, joined into a string.
- `lemmatized_text`: Stopword-removed tokens lemmatized (e.g. "running" → "run"), joined into a string.

### `bow_tfidf.csv`
- `id`: Unique row identifier.
- `text`: A sentence from one of 8 categories.
- `category`: One of Technology, Sports, Education, Business, Health, Entertainment, Science, Travel.
- `bow_relevant_terms`: All category-relevant keywords (common + distinctive) present in `text` — what a Bag-of-Words model would flag.
- `tfidf_relevant_terms`: The subset of distinctive/rare keywords present in `text` — what TF-IDF would weight highly after downweighting common terms.

### `ngrams.csv`
- `id`: Unique row identifier.
- `text`: A sentence from one of 8 categories.
- `unigrams`: Non-stopword single tokens from `text`.
- `bigrams`: Consecutive 2-word sequences from `text`.
- `trigrams`: Consecutive 3-word sequences from `text`.
- `category`: Topic category of the sentence.

### `sentiment_analysis.csv`
- `id`: Unique row identifier.
- `text`: A review/social-post style sentence.
- `sentiment`: Positive, Negative, or Neutral.
- `sentiment_score`: Numeric score from -1.0 (very negative) to 1.0 (very positive), consistent with `sentiment`.
- `emotion`: One of Happy, Sad, Angry, Excited, Fear, Disappointed, Satisfied, Neutral (consistent with `sentiment`).
- `category`: One of Product Review, Movie Review, Food Review, Travel Review, Service Review, Social Media, Education.

### `named_entity_recognition.csv`
- `id`: Unique row identifier.
- `text`: A sentence containing one or more named entities.
- `entities`: Semicolon-separated list of entity surface forms found in `text`.
- `entity_types`: Semicolon-separated list of entity types (PERSON, ORG, GPE, DATE, MONEY, PRODUCT), aligned by position with `entities`.
- `person`: Person entity found in the sentence, if any (blank otherwise).
- `organization`: Organization entity found in the sentence, if any.
- `location`: Location (city/country) entity found in the sentence, if any.
- `date`: Date entity found in the sentence, if any.
- `money`: Monetary amount found in the sentence, if any.
- `product`: Product entity found in the sentence, if any.

> **Note:** Not every sentence contains every entity type — this mirrors real-world NER data, where blank fields simply mean "no entity of this type present." This is the one intentional source of blank/missing values in the collection.

### `text_classification.csv`
- `id`: Unique row identifier.
- `text`: A news-style sentence.
- `category`: One of 10 top-level categories (Technology, Sports, Politics, Education, Business, Health, Science, Entertainment, Travel, Environment).
- `subcategory`: A more specific subcategory within `category`.
- `difficulty`: Beginner, Intermediate, or Advanced.

### `text_similarity.csv`
- `id`: Unique row identifier.
- `sentence_1`, `sentence_2`: A pair of sentences to compare.
- `similarity_score`: Numeric score from 0 to 1, consistent with `relationship`.
- `similarity_label`: Very Low, Low, Medium, High, or Very High.
- `relationship`: Same Meaning, Paraphrase, Related, Contradiction, or Unrelated.

### `word_embeddings.csv`
- `id`: Unique row identifier.
- `word`, `related_word`: A pair of words.
- `relationship`: Synonym, Antonym, Related Concept, Category Member, Profession, Location, Object, or Action.
- `category`: Vocabulary domain (Technology, Education, Science, Sports, Business, Nature, Daily Life).
- `similarity_score`: Approximate embedding-space similarity (0–1), consistent with `relationship`.

### `transformer_examples.csv`
- `id`: Unique row identifier.
- `text`: Input text (format varies by `task` — e.g. `context|question` for QA, `sentence_1|sentence_2` for similarity).
- `task`: One of 8 Transformer-era tasks (Sentiment Analysis, Text Classification, NER, Question Answering, Text Summarization, Text Similarity, Text Generation, Masked Language Modeling).
- `input_type`: Describes the shape of the input (Single Sentence, Context + Question, Sentence Pair, Paragraph, Prompt, Masked Sentence).
- `expected_output`: The target/expected model output for the given task.
- `difficulty`: Beginner, Intermediate, or Advanced.

### `question_answering.csv`
- `id`: Unique row identifier.
- `context`: A short paragraph containing the answer.
- `question`: A question answerable from `context`.
- `answer`: The exact answer substring (verified to exist in `context`).
- `answer_start`: Character index where `answer` begins in `context`.
- `difficulty`: Beginner, Intermediate, or Advanced.

### `text_summarization.csv`
- `id`: Unique row identifier.
- `text`: A short multi-sentence article/passage.
- `summary`: A concise one-sentence summary of `text`.
- `category`: Topic category of the passage.
- `difficulty`: Beginner, Intermediate, or Advanced.

### `spam_detection.csv`
- `id`: Unique row identifier.
- `text`: A message (advertisement, scam, work message, personal note, etc.).
- `label`: Spam or Ham.
- `category`: Advertisement, Promotion, Scam, Normal Message, Notification, Work, or Personal.
- `difficulty`: Beginner, Intermediate, or Advanced.

> No real phone numbers, email addresses, passwords, or financial account numbers are included anywhere in this file.

### `topic_modeling.csv`
- `id`: Unique row identifier.
- `text`: A document/sentence about a technology- or industry-related topic.
- `topic`: One of 10 topics (Artificial Intelligence, Machine Learning, Programming, Robotics, Data Science, Cybersecurity, Cloud Computing, Education, Healthcare, Finance).
- `keywords`: Comma-separated topic-relevant keywords present in or associated with `text`.

### `language_detection.csv`
- `id`: Unique row identifier.
- `text`: A simple educational sentence.
- `language`: One of English, French, Spanish, German, Italian, Portuguese, Arabic, Hindi, Urdu.
- `language_code`: ISO-639-1-style two-letter code (en, fr, es, de, it, pt, ar, hi, ur).

### `dataset_summary.csv`
- `file_name`: Name of the CSV file.
- `concept`: The core NLP concept the file teaches.
- `number_of_rows` / `number_of_columns`: Actual dimensions of the file.
- `difficulty`: Overall difficulty level of the file.
- `description`: One-paragraph description of the file's purpose and contents.

## 6. Number of Records in Each File
See the table in Section 4 above. Total records across all 15 core files: **34,000 rows**.

## 7. NLP Concepts Covered
Text statistics · Text cleaning & normalization · Tokenization · Stopword removal · Stemming & Lemmatization · Bag of Words · TF-IDF · N-grams · Sentiment Analysis · Emotion Detection · Named Entity Recognition · Text Classification · Semantic Textual Similarity · Word Embeddings · Transformer-based task formats · Extractive Question Answering · Text Summarization · Spam Detection · Topic Modeling · Language Detection

## 8. Suggested Learning Order
1. `nlp_basics.csv` — get comfortable with text statistics.
2. `text_preprocessing.csv` — learn the standard cleaning pipeline.
3. `bow_tfidf.csv` and `ngrams.csv` — classic feature extraction.
4. `sentiment_analysis.csv` — your first supervised NLP model.
5. `named_entity_recognition.csv` — structured information extraction.
6. `text_classification.csv` — multi-class classification at scale.
7. `text_similarity.csv` and `word_embeddings.csv` — semantic representations.
8. `spam_detection.csv` — a classic applied binary classification problem.
9. `topic_modeling.csv` — unsupervised learning on text.
10. `language_detection.csv` — a lightweight applied classification task.
11. `transformer_examples.csv` — bridge into modern Transformer pipelines.
12. `question_answering.csv` and `text_summarization.csv` — advanced generative/extractive tasks.

## 9. Python Libraries That Can Be Used
- **pandas / numpy** — data loading and manipulation
- **NLTK** — tokenization, stopwords, stemming, lemmatization
- **spaCy** — NER, POS tagging, dependency parsing
- **scikit-learn** — Bag of Words, TF-IDF, classical ML classifiers, clustering, LDA/NMF
- **Gensim** — word embeddings (Word2Vec), topic modeling
- **Hugging Face Transformers** — sentiment analysis, NER, QA, summarization, text generation, MLM pipelines
- **Matplotlib / Seaborn** — visualizing label distributions, word frequencies, confusion matrices

## 10. Example Kaggle Notebook Ideas
- "From Raw Text to Clean Tokens" — a walkthrough of `text_preprocessing.csv`.
- "Bag of Words vs. TF-IDF: Visualizing the Difference" using `bow_tfidf.csv`.
- "Building Your First Sentiment Classifier" with `sentiment_analysis.csv` and scikit-learn.
- "spaCy NER from Scratch" using `named_entity_recognition.csv`.
- "Multi-Class News Classification" with `text_classification.csv` and TF-IDF + Logistic Regression.
- "Sentence Embeddings and Semantic Search" using `text_similarity.csv`.
- "Topic Modeling with LDA" using `topic_modeling.csv` and Gensim.
- "Fine-Tuning a Transformer for Question Answering" using `question_answering.csv`.
- "Spam or Ham? A Classic NLP Classification Project" using `spam_detection.csv`.
- "Detecting Language with a Simple Classifier" using `language_detection.csv`.

## 11. License Recommendation
This dataset is entirely synthetic and original. It is recommended to publish it on Kaggle under the **CC0: Public Domain** license (or, alternatively, **CC BY 4.0** if attribution is desired), since it contains no copyrighted, scraped, or personally identifiable real-world data.

## 12. Data Generation Methodology
All text in this collection was generated programmatically in Python using a combination of:
- **Curated vocabulary banks** (names, organizations, cities, countries, products, topic-specific keyword lists) built specifically for this dataset — entirely original and non-copyrighted.
- **Template-based sentence construction**, where sentence "skeletons" are combined with vocabulary substitutions, prefixes/suffixes, and paraphrase wrappers to produce a very large combinatorial space of unique, grammatically coherent sentences.
- **Label-consistent generation logic** — e.g. sentiment labels are generated together with matching adjectives and score ranges; QA answers are verified via exact substring search inside their context; similarity scores are drawn from ranges tied to their relationship label; NER entity columns are populated only with entities that actually appear in the generated sentence.
- **Deduplication at generation time** — every row is checked against a running set of previously generated (text, label) keys before being added, guaranteeing no duplicate rows and no duplicate IDs.
- **Balanced sampling** — most files use per-category/per-class quotas so that labels are evenly distributed rather than randomly skewed.
- **Automated validation** (`validate_dataset.py`) — every file is programmatically checked for missing files, duplicate rows, duplicate IDs, and missing values before publication.

No text was copied or scraped from any copyrighted source, dataset, book, or website.
