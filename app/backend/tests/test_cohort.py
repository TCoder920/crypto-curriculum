"""Tests for cohort endpoints"""
import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.main import app
from app.backend.models.cohort import Cohort, CohortMember, CohortRole
from app.backend.models.user import User, UserRole
from app.backend.core.database import get_db
from app.backend.tests.conftest import override_get_db


@pytest.mark.asyncio
async def test_create_cohort(
    async_client: AsyncClient,
    test_instructor,
    override_get_db,
    test_instructor_token,
):
    """Test creating a cohort as instructor"""
    app.dependency_overrides[get_db] = override_get_db
    
    response = await async_client.post(
        "/api/v1/cohorts",
        headers={"Authorization": f"Bearer {test_instructor_token}"},
        json={
            "name": "New Test Cohort",
            "description": "A test cohort",
            "is_active": True,
        },
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Test Cohort"
    assert data["description"] == "A test cohort"
    assert data["is_active"] is True
    assert data["created_by"] == test_instructor.id
    assert len(data["members"]) == 1  # Creator is automatically added
    assert data["members"][0]["role"] == CohortRole.INSTRUCTOR.value
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_cohort_student_forbidden(
    async_client: AsyncClient,
    override_get_db,
    test_token,
):
    """Test that students cannot create cohorts"""
    app.dependency_overrides[get_db] = override_get_db
    
    response = await async_client.post(
        "/api/v1/cohorts",
        headers={"Authorization": f"Bearer {test_token}"},
        json={
            "name": "New Test Cohort",
            "description": "A test cohort",
        },
    )
    
    assert response.status_code == 403
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_list_cohorts_instructor(
    async_client: AsyncClient,
    test_cohort,
    override_get_db,
    test_instructor_token,
):
    """Test listing cohorts as instructor"""
    app.dependency_overrides[get_db] = override_get_db
    
    response = await async_client.get(
        "/api/v1/cohorts",
        headers={"Authorization": f"Bearer {test_instructor_token}"},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert any(c["id"] == test_cohort.id for c in data["cohorts"])
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_list_cohorts_student(
    async_client: AsyncClient,
    test_cohort,
    test_user,
    override_get_db,
    test_token,
    db_session: AsyncSession,
):
    """Test that students only see cohorts they're members of"""
    app.dependency_overrides[get_db] = override_get_db
    
    # Initially, student should see no cohorts
    response = await async_client.get(
        "/api/v1/cohorts",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    
    # Add student to cohort
    member = CohortMember(
        cohort_id=test_cohort.id,
        user_id=test_user.id,
        role=CohortRole.STUDENT.value,
    )
    db_session.add(member)
    await db_session.commit()
    
    # Now student should see the cohort
    response = await async_client.get(
        "/api/v1/cohorts",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["cohorts"][0]["id"] == test_cohort.id
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_cohort_details(
    async_client: AsyncClient,
    test_cohort,
    override_get_db,
    test_instructor_token,
):
    """Test getting cohort details"""
    app.dependency_overrides[get_db] = override_get_db
    
    response = await async_client.get(
        f"/api/v1/cohorts/{test_cohort.id}",
        headers={"Authorization": f"Bearer {test_instructor_token}"},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_cohort.id
    assert data["name"] == test_cohort.name
    assert "members" in data
    assert data["member_count"] >= 1
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_cohort_not_found(
    async_client: AsyncClient,
    override_get_db,
    test_instructor_token,
):
    """Test getting non-existent cohort"""
    app.dependency_overrides[get_db] = override_get_db
    
    response = await async_client.get(
        "/api/v1/cohorts/999",
        headers={"Authorization": f"Bearer {test_instructor_token}"},
    )
    
    assert response.status_code == 404
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_add_member_to_cohort(
    async_client: AsyncClient,
    test_cohort,
    test_user,
    override_get_db,
    test_instructor_token,
):
    """Test adding a member to a cohort"""
    app.dependency_overrides[get_db] = override_get_db
    
    response = await async_client.post(
        f"/api/v1/cohorts/{test_cohort.id}/members",
        headers={"Authorization": f"Bearer {test_instructor_token}"},
        json={
            "user_id": test_user.id,
            "role": "student",
        },
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == test_user.id
    assert data["role"] == CohortRole.STUDENT.value
    assert data["cohort_id"] == test_cohort.id
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_add_member_already_exists(
    async_client: AsyncClient,
    test_cohort,
    test_user,
    override_get_db,
    test_instructor_token,
    db_session: AsyncSession,
):
    """Test adding a member that already exists"""
    app.dependency_overrides[get_db] = override_get_db
    
    # Add member first
    member = CohortMember(
        cohort_id=test_cohort.id,
        user_id=test_user.id,
        role=CohortRole.STUDENT.value,
    )
    db_session.add(member)
    await db_session.commit()
    
    # Try to add again
    response = await async_client.post(
        f"/api/v1/cohorts/{test_cohort.id}/members",
        headers={"Authorization": f"Bearer {test_instructor_token}"},
        json={
            "user_id": test_user.id,
            "role": "student",
        },
    )
    
    assert response.status_code == 400
    assert "already a member" in response.json()["detail"].lower()
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_remove_member_from_cohort(
    async_client: AsyncClient,
    test_cohort,
    test_user,
    override_get_db,
    test_instructor_token,
    db_session: AsyncSession,
):
    """Test removing a member from a cohort"""
    app.dependency_overrides[get_db] = override_get_db
    
    # Add member first
    member = CohortMember(
        cohort_id=test_cohort.id,
        user_id=test_user.id,
        role=CohortRole.STUDENT.value,
    )
    db_session.add(member)
    await db_session.commit()
    
    # Remove member
    response = await async_client.delete(
        f"/api/v1/cohorts/{test_cohort.id}/members/{test_user.id}",
        headers={"Authorization": f"Bearer {test_instructor_token}"},
    )
    
    assert response.status_code == 204
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_remove_last_instructor_forbidden(
    async_client: AsyncClient,
    test_cohort,
    test_instructor,
    override_get_db,
    test_instructor_token,
):
    """Test that removing the last instructor is forbidden"""
    app.dependency_overrides[get_db] = override_get_db
    
    response = await async_client.delete(
        f"/api/v1/cohorts/{test_cohort.id}/members/{test_instructor.id}",
        headers={"Authorization": f"Bearer {test_instructor_token}"},
    )
    
    assert response.status_code == 400
    assert "last instructor" in response.json()["detail"].lower()
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_remove_member_not_found(
    async_client: AsyncClient,
    test_cohort,
    test_user,
    override_get_db,
    test_instructor_token,
):
    """Test removing a member that doesn't exist"""
    app.dependency_overrides[get_db] = override_get_db
    
    response = await async_client.delete(
        f"/api/v1/cohorts/{test_cohort.id}/members/{test_user.id}",
        headers={"Authorization": f"Bearer {test_instructor_token}"},
    )
    
    assert response.status_code == 404
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_student_cannot_access_cohort(
    async_client: AsyncClient,
    test_cohort,
    override_get_db,
    test_token,
):
    """Test that students cannot access cohorts they're not members of"""
    app.dependency_overrides[get_db] = override_get_db
    
    response = await async_client.get(
        f"/api/v1/cohorts/{test_cohort.id}",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    
    assert response.status_code == 403
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_unauthorized_cohort_access(
    async_client: AsyncClient,
    test_cohort,
):
    """Test that unauthenticated requests are rejected"""
    response = await async_client.get(
        f"/api/v1/cohorts/{test_cohort.id}",
    )
    
    assert response.status_code == 401

