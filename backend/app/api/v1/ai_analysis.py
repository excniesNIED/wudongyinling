from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import Dict, Any
from ...core.database import get_db
from ...core.security import get_current_active_user
from ...core.ai import ai_analyzer
from ...models.user import User
from ...models.course import Course
import os
import shutil

router = APIRouter()

@router.post("/analyze")
async def analyze_dance(
    video: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """分析用户上传的舞蹈视频"""
    try:
        contents = await video.read()
        result = await ai_analyzer.analyze_dance_video(contents)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/feedback/{video_id}")
async def get_feedback(
    video_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取特定视频的AI反馈"""
    # 这里假设视频URL存储在课程表中
    video = db.query(Course).filter(Course.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="视频不存在")
    
    try:
        result = await ai_analyzer.get_dance_feedback(video.video_url)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/compare")
async def compare_videos(
    user_video: UploadFile = File(...),
    standard_video: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """将用户视频与标准动作视频进行对比"""
    try:
        user_contents = await user_video.read()
        standard_contents = await standard_video.read()
        
        result = await ai_analyzer.compare_with_standard(
            user_contents,
            standard_contents
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/realtime-analysis")
async def realtime_analysis(
    websocket: WebSocket,
    current_user: User = Depends(get_current_active_user)
):
    """实时分析摄像头输入"""
    await websocket.accept()
    try:
        while True:
            # 接收视频帧数据
            frame_data = await websocket.receive_bytes()
            
            # 进行AI分析
            result = await ai_analyzer.analyze_dance_video(frame_data)
            
            # 发送分析结果
            await websocket.send_json(result)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 