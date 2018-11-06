import montecarlo
import numpy as np

cov = np.array([[0.04,0.018,0.006], [0.018, 0.0225, 0.008], [0.0064, 0.0084, 0.006]]).reshape(3,3)
weights = np.array([[0.5, 0.0, 0.5], [0.5, 0.0, 0.5]]).reshape(-1,3)

print(np.sum(np.dot(weights, cov) * weights, axis=1))
