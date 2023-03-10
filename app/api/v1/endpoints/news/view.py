from datetime import date

from fastapi import APIRouter, Depends, Path, Query
from fastapi.security import HTTPBasic
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.dependencies.paging import PaginationParams
from app.api.v1.endpoints.news.controller import CtrNews
from app.api.v1.endpoints.news.schema import (
    CommentLikeResponse, ListNewsResponse, NewsCommentRequest,
    NewsCommentResponse, NewsCommentsResponse, NewsDetailResponse,
    NewsImageRequest, NewsResponse
)

router = APIRouter()
security = HTTPBasic()


@router.post(
    path="/",
    description="Tạo mới Tin tức SCB",
    name="Tạo mới Tin tức SCB",
    responses=swagger_response(
        response_model=ResponseData[NewsResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_upload_scb_news(
        request: NewsImageRequest = Depends(NewsImageRequest.get_upload_request),
):
    (
        avatar_uuid, current_user, title, news_category_id, content, summary, start_date,
        expired_date, active_flag
    ) = request
    data = {
        "title": title,
        "news_category_id": news_category_id,
        "content": content,
        "summary": summary,
        "start_date": start_date,
        "expired_date": expired_date,
        "active_flag": active_flag
    }
    news_data = await CtrNews(current_user).ctr_save_news(
        request_data=data,
        avatar_uuid=avatar_uuid,
        current_user=current_user
    )

    return ResponseData[NewsResponse](**news_data)


@router.post(
    path="/{news_id}",
    description="Cập nhật Tin tức SCB",
    name="Cập nhật Tin tức SCB",
    responses=swagger_response(
        response_model=ResponseData[NewsResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_update_scb_news(
        request: NewsImageRequest = Depends(NewsImageRequest.get_upload_request),
        news_id: str = Path(..., description='News ID')
):
    (
        avatar_uuid, current_user, title, news_category_id, content, summary, start_date,
        expired_date, active_flag
    ) = request
    data = {
        "tilte": title,
        "news_category_id": news_category_id,
        "content": content,
        "summary": summary,
        "start_date": start_date,
        "expired_date": expired_date,
        "active_flag": active_flag
    }
    news_data = await CtrNews(current_user).ctr_update_nesws(
        news_id=news_id,
        request_data=data,
        avatar_uuid=avatar_uuid,
        current_user=current_user
    )

    return ResponseData[NewsResponse](**news_data)


@router.get(
    path="/{news_id}",
    name="Chi tiết tin tức",
    description='Chi tiết tin tức',
    responses=swagger_response(
        response_model=ResponseData[NewsDetailResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_detail_scb_news(
        news_id: str = Path(..., description='News ID'),
        current_user=Depends(get_current_user_from_header())
):
    scb_news = await CtrNews(current_user).ctr_get_detail_news(news_id=news_id)
    return ResponseData[NewsDetailResponse](**scb_news)


@router.get(
    path="/",
    name="Danh sách tin tức",
    description='Danh sách tin tức',
    responses=swagger_response(
        response_model=ResponseData[ListNewsResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_scb_news(
        current_user=Depends(get_current_user_from_header()),
        pagination_params: PaginationParams = Depends(),
        title: str = Query(None, description='Tiêu đề'),
        category_news: str = Query(None, description='Danh mục'),
        start_date: date = Query(None, description='Ngày bắt đầu'),
        expired_date: date = Query(None, description='Ngày kết thúc'),
        active_flag: bool = Query(None, description='Trạng thái')
):
    scb_news = await CtrNews(current_user, pagination_params=pagination_params
                             ).ctr_get_list_scb_news(title=title,
                                                     category_news=category_news,
                                                     start_date=start_date,
                                                     expired_date=expired_date,
                                                     active_flag=active_flag)
    return ResponseData[ListNewsResponse](**scb_news)


@router.post(
    path="/{news_id}/comment/",
    name="Tạo bình luận",
    description="Tạo bình luận",
    responses=swagger_response(
        response_model=ResponseData[NewsCommentResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_news_comment(
        data_request: NewsCommentRequest,
        news_id: str = Path(..., description='News ID'),
        current_user=Depends(get_current_user_from_header()),

):
    news_comment = await CtrNews(current_user).ctr_news_comment(data_comment=data_request, news_id=news_id)
    return ResponseData(**news_comment)


@router.get(
    path="/{news_id}/comment/",
    name="Danh sách bình luận",
    description="Danh sách bình luận",
    responses=swagger_response(
        response_model=ResponseData[NewsCommentsResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_comment_by_news(
        news_id: str = Path(..., description='News ID'),
        filter_by: str = Query(..., description="Quan tâm / mới nhất"),
        page: int = Query(default=1, ge=1, description="Số trang của comment"),
        current_user=Depends(get_current_user_from_header()),

):
    news_comment = await CtrNews(current_user).ctr_get_comment_by_news_id(news_id=news_id, filter_by=filter_by,
                                                                          page=page)
    return ResponseData[NewsCommentsResponse](**news_comment)


@router.get(
    path="/comment/{comment_id}/like/",
    name="Like",
    description=" Like bình luận",
    responses=swagger_response(
        response_model=ResponseData[CommentLikeResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_comment_like(
        comment_id: str = Path(..., description="ID bình luận"),

        current_user=Depends(get_current_user_from_header())
):
    like_data = await CtrNews(current_user).ctr_comment_like(comment_id=comment_id)
    return ResponseData[CommentLikeResponse](**like_data)
