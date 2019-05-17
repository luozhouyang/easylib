import logging
import os

import tensorflow as tf


class DatasetRunner:
    """Tensorflow 2.x models runner, using tf.data API."""

    def __init__(self, model: tf.keras.Model, model_dir, model_name='model', logger_name=None):
        """Init.

        Args:
            model: Model, instance of `tf.keras.Model`
            model_dir: The directory to save model files
            model_name: The name of the model, used as checkpoint file names.
            logger_name: The name of the logger.
        """
        self.model = model
        self.model_dir = model_dir
        self.model_name = model_name
        self.logger = logging.getLogger(logger_name)

    def train(self, dataset, val_dataset=None, ckpt=None):
        """Train the model.

        Args:
            dataset: Dataset for training, instance of `tf.data.Dataset`
            val_dataset: Dataset for validation, instance of `tf.data.Dataset`
            ckpt: The checkpoint dir or path
        """
        raise NotImplementedError()

    def eval(self, dataset, ckpt=None):
        """Evaluate the model.

        Args:
            dataset: Dataset for evaluation, instance of `tf.data.Dataset`
            ckpt: The checkpoint dir or path
        """
        raise NotImplementedError()

    def predict(self, dataset, ckpt=None):
        """Predict the model.

        Args:
            dataset: Dataset for prediction
            ckpt: The checkpoint dir or path
        """
        raise NotImplementedError()

    def export(self, path, ckpt=None):
        """Export the saved model.

        Args:
            path: The directory to save the exported model
            ckpt: The checkpoint dir or path
        """
        self._load_weights(ckpt)
        tf.keras.experimental.export_saved_model(self.model, path)

    def _load_weights(self, ckpt=None):
        if not ckpt:
            ckpt = self.model_dir
        if os.path.isdir(ckpt):
            # empty dir
            if len(os.listdir(ckpt)) == 0:
                return
            if all('.ckpt' not in f for f in os.listdir(ckpt)):
                return
            ckpt = tf.train.latest_checkpoint(ckpt)
        self.model.load_weights(ckpt)
        self.logger.info('Load weights from ckpt: %s' % ckpt)


class KerasModelDatasetRunner(DatasetRunner):
    """Train, eval, predict and export tf.keras.Model, using `tf.data` API."""

    def __init__(self,
                 model,
                 model_dir,
                 model_name='model',
                 train_callbacks=None,
                 eval_callbacks=None,
                 predict_callbacks=None,
                 configs=None,
                 logger_name=None):
        """Init.

        Args:
            model: Model, instance of `tf.keras.Model`
            model_dir: The directory to save model files
            model_name: The name of the model, used as checkpoint file names.
            train_callbacks: A list of extra callbacks for training
            eval_callbacks: A list of extra callbacks for evaluation
            predict_callbacks: A list of extra callbacks for prediction
            configs: A dict of configuration, see `default_configs()`
            logger_name: The name of the logger.
        """
        super(KerasModelDatasetRunner, self).__init__(model, model_dir, model_name, logger_name)
        default_configs = self.default_config()
        if configs:
            default_configs.update(configs)
        self.configs = default_configs

        self.train_callbacks = None
        self.eval_callbacks = None
        self.predict_callbacks = None
        self._init_callbacks(train_callbacks, eval_callbacks, predict_callbacks)

    def train(self, dataset, val_dataset=None, ckpt=None):
        """Train the model.

        Args:
            dataset: Dataset for training, instance of `tf.data.Dataset`
            val_dataset: Dataset for validation, instance of `tf.data.Dataset`
            ckpt: The checkpoint dir or path

        Returns:
            A `History` object
         """
        self._load_weights(ckpt)
        history = self.model.fit(
            dataset,
            validation_data=val_dataset,
            callbacks=self.train_callbacks,
            epochs=self.configs['epochs'])
        return history

    def eval(self, dataset, ckpt=None):
        """Evaluate the model.

        Args:
            dataset: Dataset for evaluation, instance of `tf.data.Dataset`
            ckpt: The checkpoint dir or path

        Returns:
            The result of `tf.keras.Model.evaluate(...)`
        """
        self._load_weights(ckpt)
        return self.model.evaluate(dataset, callbacks=self.eval_callbacks)

    def predict(self, dataset, ckpt=None):
        """Predict the model.

        Args:
            dataset: Dataset for prediction
            ckpt: The checkpoint dir or path

        Returns:
            Numpy array of predictions
        """
        self._load_weights(ckpt)
        return self.model.predict(dataset, callbacks=self.predict_callbacks)

    def _init_callbacks(self, train_callbacks=None, eval_callbacks=None, predict_callbacks=None):
        """Extend the callbacks by the default callbacks"""
        default_train_callbacks = [
            tf.keras.callbacks.ModelCheckpoint(
                os.path.join(self.model_dir, '%s-{epoch:04d}.ckpt' % self.model_name),
                save_weights_only=self.configs['ckpt_only_weights'],
                period=self.configs['ckpt_period']),
            tf.keras.callbacks.TensorBoard(log_dir=os.path.join(self.model_dir, 'tensorboard')),
            tf.keras.callbacks.EarlyStopping(patience=self.configs['early_stopping_patience'])
        ]
        if train_callbacks:
            default_train_callbacks.extend(train_callbacks)
        self.train_callbacks = default_train_callbacks

        default_eval_callbacks = []
        if eval_callbacks:
            default_eval_callbacks.extend(eval_callbacks)
        self.eval_callbacks = default_eval_callbacks

        default_predict_callbacks = []
        if predict_callbacks:
            default_predict_callbacks.extend(predict_callbacks)
        self.predict_callbacks = default_predict_callbacks

    def default_config(self):
        """Default configurations. Can be override by `configs` in constructor, or set `self.configs` directly."""
        c = {
            'ckpt_only_weights': True,
            'ckpt_period': 5,
            'early_stopping_patience': 10,
            'epochs': 20,
        }
        return c
