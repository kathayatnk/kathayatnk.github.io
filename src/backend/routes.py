from fastapi import APIRouter
from src.backend.auth.routes import router as auth_router
from src.backend.user.routes import router as user_router
from src.backend.bank.routes import router as bank_router
from src.backend.card.routes import router as card_router
from src.backend.device.routes import router as device_router
from src.backend.seeder.routes import router as seeder_router
from src.backend.root.root import router as root_router
from src.core.settings import settings

router = APIRouter(prefix=settings.FASTAPI_API_V1_PATH)
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(bank_router)
router.include_router(card_router)
router.include_router(device_router)
router.include_router(seeder_router)
router.include_router(root_router)