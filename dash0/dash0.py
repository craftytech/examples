import atexit
import logging
import random
import time
from flask import Flask

# ---------- OpenTelemetry: traces ----------
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# ---------- OpenTelemetry: logs ----------
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.instrumentation.logging import LoggingInstrumentor

# If you like structured console output too
try:
    from pythonjsonlogger import jsonlogger
    USE_JSON = True
except Exception:
    USE_JSON = False

# ----- Resources (shared) -----
resource = Resource.create({
    "service.name": "craaftytech-python-app",
    "service.version": "1.0.0",
})

# ----- Traces -----
trace_provider = TracerProvider(resource=resource)
trace_exporter = OTLPSpanExporter()  # uses OTEL_EXPORTER_* env vars
trace_processor = BatchSpanProcessor(trace_exporter)
trace_provider.add_span_processor(trace_processor)
trace.set_tracer_provider(trace_provider)

# ----- Logs -----
log_provider = LoggerProvider(resource=resource)
log_exporter = OTLPLogExporter()      # uses OTEL_EXPORTER_* env vars
log_processor = BatchLogRecordProcessor(log_exporter)
log_provider.add_log_record_processor(log_processor)
# Note: set_logger_provider is not available in OpenTelemetry SDK 1.36.0+
# The logger provider is used directly by the LoggingHandler

# Inject trace/span IDs into stdlib logs (adds fields like otelTraceID, otelSpanID)
LoggingInstrumentor().instrument(set_logging_format=True)

# ----- stdlib logging config -----
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Console handler (keep console + export via OTLP)
console_handler = logging.StreamHandler()
if USE_JSON:
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s "
        "%(otelTraceID)s %(otelSpanID)s %(otelServiceName)s"
    )
else:
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - "
        "%(message)s (trace_id=%(otelTraceID)s span_id=%(otelSpanID)s)"
    )
console_handler.setFormatter(formatter)
root_logger.addHandler(console_handler)

# Optional: send stdlib logs through OTel too (in addition to console)
otel_logging_handler = LoggingHandler(level=logging.INFO, logger_provider=log_provider)
root_logger.addHandler(otel_logging_handler)

logger = logging.getLogger(__name__)

# Ensure everything flushes on exit
atexit.register(trace_provider.shutdown)
atexit.register(log_provider.shutdown)

# ----- Flask app -----
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.route("/")
def hello_world():
    logger.info("Hello endpoint called")
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("hello-span"):
        colors = ["red", "blue", "green", "purple", "orange", "pink", "yellow", "cyan"]
        animals = ["cat", "dog", "elephant", "giraffe", "penguin", "dolphin", "eagle", "tiger"]
        response = (
            f"<p>Hello, World! Today's color is {random.choice(colors)} "
            f"and the animal is {random.choice(animals)}. "
            f"Timestamp: {int(time.time())}</p>"
        )
        logger.info("Generated response with random values")
        return response

if __name__ == "__main__":
    # Example env:
    #   OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
    #   OTEL_EXPORTER_OTLP_HEADERS=authorization=Bearer <token>   (if needed)
    app.run(debug=True)
