import unittest
import tensorflow as tf

from easylib.dl import KerasModelDatasetRunner

(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()

train_labels = train_labels[:1000]
test_labels = test_labels[:1000]

train_images = train_images[:1000].reshape(-1, 28 * 28) / 255.0
test_images = test_images[:1000].reshape(-1, 28 * 28) / 255.0

print(type(train_images))
print(train_images.shape)


class DatasetRunnerTest(unittest.TestCase):

    def createModel(self):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(512, activation='relu', input_shape=(784,)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(10, activation='softmax')
        ])

        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])

        return model

    def testKerasModelDatasetRunner(self):
        model = self.createModel()
        r = KerasModelDatasetRunner(model, model_dir='/tmp/mnist', model_name='mnist', logger_name='easylib')

        image = tf.data.Dataset.from_tensor_slices(train_images)
        label = tf.data.Dataset.from_tensor_slices(train_labels)
        dataset = tf.data.Dataset.zip((image, label)).shuffle(10000).batch(32)
        r.configs['epochs'] = 30
        r.train(dataset, ckpt='/tmp/mnist/mnist-0015.ckpt')


if __name__ == '__main__':
    unittest.main()
