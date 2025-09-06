# Le Stats Sportifs

Le Stats Sportifs is a Flask based web server that answers questions about the
**Nutrition, Physical Activity, and Obesity** dataset.  The project was created
as part of the [ASC assignment 1](https://ocw.cs.pub.ro/courses/asc/teme/tema1)
which requires handling requests asynchronously with a custom thread pool.

The server accepts questions through a REST API.  Each POST request schedules a
job in the background thread pool.  Clients can later retrieve the computed
answer by querying the job identifier.

## Requirements

* Python 3.12+
* [Flask](https://flask.palletsprojects.com/)
* [pandas](https://pandas.pydata.org/)

Place the data file `nutrition_activity_obesity_usa_subset.csv` in the project
root.  The file is loaded automatically when the application starts.

## Installation

```bash
pip install flask pandas
```

## Running the server

```bash
flask --app api_server run
```

The application creates a thread pool for background jobs and exposes the
following API endpoints:

### Job management

| Method | Route | Description |
| ------ | ----- | ----------- |
| `GET`  | `/api/jobs` | List all known jobs and their status |
| `GET`  | `/api/num_jobs` | Number of tasks waiting in the thread pool |
| `GET`  | `/api/get_results/<job_id>` | Retrieve results for a job |
| `GET`  | `/api/graceful_shutdown` | Stop the server and reject new jobs |

### Statistics queries

Each of the following routes schedules a job that analyses the CSV data.  The
request body must contain a `question` field and, where appropriate, a `state`
field.  The server responds with a job identifier which can be queried using the
`/api/get_results/<job_id>` route.

| Method | Route | Purpose |
| ------ | ----- | ------- |
| `POST` | `/api/states_mean` | Mean value for each state |
| `POST` | `/api/state_mean` | Mean value for a given state |
| `POST` | `/api/best5` | Top 5 states (lower is better for some questions) |
| `POST` | `/api/worst5` | Worst 5 states |
| `POST` | `/api/global_mean` | Global mean across all states |
| `POST` | `/api/diff_from_mean` | Difference between each state and the global mean |
| `POST` | `/api/state_diff_from_mean` | Difference between a given state and the global mean |
| `POST` | `/api/mean_by_category` | Mean grouped by category and stratification |
| `POST` | `/api/state_mean_by_category` | Category means for a specific state |

Example request:

```bash
curl -X POST http://localhost:5000/api/state_mean \
     -H "Content-Type: application/json" \
     -d '{"question": "Percent of adults aged 18 years and older who have obesity", "state": "Alabama"}'
```

Example response:

```json
{"status": "done", "job_id": "job_id_1"}
```

## Testing

Unit tests validate the data processing logic:

```bash
python -m unittest
```

## License

This project was developed for educational purposes as part of the ASC
curriculum at the Polytechnic University of Bucharest.
