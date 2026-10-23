\# Infrastructure Health Monitor



A lightweight, Python-based infrastructure monitoring and diagnostics application designed to collect system resource metrics, evaluate configurable warning conditions, monitor HTTP service availability, and preserve timestamped results for troubleshooting.



\## Project Overview



This project simulates a small-business IT monitoring requirement.



IT administrators need visibility into resource utilization and service availability to help identify potential infrastructure issues.



The application provides a lightweight, locally executed monitoring solution that demonstrates Python automation, system administration, networking, configuration management, logging, and reliability testing.



\*\*Project status:\*\* Functional local prototype. Not intended as a production monitoring platform.



\## Technologies Used



\- Python 3.14

\- psutil

\- Windows PowerShell

\- Python unittest and unittest.mock

\- JSON and JSON Lines (JSONL)

\- Git



\## Implemented Features



\### System Resource Monitoring



\- Collects CPU utilization over one-second sampling intervals.

\- Collects RAM utilization percentages.

\- Measures disk utilization of the home drive.

\- Displays three consecutive resource samples per execution.



\### Threshold-Based Warning Detection



\- Evaluates CPU and memory utilization against configurable thresholds.

\- Requires three consecutive qualifying samples for CPU and memory warnings.

\- Evaluates disk usage against a configurable threshold.

\- Displays warnings in the console.



\### HTTP Service Availability



\- Sends an HTTP request to a configurable endpoint.

\- Treats HTTP 2xx responses as successful checks.

\- Detects unsuccessful HTTP responses, connection failures, and timeouts.

\- Records service availability with each monitoring report.



\### Historical Reporting



\- Saves timestamped results to `reports/metrics.jsonl`.

\- Preserves records from previous executions.

\- Stores resource samples, warning states, and configured thresholds.

\- Reports file-writing failures rather than silently ignoring them.



\### Configuration Management



\- Uses `config/monitor.json` to define monitoring thresholds, HTTP endpoint, and request timeout.

\- Validates settings before collecting metrics.

\- Rejects invalid thresholds, unsupported URL schemes, and invalid timeout values.



\## Getting Started



\*\*Requirements:\*\* Windows, Python 3.14, and an internet connection for initial dependency installation.



1\. Clone or download the repository.

2\. Open PowerShell in the project directory.

3\. Create a virtual environment using `py -V:3.14 -m venv .venv`.

4\. Install dependencies using `.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt`.

5\. Review `config/monitor.json` and adjust settings if necessary.

6\. Run the application using `.\\.venv\\Scripts\\python.exe .\\src\\monitor.py`.



The application displays resource measurements, evaluates warnings, saves a report, and then exits.



\*\*Note:\*\* The default HTTP endpoint is `http://127.0.0.1:8765/`. If no test web server is listening there, an HTTP service warning is expected.



\## Configuration



The configuration file supports:



| Setting | Default |

|---|---|

| CPU warning threshold | 85% |

| RAM warning threshold | 85% |

| Disk warning threshold | 90% |

| HTTP service URL | `http://127.0.0.1:8765/` |

| HTTP timeout | 2 seconds |



CPU, RAM, and disk thresholds must be between 1% and 100%. The HTTP timeout must be greater than zero and no more than 30 seconds.



\## Testing and Validation



The application has been tested using Python's built-in unittest framework.



\*\*Most recently verified:\*\* October 20, 2026 — 22 automated tests passed.



Verified scenarios include:



\- Temporary and consecutive high-utilization measurements.

\- Alert threshold boundaries.

\- Valid and invalid configuration settings.

\- HTTP success, server errors, connection failures, and timeouts.

\- Appending multiple JSONL records.

\- Simulated report-writing failures.

\- Unavailable HTTP services with successful reporting.

\- Configuration integration and startup validation.



Run the test suite using:



`.\\.venv\\Scripts\\python.exe -m unittest discover -s tests -v`



\## Application Exit Codes



\- `0` — Monitoring completed and the report was saved.

\- `1` — Monitoring completed but report writing failed.

\- `2` — Configuration loading or validation failed.



An exit code of `0` does not necessarily mean all monitored resources and services are healthy.



\## Security Considerations



\- The application does not require administrator privileges for its current functionality.

\- The development HTTP test service can be restricted to localhost.

\- Monitoring reports are excluded from Git through `.gitignore`.

\- Credentials, personal data, and confidential infrastructure information should never be added to the repository.

\- Only authorized endpoints should be monitored.



\## Known Limitations



\- Monitoring runs once per execution; continuous background monitoring is not implemented.

\- CPU and memory warnings use three consecutive samples, not a configurable historical duration.

\- The application checks one HTTP endpoint per execution.

\- HTTP availability does not guarantee that every feature of an application is healthy.

\- Reports are stored locally without centralized aggregation.

\- Automated notifications, scheduling, and dashboards are not implemented.



\## Future Improvements



\- Scheduled monitoring.

\- Multiple service endpoints.

\- More advanced historical analysis.

\- Configurable sampling intervals.

\- Additional monitoring and failure-recovery tests.

\- Optional dashboards and notification integrations.



\## Skills Demonstrated



Python programming, Windows system monitoring, HTTP troubleshooting, configuration validation, structured logging, automated testing, exception handling, Git version control, and technical documentation.



This is an independently developed educational home-lab project and does not represent production deployment or employer infrastructure.

