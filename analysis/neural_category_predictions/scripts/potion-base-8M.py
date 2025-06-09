from model2vec.train import StaticModelForClassification
from load_dataset import train_test_dataset

model_name="minishlab/potion-base-8M"
#model_name="minishlab/potion-multilingual-128M" # fonctionne moins bien (probably overfit)
model = StaticModelForClassification.from_pretrained(model_name=model_name)
X_train, X_test, y_train, y_test=train_test_dataset()
model.fit(X_train, y_train)
print(model.evaluate(X_test, y_test))
