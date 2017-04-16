"""
This is an example of a controller. It places networks into the
DB for the worker(s) to pull from.
"""
import random
import time
from database import Database

def gen_network(inputs, outputs):
    """Generate a network as an example.

    Args:
        inputs (int): The shape of the input vector
        outputs (int): Number of output classes (this is a classificatoin eg)
    """
    units = random.choice([8, 16, 32, 64])

    # Note that network has to be a JSON string, not a dictionary.
    network = '{"backend": "tensorflow", "config": [{"config": {"kernel_regularizer": null, "activation": "relu", "units": ' + str(units) + ', "bias_regularizer": null, "use_bias": true, "name": "dense_1", "trainable": true, "kernel_constraint": null, "bias_initializer": {"config": {}, "class_name": "Zeros"}, "batch_input_shape": [null, ' + str(inputs) + '], "dtype": "float32", "bias_constraint": null, "kernel_initializer": {"config": {"distribution": "uniform", "seed": null, "mode": "fan_avg", "scale": 1.0}, "class_name": "VarianceScaling"}, "activity_regularizer": null}, "class_name": "Dense"}, {"config": {"kernel_regularizer": null, "activation": "relu", "units": ' + str(units) + ', "bias_regularizer": null, "use_bias": true, "name": "dense_2", "kernel_initializer": {"config": {"distribution": "uniform", "seed": null, "mode": "fan_avg", "scale": 1.0}, "class_name": "VarianceScaling"}, "trainable": true, "kernel_constraint": null, "bias_initializer": {"config": {}, "class_name": "Zeros"}, "bias_constraint": null, "activity_regularizer": null}, "class_name": "Dense"}, {"config": {"trainable": true, "rate": 0.2, "name": "dropout_1"}, "class_name": "Dropout"}, {"config": {"kernel_regularizer": null, "activation": "softmax", "units": ' + str(outputs) + ', "bias_regularizer": null, "use_bias": true, "name": "dense_3", "kernel_initializer": {"config": {"distribution": "uniform", "seed": null, "mode": "fan_avg", "scale": 1.0}, "class_name": "VarianceScaling"}, "trainable": true, "kernel_constraint": null, "bias_initializer": {"config": {}, "class_name": "Zeros"}, "bias_constraint": null, "activity_regularizer": null}, "class_name": "Dense"}], "keras_version": "2.0.2", "class_name": "Sequential"}'
    return network

def add_job(dataset, network, db):
    """Add the network and dataset into the DB.

    Args:
        network (dict): The JSON network definition
        dataset (string): The name of the dataset, example:
            mnist, cifar10
        db (Obj): The database class
    """
    db.insert_job(dataset, network)

def main():
    """Toy example of adding jobs to be processed."""
    db = Database('blog-test')

    while True:
        print("Creating job.")
        network = gen_network(784, 10)  # mnist settings
        add_job('mnist', network, db)

        sleep_time = random.randint(60, 120)
        print("Waiting %d seconds." % (sleep_time))
        time.sleep(sleep_time)

if __name__ == '__main__':
    main()
