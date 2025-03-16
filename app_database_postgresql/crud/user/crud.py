import inspect


import bcrypt

from sqlalchemy import select, insert, update, and_, or_, asc, desc, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic_core import PydanticUndefined

from app_database_postgresql.models.user import User
from commons.core.password_context import get_hashed_password


async def create_user(database: AsyncSession, name: str, email: str, password: str, role: str) -> User | None:
    """
    User 생성을 시도한다.
    생성에 성공한다면 User객체를, 실패한다면 None을 반환받는다.
    """
    model = User

    values = {
        "name": name,
        "email": email,
        "password": password,
        "role": role,
    }
    orm_object = model(**values)

    try:
        database.add(orm_object)
        await database.commit()

    except Exception as e:
        current_func_name = inspect.currentframe().f_code.co_name
        print(f"Error - {current_func_name} : {str(e)}")

        await database.rollback()

        return None

    return orm_object


async def read_user_with_kwargs(database: AsyncSession, **kwargs) -> User | None:
    """
    하나의 User 읽기를 시도한다.
    읽기에 성공한다면 User객체를, 실패한다면 None을 반환받는다.
    실패는 가져온 User의 갯수가 1개가 아닐 때도 포함된다.
    """
    model = User

    result = None

    try:
        stmt = select(model).where(model.is_deleted == False, model.is_banned == False)

        for field, value in kwargs.items():
            if hasattr(model, field):
                stmt = stmt.where(getattr(model, field) == value)
            else:
                print(f"경고: '{field}'는 {model.__name__}에서 존재하지 않는 필드입니다.")

        database_result = await database.execute(stmt)
        result = database_result.scalar_one_or_none()

    except Exception as e:
        current_func_name = inspect.currentframe().f_code.co_name
        print(f"Error - {current_func_name} : {str(e)}")

        return None

    return result


async def read_user_with_name(database: AsyncSession, name: str) -> User | None:
    """
    하나의 User를 name으로 검색해 읽기를 시도한다.
    읽기에 성공한다면 User객체를, 실패한다면 None을 반환받는다.
    실패는 가져온 User의 갯수가 1개가 아닐 때도 포함된다.
    """
    return await read_user_with_kwargs(database=database, name=name)


async def read_user_with_email(database: AsyncSession, email: str) -> User | None:
    """
    하나의 User를 email로 검색해 읽기를 시도한다.
    읽기에 성공한다면 User객체를, 실패한다면 None을 반환받는다.
    실패는 가져온 User의 갯수가 1개가 아닐 때도 포함된다.
    """
    return await read_user_with_kwargs(database=database, email=email)


async def update_user(
    database: AsyncSession,
    id: int,
    email: str | None = PydanticUndefined,
) -> bool:
    """
    하나의 User를 id로 검색하고, 입력된 값들을 이용하여 데이터를 갱신한다.
    갱신에 성공하면 True를 실패하면 False를 반환한다.
    성공에는 존재하지 않는 id를 통한 User 검색 후 갱신 시도를 포함한다.
    """

    model = User
    values = {}

    if email is not PydanticUndefined:
        values["email"] = email

    try:
        stmt = update(model).where(model.id == id).values(values)

        await database.execute(stmt)
        await database.commit()

    except Exception as e:
        current_func_name = inspect.currentframe().f_code.co_name
        print(f"Error - {current_func_name} : {str(e)}")

        await database.rollback()
        return False

    return True


async def update_user_password(database: AsyncSession, id: int, new_password: str) -> bool:
    """
    하나의 User를 name으로 검색하고, 입력된 값을 이용하여 패스워드 해시를 갱신한다.
    갱신에 성공하면 True를 실패하면 False를 반환한다.
    성공에는 존재하지 않는 name을 통한 User 검색 후 갱신 시도를 포함한다.
    """
    model = User

    try:
        hashed_password = get_hashed_password(new_password)

        stmt = update(model).where(model.id == id).values(password=hashed_password)

        await database.execute(stmt)
        await database.commit()

    except Exception as e:
        current_func_name = inspect.currentframe().f_code.co_name
        print(f"Error - {current_func_name} : {str(e)}")

        await database.rollback()
        return False

    return True


async def delete_user(
    database: AsyncSession,
    id: int,
) -> bool:
    """
    하나의 User를 id로 검색하고, User를 삭제한다. (Soft delete)
    삭제에 성공하면 True를 실패하면 False를 반환한다.
    성공에는 존재하지 않는 id를 통한 User 검색 후 삭제 시도를 포함한다.
    """

    model = User

    values = {"is_deleted": True}

    stmt = update(model).where(model.id == id).values(**values)

    try:
        await database.execute(stmt)
        await database.commit()

    except Exception as e:
        current_func_name = inspect.currentframe().f_code.co_name
        print(f"Error - {current_func_name} : {str(e)}")

        await database.rollback()
        return False

    return True


async def ban_user(
    database: AsyncSession,
    id: int,
) -> bool:
    """
    하나의 User를 id로 검색하고, User를 차단한다. (Soft delete)
    차단에 성공하면 True를 실패하면 False를 반환한다.
    성공에는 존재하지 않는 id를 통한 User 검색 후 차단 시도를 포함한다.
    """

    model = User

    values = {"is_banned": True}

    stmt = update(model).where(model.id == id).values(**values)

    try:
        await database.execute(stmt)
        await database.commit()

    except Exception as e:
        current_func_name = inspect.currentframe().f_code.co_name
        print(f"Error - {current_func_name} : {str(e)}")

        await database.rollback()
        return False

    return True
