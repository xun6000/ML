# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
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

"""A very simple MNIST classifier.

See extensive documentation at
http://tensorflow.org/tutorials/mnist/beginners/index.md
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import gzip
import csv
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import argparse
import sys
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
import pickle
import tensorflow as tf
#mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
FLAGS = None
cover=0; #hide the left and right, 1 or 0
flip=0; #change black to whtie , 1 and 0
repeat=1; #repeat=2 is not good, 1 or 2
extra=1;
ep=5
hidden=1024
print ("loading bbb")
#f = open('newgray.txt','rb')
f = open('newgray.txt','rb')
bbb = pickle.load(f)#,encoding="latin1"
f.close()

# 0 to1
print ("loading lable")

f = open('newlabley2.txt','rb')
labley = pickle.load(f)
f.close()  # 0 to1
print(labley.shape)
if extra==1:
    f = open('extratring1.txt', 'rb')
    exdata = pickle.load(f)
    f.close()
    bbb=np.vstack((bbb, exdata))
    f = open('extralable50000.txt', 'rb')
    exdatala = pickle.load(f)
    f.close()
    print(exdatala.shape)
    labley = np.vstack((labley, exdatala))





if repeat==2:
    bbb = np.vstack((bbb, -bbb))
    labley = np.vstack((labley, labley))
#print("maxis",labley[0:10])
f = open('test0309.txt','rb')
testdatax = pickle.load(f)
f.close()  # 0 to1
print(np.min(testdatax),np.max(testdatax))
compare = np.loadtxt('compare.txt')
print( testdatax.shape)




if flip==1:
    for i in range(len(bbb)):
        a = np.average(bbb[i])
        ll = bbb[i] >= a
        if sum(ll) > 512:
            bbb[i] = 1 - bbb[i]
    for i in range(len(testdatax)):
        a = np.average(testdatax[i])
        ll = testdatax[i] >= a
        if sum(ll) > 512:
            testdatax[i] = 1 - testdatax[i]


if cover==1:
    bbb = bbb.reshape(-1, 32, 32)
    for i in range(len(bbb)):
        summ=np.sum(bbb[i],axis=0)
    #print (summ.shape)
        avg=np.average(bbb[i])
        if np.sum(summ[6:26])<0.8*np.sum(summ):
            bbb[i,:,0:6]=avg
            bbb[i,:,26:]=avg
    bbb = bbb.reshape(-1, 1024)
for i in range(len(bbb)):
    #print (np.average(bbb[i]))
    #print (np.max(bbb[i]))
    bbb[i]=bbb[i]-np.average(bbb[i])
if cover==1 :
    testdatax = testdatax.reshape(-1, 32, 32)
    for i in range(len(testdatax)):
        summ=np.sum(testdatax[i],axis=0)
        avg=np.average(testdatax[i])
        if np.sum(summ[6:26])<0.8*np.sum(summ):
            testdatax[i,:,0:6]=avg
            testdatax[i,:,26:]=avg

    testdatax=testdatax.reshape(-1,1024)
for i in range(len(testdatax)):
    #print (np.average(bbb[i]))
    #print (np.max(bbb[i]))
    testdatax[i]=testdatax[i]-np.average(testdatax[i])

print(np.max(bbb))
x = tf.placeholder(tf.float32, [None, 32*32])
W = tf.Variable(tf.zeros([32*32, 10]))
b = tf.Variable(tf.zeros([10]))
  #y = tf.matmul(x, W) + b
y = tf.nn.softmax(tf.matmul(x, W) + b)
  # Define loss and optimizer
y_ = tf.placeholder(tf.float32, [None, 10])

  # The raw formulation of cross-entropy,
  #
  #   tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(tf.nn.softmax(y)),
  #                                 reduction_indices=[1]))
  #
  # can be numerically unstable.
  #
  # So here we use tf.nn.softmax_cross_entropy_with_logits on the raw
  # outputs of 'y', and then average across the batch.
# cross_entropy = tf.reduce_mean(
#       tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
# train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
#
sess = tf.InteractiveSession()
tf.global_variables_initializer().run()
#
# for i in range(500):
#   batch_xs, batch_ys =bbb[100*i:100*i+100],labley[100*i:100*i+100] #mnist.train.next_batch(100)
#   sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
#
#   # Test trained model
# correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
# accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
# print(sess.run(accuracy, feed_dict={x: bbb[60000:61000],#mnist.test.images,
#                                       y_: labley[60000:61000]}))


def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')

W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])
x_image = tf.reshape(x, [-1,32,32,1])

h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)



W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)


W_conv3 = weight_variable([5, 5, 64, 64])
b_conv3 = bias_variable([64])
h_conv3 = tf.nn.relu(conv2d(h_pool2, W_conv3) + b_conv3)
h_pool3 = max_pool_2x2(h_conv3)

W_fc1 = weight_variable([4 * 4 * 64, hidden])
b_fc1 = bias_variable([hidden])
h_pool2_flat = tf.reshape(h_pool3, [-1, 4*4*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)


# W_fc3 = weight_variable([1024, 300])
# b_fc3 = bias_variable([10])
# y_conv = tf.matmul(h_fc1_drop, W_fc3) + b_fc3


W_fc2 = weight_variable([hidden, 10])
b_fc2 = bias_variable([10])
y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2




cross_entropy = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
train_step = tf.train.AdamOptimizer(1e-3).minimize(cross_entropy)#1e-4 changed to 1e-3
y_p = tf.argmax(y_conv,1)
correct_prediction = tf.equal(y_p, tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
sess.run(tf.global_variables_initializer())
startn=140000
dn=3000
valiresult=[]
trainsult=[]
for j in range(int(ep)):
  print(j)
  for i in range((700+500*extra)*repeat*(flip+1)):
  #batch = mnist.train.next_batch(50)

    if i%100 == 0:
      train_accuracy = accuracy.eval(feed_dict={
          x:bbb[100 * i:100 * i + 100], y_: labley[100 * i:100 * i + 100], keep_prob: 1})
      print("step %d, training accuracy %g"%(i, train_accuracy))
      trainsult.append(train_accuracy)

    train_step.run(feed_dict={x: bbb[100 * i:100 * i + 100], y_: labley[100 * i:100 * i + 100], keep_prob: 0.5})#0.5 changed to 1
    # print(np.array(tf.argmax(y_,1)))
    #print(len(tf.argmax(y_,1)))
  #a=accuracy.eval(feed_dict={
     #x: bbb[startn:startn+dn], y_: labley[startn:startn+dn], keep_prob: 1.0});
  #valiresult.append(a)
    #print("test accuracy %g"%accuracy.eval(feed_dict={
   #x: testdatax[0:100], y_: compare[0:100], keep_prob: 1.0}))


result=[]

#
#plt.plot(trainsult)
#plt.plot(valiresult)
#plt.show()
for i in range(int(26040/40)):
    pred = sess.run(y_p, feed_dict={x: testdatax[40*i:40*i+40], keep_prob: 1})
    #pred = np.asarray(pred)
    result.append(pred)

result=np.array(result)
result=result.reshape(1,26040)
result[result==0]=10
print(result.shape)
happy=0;
plotnumber=[0 for i in range(20)]
ll=0;
for i in range(100):
    if result[0,i]==compare[i]:
        happy=happy+1;
    else:

        plotnumber[ll]=i
        #print(result[0,i])
        ll=ll+1
print("happ", happy)
for k in range(2):
    for j in range(10):
        curr = testdatax[plotnumber[10*k+j]].reshape(32, 32)
        curr = curr * 256;
        plt.subplot(2, 10, 10 * (k) + j + 1)
        plt.imshow(curr,cmap=cm.gray)

        plt.title("{0}".format(result[0,plotnumber[10*k+j]]) )

plt.show();

twe = np.zeros((2, 26032))
twe[0] = [i for i in range(0, 26032)]
twe[1] = result[0,0:26032]
twe=twe.T.astype(int)

csvfile = open('predit0301.csv', 'w')
writer = csv.writer(csvfile)
writer.writerow(['ImageId','Label'])
writer.writerows(twe)
csvfile.close()

