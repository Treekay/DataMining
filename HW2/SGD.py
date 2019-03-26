# Stochastic Gradient Decesent

import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt
from sklearn import preprocessing

DATA_PATH = r'./dataForTraining.txt'
TEST_PATH = r'./dataForTesting.txt'

ITERATION_TIMES = 1500000
DRAW_STEP = 100

train_error = []
test_error = []

def readFile(datapath):
    return np.genfromtxt(datapath, delimiter=' ')


# z = ax + by + c
def computeError(a, b, c, points):
    totalError = 0
    for i in range(0, len(points)):
        x = points[i, 0]
        y = points[i, 1]
        z = points[i, 2]
        totalError += (z - (a * x + b * y + c)) ** 2
    return totalError / float(len(points))


def randGradient(a_current, b_current, c_current, points, learningRate):
    # 随机梯度下降
    i = np.random.randint(len(points)/3)
    x = points[i, 0]
    y = points[i, 1]
    z = points[i, 2]
    a_gradient = -1 * x * (z - (a_current * x + b_current * y + c_current))
    b_gradient = -1 * y * (z - (a_current * x + b_current * y + c_current))
    c_gradient = -1 * (z - (a_current * x + b_current * y + c_current))
    new_a = a_current - (learningRate * a_gradient)
    new_b = b_current - (learningRate * b_gradient)
    new_c = c_current - (learningRate * c_gradient)
    return [new_a, new_b, new_c]


def gradientDescent(points, starting_a, starting_b, starting_c, learning_rate, iteration_times, testData):
    a = starting_a
    b = starting_b
    c = starting_c
    for i in range(iteration_times):
        a, b, c = randGradient(a, b, c, np.array(points), learning_rate)
        if i != 0 and i % DRAW_STEP == 0:
            current_train_error = computeError(a, b, c, points)
            current_test_error = computeError(a, b, c, testData)
            train_error.append(current_train_error)
            test_error.append(current_test_error)
            # print("After {0} iterations a = {1}, b = {2}, c = {3}, train error = {4}, testData loss = {5}".format(
            #     i, a, b, c, current_train_error, current_test_error))
    return [a, b, c]


if __name__ == "__main__":
    # 测试数据
    testData = readFile(TEST_PATH)
    # 归一化
    testData = preprocessing.scale(testData)

    # 读取文件
    points = readFile(DATA_PATH)
    # 归一化
    points = preprocessing.scale(points)
    # 参数设置
    iteration_times = ITERATION_TIMES
    learning_rate = 0.00015
    initial_a = 0.0  # initial a`
    initial_b = 0.0  # initial b
    initial_c = 0.0  # initial c

    print("Running...")
    [a, b, c] = gradientDescent(
        points, initial_a, initial_b, initial_c, learning_rate, iteration_times, testData)
    print("After {0} iterations a = {1}, b = {2}, c = {3}, train error = {4}, testData loss = {5}".format(
        iteration_times, a, b, c, computeError(a, b, c, points), computeError(a, b, c, testData)))
    train_error.append(computeError(a, b, c, points))
    test_error.append(computeError(a, b, c, testData))

    # 绘制图表
    # 训练错误率随迭代次数的变化
    plt.figure()
    plt.subplot(121)
    plt.plot(range(1, iteration_times + 1, DRAW_STEP),
             train_error, c='blue', label='train loss')
    plt.legend()
    plt.ylim(0, 1.00)
    plt.ylabel('train loss')
    plt.xlabel('iteration times')
    plt.ylim(0, np.max(train_error) * 1.2)
    # 测试错误率随迭代次数的变化
    plt.subplot(122)
    plt.plot(range(1, iteration_times + 1, DRAW_STEP),
             test_error, c='red', label='test loss')
    plt.legend()
    plt.ylim(0, 1.00)
    plt.ylabel('test loss')
    plt.xlabel('iteration times')
    plt.ylim(0, np.max(test_error) * 1.2)

    plt.show()
    