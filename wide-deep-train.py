# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Example code for TensorFlow Wide & Deep Tutorial using TF.Learn API."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
import tempfile
import MySQLdb

from six.moves import urllib

import pandas as pd
import tensorflow as tf

from gamescout_db import db, cur

COLUMNS = [
  'ONE_RUN_GAME',
  'HT_WPCT',
  'HT_WPCT_1R',
  'HT_WPCT_2R',
  'AT_WPCT',
  'AT_WPCT_1R',
  'AT_WPCT_2R',
  'HT_RUN_DIFF',
  'HT_AVG_RS_WIN',
  'HT_AVG_RA_WIN',
  'HT_AVG_RS_LOSS',
  'HT_AVG_RA_LOSS',
  'AT_RUN_DIFF',
  'AT_AVG_RS_WIN',
  'AT_AVG_RA_WIN',
  'AT_AVG_RS_LOSS',
  'AT_AVG_RA_LOSS',
  'HP_RUNS_PER_9',
  'HP_BB_PER_9',
  'HP_H_PER_9',
  'HP_K_PER_9',
  'HP_IP',
  'HP_ERA',
  'HP_AVG_IP',
  'AP_RUNS_PER_9',
  'AP_BB_PER_9',
  'AP_H_PER_9',
  'AP_K_PER_9',
  'AP_IP',
  'AP_ERA',
  'AP_AVG_IP',
  'HT_P_AVG',
  'HT_C_AVG',
  'HT_1B_AVG',
  'HT_2B_AVG',
  'HT_3B_AVG',
  'HT_SS_AVG',
  'HT_LF_AVG',
  'HT_CF_AVG',
  'HT_RF_AVG',
  'AT_P_AVG',
  'AT_C_AVG',
  'AT_1B_AVG',
  'AT_2B_AVG',
  'AT_3B_AVG',
  'AT_SS_AVG',
  'AT_LF_AVG',
  'AT_CF_AVG',
  'AT_RF_AVG',
  'HT_AVG_HRS',
  'AT_AVG_HRS']

LABEL_COLUMN = 'ONE_RUN_GAME'

