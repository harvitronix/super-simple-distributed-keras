"""
The worker looks for jobs in the DB, trains and scores a network and
updates the DB entry with the results.
"""
import time
from keras.models import model_from_json
from keras.callbacks import EarlyStopping
from database import Database
from datasets import get_dataset

# Helper: Early stopping.
early_stopper = EarlyStopping(patience=1)

class Worker():
    """Class for performing worker duties."""

    def __init__(self, collection, db_host='localhost'):
        """Initialize.

        Args:
            collection (string): The name of the Mongo collection to use
            db_host (string): The host where the controller DB lives
        """
        self.db = Database(collection, db_host)

    def check_for_jobs(self):
        """Query the DB for jobs that need to be done. Only get one,
        since other workers will grab other jobs."""
        return self.db.find_job()

    @staticmethod
    def evaluate_network(network, dataset):
        """Spawn a training sessions.

        Args:
            network (dict): The JSON definition of the network
            dataset (string): The name of the dataset to use
        """
        # Get the dataset.
        _, batch_size, _, x_train, x_test, y_train, y_test = get_dataset(dataset)

        model = model_from_json(network)
        model.compile(loss='categorical_crossentropy', optimizer='adam',
                      metrics=['accuracy'])

        model.fit(x_train, y_train,
                  batch_size=batch_size,
                  epochs=10000,  # essentially infinite, uses early stopping
                  verbose=1,
                  validation_data=(x_test, y_test),
                  callbacks=[early_stopper])

        score = model.evaluate(x_test, y_test, verbose=0)

        metrics = {'loss': score[0], 'accuracy': score[1]}

        return metrics

    def update_results(self, job_id, metrics):
        """After training, update the database with the results.

        Args:
            job_id (string): The Mongo Object Id of the job
            score (dict): The resulting score
        """
        self.db.score_job(job_id, metrics)

def main():
    """Do the loop."""
    worker = Worker('blog-test')

    while True:
        print("Looking for job.")
        job = worker.check_for_jobs()

        if job is not None:
            print("Found job %s." % (job['_id']))
            metrics = worker.evaluate_network(job['network'], job['dataset'])
            worker.update_results(job['_id'], metrics)
        else:
            print("Waiting for job.")
            time.sleep(30)  # wait 30 seconds to find another one.

if __name__ == '__main__':
    main()
