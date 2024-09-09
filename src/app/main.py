from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.jaeger.proto.grpc import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from src.app.routers import face_verification

app = FastAPI()

# Настройка трейсера
trace.set_tracer_provider(TracerProvider())
jaeger_exporter = JaegerExporter(
    agent_host_name='jaeger',  # Jaeger host из docker-compose
    agent_port=6831,           # порт Jaeger для UDP
)
span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Инструментирование FastAPI
FastAPIInstrumentor.instrument_app(app)

# Инструментирование HTTP-клиентов (например, requests)
RequestsInstrumentor().instrument()

@app.get('/')
def read_main():
    """Func for hello page."""
    return {'message': 'Welcome to the Face Verification API'}


app.include_router(
    face_verification.router, prefix='/face_verification', tags=['face_verification'],
)
