# Learning Curves Notes: Understanding Training Behavior in Deep Learning

This document summarizes key patterns observed in training and validation curves, and how to diagnose model behavior during training.

The goal is not just to look at graphs, but to understand what they imply about learning dynamics and model performance.

---

## Core Idea

At a high level, training curves reflect how well a model is learning over time:

- **Loss** → measures error (continuous)  
- **Accuracy** → measures correctness (discrete)

These two metrics behave differently and must be interpreted together.

---

## Key Insight

Loss and accuracy do not evolve in the same way:

- Loss improves **smoothly**
- Accuracy improves in **steps (plateaus and jumps)**

This happens because:

- Loss measures *distance to the correct answer*
- Accuracy measures *whether the prediction crossed a threshold*

---

## Why Accuracy Shows Plateaus

In classification:

- Predictions are converted using a threshold (e.g., 0.5)

Example:

- Prediction: 0.3 → incorrect  
- Prediction: 0.4 → still incorrect  
→ Loss improves, but accuracy stays the same

- Prediction: 0.51 → correct  
→ Accuracy suddenly increases

Accuracy only changes when predictions cross the decision boundary.

---

## Types of Learning Behavior

### 1. Healthy Training

**Characteristics:**

- Training and validation loss decrease smoothly  
- Small gap between training and validation metrics  
- Curves eventually converge  

👉 Indicates good generalization

---

### 2. Overfitting

**Symptoms:**

- Training loss decreases  
- Validation loss increases or plateaus  
- Training accuracy much higher than validation accuracy  

👉 Model memorizes training data but fails to generalize

**Solutions:**

- Regularization (dropout, weight decay)  
- Early stopping  
- Data augmentation  
- Reduce model complexity  

---

### 3. Underfitting

**Symptoms:**

- Both training and validation loss remain high  
- Training accuracy is low  
- Learning plateaus early  

👉 Model is too simple or not trained enough

**Solutions:**

- Increase model capacity  
- Train for more epochs  
- Adjust learning rate  
- Improve data quality  

---

### 4. Erratic Learning Curves

**Symptoms:**

- Loss and accuracy fluctuate heavily  
- No clear upward or downward trend  
- Training is unstable  

👉 Model fails to learn consistently

**Common Causes:**

- Learning rate too high  
- Batch size too small  
- Noisy or poorly preprocessed data  
- Exploding gradients  

**Solutions:**

- Lower learning rate  
- Increase batch size  
- Apply gradient clipping  
- Improve preprocessing  

---

## Regularization Techniques

### Dropout

Randomly disables neurons during training to prevent over-reliance on specific features.

**Effect:**

- Improves generalization  
- Adds stochasticity to training  

---

### Weight Decay

Penalizes large weights by adding a constraint to the loss function.

**Effect:**

- Encourages simpler models  
- Reduces overfitting  

---

## Early Stopping

Stops training when validation performance stops improving.

**Example:**

- `patience = 3`  
→ Stop if validation loss does not improve for 3 consecutive epochs  

**Effect:**

- Prevents overfitting  
- Saves training time  

---

## What Matters Conceptually

1. Loss and accuracy tell different stories  
   - Loss shows *how close*  
   - Accuracy shows *whether correct*  

2. Plateaus do not mean learning stopped  
   - The model may still be improving internally  

3. Validation metrics are the source of truth  
   - Training metrics alone can be misleading  

4. Learning stability matters  
   - Unstable curves often indicate hyperparameter issues  

---

## Common Failure Points

- Focusing only on accuracy  
- Ignoring validation loss trends  
- Using too high learning rate  
- Over-regularizing (causing underfitting)  
- Misinterpreting plateaus as no learning  

---

## Why This Matters

Understanding learning curves allows you to:

- Diagnose training problems quickly  
- Choose the right fixes (not guess blindly)  
- Distinguish between overfitting, underfitting, and instability  

It turns training from trial-and-error into a more principled process.

---

## Next Steps

- Visualize real training curves and classify them  
- Experiment with learning rate and batch size  
- Compare effects of dropout vs weight decay  
- Practice diagnosing models from logs alone  