from hypaz_core.mongo_core import mongo_find_one
from bson import ObjectId

async def has_access_to_user(user_id: str, patient_id: str) -> bool:
    """
    Check if a user has access to a patient's data.

    Args:
        user_id (str): The ID of the user (nutrizionista).
        patient_id (str): The ID of the patient.

    Returns:
        bool: True if the user has access, False otherwise.
    """
    query = {"_id": ObjectId(patient_id), "nutrizionista": user_id}
    result = await mongo_find_one("patients", query)
    return result is not None

async def has_access_to_measure(user_id: str, measureUUId: str) -> bool:
    """
    Check if a user has access to measure data.

    Args:
        user_id (str): The ID of the user (nutrizionista).
        measureUUId (str): The ID of the measure.

    Returns:
        bool: True if the user has access, False otherwise.
    """
    query = {"UUID": measureUUId, "nutrizionista": user_id}
    result = await mongo_find_one("measurements", query)
    return result is not None

async def has_access_to_diet(user_id: str, diet_id: str) -> bool:
    """
    Check if a user has access to diet data.

    Args:
        user_id (str): The ID of the user (nutrizionista).
        diet_id (str): The ID of the diet.

    Returns:
        bool: True if the user has access, False otherwise.
    """
    query = {"_id": ObjectId(diet_id), "nutrizionista": user_id}
    result = await mongo_find_one("diets", query)
    return result is not None