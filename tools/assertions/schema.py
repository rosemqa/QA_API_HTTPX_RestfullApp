from typing import Any
import allure
from jsonschema import validate
from jsonschema.validators import Draft202012Validator
from tools.logger import get_logger

logger = get_logger('SCHEMA_ASSERTIONS')


@allure.step("Validating JSON schema")
def validate_json_schema(instance: Any, schema: dict) -> None:
    logger.info('Validating JSON schema')

    validate(
        instance=instance,
        schema=schema,
        format_checker=Draft202012Validator.FORMAT_CHECKER   # Проверка форматов (например, email, дата и т.д.)
    )
