# Super Simple Distributed Hyperparameter Tuning with Keras and Mongo

This is a really simple (read: basic) way to do distributed hyperparameter tuning with Keras, Mongo, and any assortment of servers.

It works by doing the following:

- Some controller creates JSON representations of Keras models
- It adds thsoe models to a Mongo DB, along with the name of the dataset to train on
- One or more workers watches the DB for new jobs
- When a new network shows up in the DB, the network trains the network on the dataset then scores it
- It updates the job in the DB with the score
- Then it looks for another job

## To run

You'll need Mongo running. You can test it out locally or you can use remote servers. If you use remote, you'll need to specify the host for the Mongo server. I use this on a cluster of AWS servers that share a security group, so I only need to specify the host. If you're using a Mongo server that requires username/password/etc., you'll need to update the code. Pull requests welcome!

Once you have Mongo running, start the controller with:

`python3 controller.py`

This will start putting random-ish networks into the DB.

Then run a worker with:

`python3 worker.py`

This will start a worker who will look for jobs and process them. You can start as many workers as you want, but note that you likely only want to run one worker per instance or GPU.
