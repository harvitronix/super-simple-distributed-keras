"""
A class to store the data needed to communicate between the controller
and the workers.
"""
from pymongo import MongoClient

class Database():
    """Data storage operations. Uses Mongo."""

    def __init__(self, collection, mongo_host='localhost'):
        """Initialize.

        Args:
            collection (string): The name of the Mongo collection to use.
            mongo_host (string): The host where the controller DB lives.
        """
        client = MongoClient(mongo_host)
        self.collection = client[collection]

    def insert_job(self, dataset, network):
        """Add the job details to the DB.

        Args:
            dataset (string): The name of the dataset
            network (string): The JSON network definition

        Returns:
            job_id (string): The Mongo ObjectId of the job
        """
        assert isinstance(dataset, str)
        assert isinstance(network, str)
        assert 'config' in network

        job_id = self.collection.jobs.insert_one({
            'dataset': dataset,
            'network': network,
            'processing': 0,
            'processed': 0,
            'metrics': {},
        })

        return job_id

    def get_job(self, job_id):
        """Get a job from the collection.

        Args:
            job_id (string): The Mongo ObjectId of the job
        """
        job = self.collection.jobs.find_one({'_id': job_id})

        return job

    def find_job(self):
        """Get a job that isn't being processed.

        Once we find it, also set it to processing so another
        worker doesn't grab it.
        """
        job = self.collection.jobs.find_one({
            'processing': 0
        })

        if job is not None:
            self.collection.jobs.update_one({
                '_id': job['_id']
            }, {
                '$set': {
                    'processing': 1
                }
            }, upsert=False)

        return job

    def score_job(self, job_id, metrics):
        """Update a job with its scoring metrics.

        Args:
            job_id (string): The Mongo ObjectId of the job
            metrics (dict): The results of the work. For example:
                {'loss': 1.04834, 'accuracy': 0.88739}
        """
        assert isinstance(metrics, dict)

        self.collection.jobs.update_one({
            '_id': job_id
        }, {
            '$set': {
                'processed': 1,
                'metrics': metrics
            }
        }, upsert=False)
