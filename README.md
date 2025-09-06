Name: Maria Andreea Chirnogeanu
Group: 333CB 

# Assignment 1 ASC - Le Stats Sportifs
#### Application for http requests with multithreaded implementation

Organisation
-
The assignment is implementing using Flask a web application where you can ask a question from a set of questions to a certain route by making a POST request, it gets answered and then you can get the result of the question by making a GET request based on the job id.

Firstly, I completed the DataIngestor class from the skell of the assignment to include the extraction of data from csv file and to answer a question, given the data from the POST request and the route type.

For this assignment we had to implement the task handling multithreaded and we had to use a ThreadPool of TaskRunners.
I chose to create those classes myself for better control of the application.
I used an event for the thread pool to handle the graceful shutdown route. If I try to create a task after the graceful shutdown, I print an error that signals that the server was shut down.

I also implemented a Job class where I handle the execution of a task. This is pretty simple. I just call the answer_question method from the data ingestor and I return the result.

The flow of the application is the following:
For a POST request:
1. I create a job with a job id (which has an index determined by job_counter), a status (which is "running", then, when I finish the task, the status is "done"), a type (based on the route of the question) and a reference to the data ingestor in order to get the answer of the question
2. I insert the new job into a job dictionary
3. I submit the job (I put the job into the thread pool queue)
4. A task runner gets the task and executes it (meaning the question gets an answer)
5. I mark the job as done for the job, as well as the dictionary
6. I write the answer into a file called results/{job_id}

For a GET request for a given job_id:
1. I check if the job_id was created. If it wasn't, it returns an error
2. If it exists, I try to get the result (meaning I read from results/{job_id} and get the result)
3. If the file is empty, meaning the result is empty, the job is still running
4. If it isn't, return the result into a json

I also implemented the jobs, num_jobs and graceful_shutdown routes, which are not checked by the local checker.
Jobs prints all jobs with the format job_id: status, num_jobs gets all tasks that are still in the thread pool and graceful_shutdown shuts dowm the application.

The unittests implementation uses the answer_question method from data ingestor. I get the input data from the json of the input, I answer the question, then I compare it with the data from the json of the output file. My implementation was heavily based on the checker provided by the assignment.

For logging, I created an extra file called webserver_logger.py, I created two objects (one for info, one for error). I include all inputs and outputs into the file.log files using rotating file handlers and I also formatted the time. The error handling was done using the webserver.log file.


Implementation
-

* I implemented all criteria for the assignment (all the POST requests, all the GET requests, the creation of unittests and the logging)
* I didn't implement extra routes for the application, but I implemented some error messages that were not specified in the text of our assignment. such as for not finding jobs in the jobs dictionary.
* I had quite a difficult time understanding the application and how it works at first. The assignment was not very clear to me when I read it, but I had asked some uni mates and it was all clear in the end.
* I had a lot of fun with this homework. It was one of the most insightful of them all. It made me understand web applications more and it was fun creating unittests and learning about logging.


Resources
-

I had used the resources linked into the homework assignment from OCW, the 1-3 labs on Python threads, thread pool executor, reqbin.com used for testing my application manually (by sending requests by hand) and realpython.com that explained to me python logging using examples. I also took a look at an old homework that made us create a thread pool my hand (2nd Homework for APD) and the explanation on how thread pools work at Lab 7 at this subject.