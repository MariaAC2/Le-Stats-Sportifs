"""
Task Runner Module

This module contains two classes.
'ThreadPool' class creates a thread pool of task runners, along with 
its functionalties. It is responsible with the flow of the tasks.

'TaskRunner' class is the one that runs the tasks at hand. It processes
the task from the task queue and then puts the result into a file.
"""

from queue import Queue
import os
import multiprocessing
from threading import Thread, Event
from app.extra import post_result

class ThreadPool:
    """Class that creates the thread pool used for the application"""
    def __init__(self):
        """Method that initiates the variables, as well as creates the list
        of task runners"""
        self.num_threads = self._get_num_threads()
        self.task_queue = Queue()
        self.shutdown_event = Event()
        self.task_runners = []
        self.jobs = {}
        self._create_task_runners()

    # Check if the environment variable TP_NUM_OF_THREADS is defined
    # If the env var is defined, that is the number of threads to be used by the thread pool
    # Otherwise, use what the hardware concurrency allows
    def _get_num_threads(self):
        """Method that gets the number of threads needed"""
        env_num_threads = os.getenv("TP_NUM_OF_THREADS")

        if env_num_threads:
            return min(int(env_num_threads), multiprocessing.cpu_count())
        return multiprocessing.cpu_count()

    # Creates list of task_runners which share the same
    # queue, jobs dictionary and shutdown event
    def _create_task_runners(self):
        """Method that creates the task runners list"""
        for _ in range(self.num_threads):
            task_runner = TaskRunner(self.task_queue, self.shutdown_event, self.jobs)
            self.task_runners.append(task_runner)

    # Start all threads simultaniously
    def start(self):
        """Method that starts all task runners"""
        for task_runner in self.task_runners:
            task_runner.start()

    # Add job into the queue
    # If the shutdown event is not set, we can add a task
    def submit(self, task):
        """Method that submits the task into the thread pool"""
        self.task_queue.put(task)

    # Shutdown the whole application
    def shutdown(self):
        """Method that shuts down the application"""
        self.shutdown_event.set() # set the shutdown event

        # Change all instances of task_runner from the
        # list of task runners into None
        for _ in range(self.num_threads):
            self.task_queue.put(None)

        # Join all threads
        for task_runner in self.task_runners:
            task_runner.join()

class TaskRunner(Thread):
    """Class that creates the task runner that handles the execution of tasks"""
    def __init__(self, task_queue, shutdown_event, jobs):
        """Method that initiates the task runner"""
        super().__init__()
        self.task_queue = task_queue
        self.shutdown_event = shutdown_event
        self.jobs = jobs

    def run(self):
        """Method that runs the tasks from the queue"""
        while not self.shutdown_event.is_set():
            # Wait for notification or until task queue is not empty
            task = self.task_queue.get()

            # Check if it's time to exit
            if task is None:
                break
            try:
                # Get the result from the execute function of
                # the task from the queue
                results = task.execute()

                # Mark job as done
                task.status = "done"

                # Put the job with the updated information into
                # the jobs dictionary
                self.jobs[task.job_id] = task

                # Post the result into its respective file
                post_result(task.job_id, results)
            except Exception as e:
                print(f"Error executing task: {e}")
