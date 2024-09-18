from random import randint
from flask import Flask, request

from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry import metrics
# from opentelemetry.exporter.jaeger
# from opentelemetry.sdk.metrics import MeterProvider
# from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader , ConsoleMetricExporter

import logging

resource = Resource(attributes={
    SERVICE_NAME: "justTest_http"
})

traceProvider = TracerProvider(resource=resource)

jaeger_exporter = JaegerExporter(
    # agent_host_name="localhost",
    # agent_port=14268,
    collector_endpoint="http://jaeger:14268/api/traces"
)

processor = BatchSpanProcessor(jaeger_exporter)
traceProvider.add_span_processor(processor)
trace.set_tracer_provider(traceProvider)

# reader = PeriodicExportingMetricReader(
#     OTLPMetricExporter(endpoint="localhost:4317" , insecure=True)
# )

# # reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
# meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
# metrics.set_meter_provider(meterProvider)

tracer = trace.get_tracer(__name__)

# meter = metrics.get_meter(__name__)

# roll_counter = meter.create_counter(
#     "dice.rolls",
#     description="The number of rolls by roll value",
# )

app = Flask(__name__)
# FlaskInstrumentor().instrument_app(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/rolldice")
def roll_dice():
    # This creates a new span that's the child of the current one
    with tracer.start_as_current_span("roll") as roll_span:
        player = request.args.get('player', default = None, type = str)
        result = str(roll())
        roll_span.set_attribute("roll.value", result)
        # This adds 1 to the counter for the given roll value
        # roll_counter.add(1, {"roll.value": result})
        if player:
            logger.warning("{} is rolling the dice: {}", player, result)
        else:
            logger.warning("Anonymous player is rolling the dice: %s", result)
        return result

def roll():
    return randint(1, 6)