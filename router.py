from fastapi import APIRouter
from apps.domain.domain_routes import domainroute
from apps.domainuser.login import loginroute
from apps.document.doc import docroute
from apps.question.question import questionroute

routingapp = APIRouter()


routingapp.include_router(domainroute, prefix="/api/v1")
routingapp.include_router(loginroute, prefix="/api/v1")
routingapp.include_router(docroute, prefix="/api/v1")
routingapp.include_router(questionroute, prefix="/api/v1")
