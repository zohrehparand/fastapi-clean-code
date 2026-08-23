from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from core.app.database import get_db
from core.auth.jwtauth import get_authenticated_user
from core.costs.model import CostModel
from core.costs.schema import CostSchema, CostResponseSchema
from core.user.model import UserModel


router = APIRouter(tags=["Costs"], prefix="/manage")


@router.post("/costs", response_model=CostResponseSchema, status_code=status.HTTP_201_CREATED)
def create(cost_data: CostSchema, current_user: UserModel = Depends(get_authenticated_user), db: Session = Depends(get_db)):
    new_obj = CostModel(
        user_id=current_user.id,
        description=cost_data.description,
        amount=cost_data.amount,
    )
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    return new_obj


@router.get("/costs", response_model=list[CostResponseSchema])
def get_list(
    description: str | None = Query(default=None),
    min_amount: float | None = Query(default=None, gt=0),
    max_amount: float | None = Query(default=None, gt=0),
    current_user: UserModel = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    query = db.query(CostModel).filter(CostModel.user_id == current_user.id)

    if description:
        query = query.filter(CostModel.description == description)
    if min_amount is not None:
        query = query.filter(CostModel.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(CostModel.amount <= max_amount)

    return query.all()


@router.get("/costs/{id}", response_model=CostResponseSchema)
def search(id: int, current_user: UserModel = Depends(get_authenticated_user), db: Session = Depends(get_db)):
    db_cost = db.query(CostModel).filter(CostModel.id == id, CostModel.user_id == current_user.id).first()
    if db_cost is None:
        raise HTTPException(status_code=404, detail="Cost not found")
    return db_cost


@router.put("/costs/{id}", response_model=CostResponseSchema)
def update(id: int, cost_data: CostSchema, current_user: UserModel = Depends(get_authenticated_user), db: Session = Depends(get_db)):
    query = db.query(CostModel).filter(CostModel.id == id, CostModel.user_id == current_user.id).first()
    if query is None:
        raise HTTPException(status_code=404, detail="Cost not found")

    query.description = cost_data.description
    query.amount = cost_data.amount
    db.commit()
    db.refresh(query)
    return query


@router.delete("/costs/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, current_user: UserModel   = Depends(get_authenticated_user), db: Session = Depends(get_db)):
    query = db.query(CostModel).filter(CostModel.id == id, CostModel.user_id == current_user.id).first()
    if query is None:
        raise HTTPException(status_code=404, detail="Cost not found")

    db.delete(query)
    db.commit()
