from fastapi import FastAPI, HTTPException
from app.author import Author, CreateAuthor


authors: list[Author] = [
    #Author(0, 'Людовико Эйнауди', 'Минимализм'),
    #Author(1, 'Роберто Каччапалья', 'Современная классика'),
    #Author(2, 'Джо Хисаиси', 'Классика')
]

app = FastAPI()

########
# Jaeger

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Service name is required for most backends,
# and although it's not necessary for console export,
# it's good to set service name anyways.
resource = Resource(attributes={
    SERVICE_NAME: "author-service"
})

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

FastAPIInstrumentor.instrument_app(app)

#
########

########
# Prometheus

from prometheus_fastapi_instrumentator import Instrumentator

@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)

#
########

def add_authors(content: CreateAuthor):
    id = len(authors)
    authors.append(Author(id, content.nickname, content.genre))
    return id

@app.get("/v1/auth")
async def get_auth():
    return authors

@app.post("/v1/auth")
async def add_author(content: CreateAuthor):
    add_authors(content)
    return authors[-1]

@app.get("/v1/auth/{id}")
async def get_auth_by_id(id: int):
    result = [item for item in authors if item.id == id]
    if len(result) > 0:
        return result[0]
    raise HTTPException(status_code = 404, detail="Автор не найден")

@app.get("/__health")
async def check_service():
    return