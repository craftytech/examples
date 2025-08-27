# Dash0 - OpenTelemetry Instrumented Flask App

A simple Flask web application with OpenTelemetry instrumentation for distributed tracing and observability.

## Features

- **Flask Web Server** - Basic HTTP server with a dynamic hello endpoint
- **OpenTelemetry Integration** - Automatic instrumentation for tracing and metrics
- **Distinct Responses** - Each request returns a unique response with random colors, animals, and timestamps
- **Structured Logging** - Comprehensive logging with timestamps and log levels
- **OTLP Export** - Configured to export traces to OpenTelemetry Protocol (OTLP) endpoints

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd dash0
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install flask opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-flask opentelemetry-exporter-otlp
   ```

## Configuration

The application is configured with OpenTelemetry tracing. You can modify the configuration in `dash0.py`:

- **Service Name**: `craaftytech-python-app`
- **Service Version**: `1.0.0`
- **OTLP Endpoint**: Configured for gRPC export (modify as needed)

## Running the Application

1. **Activate your virtual environment:**
   ```bash
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

2. **Start the Flask server:**
   ```bash
   python dash0.py
   ```

3. **Access the application:**
   - Open your browser and go to: `http://localhost:5000`
   - Or use curl: `curl http://localhost:5000`

## What You'll See

Each time you refresh the page or make a request, you'll get a unique response like:
```
Hello, World! Today's color is blue and the animal is elephant. Timestamp: 1703123456
```

The response includes:
- A random color from a predefined list
- A random animal from a predefined list
- A current Unix timestamp

## Logging

The application provides structured logging with:
- Request logging when the endpoint is called
- Generated response details (color, animal)
- OpenTelemetry trace information

Logs appear in your console/terminal when running the application.

## OpenTelemetry Integration

The app automatically instruments Flask requests and creates spans for:
- HTTP requests
- Custom business logic (hello-span)
- Automatic correlation between requests and traces

## Development

- **Debug Mode**: Enabled by default (`app.run(debug=True)`)
- **Port**: Default Flask port 5000
- **Hot Reload**: Flask debug mode enables automatic reloading on code changes

## Project Structure

```
dash0/
├── dash0.py          # Main Flask application
├── env/              # Python virtual environment (gitignored)
├── env-example       # Example environment configuration
├── .gitignore        # Git ignore patterns
└── README.md         # This file
```

## Next Steps

- Configure OTLP endpoint for your observability backend (Jaeger, Zipkin, etc.)
- Add more endpoints and business logic
- Implement metrics collection
- Add health checks and monitoring endpoints
