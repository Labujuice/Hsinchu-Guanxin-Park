#!/bin/bash
set -e

# 允許本機 X11 顯示連接
xhost +local:root > /dev/null 2>&1 || true

# 檢查 NVIDIA GPU 與驅動是否正常運作
GPU_FLAG=""
if nvidia-smi &> /dev/null; then
    echo "[run.sh] 檢測到可用 NVIDIA GPU，啟用 GPU 加速模式 (--gpus all)"
    GPU_FLAG="--gpus all"
else
    echo "[run.sh] 未檢測到可用 NVIDIA 驅動或 GPU，啟用 Mesa / DRI CPU 渲染模式"
fi

# 檢查是否有 DRI 設備以支援 Intel / AMD / 軟體 Mesa 加速
DRI_FLAG=""
if [ -d /dev/dri ]; then
    DRI_FLAG="--device /dev/dri:/dev/dri"
fi

# 如果未建置映像檔，提示先建置
if [[ "$(docker images -q guanxin_sim:latest 2> /dev/null)" == "" ]]; then
    echo "[run.sh] 找不到 guanxin_sim:latest 映像檔，開始自動執行建置..."
    docker build -t guanxin_sim:latest .
fi

# 預設執行指令
COMMAND="${@:-ros2 launch guanxin_sim sim.launch.py}"

echo "[run.sh] 正在啟動 guanxin_sim_container..."
echo "[run.sh] 執行指令: $COMMAND"

docker run -it --rm \
    $GPU_FLAG \
    $DRI_FLAG \
    --net=host \
    --ipc=host \
    -e DISPLAY="${DISPLAY:-:0}" \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v "$(pwd)/src:/ros2_ws/src" \
    --name guanxin_sim_container \
    guanxin_sim:latest \
    $COMMAND
