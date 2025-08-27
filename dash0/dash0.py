import logging
import random
import time
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from flask import Flask

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure OpenTelemetry
resource = Resource.create({
    "service.name": "craaftytech-python-app",
    "service.version": "1.0.0",
    # Add other relevant resource attributes
})

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Initialize Flask app
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app) # Auto-instrument Flask

@app.route("/")
def hello_world():
    logger.info("Hello endpoint called")
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("hello-span"):
        # Generate distinct response each time
        colors = ["red", "blue", "green", "purple", "orange", "pink", "yellow", "cyan"]
        animals = ["cat", "dog", "elephant", "giraffe", "penguin", "dolphin", "eagle", "tiger"]
        
        random_color = random.choice(colors)
        random_animal = random.choice(animals)
        timestamp = int(time.time())
        
        response = f"<p>Hello, World! Today's color is {random_color} and the animal is {random_animal}. Timestamp: {timestamp}</p>"
        logger.info(f"Generated response with color: {random_color}, animal: {random_animal}")
        return response

if __name__ == "__main__":
    app.run(debug=True)