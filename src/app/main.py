from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from src.app.routers import face_verification

app = FastAPI()

# Настройка ресурса с указанием имени сервиса
resource = Resource.create(attributes={'service.name': 'face_verification_service'})

# Инициализация трейсера с ресурсом
trace_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(trace_provider)

# Настройка Jaeger Exporter
jaeger_exporter = JaegerExporter(
    agent_host_name='jaeger',  # Jaeger host из docker-compose
    agent_port=6831,           # порт Jaeger для UDP
)

# Создание процессора для отправки трейсингов в Jaeger
span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Инструментирование FastAPI
FastAPIInstrumentor.instrument_app(app)

# Инструментирование HTTP-клиентов (например, requests)
RequestsInstrumentor().instrument()


@app.on_event('shutdown')
def shutdown_tracer():
    """Завершение работы."""
    try:
        trace.get_tracer_provider().shutdown()
    except Exception as exc:
        return f'Ошибка завершения трейсера: {exc}'


@app.get('/')
def read_main():
    """Функция для привественного сообщения."""
    return {'message': 'Welcome to the Face Verification API'}


app.include_router(
    face_verification.router, prefix='/face_verification', tags=['face_verification'],
)