def build_estimator(model_dir, model_type):
  """Build an estimator."""

  #HT
  #AT
  
  # Continuous base columns.
  HT_WPCT = tf.contrib.layers.real_valued_column("HT_WPCT")
  HT_WPCT_1R = tf.contrib.layers.real_valued_column("HT_WPCT_1R")
  HT_WPCT_2R = tf.contrib.layers.real_valued_column("HT_WPCT_2R")
  AT_WPCT = tf.contrib.layers.real_valued_column("AT_WPCT")
  AT_WPCT_1R = tf.contrib.layers.real_valued_column("AT_WPCT_1R")
  AT_WPCT_2R = tf.contrib.layers.real_valued_column("AT_WPCT_2R")
  HT_RUN_DIFF = tf.contrib.layers.real_valued_column("HT_RUN_DIFF")
  HT_AVG_RS_WIN = tf.contrib.layers.real_valued_column("HT_AVG_RS_WIN")
  HT_AVG_RA_WIN = tf.contrib.layers.real_valued_column("HT_AVG_RA_WIN")
  HT_AVG_RS_LOSS = tf.contrib.layers.real_valued_column("HT_AVG_RS_LOSS")
  HT_AVG_RA_LOSS = tf.contrib.layers.real_valued_column("HT_AVG_RA_LOSS")
  AT_RUN_DIFF = tf.contrib.layers.real_valued_column("AT_RUN_DIFF")
  AT_AVG_RS_WIN = tf.contrib.layers.real_valued_column("AT_AVG_RS_WIN")
  AT_AVG_RA_WIN = tf.contrib.layers.real_valued_column("AT_AVG_RA_WIN")
  AT_AVG_RS_LOSS = tf.contrib.layers.real_valued_column("AT_AVG_RS_LOSS")
  AT_AVG_RA_LOSS = tf.contrib.layers.real_valued_column("AT_AVG_RA_LOSS")
  HP_RUNS_PER_9 = tf.contrib.layers.real_valued_column("HP_RUNS_PER_9")
  HP_BB_PER_9 = tf.contrib.layers.real_valued_column("HP_BB_PER_9")
  HP_H_PER_9 = tf.contrib.layers.real_valued_column("HP_H_PER_9")
  HP_K_PER_9 = tf.contrib.layers.real_valued_column("HP_K_PER_9")
  HP_IP = tf.contrib.layers.real_valued_column("HP_IP")
  HP_ERA = tf.contrib.layers.real_valued_column("HP_ERA")
  HP_AVG_IP = tf.contrib.layers.real_valued_column("HP_AVG_IP")
  AP_RUNS_PER_9 = tf.contrib.layers.real_valued_column("AP_RUNS_PER_9")
  AP_BB_PER_9 = tf.contrib.layers.real_valued_column("AP_BB_PER_9")
  AP_H_PER_9 = tf.contrib.layers.real_valued_column("AP_H_PER_9")
  AP_K_PER_9 = tf.contrib.layers.real_valued_column("AP_K_PER_9")
  AP_IP = tf.contrib.layers.real_valued_column("AP_IP")
  AP_ERA = tf.contrib.layers.real_valued_column("AP_ERA")
  AP_AVG_IP = tf.contrib.layers.real_valued_column("AP_AVG_IP")
  HT_P_AVG = tf.contrib.layers.real_valued_column("HT_P_AVG")
  HT_C_AVG = tf.contrib.layers.real_valued_column("HT_C_AVG")
  HT_1B_AVG = tf.contrib.layers.real_valued_column("HT_1B_AVG")
  HT_2B_AVG = tf.contrib.layers.real_valued_column("HT_2B_AVG")
  HT_3B_AVG = tf.contrib.layers.real_valued_column("HT_3B_AVG")
  HT_SS_AVG = tf.contrib.layers.real_valued_column("HT_SS_AVG")
  HT_LF_AVG = tf.contrib.layers.real_valued_column("HT_LF_AVG")
  HT_CF_AVG = tf.contrib.layers.real_valued_column("HT_CF_AVG")
  HT_RF_AVG = tf.contrib.layers.real_valued_column("HT_RF_AVG")
  AT_P_AVG = tf.contrib.layers.real_valued_column("AT_P_AVG")
  AT_C_AVG = tf.contrib.layers.real_valued_column("AT_C_AVG")
  AT_1B_AVG = tf.contrib.layers.real_valued_column("AT_1B_AVG")
  AT_2B_AVG = tf.contrib.layers.real_valued_column("AT_2B_AVG")
  AT_3B_AVG = tf.contrib.layers.real_valued_column("AT_3B_AVG")
  AT_SS_AVG = tf.contrib.layers.real_valued_column("AT_SS_AVG")
  AT_LF_AVG = tf.contrib.layers.real_valued_column("AT_LF_AVG")
  AT_CF_AVG = tf.contrib.layers.real_valued_column("AT_CF_AVG")
  AT_RF_AVG = tf.contrib.layers.real_valued_column("AT_RF_AVG")
  HT_AVG_HRS = tf.contrib.layers.real_valued_column("HT_AVG_HRS")
  AT_AVG_HRS = tf.contrib.layers.real_valued_column("AT_AVG_HRS")

  # Wide columns and deep columns.
  _columns = [
    HT_WPCT,
    HT_WPCT_1R,
    HT_WPCT_2R,
    AT_WPCT,
    AT_WPCT_1R,
    AT_WPCT_2R,
    HT_RUN_DIFF,
    HT_AVG_RS_WIN,
    HT_AVG_RA_WIN,
    HT_AVG_RS_LOSS,
    HT_AVG_RA_LOSS,
    AT_RUN_DIFF,
    AT_AVG_RS_WIN,
    AT_AVG_RA_WIN,
    AT_AVG_RS_LOSS,
    AT_AVG_RA_LOSS,
    HP_RUNS_PER_9,
    HP_BB_PER_9,
    HP_H_PER_9,
    HP_K_PER_9,
    HP_IP,
    HP_ERA,
    HP_AVG_IP,
    AP_RUNS_PER_9,
    AP_BB_PER_9,
    AP_H_PER_9,
    AP_K_PER_9,
    AP_IP,
    AP_ERA,
    AP_AVG_IP,
    HT_P_AVG,
    HT_C_AVG,
    HT_1B_AVG,
    HT_2B_AVG,
    HT_3B_AVG,
    HT_SS_AVG,
    HT_LF_AVG,
    HT_CF_AVG,
    HT_RF_AVG,
    AT_P_AVG,
    AT_C_AVG,
    AT_1B_AVG,
    AT_2B_AVG,
    AT_3B_AVG,
    AT_SS_AVG,
    AT_LF_AVG,
    AT_CF_AVG,
    AT_RF_AVG,
    HT_AVG_HRS,
    AT_AVG_HRS
  ]


  if model_type == "wide":
    m = tf.contrib.learn.LinearClassifier(model_dir=model_dir,
                                          feature_columns=_columns)
  elif model_type == "deep":
    m = tf.contrib.learn.DNNClassifier(model_dir=model_dir,
                                       feature_columns=_columns,
                                       hidden_units=[100, 50])
  else:
    m = tf.contrib.learn.DNNLinearCombinedClassifier(
        model_dir=model_dir,
        linear_feature_columns=_columns,
        dnn_feature_columns=_columns,
        dnn_hidden_units=[100, 50])
  return m


