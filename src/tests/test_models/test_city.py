from sqlalchemy.ext.asyncio import AsyncSession

from models.city import City


class TestCityModel:
    async def test_fields(self, async_session: AsyncSession) -> None:
        current_fields_name = [i.name for i in City.__table__.columns]
        related_fields = [
            i._dependency_processor.key for i in City.__mapper__.relationships
        ]
        all_model_fields = current_fields_name + related_fields
        schema_fields_name = {
            "name",
            "users",
        }
        for field in schema_fields_name:
            assert field in all_model_fields, (
                "Нет необходимого поля %s" % field
            )
