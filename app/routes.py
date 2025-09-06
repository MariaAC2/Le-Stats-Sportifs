"""
Route Module

This module contains different routes in order to access HTTP requests.
If we have a GET request, we can get data about the jobs and print it.

If we have a POST request, we can get a question, create a job and return
the data for it.
"""

from flask import request, jsonify
from app import webserver
from app.extra import Job, get_result
from app.webserver_logger import logger, error_logger

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    """Example method for http POST request"""
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        logger.info("Got data in post %s", data)

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        logger.info(response)
        # Sending back a JSON response
        return jsonify(response)

    # Method Not Allowed
    error_logger.error({"error": "Method not allowed"})
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Method that returns a list of job ids and the status of each job"""
    # Check if I sent a GET request
    if request.method == 'GET':
        logger.info("Print all jobs")

        # Check if dict is not empty
        if webserver.tasks_runner.jobs:
            # Format data according to the example provided
            jobs_list = []

            for job_id, job in webserver.tasks_runner.jobs.items():
                jobs_list.append({job_id: job.status})

            # Return all jobs
            response = {"status": "done", "data": jobs_list}
            logger.info(response)

        # Sent json with error
        else:
            response = {"status": "error", "reason": "Jobs not found"}
            error_logger.error(response)

        return jsonify(response)

    # Method Not Allowed
    error_logger.error({"error": "Method not allowed"})
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/num_jobs', methods=['GET'])
def get_running_jobs():
    """Method that returns the number of jobs in the thread pool"""
    if request.method == 'GET':
        logger.info("Print running jobs")

        # Get size of task queue from thread pool
        running_jobs = webserver.tasks_runner.task_queue.qsize()

        # Return running jobs
        response = {"status": "done", "num_jobs": str(running_jobs)}

        logger.info(response)
        return jsonify(response)

    # Method Not Allowed
    error_logger.error({"error": "Method not allowed"})
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """Method that returns the data with a certain job id"""
    # Check if I sent a GET request
    if request.method == 'GET':
        # Assuming the request contains JSON data
        logger.info("JobID is %s", job_id)

        # Check if job_id is valid
        if job_id not in webserver.tasks_runner.jobs:
            response = {"status": "error", "reason": "Invalid job_id"}
            error_logger.error(response)

        # Get result from file with the given job_id
        # from results
        result = get_result(job_id)

        # If I didn't create a result file, but the job id
        # exists, it means that the task is still running
        if not result:
            response = {"status": "running"}
            logger.info(response)

        # Return result
        else:
            response = {"status": "done", "data": result}
            logger.info(response)

        return jsonify(response)

    # Method Not Allowed
    error_logger.error({"error": "Method not allowed"})
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def get_graceful_shutdown():
    """Method that shuts down application"""
    # Check if I sent GET request
    if request.method == 'GET':
        logger.info("The application will shut down")
        # Shut down app
        webserver.tasks_runner.shutdown()

        # Return done status
        response = {"status": "done"}

        logger.info(response)
        return jsonify(response)

    # Method Not Allowed
    error_logger.error({"error": "Method not allowed"})
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """Method that calculates the states mean"""
    # Check if I sent a POST request
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        logger.info("Got request %s", data)

        # Check if server is not shut down
        if not webserver.tasks_runner.shutdown_event.is_set():
            # Create job_id for the job
            job_id = "job_id_" + str(webserver.job_counter)

            # Create job with the request type, job_id, data from the json file
            # and the data ingestor in order to process data
            job = Job("states_mean", job_id, data, webserver.data_ingestor)

            # Add the job into the jobs dict where I hold all jobs created
            # and submit job into thread pool
            webserver.tasks_runner.jobs[job_id] = job
            webserver.tasks_runner.submit(job)

            # Increment the job_counter
            webserver.job_counter += 1

            # Return response with job_id
            response = {"status": "done", "job_id": job_id}
            logger.info(response)
        else:
            # Return error because the server is not active
            # because it was shut down
            response = {"status": "error", "reason": "Server not active"}
            error_logger.error(response)

        return jsonify(response)

    # Method Not Allowed
    error_logger.error({"error": "Method not allowed"})
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """Method that calculates a given state's mean"""
    # Check if I sent a POST request
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        logger.info("Got request %s", data)

        # Check if server is not shut down
        if not webserver.tasks_runner.shutdown_event.is_set():
            # Create job_id for the job
            job_id = "job_id_" + str(webserver.job_counter)

            # Create job with the request type, job_id, data from the json file
            # and the data ingestor in order to process data
            job = Job("state_mean", job_id, data, webserver.data_ingestor)

            # Add the job into the jobs dict where I hold all jobs created
            # and submit job into thread pool
            webserver.tasks_runner.jobs[job_id] = job
            webserver.tasks_runner.submit(job)

            # Increment the job_counter
            webserver.job_counter += 1

            # Return response with job_id
            response = {"status": "done", "job_id": job_id}
            logger.info(response)
        else:
            # Return error because the server is not active
            # because it was shut down
            response = {"status": "error", "reason": "Server not active"}
            error_logger.error(response)

        return jsonify(response)

    # Method Not Allowed
    error_logger.error({"error": "Method not allowed"})
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """Method that calculates the best 5 states"""
    # Check if I sent a POST request
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        logger.info("Got request %s", data)

        # Check if server is not shut down
        if not webserver.tasks_runner.shutdown_event.is_set():
            # Create job_id for the job
            job_id = "job_id_" + str(webserver.job_counter)

            # Create job with the request type, job_id, data from the json file
            # and the data ingestor in order to process data
            job = Job("best5", job_id, data, webserver.data_ingestor)

            # Add the job into the jobs dict where I hold all jobs created
            # and submit job into thread pool
            webserver.tasks_runner.jobs[job_id] = job
            webserver.tasks_runner.submit(job)

            # Increment the job_counter
            webserver.job_counter += 1

            # Return response with job_id
            response = {"status": "done", "job_id": job_id}
            logger.info(response)
        else:
            # Return error because the server is not active
            # because it was shut down
            response = {"status": "error", "reason": "Server not active"}
            error_logger.error(response)

        return jsonify(response)

    # Method Not Allowed
    error_logger.error({"error": "Method not allowed"})
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """Method that calculates the worst 5 states"""
    # Check if I sent a POST request
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        logger.info("Got request %s", data)

        # Check if server is not shut down
        if not webserver.tasks_runner.shutdown_event.is_set():
            # Create job_id for the job
            job_id = "job_id_" + str(webserver.job_counter)

            # Create job with the request type, job_id, data from the json file
            # and the data ingestor in order to process data
            job = Job("worst5", job_id, data, webserver.data_ingestor)

            # Add the job into the jobs dict where I hold all jobs created
            # and submit job into thread pool
            webserver.tasks_runner.jobs[job_id] = job
            webserver.tasks_runner.submit(job)

            # Increment the job_counter
            webserver.job_counter += 1

            # Return response with job_id
            response = {"status": "done", "job_id": job_id}
            logger.info(response)
        else:
            # Return error because the server is not active
            # because it was shut down
            response = {"status": "error", "reason": "Server not active"}
            error_logger.error(response)

        return jsonify(response)

    # Method Not Allowed
    error_logger.error({"error": "Method not allowed"})
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """Method that calculates the global mean"""
    # Check if I sent a POST request
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        logger.info("Got request %s", data)

        # Check if server is not shut down
        if not webserver.tasks_runner.shutdown_event.is_set():
            # Create job_id for the job
            job_id = "job_id_" + str(webserver.job_counter)

            # Create job with the request type, job_id, data from the json file
            # and the data ingestor in order to process data
            job = Job("global_mean", job_id, data, webserver.data_ingestor)

            # Add the job into the jobs dict where I hold all jobs created
            # and submit job into thread pool
            webserver.tasks_runner.jobs[job_id] = job
            webserver.tasks_runner.submit(job)

            # Increment the job_counter
            webserver.job_counter += 1

            # Return response with job_id
            response = {"status": "done", "job_id": job_id}
            logger.info(response)
        else:
            # Return error because the server is not active
            # because it was shut down
            response = {"status": "error", "reason": "Server not active"}
            error_logger.error(response)

        return jsonify(response)

    # Method Not Allowed
    error_logger.error({"error": "Method not allowed"})
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """Method that calculates the diff between the global mean and the states mean"""
    # Check if I sent a POST request
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        logger.info("Got request %s", data)

        # Check if server is not shut down
        if not webserver.tasks_runner.shutdown_event.is_set():
            # Create job_id for the job
            job_id = "job_id_" + str(webserver.job_counter)

            # Create job with the request type, job_id, data from the json file
            # and the data ingestor in order to process data
            job = Job("diff_from_mean", job_id, data, webserver.data_ingestor)

            # Add the job into the jobs dict where I hold all jobs created
            # and submit job into thread pool
            webserver.tasks_runner.jobs[job_id] = job
            webserver.tasks_runner.submit(job)

            # Increment the job_counter
            webserver.job_counter += 1

            # Return response with job_id
            response = {"status": "done", "job_id": job_id}
            logger.info(response)
        else:
            # Return error because the server is not active
            # because it was shut down
            response = {"status": "error", "reason": "Server not active"}
            error_logger.error(response)

        return jsonify(response)

    # Method Not Allowed
    error_logger.error({"error": "Method not allowed"})
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """Method that calculates the diff between the global mean and a given state's mean"""
    # Check if I sent a POST request
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        logger.info("Got request %s", data)

        # Check if server is not shut down
        if not webserver.tasks_runner.shutdown_event.is_set():
            # Create job_id for the job
            job_id = "job_id_" + str(webserver.job_counter)

            # Create job with the request type, job_id, data from the json file
            # and the data ingestor in order to process data
            job = Job("state_diff_from_mean", job_id, data, webserver.data_ingestor)

            # Add the job into the jobs dict where I hold all jobs created
            # and submit job into thread pool
            webserver.tasks_runner.jobs[job_id] = job
            webserver.tasks_runner.submit(job)

            # Increment the job_counter
            webserver.job_counter += 1

            # Return response with job_id
            response = {"status": "done", "job_id": job_id}
            logger.info(response)
        else:
            # Return error because the server is not active
            # because it was shut down
            response = {"status": "error", "reason": "Server not active"}
            error_logger.error(response)

        return jsonify(response)

    # Method Not Allowed
    error_logger.error({"error": "Method not allowed"})
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """Method that calculates the mean by category"""
    # Check if I sent a POST request
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        logger.info("Got request %s", data)

        # Check if server is not shut down
        if not webserver.tasks_runner.shutdown_event.is_set():
            # Create job_id for the job
            job_id = "job_id_" + str(webserver.job_counter)

            # Create job with the request type, job_id, data from the json file
            # and the data ingestor in order to process data
            job = Job("mean_by_category", job_id, data, webserver.data_ingestor)

            # Add the job into the jobs dict where I hold all jobs created
            # and submit job into thread pool
            webserver.tasks_runner.jobs[job_id] = job
            webserver.tasks_runner.submit(job)

            # Increment the job_counter
            webserver.job_counter += 1

            # Return response with job_id
            response = {"status": "done", "job_id": job_id}
            logger.info(response)
        else:
            # Return error because the server is not active
            # because it was shut down
            response = {"status": "error", "reason": "Server not active"}
            error_logger.error(response)

        return jsonify(response)

    # Method Not Allowed
    error_logger.error({"error": "Method not allowed"})
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """Method that calculates a given state's mean by category"""
    # Check if I sent a POST request
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        logger.info("Got request %s", data)

        # Check if server is not shut down
        if not webserver.tasks_runner.shutdown_event.is_set():
            # Create job_id for the job
            job_id = "job_id_" + str(webserver.job_counter)

            # Create job with the request type, job_id, data from the json file
            # and the data ingestor in order to process data
            job = Job("state_mean_by_category", job_id, data, webserver.data_ingestor)

            # Add the job into the jobs dict where I hold all jobs created
            # and submit job into thread pool
            webserver.tasks_runner.jobs[job_id] = job
            webserver.tasks_runner.submit(job)

            # Increment the job_counter
            webserver.job_counter += 1

            # Return response with job_id
            response = {"status": "done", "job_id": job_id}
            logger.info(response)
        else:
            # Return error because the server is not active
            # because it was shut down
            response = {"status": "error", "reason": "Server not active"}
            error_logger.error(response)

        return jsonify(response)

    # Method Not Allowed
    error_logger.error({"error": "Method not allowed"})
    return jsonify({"error": "Method not allowed"}), 405

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    """Method that prints all types of requests and its routes"""
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    """Return all defined routes"""
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