def input_fn(df):
  """Input builder function."""
  # Creates a dictionary mapping from each continuous feature column name (k) to
  # the values of that column stored in a constant Tensor.
  continuous_cols = {k: tf.constant(df[k].values) for k in COLUMNS}

  # Merges the two dictionaries into one.
  feature_cols = dict(continuous_cols)
  # Converts the label column into a constant Tensor.
  label = tf.constant(df[LABEL_COLUMN].values)
  # Returns the feature columns and the label.
  return feature_cols, label


def train_and_eval(model_dir, model_type, train_steps, train_data, test_data):
  """Train and evaluate the model."""

  df_train = pd.read_sql('select * from GamePrediction where G_DATE < "2012-05-11";', columns=COLUMNS, con=db) 
  df_test = pd.read_sql('select * from GamePrediction where G_DATE > "2012-05-11";', columns=COLUMNS, con=db) 

  # remove NaN elements
  df_train = df_train.dropna(how='any', axis=0)
  df_test = df_test.dropna(how='any', axis=0)

  model_dir = tempfile.mkdtemp() if not model_dir else model_dir
  print("model directory = %s" % model_dir)

  m = build_estimator(model_dir, model_type)
  m.fit(input_fn=lambda: input_fn(df_train), steps=train_steps)
  results = m.evaluate(input_fn=lambda: input_fn(df_test), steps=1)
  for key in sorted(results):
    print("%s: %s" % (key, results[key]))

FLAGS = None

def main(_):
  train_and_eval(FLAGS.model_dir, FLAGS.model_type, FLAGS.train_steps,
                 FLAGS.train_data, FLAGS.test_data)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.register("type", "bool", lambda v: v.lower() == "true")
  parser.add_argument(
      "--model_dir",
      type=str,
      default="",
      help="Base directory for output models."
  )
  parser.add_argument(
      "--model_type",
      type=str,
      default="wide_n_deep",
      help="Valid model types: {'wide', 'deep', 'wide_n_deep'}."
  )
  parser.add_argument(
      "--train_steps",
      type=int,
      default=200,
      help="Number of training steps."
  )
  parser.add_argument(
      "--train_data",
      type=str,
      default="",
      help="Path to the training data."
  )
  parser.add_argument(
      "--test_data",
      type=str,
      default="",
      help="Path to the test data."
  )
  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)

  mysql_cn.close()
