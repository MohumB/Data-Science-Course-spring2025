# Data Science Course - Spring 2025

A comprehensive repository containing coursework assignments and a multi-phase NLP project focused on text analysis, processing pipelines, and deep learning models.

## Repository Structure

### Course Assignments

#### CA-0: Introduction to Data Science
Basic Python programming exercises covering fundamental data manipulation and visualization techniques.
- Problem sets on data structures and algorithms
- Exploratory data analysis exercises

#### CA-1: Statistical Analysis
Statistical methods and hypothesis testing with bonus implementation tasks.
- Probability distributions and statistical inference
- Data analysis with NumPy and Pandas

#### CA-2: Real-Time Data Pipeline with Kafka and PySpark

**Note: See `pySpark` branch for complete implementation**

A production-grade payment processing pipeline for "Darooghe" payment service provider.

**Technology Stack:**
- Apache Kafka for real-time event streaming
- PySpark for batch and stream processing
- MongoDB for data persistence
- Docker Compose for containerized deployment
- Kafdrop for Kafka monitoring

**Key Components:**
- **Data Ingestion:** Kafka consumer with schema validation and error handling
- **Batch Processing:** Commission analysis, transaction pattern mining, customer segmentation
- **Real-Time Processing:** Fraud detection system with velocity checks and geographic anomaly detection
- **Visualization:** Interactive dashboards for transaction monitoring and analytics

**Setup:**
```bash
docker-compose -f docker-compose-dev.yaml up --build
```

Access Kafdrop UI at http://localhost:9000

#### CA-3: Machine Learning Models
Three distinct ML tasks demonstrating various algorithms and techniques.

**Bike Rental Prediction:**
- Regression task with ensemble methods (Gradient Boosting, XGBoost, LightGBM)
- Feature engineering with cyclic encodings and interaction terms
- Cross-validation and hyperparameter tuning

**Cancer Prediction:**
- Binary classification using CatBoost, LightGBM, and XGBoost
- Model ensembling for improved accuracy
- Feature importance analysis

**Recommender System:**
- Collaborative filtering with matrix factorization
- XGBoost-based recommendation engine
- Social trust network integration

#### CA-4: Deep Learning with PyTorch
Neural network implementations for various tasks.

**Task 1: World Cup Match Prediction**
- MLP model for match outcome prediction
- Class imbalance handling with weighted loss
- FIFA 2022 World Cup simulation
- Validation accuracy: 54.55%

**Task 2: Time Series Analysis**
- Sequential data processing
- Pattern recognition in temporal data

**Task 3: Financial Data Analysis**
- Bitcoin price prediction using historical data
- Technical indicator feature engineering

#### CA-5-6: Semi-Supervised and Advanced ML
Advanced machine learning techniques and ensemble methods.

**Topics Covered:**
- Semi-supervised learning with labeled and unlabeled data
- Active learning strategies
- Ensemble methods and model stacking
- Feature selection and dimensionality reduction

### Main Project: Next Word Prediction and Language Modeling Pipeline

A three-phase NLP project analyzing literary text (David Copperfield) with progressively advanced techniques.

#### Phase 1: Text Preprocessing and Analysis

**Data Collection:**
- Web crawler for e-book acquisition
- Text extraction and cleaning pipeline

**Analysis Components:**
- Word frequency analysis and n-gram extraction (bigrams, trigrams)
- Part-of-speech (POS) tagging and transition analysis
- POS diversity metrics per sentence
- Word count statistics
- Distance metrics from last occurrence of specific POS tags

**Outputs:**
- CSV datasets for visualization in Power BI
- Word clouds and frequency distributions
- POS transition matrices

#### Phase 2: Data Pipeline with PySpark

**Pipeline Architecture:**
```python
Raw Data -> Load -> Preprocess -> Feature Engineering -> Database Storage
```

**Components:**
- Data loading from multiple sources
- Text preprocessing (tokenization, normalization, stopword removal)
- Feature extraction and transformation
- Database integration with connection pooling
- Configuration management system

**Technologies:**
- PySpark for distributed processing
- SQLite for data persistence
- Modular Python scripts for pipeline stages

#### Phase 3: Deep Learning for Text Generation

**Models Implemented:**

1. **LSTM Model:**
   - Character-level language modeling
   - Bidirectional architecture
   - Temperature-based sampling for text generation

2. **Transformer Model:**
   - Custom transformer encoder-decoder architecture
   - Multi-head self-attention mechanisms
   - Positional encoding for sequence modeling

3. **Fine-tuned LLaMA 3.2:**
   - LoRA (Low-Rank Adaptation) for efficient fine-tuning
   - 8-bit quantization for memory efficiency
   - Model: meta-llama/Llama-3.2-3B-Instruct
   - Training on literary text corpus

**MLflow Integration:**
- Experiment tracking and model versioning
- Hyperparameter logging
- Model registry for deployment

**Training Pipeline:**
- Automated data loading and preprocessing
- Model training with configurable hyperparameters
- Evaluation metrics tracking
- Model checkpointing and saving

## Technologies Used

### Core Libraries
- Python 3.8+
- NumPy, Pandas for data manipulation
- Matplotlib, Seaborn, Plotly for visualization
- Scikit-learn for traditional ML
- PyTorch for deep learning

### Big Data & Streaming
- Apache Kafka (kafka-python, confluent-kafka-python)
- Apache Spark (PySpark)
- MongoDB (PyMongo)

### Deep Learning Frameworks
- PyTorch
- Transformers (Hugging Face)
- PEFT (Parameter-Efficient Fine-Tuning)
- BitsAndBytes for quantization

### Natural Language Processing
- NLTK for text preprocessing
- WordCloud for visualization
- Transformers for pre-trained models

### DevOps & Deployment
- Docker & Docker Compose
- MLflow for experiment tracking
- Git for version control

## Key Features

### Real-Time Processing (CA-2)
- Event-driven architecture with Kafka
- Micro-batch processing with configurable windows
- Fraud detection with multiple rule engines
- Checkpoint mechanism for fault tolerance

### Machine Learning (CA-3, CA-4)
- Ensemble methods with voting and stacking
- Hyperparameter optimization with GridSearchCV
- Cross-validation for robust evaluation
- Feature engineering pipelines

### Deep Learning (Phase 3)
- Custom neural architectures
- Transfer learning with fine-tuning
- Efficient training with LoRA and quantization
- Text generation with temperature sampling

### Data Engineering (Phase 2)
- Modular pipeline design
- Configuration-driven processing
- Database integration with ORM
- Scalable distributed processing

## Project Highlights

### Comprehensive Data Pipeline (CA-2, pySpark branch)
- Production-ready architecture with containerization
- Real-time fraud detection with 99%+ accuracy on rule-based checks
- Scalable processing handling 1000+ events/minute
- Complete observability with Kafdrop monitoring

### Advanced NLP (Main Project Phase 3)
- Fine-tuned LLaMA 3.2 model on literary text
- Custom transformer implementation from scratch
- MLflow integration for reproducible experiments
- Multiple model comparisons (LSTM vs Transformer vs LLaMA)

### Machine Learning Best Practices (Throughout)
- Cross-validation for all models
- Proper train/validation/test splits
- Feature engineering with domain knowledge
- Model ensembling for improved performance
- Handling class imbalance with weighted losses

## Contributors

Student IDs: [Moho](https://github.com/MohumB), [Parmis](https://github.com/parmisDavari), [Narges](https://github.com/nelyasi71)

## License

This repository contains academic coursework for educational purposes.
