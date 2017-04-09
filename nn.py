from __future__ import division
import tensorflow as tf
import numpy as np 
import os
import pandas as pd
from gamescout_db import db, cur
import time

data = pd.read_sql('select * from GamePrediction;', con=db).dropna()

data['WPCT_DIFF'] = np.abs(data['HT_WPCT'] - data['AT_WPCT'])
data['RUN_DIFF'] = np.abs(data['HT_RUN_DIFF'] - data['AT_RUN_DIFF'])
data['HT_WIN_DIFF'] = data['HT_AVG_RS_WIN'] - data['HT_AVG_RA_WIN']
data['HT_LOSS_DIFF'] = data['HT_AVG_RS_LOSS'] - data['HT_AVG_RA_LOSS']
data['AT_WIN_DIFF'] = data['AT_AVG_RS_WIN'] - data['AT_AVG_RA_WIN']
data['AT_LOSS_DIFF'] = data['AT_AVG_RS_LOSS'] - data['AT_AVG_RA_LOSS']
data['P'] = np.abs(data['HT_P_AVG'] - data['AT_P_AVG'])
data['C'] = np.abs(data['HT_C_AVG'] - data['AT_C_AVG'])
data['1B'] = np.abs(data['HT_1B_AVG'] - data['AT_1B_AVG'])
data['2B'] = np.abs(data['HT_2B_AVG'] - data['AT_2B_AVG'])
data['3B'] = np.abs(data['HT_3B_AVG'] - data['AT_3B_AVG'])
data['SS'] = np.abs(data['HT_SS_AVG'] - data['AT_SS_AVG'])
data['LF'] = np.abs(data['HT_LF_AVG'] - data['AT_LF_AVG'])
data['CF'] = np.abs(data['HT_CF_AVG'] - data['AT_CF_AVG'])
data['RF'] = np.abs(data['HT_RF_AVG'] - data['AT_RF_AVG'])

y = data[["THREE_RUN_GAME"]].astype(np.float32)
x = data[['WPCT_DIFF', 'HP_ERA', 'AP_ERA', 'HT_WIN_DIFF', 'HT_LOSS_DIFF', 'AT_WIN_DIFF', 'AT_LOSS_DIFF',
         'P', 'C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF']].astype(np.float32)


train_x = x[:8000].as_matrix()
test_x = x[8001:].as_matrix()

train_y = y[:8000].as_matrix()
test_y = y[8001:].as_matrix()

numFeatures = train_x.shape[1]
numLabels = train_y.shape[1]

numEpochs = 27000

learningRate = tf.train.exponential_decay(  learning_rate = .0008, 
                                            global_step = 1, 
                                            decay_steps = train_x.shape[0], 
                                            decay_rate = 0.95, 
                                            staircase = True)


X = tf.placeholder(tf.float32, [None, numFeatures])
yGold = tf.placeholder(tf.float32, [None, numLabels])

weights = tf.Variable(  tf.random_normal([numFeatures, numLabels], 
                            mean = 0, 
                            stddev = (np.sqrt(6 / numFeatures + numLabels + 1)), 
                            name = "weights"))

bias = tf.Variable(  tf.random_normal([1, numLabels], 
                            mean = 0, 
                            stddev = (np.sqrt(6 / numFeatures + numLabels + 1)), 
                            name = "bias"))

init_OP = tf.global_variables_initializer()
apply_weights_OP = tf.matmul(X, weights, name = "apply_weights")
add_bias_OP = tf.add(apply_weights_OP, bias, name = "add_bias")
activation_OP = tf.nn.sigmoid(add_bias_OP, name = "activation")
cost_OP = tf.nn.l2_loss(activation_OP-yGold, name="squared_error_cost")
training_OP = tf.train.GradientDescentOptimizer(learningRate).minimize(cost_OP)

# Create a tensorflow session
sess = tf.Session()

# Initialize all tensorflow variables
sess.run(init_OP)

## Ops for vizualization
# argmax(activation_OP, 1) gives the label our model thought was most likely
# argmax(yGold, 1) is the correct label
correct_predictions_OP = tf.equal(tf.argmax(activation_OP,1),tf.argmax(yGold,1))
# False is 0 and True is 1, what was our average?
accuracy_OP = tf.reduce_mean(tf.cast(correct_predictions_OP, "float"))
# Summary op for regression output
activation_summary_OP = tf.summary.histogram("output", activation_OP)
# Summary op for accuracy
accuracy_summary_OP = tf.summary.scalar("accuracy", accuracy_OP)
# Summary op for cost
cost_summary_OP = tf.summary.scalar("cost", cost_OP)
# Summary ops to check how variables (W, b) are updating after each iteration
weightSummary = tf.summary.histogram("weights", weights.eval(session=sess))
biasSummary = tf.summary.histogram("biases", bias.eval(session=sess))
# Merge all summaries
all_summary_OPS = tf.summary.merge_all()
# Summary writer
writer = tf.summary.FileWriter("summary_logs", sess.graph)

epoch_values=[]
accuracy_values=[]
cost_values=[]
# Turn on interactive plotting
plt.ion()
# Create the main, super plot
fig = plt.figure()
# Create two subplots on their own axes and give titles
ax1 = plt.subplot("211")
ax1.set_title("TRAINING ACCURACY", fontsize=18)
ax2 = plt.subplot("212")
ax2.set_title("TRAINING COST", fontsize=18)
plt.tight_layout()

# Initialize reporting variables
cost = 0
diff = 1

# Training epochs
for i in range(numEpochs):
    if i > 1 and diff < .0001:
        print("change in cost %g; convergence."%diff)
        break
    else:
        # Run training step
        step = sess.run(training_OP, feed_dict={X: train_x, yGold: train_y})
        # Report occasional stats
        if i % 5000 == 0:

            # Generate accuracy stats on test data
            summary_results, train_accuracy, newCost = sess.run(
                [all_summary_OPS, accuracy_OP, cost_OP], 
                feed_dict={X: train_x, yGold: train_y}
            )
            # Write summary stats to writer
            writer.add_summary(summary_results, i)
            # Re-assign values for variables
            diff = abs(newCost - cost)
            cost = newCost

            #generate print statements
            print("step %d, training accuracy %g"%(i, train_accuracy))
            print("step %d, cost %g"%(i, newCost))
            print("step %d, change in cost %g"%(i, diff))
            time.sleep(1)

            # How well do we perform on held-out test data?
print("final accuracy on test set: %s" %str(sess.run(accuracy_OP, 
                                                     feed_dict={X: test_x, 
                                                                yGold: test_y})))